import ast
import CodeModul


# Считывание строк кода с файла
with open('file.py', 'r+') as file:
    code_file = file.readlines()


# Преобразование строк кода в блоки
new_code = CodeModul.add_string_child(code_file)

# print(new_code)


print(CodeModul.convert_code_line(new_code))
# print(Structure_dct)
# print(CodeModul.Structure_dct)