import ast

#Словарь для определения структуры данных
Structure_dct = {}

def processing_str_code(code : list[str]):
    '''Функция для обработки строк кода'''
    new_code = []
    for i in range(len(code)):
        if not(code[i] == '\n') and not('#' in code[i]):
            code[i] = code[i].replace('    ', '\t')
            new_code.append(code[i])

    return new_code


def add_string_child(text_code : list[str]) -> list[str]:
    '''Функция переработки строк кода из списка
        Сложение строк, которые вложенны в циклы, условия, функции'''
    new_code = []
    temp_line = text_code[0]

    for i in range(1, len(text_code)):
        if not('    ' in text_code[i]) :
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

    # Присвоение
    elif isinstance(code, ast.Assign):

        targets = ''.join([convert_to_Pascal(i) for i in code.targets])
        value = convert_to_Pascal(code.value)

        if value == 'input':
            return f'Readln({targets});'
        else:
            Structure_dct[targets] = type(value)
            return f'{targets} := {value};'

    # Конвертация For
    elif isinstance(code, ast.For):
        # Переменные цикла
        target = convert_to_Pascal(code.target)
        start, stop = convert_to_Pascal(code.iter)
        Structure_dct[target] = type(start)

        # Тело цикла
        elements = '\n'.join([convert_to_Pascal(elem) for elem in code.body])
        body = '\n{\n' + elements + '\n}\n'

        return f'for {target} := {start} to {stop} do' + body

    # Математические операции
    elif isinstance(code, ast.BinOp):
        left = convert_to_Pascal(code.left)
        right = convert_to_Pascal(code.right)
        operation = convert_to_Pascal(code.op)
        
        return f'{left} {operation} {right}'

    # Конвертация If
    elif isinstance(code, ast.If):
        pass

    elif isinstance(code, ast.Expr):
        # Перевод print - writeln
        elem = convert_to_Pascal(code.value)
        elems = []

        for i in elem:
            if i in Structure_dct:
                elems.append(i)
            else:
                elems.append(f'"{i}"')

        return f'Writeln({', '.join(elems)});'


    elif isinstance(code, ast.Call):
        # Определение функции
        func = convert_to_Pascal(code.func)
        
        if func == 'input':
            return 'input'
        else:
            return [convert_to_Pascal(arg) for arg in code.args]
        
        
    # Получение базового элемента названия переменной =
    elif isinstance(code, ast.Name):
        return code.id
    
    # Получение базового элемента константы
    elif isinstance(code, ast.Constant):
        return code.value
    
    elif isinstance(code, ast.Add):
        return '+'
    
    elif isinstance(code, ast.Sub):
        return '-'
    
    elif isinstance(code, ast.Mult):
        return '*'
    
    elif isinstance(code, ast.Div):
        return '/'
    
    elif isinstance(code, ast.FloorDiv):
        return 'Div'
    
    elif isinstance(code, ast.Mod):
        return 'Mod'