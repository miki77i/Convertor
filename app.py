import ast
import CodeModul


# Считывание строк кода с файла
with open('file.py', 'r+') as file:
    code_file = file.readlines()


# Преобразование строк кода в блоки
new_code = CodeModul.add_string_child(code_file)


# CodeModul.set_global_var(''.join(code_file))
print(CodeModul.convert_code_line(new_code))

# print(Structure_dct)
# print(CodeModul.Structure_dct)


from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Получаем данные из формы
#         text1 = ''
#         text1 = request.form.get('text1')
#         new_text = CodeModul.convert_code_line([text1])


#         return render_template('index2.html', text=text1, new_text=new_text)
#     return render_template('index2.html', text='', new_text='')

# if __name__ == '__main__':
#     app.run(debug=True)