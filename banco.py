from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import POSTGRES_CONFIG
import pandas as pd

def motor(dbname=None):
    
    if dbname is None:
        dbname = 'postgres'  
    
    url = (
        f"postgresql+psycopg2://"
        f"{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}"
        f"@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{dbname}"
    )
    
    try:
        engine = create_engine(url, connect_args={"client_encoding": "utf8"})
        return engine
    except Exception as e:
        print(f"Erro ao criar engine: {e}")
        return None

def conectar(dbname='analise_de_gastos_publicos'):
    
    try:
        engine = motor(dbname)
        conexao = engine.connect()
        return conexao
    except SQLAlchemyError as e:
        print(f"❌ Erro ao conectar ao PostgreSQL:")
        print(f"   Host: {POSTGRES_CONFIG['host']}")
        print(f"   Porta: {POSTGRES_CONFIG['port']}")
        print(f"   Usuário: {POSTGRES_CONFIG['user']}")
        print(f"   Banco: {dbname}")
        print(f"   Mensagem: {e.orig}")
        return None

def executar(conexao, sql, commit=True):
    
    try:
        conexao.execute(text(sql))
        if commit:
            conexao.commit()
        return True
    except SQLAlchemyError as e:
        print(f"❌ Erro ao executar SQL: {e.orig}")
        conexao.rollback()
        return False

def consultar(sql, conexao):
    
    try:
        df = pd.read_sql(text(sql), conexao, coerce_float=True)
        return df
    except SQLAlchemyError as e:
        print(f"❌ Erro ao consultar: {e.orig}")
        return None

def inserir_em_lote(conexao, tabela, dataframe):
    
    try:
        dataframe.to_sql(
            tabela,
            conexao,
            if_exists='append',
            method='multi',
            chunksize=1000,
            index=False
        )
        conexao.commit()
        return True
    except SQLAlchemyError as e:
        print(f"❌ Erro ao inserir em lote: {e.orig}")
        conexao.rollback()
        return False