import os
import sys
import re

def check_env_variable(var_name):
    return var_name in os.environ

def extract_file_paths(input_file, file_paths=[], depth=0):
    with open(input_file, 'r') as f:
        content = f.read()
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not (line.startswith("//") or line.startswith("#")):
            if line.startswith("-f") or line.startswith("-F"):
                if line.startswith("-f"):   
                    nested_file_paths = line.lstrip("-f")
                elif line.startswith("-F"):
                    nested_file_paths = line.lstrip("-F")
                nested_file_paths = os.path.abspath(nested_file_paths.strip())
                extract_file_paths(nested_file_paths, file_paths, depth + 1)
            elif line.startswith("-v"):
                line = replace_content(line, "-v")
                file_paths.append(line)
            elif line.startswith("-y"):
                line = replace_content(line, "-y")
                file_paths.append(line)
            elif line.startswith("-I"):
                line = replace_content(line, "-I")
                file_paths.append(line)
            elif line.startswith("`"):
                pass              
            else:  
                file_paths.append(line)
    return file_paths

def replace_content(line, keyword):
    line = line.lstrip(keyword)
    line = line.lstrip()
    if line.startswith("$"):
        pass
    else:
        line = keyword + " " + os.path.abspath(line)
    return  line  

def replace_file_paths(file_paths):
    replaced_paths = []
    for path in file_paths:
        if "$" in path and "\$" not in path:
            idx = path.index("$")
            if "{" == path[idx+1]:
                lower = idx+1
                upper = path[idx:].index("}") + idx
                path = path.replace(path[lower-1:upper+1], os.environ[path[lower+1:upper]])
            elif "/" in path[idx:]:
                lower = idx
                upper = path[idx:].index("/") + idx
                path = path.replace(path[lower:upper], os.environ[path[lower+1:upper]])
            else:
                path = path.replace(path[idx:], os.environ[path[idx+1:]])
        if path.startswith("+") or  path.startswith("-"):
            pass
        else:
            path = os.path.abspath(path)
        replaced_paths.append(path)
    return replaced_paths

# def process_directive(line):
#     processed_paths = []
#     for path in file_paths:
#         # 处理嵌套的ifdef、elseif和endif的逻辑
#             # 处理条件编译指令  
#             if line.startswith('`'):  
#                 directive = line[1:].strip()  
#                 if directive.startswith('ifdef') or directive.startswith('ifndef'):  
#                     # 解析ifdef和ifndef指令  
#                     macro = directive.split()[1]  
#                     if (directive.startswith('ifdef') and not defines.get(macro)) or \  
#                             (directive.startswith('ifndef') and defines.get(macro)):  
#                         # 跳过未定义或不定义的代码块  
#                         while lines and not lines[0].strip().startswith('`endif'):  
#                             lines.pop(0)  
#                     else:  
#                         # 定义宏  
#                         defines[macro] = True  
#                 elif directive.startswith('else') or directive.startswith('elsif'):  
#                     # 解析else和elsif指令  
#                     if directive.startswith('elsif'):  
#                         macro = directive.split()[1]  
#                         if not defines.get(macro):  
#                             # 跳过未定义的代码块  
#                             while lines and not lines[0].strip().startswith('`endif'):  
#                                 lines.pop(0)  
#                         else:  
#                             # 定义宏  
#                             defines[macro] = True  
#                     # 处理else指令时，跳过之前的代码块  
#                     while lines and not lines[0].strip().startswith('`endif'):  
#                         prev_line = lines.pop(0)  
#                         if prev_line.strip().startswith('`elsif') or prev_line.strip().startswith('`else'):  
#                             break  
#                 elif directive.startswith('endif'):  
#                     # 解析endif指令，移除定义的宏  
#                     macro = directive.split()[1] if len(directive.split()) > 1 else None  
#                     if macro:  
#                         defines.pop(macro, None)  
#                 continue 
#         pass
#     return processed_paths

def main(input_file, output_file=None, macro=None):
    base_path = os.getcwd()
    file_paths = extract_file_paths(input_file)
    print(f"file_paths_0 = {file_paths}")
    file_paths = replace_file_paths(file_paths)
    print(f"file_paths_1 = {file_paths}")
    with open(output_file, mode='w') as f:
        for path in file_paths:
            f.write(path + '\n')


if __name__ == '__main__':
    input_file = None
    output_file = "out.vc"
    macro = []
    options = sys.argv[1:]

    if "-i" in options:
        input_file = options[options.index("-i")+1]
    else:
        print("The command is incomplete !!!")
        print("flatf -i input_file [-o output_file] [+define+MACRO] ...")
        sys.exit()

    if "-o" in options:        
        output_file = options[options.index("-o")+1]
          
    if len(sys.argv) > 3:  
        for option in options:
            if option.startswith("-D"):
                macro.append(option.lstrip("-D"))
    main(input_file, output_file, macro)
