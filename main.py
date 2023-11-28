from flask import Flask, render_template, redirect, request, flash
import psycopg2

conn = psycopg2.connect(
    database='bank',
    host='localhost',
    user='postgres',
    password='tatakae',
    port='5432'
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def sla():
    return render_template('cadastro.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    nome_cadastro = request.form.get('nome')
    cpf_cadastro = request.form.get('cpf')
    email_cadastro = request.form.get('email')
    senha_cadastro = request.form.get('senha')

    if cadastro_usuario(email_cadastro, cpf_cadastro):
        print("n funciono")
        return render_template('cadastro.html')
    else:
        cadastrar(nome_cadastro, cpf_cadastro, email_cadastro, senha_cadastro)
        print("funciono")
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    email_login = request.form.get('email')
    senha_login = request.form.get('senha')
    id_cliente = teste_cliente(email_login, senha_login)

    if id_cliente:

        return render_template('menu.html')
    else:
        id_funcionario = teste_funcionario(email_login, senha_login)
        if id_funcionario:

            return render_template('menu.html')
        else:
            flash("Login ou senha inválidos")
            return render_template('login.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


def teste_cliente(email, senha):
    cur = conn.cursor()
    cur.execute("SELECT cliente_email, cliente_senha FROM clientes")
    lista_login = cur.fetchall()
    login = (email, senha)
    if login in lista_login:
        cur.execute(f"SELECT cliente_id FROM clientes WHERE cliente_email = '{email}'")
        id_cliente = cur.fetchone()[0]
        cur.close()
        return id_cliente
    else:
        cur.close()
        return None


def teste_funcionario(email, senha):
    cur = conn.cursor()
    cur.execute("SELECT funcionario_email, funcionario_senha FROM funcionarios")
    lista_login = cur.fetchall()
    login = (email, senha)
    if login in lista_login:
        cur.execute(f"SELECT funcionario_id FROM funcionarios WHERE funcionario_email = '{email}'")
        id_funcionario = cur.fetchone()[0]
        cur.close()
        return id_funcionario
    else:
        cur.close()
        return None

def cadastro_usuario(email, cpf):
    cur = conn.cursor()
    cur.execute("SELECT cliente_email, cliente_cpf FROM clientes")
    lista_cadastro = cur.fetchall()
    test_cadastro = (email,cpf)
    if test_cadastro in lista_cadastro:
        cur.close()
        print("false do cadastro")
        return True
    else:
        print("true do cadastro")
        cur.close()
        return False
def cadastrar(nome, cpf, email, senha):
    cpfNumber = int(cpf)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clientes (cliente_id, cliente_email, cliente_cpf, cliente_nome, cliente_senha)
        VALUES (default, %(email)s, %(cpf)s, %(nome)s, %(senha)s);
    """, {'email': email, 'cpf': cpfNumber, 'nome': nome, 'senha': senha})
    conn.commit()
    cur.close()
    print("cadastrou")

if __name__ == "__main__":
    app.run(debug=True)
