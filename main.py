from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.model import Clientes


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


if __name__ == "__main__":
    app.run(debug=True)
