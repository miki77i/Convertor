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

def set_global_var(code_str):
    '''Функция для определения всех глобальных переменных'''
    def get_type_input(prompt=""):
        return '1'
    
    global_var = {'input': get_type_input}

    exec(''.join(code_str), global_var)

    user_global_var = {key : type(value)  for key, value in global_var.items() if not '__' in key}

    user_global_var.pop('input')

    Structure_dct.update(user_global_var)
    
    
    
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

    if len(var_sp) > 0:
        vars = '\n'.join(var_sp)
        return f'Var\n{vars}'
    return ''



def get_var_type(code):
    '''Функция определения типа переменной'''
    if isinstance(code, ast.Return):
        if get_var_type(code.value) == int:
            return int

    if isinstance(code, ast.BinOp):
        left_type = get_var_type(code.left)
        right_type = get_var_type(code.right)

        if left_type == int and right_type == int:
            return int
        
    elif isinstance(code, ast.Call):
        func = get_var_type(code.func)
        
        if func == 'int':
            return int
        elif func == 'input':
            return str
        elif func == 'float':
            return float
    
    elif isinstance(code, ast.Name):
        return code.id

    elif isinstance(code, ast.Constant):
        if type(code.value) == int:
            return int
        
        elif type(code.value) == str:
            return str
        
        return 'Unknown'


def get_function(code):
    '''Функция для инициализации функции Pascal'''  
    return convert_to_Pascal(code)


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
            return f'\n{targets} := {value};'

    # Конвертация For
    elif isinstance(code, ast.For):
        # Переменные цикла
        target = convert_to_Pascal(code.target)
        iter = convert_to_Pascal(code.iter)
        # Проверка на диапазон для for
        if len(iter) == 1: 
            start, stop = 0, iter[0]
        else:
            start, stop = iter

        Structure_dct[target] = type(start)
        
        # Тело цикла
        elements = '\n'.join([convert_to_Pascal(elem) for elem in code.body])
        body = '\nbegin' + elements + '\nend'
        if int(start) < int(stop):
            return f'\nfor {target} := {start} to {stop} do' + body
        return f'\nfor {target} := {start} downto {stop} do' + body
    
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
            if len(code.orelse) == 1:
                else_ = convert_to_Pascal(code.orelse[0]) 
            else:
                else_ = '\n'.join([convert_to_Pascal(elem) for elem in code.orelse])
            else_ = f'\nElse\nbegin \n{else_} \nend' 
        
        return f'\nIf {test} then\n' + 'begin\n' + body + '\nend' + else_
    
    
    elif isinstance(code, ast.FunctionDef):
        def_name = code.name
        args = convert_to_Pascal(code.args)
        body = '\n'.join([convert_to_Pascal(arg) for arg in code.body])
        return f'function {def_name}({','.join([arg + ':Integer' for arg in args])}) of Integer;\nbegin\n{body}\nend;'

    elif isinstance(code, ast.Return):
        ret = convert_to_Pascal(code.value)
        return f'{ret}'

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
                elems.append(f"'{i}'")

        return f'\nWriteln({', '.join(elems)});'


    elif isinstance(code, ast.Call):
        # Определение функции
        func = convert_to_Pascal(code.func)
        
        if func == 'input' or func == 'int':
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
    
    elif isinstance(code, ast.arguments):

        return [convert_to_Pascal(arg) for arg in code.args]
    
    elif isinstance(code, ast.arg):
        return code.arg
    
    #Получение списка элементов
    elif isinstance(code, ast.List):
        elems = [convert_to_Pascal(elem) for elem in code.elts]
        return elems

    # Получение базовых эдементов
    #Получение имени аргумента функции
    elif isinstance(code, ast.arg):
        return code.arg

    # Получение базового элемента названия переменной =
    elif isinstance(code, ast.Name):
        return code.id
    
    # Получение базового элемента константы
    elif isinstance(code, ast.Constant):
        return code.value
    
    

def convert_code_line(new_code):
    '''Функция для преобразования каждой строки в код pascal'''
    Structure_dct.clear()
    Array_struct.clear()
    code_lines = []
    function_lines = []

    for i in range(len(new_code)):
        tree = ast.parse(new_code[i])
        print(ast.dump(tree, indent=5))

        if 'def' in new_code[i]:
            function_lines.append(convert_to_Pascal(tree))
        else:
            code_lines.append(convert_to_Pascal(tree))  
    
    vars = create_var()

    # print(f"{vars} \nbegin\n {''.join(code_lines)} \nend.")
    if vars == '':
        return f"{''.join(function_lines)}\nbegin\n {''.join(code_lines)} \nend."
    return f"{''.join(function_lines)}\n{vars} \nbegin {''.join(code_lines)} \nend."