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