import ast
import CodeModul


# Считывание строк кода с файла
with open('file.py', 'r+') as file:
    code_file = file.readlines()


# print(code_file)

# Преобразование строк кода в блоки
new_code = CodeModul.add_string_child(code_file)

# print(new_code)

for i in range(4,5):
    tree = ast.parse(new_code[i])
    print(ast.dump(tree, indent=5))
    print(CodeModul.convert_to_Pascal(tree))

# print(Structure_dct)
print(CodeModul.Structure_dct)