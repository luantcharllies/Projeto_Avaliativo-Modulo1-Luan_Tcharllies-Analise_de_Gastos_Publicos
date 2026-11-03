# 📊 Pipeline de Análise de Gastos Públicos (2025)

Projeto desenvolvido com arquitetura em camadas (Medallion: **Raw**, **Silver** e **Gold**) utilizando **Python**, **PostgreSQL** e **Jupyter Notebook**, com o objetivo de ingerir, tratar, transformar e analisar dados de viagens e gastos públicos federais.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python 3.x
* **Banco de Dados Relacional:** PostgreSQL
* **Bibliotecas de Dados & Manipulação:** Pandas, SQLAlchemy, Psycopg2
* **Visualização de Dados (Dataviz):** Matplotlib
* **Ambiente de Desenvolvimento:** VS Code & Jupyter Notebook

---

## 📂 Arquitetura do Projeto

O projeto segue um pipeline estruturado em etapas bem definidas:

1. **Camada Raw (Dados Brutos):** Ingestão e armazenamento fiel dos ficheiros de dados originais (viagens, passagens, trechos e pagamentos) em tabelas no PostgreSQL.
2. **Camada Silver (Dados Limpos e Tratados):** Limpeza de nulos, padronização de nomenclaturas, tratamento de tipos de dados e criação de campos calculados (como duração de viagens).
3. **Camada Gold (Análise e Negócio):** Extração de indicadores de valor e cruzamento de tabelas para responder a perguntas estratégicas de negócio através de consultas SQL avançadas e gráficos.

---

## 🔍 Respostas às 7 Perguntas de Negócio (Camada Gold)

O notebook `3_analise.ipynb` responde de forma automatizada e visual às seguintes questões obrigatórias do projeto:

1. **Top 5 Órgãos com Maior Custo Total:** Ranking dos órgãos superiores que concentram o maior volume de recursos financeiros em viagens.
2. **Top 3 Destinos com Maior Custo Médio por Viagem:** Identificação dos destinos mais onerosos por deslocamento (aplicando filtro de robustez para destinos com 2 ou mais viagens).
3. **Viagem de Maior Duração e Custo Total:** Destaque para o processo de viagem mais longo registado, detalhando o viajante, cargo, órgão, dias de duração e custo total.
4. **Tipo de Pagamento com Maior Valor Médio:** Análise dos meios/tipos de pagamento associados aos maiores valores médios de transação.
5. **Meio de Transporte Mais Usado nos Trechos:** Contagem e visualização gráfica dos meios de transporte mais recorrentes nas rotas.
6. **UF de Destino com Mais Trechos:** Identificação da Unidade Federativa que mais recebe trechos de viagens.
7. **Órgão que Pagou Mais no Total:** Cruzamento avançado entre as tabelas de viagens e pagamentos (`JOIN`) para apurar o órgão líder em pagamentos totais.

---

## 🚀 Como Executar o Projeto

1. **Pré-requisitos:**
   * Ter o **Python** e o **PostgreSQL** instalados na sua máquina.
   * Criar um banco de dados no PostgreSQL com o nome configurado no projeto (ex: `analise_de_gastos_publicos`).

2. **Instalar as Dependências:**
   ```bash
   pip install -r requirements.txt