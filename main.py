from flask import Flask, render_template, redirect, request, url_for
from flask_login import login_user, logout_user
from flask_login.utils import _get_user

from app import app, db
from app.model import Clientes, Emprestimos


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
        if request.method == 'POST':
                print("POST")
                nome = request.form['nome']
                cpf = request.form['cpf']
                email = request.form['email']
                senha = request.form['senha']

                cliente = Clientes(email, senha, nome, cpf)
                db.session.add(cliente)
                db.session.commit()
                return redirect(url_for('login'))

        return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
                print("POST")
                email = request.form['email']
                senha = request.form['senha']

                cliente = Clientes.query.filter_by(cliente_email=email).first()
                print(cliente)
                if not cliente or not cliente.verify_password(senha):
                        return redirect(url_for('login'))

                login_user(cliente)
                return redirect(url_for('menu'))
        return render_template('login.html')

@app.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('login'))


@app.route('/menu')
def menu():
    return render_template('menu.html')

def calcular_parcelas(valor, taxa, n_parcelas, parcela_atual):
    saldo = valor
    arrebate = valor/n_parcelas
    custo_mensal = []
    while saldo != 0:
        juros = saldo*taxa
        custo_mensal.append(juros+arrebate)
        print(juros)
        saldo = saldo-arrebate

    return custo_mensal
def verificar_emprestimo():
    print(_get_user())
    user_id = db.session.execute(_get_user()).fetchall()[0][0].get_id()
    db.session.commit()
    print(user_id)
    emprestimo = Emprestimos.query.filter_by(cliente_id=user_id).first()
    print(emprestimo)
    if emprestimo != None:
        valor = float(emprestimo.get_valor())
        taxa = float(emprestimo.get_taxa())
        data_inicio = emprestimo.get_data()
        n_parcelas = int(emprestimo.get_n_parcelas())
        parcela_atual = int(emprestimo.get_parcela_atual())
        parcelas = calcular_parcelas(valor, taxa, n_parcelas, parcela_atual)
        return parcelas
    else:
        return False
@app.route('/emprestimos')
def emprestimos():
    if verificar_emprestimo():
        return render_template('login.html')
        # return render_template('pagina_emprestimos_cliente.html')
    else:
      return render_template('menu.html')

if __name__ == "__main__":
    app.run(debug=True)


