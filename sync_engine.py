import os
import shutil
from datetime import datetime

def sincronizar_diretorios(pasta_origem, pasta_destino, dry_run=False):
    """
    Sincroniza arquivos da origem para o destino de forma incremental.
    """
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta de origem '{pasta_origem}' não existe.")
        return

    if not os.path.exists(pasta_destino):
        if dry_run:
            print(f"[SIMULAÇÃO] Criaria a pasta de destino: {pasta_destino}")
        else:
            print(f"Destino '{pasta_destino}' não encontrado. Criando nova pasta...")
            os.makedirs(pasta_destino)

    arquivos_verificados = 0
    arquivos_copiados = 0
    bytes_transferidos = 0
    
    modo_texto = "[MODO SIMULAÇÃO] " if dry_run else ""
    print(f"{modo_texto}Iniciando sincronização...\nOrigem: {pasta_origem}\nDestino: {pasta_destino}\n" + "-"*40)

    for raiz, diretorios, arquivos in os.walk(pasta_origem):
        caminho_relativo = os.path.relpath(raiz, pasta_origem)
        caminho_destino_atual = os.path.join(pasta_destino, caminho_relativo)

        if not os.path.exists(caminho_destino_atual) and not dry_run:
            os.makedirs(caminho_destino_atual)

        for nome_arquivo in arquivos:
            arquivos_verificados += 1
            caminho_origem_completo = os.path.join(raiz, nome_arquivo)
            caminho_destino_completo = os.path.join(caminho_destino_atual, nome_arquivo)

            precisa_copiar = False

            if not os.path.exists(caminho_destino_completo):
                precisa_copiar = True
            else:
                tempo_origem = os.path.getmtime(caminho_origem_completo)
                tempo_destino = os.path.getmtime(caminho_destino_completo)
                
                if tempo_origem > tempo_destino:
                    precisa_copiar = True

            if precisa_copiar:
                tamanho = os.path.getsize(caminho_origem_completo)
                
                if dry_run:
                    print(f"[SIMULAÇÃO] Copiaria: {nome_arquivo} ({tamanho} bytes)")
                else:
                    print(f"Copiando: {nome_arquivo}")
                    shutil.copy2(caminho_origem_completo, caminho_destino_completo)
                
                arquivos_copiados += 1
                bytes_transferidos += tamanho

    print("-" * 40)
    print("Resumo da Sincronização:")
    print(f"Verificados: {arquivos_verificados} | Copiados/Simulados: {arquivos_copiados} | Total: {bytes_transferidos} bytes")

    return arquivos_verificados, arquivos_copiados, bytes_transferidos