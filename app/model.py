from sqlalchemy.orm import backref
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


class Emprestimos(db.Model, UserMixin):
    __tablename__ = "emprestimos"
    emprestimo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.cliente_id"))
    relation = db.relationship("Clientes", backref=backref("clientes", uselist=False))
    valor = db.Column(db.Double, nullable=False)
    taxa = db.Column(db.Double, nullable=False)
    n_parcelas = db.Column(db.Integer, nullable=False)
    parcela_atual = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.String(10), nullable=False)


    def __init__(self, cliente_id, valor, taxa, n_parcelas, parcela_atual, data_inicio):
        self.cliente_id = cliente_id
        self.valor = valor
        self.taxa = taxa
        self.n_parcelas = n_parcelas
        self.parcela_atual = parcela_atual
        self.data_inicio = data_inicio

    def get_id(self):
        return (self.emprestimo_id)

    # Getter para cliente_id
    def get_cliente_id(self):
        return self.cliente_id

    # Getter para valor
    def get_valor(self):
        return self.valor

    def get_taxa(self):
        return self.taxa

    # Getter para n_parcelas
    def get_n_parcelas(self):
        return self.n_parcelas

    # Getter para parcela_atual
    def get_parcela_atual(self):
        return self.parcela_atual

    # Getter para data_inicio
    def get_data(self):
        return self.data_inicio

    def calcular_parcelas(self, valor, taxa, n_parcelas, parcela_atual):
        valor = (valor / n_parcelas) * (n_parcelas - parcela_atual)
        saldo = valor
        arrebate = valor / n_parcelas
        custo_mensal = []
        while saldo != 0:
            juros = saldo * taxa
            saldo = saldo - arrebate
            valor_total = valor_total + juros + arrebate
        custo_mensal.append(juros + arrebate)
        return custo_mensal

    def verificar_emprestimo(self, user_id):
        emprestimo = Emprestimos.query.filter_by(cliente_id=user_id).first()

        if emprestimo != None:
           valor = float(emprestimo.get_valor())
           taxa = float(emprestimo.get_taxa())
           data_inicio = emprestimo.get_data()
           n_parcelas = int(emprestimo.get_n_parcelas())
           parcela_atual = int(emprestimo.get_parcela_atual())
           custo_mensal = emprestimo.calcular_parcelas(valor, taxa, n_parcelas, parcela_atual)

           dados_emprestimo = {"valor": valor, "taxa": taxa, "data_inicio": data_inicio, "n_parcelas": n_parcelas,
                                   "parcela_atual": parcela_atual, "custo_mensal": custo_mensal}

           return dados_emprestimo
        else:
           return False

