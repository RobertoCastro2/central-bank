from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def get_cliente(cliente_id):
    return Clientes.query.filter_by(cliente_id=cliente_id)

class Clientes(db.Model, UserMixin):
    __tablename__ = 'clientes'
    cliente_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cliente_email = db.Column(db.String(30), nullable=False, unique=True)
    cliente_senha = db.Column(db.String(20), nullable=False)
    cliente_nome = db.Column(db.String(30), nullable=False)
    cliente_cpf = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, cliente_email, cliente_senha, cliente_nome, cliente_cpf):
        self.cliente_email = cliente_email
        self.cliente_senha = cliente_senha
        self.cliente_nome = cliente_nome
        self.cliente_cpf = cliente_cpf

    def verify_password(self,senha ):
        return self.cliente_senha == senha

    def get_id(self):
        return (self.cliente_id)