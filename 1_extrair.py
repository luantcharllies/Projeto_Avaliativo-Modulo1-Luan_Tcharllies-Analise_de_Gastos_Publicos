import zipfile
import pandas as pd
from pathlib import Path
from banco import conectar, executar, inserir_em_lote

NOME_BANCO = 'analise_de_gastos_publicos'

ARQUIVOS_PROJETO = {
    '2025_Viagem.csv': 'raw_2025_viagem',
    '2025_Passagem.csv': 'raw_2025_passagem',
    '2025_Trecho.csv': 'raw_2025_trecho',
    '2025_Pagamento.csv': 'raw_2025_pagamento'
}

MAPA_COLUNAS = {
    'Identificador do processo de viagem': 'identificador_processo_viagem',
    'Identificador do processo de viagem ': 'identificador_processo_viagem',
    'Número da Proposta (PCDP)': 'numero_proposta_pcdp',
    'Situação': 'situacao',
    'Viagem Urgente': 'viagem_urgente',
    'Justificativa Urgência Viagem': 'justificativa_urgencia_viagem',
    'Código do órgão superior': 'codigo_orgao_superior',
    'Nome do órgão superior': 'nome_orgao_superior',
    'Código órgão solicitante': 'codigo_orgao_solicitante',
    'Nome órgão solicitante': 'nome_orgao_solicitante',
    'CPF viajante': 'cpf_viajante',
    'Nome': 'nome',
    'Cargo': 'cargo',
    'Função': 'funcao',
    'Descrição Função': 'descricao_funcao',
    'Período - Data de início': 'periodo_data_inicio',
    'Período - Data de fim': 'periodo_data_fim',
    'Destinos': 'destinos',
    'Motivo': 'motivo',
    'Valor diárias': 'valor_diarias',
    'Valor passagens': 'valor_passagens',
    'Valor devolução': 'valor_devolucao',
    'Valor outros gastos': 'valor_outros_gastos',
    'Meio de transporte': 'meio_transporte',
    'País - Origem ida': 'pais_origem_ida',
    'UF - Origem ida': 'uf_origem_ida',
    'Cidade - Origem ida': 'cidade_origem_ida',
    'País - Destino ida': 'pais_destino_ida',
    'UF - Destino ida': 'uf_destino_ida',
    'Cidade - Destino ida': 'cidade_destino_ida',
    'País - Origem volta': 'pais_origem_volta',
    'UF - Origem volta': 'uf_origem_volta',
    'Cidade - Origem volta': 'cidade_origem_volta',
    'Pais - Destino volta': 'pais_destino_volta',
    'UF - Destino volta': 'uf_destino_volta',
    'Cidade - Destino volta': 'cidade_destino_volta',
    'Valor da passagem': 'valor_passagem',
    'Taxa de serviço': 'taxa_servico',
    'Data da emissão/compra': 'data_emissao_compra',
    'Hora da emissão/compra': 'hora_emissao_compra',
    'Sequência Trecho': 'sequencia_trecho',
    'Origem - Data': 'origem_data',
    'Origem - País': 'origem_pais',
    'Origem - UF': 'origem_uf',
    'Origem - Cidade': 'origem_cidade',
    'Destino - Data': 'destino_data',
    'Destino - País': 'destino_pais',
    'Destino - UF': 'destino_uf',
    'Destino - Cidade': 'destino_cidade',
    'Número Diárias': 'numero_diarias',
    'Missao?': 'missao',
    'Codigo do órgão pagador': 'codigo_orgao_pagador',
    'Nome do órgao pagador': 'nome_orgao_pagador',
    'Código da unidade gestora pagadora': 'codigo_unidade_gestora_pagadora',
    'Nome da unidade gestora pagadora': 'nome_unidade_gestora_pagadora',
    'Tipo de pagamento': 'tipo_pagamento',
    'Valor': 'valor'
}

def verificar_ou_extrair_dados():
    data_dir = Path('Data')
    if not data_dir.exists():
        data_dir = Path('data')

    zip_path = data_dir / 'viagens_2025_6meses.zip'

    if zip_path.exists():
        print(f"📦 Extraindo arquivos de: {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print("✓ Descompressão concluída!\n")
        return data_dir

    if data_dir.exists():
        return data_dir

    print(f"❌ Diretório ou arquivo zip não encontrado em Data/ ou data/")
    return None

def carregar_csv(tabela, arquivo_csv):
    conexao = conectar(NOME_BANCO)

    if conexao is None:
        print(f"❌ Não foi possível conectar ao banco {NOME_BANCO}")
        return False

    try:
        print(f"  → Limpando tabela {tabela}...")
        executar(conexao, f"TRUNCATE TABLE {tabela}", commit=True)

        print(f"  → Lendo {arquivo_csv}...")
        chunk_size = 50000  
        total_linhas = 0

        try:
            reader = pd.read_csv(
                arquivo_csv,
                sep=';',
                encoding='utf-8',
                dtype=str,
                keep_default_na=False,
                chunksize=chunk_size
            )
            chunks = list(reader)
        except (UnicodeDecodeError, Exception):
            chunks = pd.read_csv(
                arquivo_csv,
                sep=';',
                encoding='latin-1',
                dtype=str,
                keep_default_na=False,
                chunksize=chunk_size
            )

        for chunk in chunks:
            
            chunk.columns = chunk.columns.str.strip()

            chunk = chunk.rename(columns=MAPA_COLUNAS)

            if inserir_em_lote(conexao, tabela, chunk):
                total_linhas += len(chunk)
                print(f"    → {total_linhas} linhas inseridas...")

        print(f"✓ Tabela {tabela}: {total_linhas} linhas carregadas com sucesso\n")
        return True

    except Exception as e:
        print(f"❌ Erro ao carregar {arquivo_csv}: {e}")
        return False
    finally:
        conexao.close()


print("=" * 60)
print("FASE 1: EXTRAIR DADOS PARA A CAMADA RAW")
print("=" * 60 + "\n")

pasta_dados = verificar_ou_extrair_dados()

if not pasta_dados:
    print("❌ Fase 1 falhou!")
    exit(1)

for csv_name, table_name in ARQUIVOS_PROJETO.items():
    csv_path = pasta_dados / csv_name
    print(f"Iniciando carga de {csv_name} para {table_name}...")

    if not csv_path.exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        exit(1)

    if not carregar_csv(table_name, csv_path):
        print(f"❌ Falha ao carregar a tabela {table_name}")
        exit(1)

print("=" * 60)
print("✅ Fase 1 (Ingestão Raw) concluída com sucesso!")
print("=" * 60)