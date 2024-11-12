import ast

#Словарь для определения структуры данных
Structure_dct = {}
Array_struct = {}
comp_op = {ast.Lt: "<", ast.Gt : '>', ast.GtE : '>=', ast.LtE: '<=', ast.Eq: '=', ast.NotEq: '<>'}
bool_op = {ast.Or : 'Or', ast.And : 'And'}
bin_op = {ast.Add: "+", ast.Sub: '-', ast.Mult: '*', ast.Div : '/', ast.FloorDiv : 'Div', ast.Mod: 'Mod'}
Var_type = {int : 'Integer', float : 'Real', str : 'String', bool : 'Boolean', list : 'array'}


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
        if not('    ' in text_code[i] or 'else' in text_code[i]):
            new_code.append(temp_line)
            temp_line = text_code[i]
        else:
            temp_line += text_code[i]
        
    if not(temp_line in new_code):
        new_code.append(temp_line)

    return processing_str_code(new_code)


# def create_array():


def create_var() -> str:
    '''Функция для явного задания типа переменной на синтаксисе Pascal'''
    var_sp = []
    for var, type_ in Structure_dct.items():

        if type_ == list:
            array_elems = Array_struct.get(var)
            len_array = len(array_elems)
            array_string = f'{var} : array [1..{len_array}] of {Var_type.get(type(array_elems[0]))} := ({','.join(map(str,array_elems))});'
            var_sp.append(array_string)
        else:
            var_sp.append(f'{var} : {Var_type.get(type_, None)};')

    vars = '\n'.join(var_sp)
    return f'Var\n{vars}'


def convert_to_Pascal(code):
    '''Функция конвертации кода в Pascal'''
    if isinstance(code, ast.Module):
        return '\n'.join([convert_to_Pascal(i) for i in code.body]) 

    # Присвоение
    elif isinstance(code, ast.Assign):

        targets = ''.join([convert_to_Pascal(i) for i in code.targets])
        value = convert_to_Pascal(code.value)

        if value == 'input':
            return f'\nReadln({targets});'
        elif type(value) == list:
            Array_struct[targets] = value
            Structure_dct[targets] = type(value)
            return ''
        else:
            Structure_dct[targets] = type(value)
            return f'\n{targets} := {value};'

    # Конвертация For
    elif isinstance(code, ast.For):
        # Переменные цикла
        target = convert_to_Pascal(code.target)
        start, stop = convert_to_Pascal(code.iter)
        Structure_dct[target] = type(start)

        # Тело цикла
        elements = '\n'.join([convert_to_Pascal(elem) for elem in code.body])
        body = '\nbegin' + elements + '\nend'

        return f'\nfor {target} := {start} to {stop} do' + body
    
    # Конвертация While
    elif isinstance(code, ast.While):
        test = convert_to_Pascal(code.test) 
        body = '\n'.join([convert_to_Pascal(elem) for elem in code.body])
        return f'\nwhile {test} do \nbegin{body}\nend;\n'

    # Конвертация If
    elif isinstance(code, ast.If):
        test = convert_to_Pascal(code.test) 
        body = '\n'.join([convert_to_Pascal(elem) for elem in code.body])
        else_ = ''

        if code.orelse != []:
            else_ = '\n'.join([convert_to_Pascal(elem) for elem in code.orelse])
            else_ = f'\nElse begin {else_} \nend' 
        
        return f'\nIf {test} then\n' + 'begin' + body + '\nend' + else_
    

    # Математические операции
    elif isinstance(code, ast.BinOp):
        left = convert_to_Pascal(code.left)
        right = convert_to_Pascal(code.right)
        operation = bin_op.get(type(code.op), None)
        
        return f'{left} {operation} {right}'


    elif isinstance(code, ast.Expr):
        # Перевод print - writeln
        elem = convert_to_Pascal(code.value)
        elems = []

        for i in elem:
            if i in Structure_dct:
                elems.append(i)
            else:
                elems.append(f'"{i}"')

        return f'\nWriteln({', '.join(elems)});'


    elif isinstance(code, ast.Call):
        # Определение функции
        func = convert_to_Pascal(code.func)
        
        if func == 'input':
            return 'input'
        else:
            return [convert_to_Pascal(arg) for arg in code.args]
        

    elif isinstance(code, ast.BoolOp):
        oper = bool_op[type(code.op)]
        values = [convert_to_Pascal(elem) for elem in code.values]
        return f'{values[0]} {oper} {values[1]}'
        
    elif isinstance(code, ast.Compare):
        left = convert_to_Pascal(code.left)
        ops = comp_op[type(code.ops[0])]
        right = convert_to_Pascal(code.comparators[0])
        
        return f'{left} {ops} {right}'
    
    elif isinstance(code, ast.List):
        elems = [convert_to_Pascal(elem) for elem in code.elts]
        return elems

    # Получение базового элемента названия переменной =
    elif isinstance(code, ast.Name):
        return code.id
    
    # Получение базового элемента константы
    elif isinstance(code, ast.Constant):
        return code.value
    

def convert_code_line(new_code):
    '''Функция для преобразования каждой строки в код pascal'''
    code_lines = []

    for i in range(len(new_code)):
        tree = ast.parse(new_code[i])
        # print(ast.dump(tree, indent=5))
        code_lines.append(convert_to_Pascal(tree))
    
    vars = create_var()

    print(f"{vars} \nbegin\n {''.join(code_lines)} \nend.")