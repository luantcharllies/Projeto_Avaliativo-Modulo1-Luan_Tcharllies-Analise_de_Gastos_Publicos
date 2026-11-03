import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from banco import conectar, executar
from sqlalchemy.exc import SQLAlchemyError

NOME_BANCO = 'analise_de_gastos_publicos'

print("=" * 60)
print("FASE 2: TRANSFORMAR DADOS DA RAW PARA A CAMADA SILVER")
print("=" * 60 + "\n")

conexao = conectar(NOME_BANCO)

if conexao is None:
    print(f"❌ Não foi possível conectar ao banco '{NOME_BANCO}'")
    exit(1)

try:
    print("→ Limpando tabelas silver (respeitando restrições de chaves estrangeiras)...")
    executar(conexao, "DELETE FROM silver_2025_pagamento", commit=False)
    executar(conexao, "DELETE FROM silver_2025_trecho", commit=False)
    executar(conexao, "DELETE FROM silver_2025_passagem", commit=False)
    executar(conexao, "DELETE FROM silver_2025_viagem", commit=False)
    
    print("\n→ Inserindo dados limpos em silver_2025_viagem...")
    sql_viagem = """
    INSERT INTO silver_2025_viagem (
        identificador_processo_viagem, numero_proposta_pcdp, situacao,
        viagem_urgente, justificativa_urgencia_viagem, codigo_orgao_superior,
        nome_orgao_superior, codigo_orgao_solicitante, nome_orgao_solicitante,
        cpf_viajante, nome, cargo, funcao, descricao_funcao,
        periodo_data_inicio, periodo_data_fim, destinos, motivo,
        valor_diarias, valor_passagens, valor_devolucao, valor_outros_gastos
    )
    SELECT
        TRIM(identificador_processo_viagem),
        TRIM(numero_proposta_pcdp),
        TRIM(situacao),
        TRIM(viagem_urgente),
        TRIM(justificativa_urgencia_viagem),
        TRIM(codigo_orgao_superior),
        TRIM(nome_orgao_superior),
        TRIM(codigo_orgao_solicitante),
        TRIM(nome_orgao_solicitante),
        COALESCE(NULLIF(TRIM(cpf_viajante), ''), '000.000.000-00'),
        COALESCE(NULLIF(TRIM(nome), ''), 'Não Informado'),
        TRIM(cargo),
        TRIM(funcao),
        TRIM(descricao_funcao),
        -- Tratamento seguro de datas (converte string YYYY-MM-DD ou DD/MM/YYYY se aplicável)
        NULLIF(TRIM(periodo_data_inicio), '')::DATE,
        NULLIF(TRIM(periodo_data_fim), '')::DATE,
        TRIM(destinos),
        TRIM(motivo),
        -- Tratamento de valores numéricos monetários (substitui vírgula por ponto de forma segura)
        COALESCE(CAST(REPLACE(REPLACE(TRIM(valor_diarias), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00),
        COALESCE(CAST(REPLACE(REPLACE(TRIM(valor_passagens), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00),
        COALESCE(CAST(REPLACE(REPLACE(TRIM(valor_devolucao), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00),
        COALESCE(CAST(REPLACE(REPLACE(TRIM(valor_outros_gastos), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00)
    FROM raw_2025_viagem
    WHERE TRIM(identificador_processo_viagem) <> ''
    """
    executar(conexao, sql_viagem, commit=False)

    print("→ Inserindo dados limpos em silver_2025_passagem...")
    sql_passagem = """
    INSERT INTO silver_2025_passagem (
        identificador_processo_viagem, numero_proposta_pcdp, meio_transporte,
        pais_origem_ida, uf_origem_ida, cidade_origem_ida,
        pais_destino_ida, uf_destino_ida, cidade_destino_ida,
        pais_origem_volta, uf_origem_volta, cidade_origem_volta,
        pais_destino_volta, uf_destino_volta, cidade_destino_volta,
        valor_passagem, taxa_servico, data_emissao_compra, hora_emissao_compra
    )
    SELECT
        TRIM(p.identificador_processo_viagem),
        TRIM(p.numero_proposta_pcdp),
        TRIM(p.meio_transporte),
        TRIM(p.pais_origem_ida),
        TRIM(p.uf_origem_ida),
        TRIM(p.cidade_origem_ida),
        TRIM(p.pais_destino_ida),
        TRIM(p.uf_destino_ida),
        TRIM(p.cidade_destino_ida),
        TRIM(p.pais_origem_volta),
        TRIM(p.uf_origem_volta),
        TRIM(p.cidade_origem_volta),
        TRIM(p.pais_destino_volta),
        TRIM(p.uf_destino_volta),
        TRIM(p.cidade_destino_volta),
        COALESCE(CAST(REPLACE(REPLACE(TRIM(p.valor_passagem), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00),
        COALESCE(CAST(REPLACE(REPLACE(TRIM(p.taxa_servico), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00),
        NULLIF(TRIM(p.data_emissao_compra), '')::DATE,
        NULLIF(TRIM(p.hora_emissao_compra), '')::TIME
    FROM raw_2025_passagem p
    WHERE TRIM(p.identificador_processo_viagem) IN (SELECT identificador_processo_viagem FROM silver_2025_viagem)
    """
    executar(conexao, sql_passagem, commit=False)

    print("→ Inserindo dados limpos em silver_2025_trecho...")
    sql_trecho = """
    INSERT INTO silver_2025_trecho (
        identificador_processo_viagem, numero_proposta_pcdp, sequencia_trecho,
        origem_data, origem_pais, origem_uf, origem_cidade,
        destino_data, destino_pais, destino_uf, destino_cidade,
        meio_transporte, numero_diarias, missao
    )
    SELECT
        TRIM(t.identificador_processo_viagem),
        TRIM(t.numero_proposta_pcdp),
        CASE WHEN TRIM(t.sequencia_trecho) ~ '^[0-9]+$' THEN CAST(TRIM(t.sequencia_trecho) AS INT) ELSE NULL END,
        NULLIF(TRIM(t.origem_data), '')::TIMESTAMP,
        TRIM(t.origem_pais),
        TRIM(t.origem_uf),
        TRIM(t.origem_cidade),
        NULLIF(TRIM(t.destino_data), '')::TIMESTAMP,
        TRIM(t.destino_pais),
        TRIM(t.destino_uf),
        TRIM(t.destino_cidade),
        TRIM(t.meio_transporte),
        CASE WHEN TRIM(t.numero_diarias) ~ '^[0-9.,]+$' THEN CAST(REPLACE(TRIM(t.numero_diarias), ',', '.') AS NUMERIC(5,1)) ELSE NULL END,
        TRIM(t.missao)
    FROM raw_2025_trecho t
    WHERE TRIM(t.identificador_processo_viagem) IN (SELECT identificador_processo_viagem FROM silver_2025_viagem)
    """
    executar(conexao, sql_trecho, commit=False)

    print("→ Inserindo dados limpos em silver_2025_pagamento...")
    sql_pagamento = """
    INSERT INTO silver_2025_pagamento (
        identificador_processo_viagem, numero_proposta_pcdp, codigo_orgao_superior,
        nome_orgao_superior, codigo_orgao_pagador, nome_orgao_pagador,
        codigo_unidade_gestora_pagadora, nome_unidade_gestora_pagadora,
        tipo_pagamento, valor
    )
    SELECT
        TRIM(pg.identificador_processo_viagem),
        TRIM(pg.numero_proposta_pcdp),
        TRIM(pg.codigo_orgao_superior),
        TRIM(pg.nome_orgao_superior),
        TRIM(pg.codigo_orgao_pagador),
        TRIM(pg.nome_orgao_pagador),
        TRIM(pg.codigo_unidade_gestora_pagadora),
        TRIM(pg.nome_unidade_gestora_pagadora),
        TRIM(pg.tipo_pagamento),
        COALESCE(CAST(REPLACE(REPLACE(TRIM(pg.valor), '.', ''), ',', '.') AS NUMERIC(12,2)), 0.00)
    FROM raw_2025_pagamento pg
    WHERE TRIM(pg.identificador_processo_viagem) IN (SELECT identificador_processo_viagem FROM silver_2025_viagem)
    """
    executar(conexao, sql_pagamento, commit=False)

    print("\n→ Confirmando transação da Camada Silver...")
    conexao.commit()
    
    print("\n✅ Fase 2 (Transformação para Silver) concluída com sucesso!")
    print("=" * 60)
    
except SQLAlchemyError as e:
    print(f"\n❌ Erro durante a transformação para Silver: {e}")
    print("   Revertendo mudanças (Rollback)...")
    conexao.rollback()
    exit(1)
finally:
    conexao.close()