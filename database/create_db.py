import sqlite3
import os

def criar_banco_e_tabela():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Diretório pai do script
    data_dir = os.path.join(project_dir, 'database')  # Caminho para a pasta de downloads    
    
    # Caminho absoluto com base no diretório onde o script está sendo executado
    db_directory = os.path.join(os.getcwd(), data_dir)

    # Criar a pasta, se não existir
    os.makedirs(db_directory, exist_ok=True)

    # Nome do arquivo do banco de dados
    db_name = "covid_brasil.db"
    db_path = os.path.join(db_directory, db_name)

    # Conectando ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Script SQL para criar a tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS covid_brasil (
        regiao VARCHAR(50),
        estado VARCHAR(2),
        municipio VARCHAR(100),
        coduf INT,
        codmun INT,
        codRegiaoSaude INT,
        nomeRegiaoSaude VARCHAR(100),
        ref_data DATE,
        semanaEpi INT,
        populacaoTCU2019 INT,
        casosAcumulado INT,
        casosNovos INT,
        obitosAcumulado INT,
        obitosNovos INT,
        Recuperadosnovos INT,
        emAcompanhamentoNovos INT,
        interior_metropolitana INT
    );
    """
     # Criando a tabela
    cursor.execute(create_table_query)

    # Script SQL para criar a tabela
    create_table_query = """
        CREATE TABLE ingested_file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT
        );
    """

    # Criando a tabela
    cursor.execute(create_table_query)

    # Confirmando as mudanças
    conn.commit()

    # Fechando a conexão
    conn.close()

    print(f"Banco de dados criado em: {db_path}")
    print("Tabela 'covid_brasil' criada com sucesso.")

# Executa a função principal
if __name__ == "__main__":
    criar_banco_e_tabela()