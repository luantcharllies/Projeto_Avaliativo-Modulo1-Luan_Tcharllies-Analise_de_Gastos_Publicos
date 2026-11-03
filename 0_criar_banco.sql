DROP TABLE IF EXISTS raw_2025_trecho CASCADE;
DROP TABLE IF EXISTS raw_2025_passagem CASCADE;
DROP TABLE IF EXISTS raw_2025_viagem CASCADE;
DROP TABLE IF EXISTS raw_2025_pagamento CASCADE;

CREATE TABLE raw_2025_viagem (
    identificador_processo_viagem VARCHAR(100),
    numero_proposta_pcdp VARCHAR(100),
    situacao VARCHAR(100),
    viagem_urgente VARCHAR(50),
    justificativa_urgencia_viagem TEXT,
    codigo_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante VARCHAR(50),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(50),
    nome VARCHAR(255),
    cargo VARCHAR(150),
    funcao VARCHAR(150),
    descricao_funcao VARCHAR(255),
    periodo_data_inicio VARCHAR(50),
    periodo_data_fim VARCHAR(50),
    destinos TEXT,
    motivo TEXT,
    valor_diarias VARCHAR(50),
    valor_passagens VARCHAR(50),
    valor_devolucao VARCHAR(50),
    valor_outros_gastos VARCHAR(50)
);

CREATE TABLE raw_2025_passagem (
    identificador_processo_viagem VARCHAR(100),
    numero_proposta_pcdp VARCHAR(100),
    meio_transporte VARCHAR(100),
    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(50),
    cidade_origem_ida VARCHAR(150),
    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(50),
    cidade_destino_ida VARCHAR(150),
    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(50),
    cidade_origem_volta VARCHAR(150),
    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(50),
    cidade_destino_volta VARCHAR(150),
    valor_passagem VARCHAR(50),
    taxa_servico VARCHAR(50),
    data_emissao_compra VARCHAR(50),
    hora_emissao_compra VARCHAR(50)
);

CREATE TABLE raw_2025_trecho (
    identificador_processo_viagem VARCHAR(100),
    numero_proposta_pcdp VARCHAR(100),
    sequencia_trecho VARCHAR(50),
    origem_data VARCHAR(50),
    origem_pais VARCHAR(100),
    origem_uf VARCHAR(50),
    origem_cidade VARCHAR(150),
    destino_data VARCHAR(50),
    destino_pais VARCHAR(100),
    destino_uf VARCHAR(50),
    destino_cidade VARCHAR(150),
    meio_transporte VARCHAR(100),
    numero_diarias VARCHAR(50),
    missao VARCHAR(50)
);

CREATE TABLE raw_2025_pagamento (
    identificador_processo_viagem VARCHAR(100),
    numero_proposta_pcdp VARCHAR(100),
    codigo_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador VARCHAR(50),
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora VARCHAR(50),
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(100),
    valor VARCHAR(50)
);

DROP TABLE IF EXISTS silver_2025_trecho CASCADE;
DROP TABLE IF EXISTS silver_2025_passagem CASCADE;
DROP TABLE IF EXISTS silver_2025_viagem CASCADE;
DROP TABLE IF EXISTS silver_2025_pagamento CASCADE;

CREATE TABLE silver_2025_viagem (
    identificador_processo_viagem VARCHAR(100) PRIMARY KEY,
    numero_proposta_pcdp VARCHAR(100),
    situacao VARCHAR(100),
    viagem_urgente VARCHAR(50),
    justificativa_urgencia_viagem TEXT,
    codigo_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante VARCHAR(50),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(50) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(150),
    funcao VARCHAR(150),
    descricao_funcao VARCHAR(255),
    periodo_data_inicio DATE,
    periodo_data_fim DATE,
    destinos TEXT,
    motivo TEXT,
    valor_diarias NUMERIC(12, 2) DEFAULT 0.00 CHECK (valor_diarias >= 0),
    valor_passagens NUMERIC(12, 2) DEFAULT 0.00 CHECK (valor_passagens >= 0),
    valor_devolucao NUMERIC(12, 2) DEFAULT 0.00 CHECK (valor_devolucao >= 0),
    valor_outros_gastos NUMERIC(12, 2) DEFAULT 0.00 CHECK (valor_outros_gastos >= 0)
);

CREATE TABLE silver_2025_passagem (
    id_passagem SERIAL PRIMARY KEY,
    identificador_processo_viagem VARCHAR(100) NOT NULL,
    numero_proposta_pcdp VARCHAR(100),
    meio_transporte VARCHAR(100),
    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(50),
    cidade_origem_ida VARCHAR(150),
    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(50),
    cidade_destino_ida VARCHAR(150),
    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(50),
    cidade_origem_volta VARCHAR(150),
    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(50),
    cidade_destino_volta VARCHAR(150),
    valor_passagem NUMERIC(12, 2) NOT NULL CHECK (valor_passagem >= 0),
    taxa_servico NUMERIC(12, 2) DEFAULT 0.00 CHECK (taxa_servico >= 0),
    data_emissao_compra DATE,
    hora_emissao_compra TIME,
    FOREIGN KEY (identificador_processo_viagem) REFERENCES silver_2025_viagem(identificador_processo_viagem)
);

CREATE TABLE silver_2025_trecho (
    id_trecho SERIAL PRIMARY KEY,
    identificador_processo_viagem VARCHAR(100) NOT NULL,
    numero_proposta_pcdp VARCHAR(100),
    sequencia_trecho INT,
    origem_data TIMESTAMP,
    origem_pais VARCHAR(100),
    origem_uf VARCHAR(50),
    origem_cidade VARCHAR(150),
    destino_data TIMESTAMP,
    destino_pais VARCHAR(100),
    destino_uf VARCHAR(50),
    destino_cidade VARCHAR(150),
    meio_transporte VARCHAR(100),
    numero_diarias NUMERIC(5, 1),
    missao VARCHAR(50),
    FOREIGN KEY (identificador_processo_viagem) REFERENCES silver_2025_viagem(identificador_processo_viagem)
);

CREATE TABLE silver_2025_pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    identificador_processo_viagem VARCHAR(100) NOT NULL,
    numero_proposta_pcdp VARCHAR(100),
    codigo_orgao_superior VARCHAR(50),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador VARCHAR(50),
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora VARCHAR(50),
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(100),
    valor NUMERIC(12, 2) NOT NULL CHECK (valor >= 0),
    FOREIGN KEY (identificador_processo_viagem) REFERENCES silver_2025_viagem(identificador_processo_viagem)
);
