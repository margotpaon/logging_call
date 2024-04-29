import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('roles.db')
c = conn.cursor()

# Criar tabelas se não existirem
c.execute('''CREATE TABLE IF NOT EXISTS roles (
                role_id INTEGER PRIMARY KEY,
                role_name TEXT NOT NULL
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS calls (
                member_id INTEGER,
                role_id INTEGER,
                start_time TIMESTAMP,
                duration TEXT,
                FOREIGN KEY (role_id) REFERENCES roles(role_id),
                PRIMARY KEY (member_id, start_time)
             )''')
conn.commit()
