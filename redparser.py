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
            nested_lines = replace_path_without_cmd_single_line(nested_file_paths.strip())
            extract_lines(nested_lines, collected_lines, depth + 1)
        else:  
            collected_lines.append(line)
    return collected_lines


def replace_path_with_cmd_unit(line, keyword):
    if keyword == "//":
        pass
    elif keyword == "#":
        pass
    elif keyword == "+libext":
        pass
    elif keyword == "-I":
        line = "-I" + " " + replace_path_without_cmd_single_line(line.lstrip("-I").lstrip())
    elif keyword == "-v":
        line = "-v" + " " + replace_path_without_cmd_single_line(line.lstrip("-v").lstrip())
    elif keyword == "-y":
        line = "-y" + " " + replace_path_without_cmd_single_line(line.lstrip("-y").lstrip())
    elif keyword == "-incdir":
        line = "-incdir" + " " + replace_path_without_cmd_single_line(line.lstrip("-incdir").lstrip())
    elif keyword == "+incdir+":
        line = "+incdir+" + replace_path_without_cmd_single_line(line.lstrip("+incdir+").lstrip())
    else:
        line = replace_path_without_cmd_single_line(line)
    return  line   

def replace_path_with_cmd(lines):
    replaced_lines = []
    cmds = ["-v", "-y", "-I", "-incdir", "+incdir+", "//", "#", "+libext"]
    status = 0
    for line in lines:
        line = line.lstrip()
        if line:
            for cmd in cmds:
                if line.startswith(cmd):
                    line = replace_path_with_cmd_unit(line, cmd)
                    replaced_lines.append(line)
                    status = 1
                    break
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
        replaced_paths.append(line)
    return replaced_paths


def replace_path_without_cmd_single_line(line):
    if "$" in line and "\$" not in line:
        idx = line.index("$")
        if "{" == line[idx+1]:
            lower = idx+1
            upper = line[idx:].index("}") + idx
            line = line.replace(line[lower-1:upper+1], os.environ[line[lower+1:upper]])
        elif "/" in line:
            lower = idx
            upper = line[idx:].index("/") + idx
            line = line.replace(line[lower:upper], os.environ[line[lower+1:upper]])
        else:
            line = line.replace(line[idx:], os.environ[line[idx+1:]])
    elif os.path.isabs(line):
        pass
    else:
        line = os.path.abspath(line)
    return line

def replace_path_with_cmd_unit_multi_line(lines):
    replaced_lines = [] 
    for line in lines:
        if line.startswith("//"):
            pass
        elif line.startswith("#"):
            pass
        elif line.startswith("-I"):
            pass
        elif line.startswith("-v"):
            pass
        elif line.startswith("-y"):
            pass
        elif line.startswith("-incdir"):
            pass
        elif line.startswith("+incdir+"):
            pass
        elif line.startswith("+libext"):
            pass
        elif os.path.isabs(line):
            pass
        else:
            line = os.path.abspath(line)
        replaced_lines.append(line)
    return replaced_lines  

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
    lines = extract_lines(input_file)
    lines = replace_path_with_cmd(lines)
    lines = replace_path_without_cmd(lines)
    lines = replace_path_with_cmd_unit_multi_line(lines)
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
