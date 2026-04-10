import sqlite3
from datetime import datetime
import os

# Definimos o caminho do banco para ficar na mesma pasta do script
DB_PATH = os.path.join(os.path.dirname(__file__), 'pysync_log.db')

def registrar_execucao(arquivos_verificados, arquivos_copiados, bytes_transferidos, status="Sucesso"):
    """
    Grava o log da execução da sincronização no banco de dados SQLite.
    """
    # 1. Conecta ao banco de dados (se o arquivo pysync_log.db não existir, ele cria na hora)
    conexao = sqlite3.connect(DB_PATH)
    
    # O cursor é o nosso "mensageiro" que leva os comandos SQL para o banco
    cursor = conexao.cursor()

    # 2. Cria a tabela de auditoria caso seja a primeira vez rodando
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS execucoes_backup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            arquivos_verificados INTEGER,
            arquivos_copiados INTEGER,
            bytes_transferidos INTEGER,
            status TEXT
        )
    ''')

    # 3. Prepara os dados para inserção
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 4. Insere a nova linha de log
    # Usamos (?) para evitar SQL Injection (boa prática de segurança em backend)
    cursor.execute('''
        INSERT INTO execucoes_backup 
        (data_hora, arquivos_verificados, arquivos_copiados, bytes_transferidos, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (data_atual, arquivos_verificados, arquivos_copiados, bytes_transferidos, status))

    # 5. Salva as alterações (commit) e fecha a porta do banco
    conexao.commit()
    conexao.close()
    
    print("Log de execução registrado no banco de dados com sucesso.")

# Bloco de teste
if __name__ == "__main__":
    # Vamos simular que o script rodou e copiou alguns arquivos
    registrar_execucao(arquivos_verificados=150, arquivos_copiados=5, bytes_transferidos=10240)