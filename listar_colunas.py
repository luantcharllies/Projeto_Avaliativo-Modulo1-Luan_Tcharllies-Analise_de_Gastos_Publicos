import os
import pandas as pd

print("\n=== PROCURANDO ARQUIVOS CSV NO DIRETÓRIO E SUBPASTAS ===\n")

arquivos_encontrados = {}

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.lower().endswith('.csv'):
            caminho_completo = os.path.join(root, file)
            arquivos_encontrados[file] = caminho_completo
            print(f"[ENCONTRADO] {file} -> Caminho: {caminho_completo}")

print("\n" + "="*50 + "\n")

alvos = [
    "2025_Pagamento.csv",
    "2025_Passagem.csv",
    "2025_Trecho.csv",
    "2025_Viagem.csv"
]

for alvo in alvos:
    encontrado = None
    for nome, caminho in arquivos_encontrados.items():
        if nome.lower() == alvo.lower():
            encontrado = caminho
            break
            
    if encontrado:
        print(f"📂 Lendo colunas de: {alvo}")
        print("-" * 50)
        try:
            try:
                df = pd.read_csv(encontrado, nrows=0, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(encontrado, nrows=0, encoding='latin-1')
            except Exception:
                df = pd.read_csv(encontrado, nrows=0, sep=';', encoding='utf-8')

            for coluna in df.columns:
                print(f"   - {coluna}")
        except Exception as e:
            print(f"[ERRO] Não foi possível ler o arquivo: {e}")
        print("\n")
    else:
        print(f"[AVISO] O arquivo '{alvo}' não foi localizado em nenhuma subpasta.\n")