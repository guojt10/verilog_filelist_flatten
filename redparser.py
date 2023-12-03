import os
import sys
import re

def check_env_variable(var_name):
    return var_name in os.environ

def extract_lines(input_file, collected_lines=[], depth=0):
    with open(input_file, 'r') as f:
        content = f.read()
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("-f") or line.startswith("-F"):
            if line.startswith("-f"):   
                nested_file_paths = line.lstrip("-f")
            elif line.startswith("-F"):
                nested_file_paths = line.lstrip("-F")
            nested_lines = os.path.abspath(nested_file_paths.strip())
            extract_lines(nested_lines, collected_lines, depth + 1)
        else:  
            collected_lines.append(line)
    return collected_lines

def replace_path_with_cmd_unit(line, keyword):
    line = line.lstrip(keyword)
    line = line.lstrip()
    if line.startswith("$"):
        pass
    else:
        line = keyword + " " + os.path.abspath(line)
    return  line

def replace_path_with_cmd(lines):
    replaced_lines = []
    cmds = ["-v", "-y", "-I", "-incdir", "+incdir+", "//", "#"]
    status = 0
    for line in lines:
        line = line.strip()
        if line:
            for cmd in cmds:
                if line.startswith(cmd):
                    line = replace_path_with_cmd_unit(line, cmd)
                    replaced_lines.append(line)
                    status = 1
            if status == 0:
                replaced_lines.append(line)
            else:
                status = 0
    return replaced_lines 

def replace_path_without_cmd(lines):
    replaced_paths = []
    for line in lines:
        if "$" in line and "\$" not in line:
            idx = line.index("$")
            if "{" == line[idx+1]:
                lower = idx+1
                upper = line[idx:].index("}") + idx
                line = line.replace(line[lower-1:upper+1], os.environ[line[lower+1:upper]])
            elif "/" in line[idx:]:
                lower = idx
                upper = line[idx:].index("/") + idx
                line = line.replace(line[lower:upper], os.environ[line[lower+1:upper]])
            else:
                line = line.replace(line[idx:], os.environ[line[idx+1:]])
        if line.startswith("+") or  line.startswith("-"):
            pass
        else:
            line = os.path.abspath(line)
        replaced_paths.append(line)
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
    lines = extract_lines(input_file)
    print(f"lines = {lines}")
    lines = replace_path_with_cmd(lines)
    print(f"lines = {lines}")
    lines = replace_path_without_cmd(lines)
    with open(output_file, mode='w') as f:
        for line in lines:
            f.write(line + '\n')


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
