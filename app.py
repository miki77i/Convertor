import ast
import CodeModul


# Считывание строк кода с файла
with open('file.py', 'r+') as file:
    code_file = file.readlines()


# print(code_file)

# Преобразование строк кода в блоки
new_code = CodeModul.add_string_child(code_file)

# print(new_code)

code_lines = []

for i in range(len(new_code)):
    tree = ast.parse(new_code[i])
    # print(ast.dump(tree, indent=5))
    code_lines.append(CodeModul.convert_to_Pascal(tree))

vars = CodeModul.create_var()

print(f"{vars} \nbegin\n {''.join(code_lines)} \nend.")
# print(Structure_dct)
# print(CodeModul.Structure_dct)