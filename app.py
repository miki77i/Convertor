import ast
import astor

#Словарь для определения структуры данных
Structure_dct = {}

def processing_str_code(code : list[str]):
    '''Функция для обработки строк кода'''
    new_code = []
    for i in range(len(code)):
        if not(code[i] == '\n'):
            code[i] = code[i].replace('    ', '\t')
            new_code.append(code[i])

    return new_code


def add_string_child(text_code : list[str]) -> list[str]:
    '''Функция переработки строк кода из списка
        Сложение строк, которые вложенны в циклы, условия, функции'''
    new_code = []
    temp_line = text_code[0]

    for i in range(1, len(text_code)):
        if not('    ' in text_code[i]):
            new_code.append(temp_line)
            temp_line = text_code[i]
        else:
            temp_line += text_code[i]
        
    if not(temp_line in new_code):
        new_code.append(temp_line)

    return processing_str_code(new_code)


def convert_to_Pascal(code):
    '''Функция конвертации кода в Pascal'''
    if isinstance(code, ast.Module):
        return '\n'.join([convert_to_Pascal(i) for i in code.body]) 

    elif isinstance(code, ast.Assign):
        targets = ''.join([convert_to_Pascal(i) for i in code.targets])
        value = convert_to_Pascal(code.value)
        Structure_dct[targets] = type(value)
        return f'{targets} := {value}'

    elif isinstance(code, ast.Name):
        return code.id
    
    elif isinstance(code, ast.Constant):
        return code.value

# Считывание строк кода с файла
with open('file.py', 'r+') as file:
    code_file = file.readlines()

# Преобразование строк кода в блоки
new_code = add_string_child(code_file)
# print(new_code)

# for i in new_code:
#     print(ast.dump(ast.parse(i), indent=4))

tree = ast.parse(new_code[0])
print(ast.dump(tree))
print(convert_to_Pascal(tree))
