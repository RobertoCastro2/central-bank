import psycopg2
#configure conection
conn = psycopg2.connect(
    database = 'bank',
    host = 'localhost',
    user = 'postgres',
    password = '123',
    port = '5432'

)
print(conn.info)
print(conn.status)

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS clientes("
            "cliente_id SERIAL PRIMARY KEY,"
            "cliente_email VARCHAR (30) NOT NULL UNIQUE,"
            "cliente_nome VARCHAR (30) NOT NULL,"
            "cliente_cpf INT NOT NULL UNIQUE,"
            "cliente_senha VARCHAR (20) NOT NULL"
            ");")

cur.execute("INSERT INTO funcionarios VALUES(1, 'Roberto', '1232390', '12908372')")

cur.execute("SELECT * FROM funcionarios")
tabela = cur.fetchall()

conn.commit()
cur.close()
conn.close()


from flask import Flask, render_template, redirect, request, flash, url_for
from app import app, db
from app.model import Clientes


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        senha = request.form.get('senha')
        print("commit ?")

        cliente = Clientes(email, senha, nome, cpf)
        db.session.add(cliente)
        db.session.commit()
        print("commit ?")

        return render_template('cadastro.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     email_login = request.form.get('email')
#     senha_login = request.form.get('senha')
#     id_cliente = teste_cliente(email_login, senha_login)
#
#     if id_cliente:
#         return redirect('/menu')
#     else:
#         id_funcionario = teste_funcionario(email_login, senha_login)
#         if id_funcionario:
#
#             return render_template('/menu')
#         else:
#             flash("Login ou senha inválidos")
#             return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

#
# def teste_cliente(email, senha):
#     cur = conn.cursor()
#     cur.execute("SELECT cliente_email, cliente_senha FROM clientes")
#     lista_login = cur.fetchall()
#     login = (email, senha)
#     if login in lista_login:
#         cur.execute(f"SELECT cliente_id FROM clientes WHERE cliente_email = '{email}'")
#         id_cliente = cur.fetchone()[0]
#         return id_cliente
#     else:
#         return None
#
#
# def teste_funcionario(email, senha):
#     cur = conn.cursor()
#     cur.execute("SELECT funcionario_email, funcionario_senha FROM funcionarios")
#     lista_login = cur.fetchall()
#     login = (email, senha)
#     if login in lista_login:
#         cur.execute(f"SELECT funcionario_id FROM funcionarios WHERE funcionario_email = '{email}'")
#         id_funcionario = cur.fetchone()[0]
#         return id_funcionario
#     else:
#         return None
#
# def cadastro_usuario(email, cpf):
#     cur = conn.cursor()
#     cur.execute("SELECT cliente_email, cliente_cpf FROM clientes")
#     lista_cadastro = cur.fetchall()
#     test_cadastro = (email,cpf)
#     if test_cadastro in lista_cadastro:
#         print("false do cadastro")
#         return True
#     else:
#         print("true do cadastro")
#         return False
# def cadastrar(nome, cpf, email, senha):
#     cpfNumber = int(cpf)
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO clientes (cliente_id, cliente_email, cliente_cpf, cliente_nome, cliente_senha)
#         VALUES (default, %(email)s, %(cpf)s, %(nome)s, %(senha)s);
#     """, {'email': email, 'cpf': cpfNumber, 'nome': nome, 'senha': senha})
#     conn.commit()
#     print("cadastrou")

if __name__ == "__main__":
    app.run(debug=True)

    < form
    action = ""
    method = "post" >
    < input


    class ="inputInput" type="text" name="nome" placeholder="Nome" >

    < input


    class ="inputInput" type="text"  name="cpf" placeholder="CPF" >

    < input


    class ="inputInput" type="text"  name="email" placeholder="Email" >

    < input


    class ="inputInput" type="password"  name="senha" placeholder="Senha" >

    < button


    class ="bntInput" type="submit" > Cadastrar < /button >
< / form >