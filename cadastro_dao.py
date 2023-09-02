from typing import List
import sqlite3

# Função para configurar o banco de dados
def configurar_banco_de_dados():
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        
        # Verifica se a tabela 'cadastro' já existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cadastro'")
        
        if cursor.fetchone() is None:
            criar_tabela_cadastro(cursor)

        conexao.commit()


# Função para criar a tabela cadastro
def criar_tabela_cadastro(cursor):
    cursor.execute('''
                   CREATE TABLE cadastro (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   cpf TEXT,
                   cnpj TEXT)
                   ''')


# Função para cadastrar novo registro
def cadastrar(nome, cpf, cnpj):
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO cadastro (nome, cpf, cnpj) VALUES (?, ?, ?)", (nome, cpf, cnpj))
        conexao.commit()


# Função para listar todos os dados
def listar_dados():
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cadastro ORDER BY nome ASC")
        return cursor.fetchall()


# Função para listar apenas os nomes
def listar_nomes() -> List[str]:
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM cadastro ORDER BY nome")
        return [registro[0] for registro in cursor.fetchall()]


# Função para filtrar e listar dados
def filtro_listar_dados(nome_selecionado=None):
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        
        if nome_selecionado and nome_selecionado != "TodosSelecione um Cadastro para Edição":
            cursor.execute("SELECT * FROM cadastro WHERE nome = ?", (nome_selecionado,))
        
        return cursor.fetchall()


# Função para editar um registro existente
def editar(id_registro, nome, cpf, cnpj):
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("UPDATE cadastro SET nome = ?, cpf = ?, cnpj = ? WHERE id = ?", (nome, cpf, cnpj, id_registro))
        conexao.commit()


# Função para excluir um registro pelo ID
def excluir(id_registro):
    with sqlite3.connect('db_cadastro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM cadastro WHERE id = ?", (id_registro,))
        conexao.commit()
