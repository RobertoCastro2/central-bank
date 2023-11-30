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


@app.route('/emprestimos')
def emprestimos():
    id = db.session.execute(_get_user()).fetchall()[0][0].get_id()
    db.session.commit()

    if Emprestimos.verificar_emprestimo(Emprestimos,id):
        # return render_template('login.html')
        return render_template('emprestimo.html')
    else:
      return render_template('emprestimo_novo.html')


@app.route('/emprestimos_cliente')
def cliente_emprestimo():
    return render_template('/emprestimo.html')

@app.route('/emprestimos_novo')
def cliente_novo_emprestimo():
    return render_template('/emprestimo_novo.html')


if __name__ == "__main__":
    app.run(debug=True)


