from banco import motor
from sqlalchemy import text

try:
    with open('0_criar_banco.sql', 'r', encoding='utf-8') as arquivo:
        sql_content = arquivo.read() 
    
except UnicodeDecodeError:
    with open('0_criar_banco.sql', 'r', encoding='latin-1') as arquivo:
        sql_content = arquivo.read()

engine = motor('postgres')

if engine is None:
    print("❌ Falha ao conectar. Verifique suas credenciais no .env")
    exit(1)

print("✓ Conectado ao PostgreSQL")

connection = engine.raw_connection()
connection.set_isolation_level(0)
cursor = connection.cursor()

try:
    cursor.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'analise_de_gastos_publicos'
          AND pid <> pg_backend_pid()
    """)
    
    cursor.execute("COMMIT;")
    
    cursor.execute("DROP DATABASE IF EXISTS analise_de_gastos_publicos")
    cursor.execute("CREATE DATABASE analise_de_gastos_publicos ENCODING 'UTF8'")
    connection.commit()
    
    print("✓ Banco 'analise_de_gastos_publicos' criado")
except Exception as e:
    print(f"❌ Erro ao criar banco: {e}")
    connection.rollback()
    exit(1)
finally:
    cursor.close()
    connection.close()

engine_gastos = motor('analise_de_gastos_publicos')

if engine_gastos is None:
    print("❌ Falha ao conectar no banco 'analise_de_gastos_publicos'.")
    exit(1)

try:
    with engine_gastos.begin() as connection:
        connection.execute(text(sql_content))
        
    print("✓ Tabelas criadas com sucesso")
    
except Exception as e:
    print(f"❌ Erro ao criar tabelas: {e}")
    exit(1)

print("\n✅ Fase 0 concluída!")
