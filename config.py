import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONFIG = {
    'host': os.environ.get('PG_HOST', 'localhost'),
    'port': os.environ.get('PG_PORT', '5432'),
    'user': os.environ.get('PG_USER', 'postgres'),
    'password': os.environ.get('PG_PASSWORD', '5432'),
    'dbname': os.environ.get('PG_DATABASE', 'analise_de_gastos_publicos'),
}

ARQUIVOS = {
   
    "2025_Pagamento.csv": "raw_2025_pagamento",
    "2025_Passagem.csv": "raw_2025_passagem",
    "2025_Trecho.csv": "raw_2025_trecho",
    "2025_Viagem.csv": "raw_2025_viagem"

}