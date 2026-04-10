import os
import shutil
from datetime import datetime

def sincronizar_diretorios(pasta_origem, pasta_destino):
    """
    Sincroniza arquivos da origem para o destino de forma incremental.
    """
    # 1. Valida se a origem existe
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta de origem '{pasta_origem}' não existe.")
        return

    # 2. A SUA OBSERVAÇÃO: Se o destino não existe, nós criamos!
    if not os.path.exists(pasta_destino):
        print(f"Destino '{pasta_destino}' não encontrado. Criando nova pasta...")
        os.makedirs(pasta_destino)

    arquivos_verificados = 0
    arquivos_copiados = 0
    bytes_transferidos = 0

    print(f"Iniciando sincronização...\nOrigem: {pasta_origem}\nDestino: {pasta_destino}\n" + "-"*40)

    # 3. Percorre a origem
    for raiz, diretorios, arquivos in os.walk(pasta_origem):
        
        # 4. Magia do os.path: Descobrir a estrutura de subpastas para replicar no destino
        caminho_relativo = os.path.relpath(raiz, pasta_origem)
        caminho_destino_atual = os.path.join(pasta_destino, caminho_relativo)

        # Se houver subpastas na origem, cria elas no destino também
        if not os.path.exists(caminho_destino_atual):
            os.makedirs(caminho_destino_atual)

        # 5. Verifica os arquivos
        for nome_arquivo in arquivos:
            arquivos_verificados += 1
            caminho_origem_completo = os.path.join(raiz, nome_arquivo)
            caminho_destino_completo = os.path.join(caminho_destino_atual, nome_arquivo)

            precisa_copiar = False

            # Regra CDC 1: O arquivo NÃO existe no destino?
            if not os.path.exists(caminho_destino_completo):
                precisa_copiar = True
            else:
                # Regra CDC 2: O arquivo existe, mas o da origem foi modificado mais recentemente?
                tempo_origem = os.path.getmtime(caminho_origem_completo)
                tempo_destino = os.path.getmtime(caminho_destino_completo)
                
                if tempo_origem > tempo_destino:
                    precisa_copiar = True

            # 6. Realiza a cópia
            if precisa_copiar:
                tamanho = os.path.getsize(caminho_origem_completo)
                print(f"Copiando: {nome_arquivo}")
                
                # O shutil.copy2 é essencial aqui: ele copia o arquivo E preserva a data de modificação original!
                shutil.copy2(caminho_origem_completo, caminho_destino_completo)
                
                arquivos_copiados += 1
                bytes_transferidos += tamanho

    print("-" * 40)
    print("Resumo da Sincronização:")
    print(f"Verificados: {arquivos_verificados} | Copiados: {arquivos_copiados} | Total: {bytes_transferidos} bytes")

    return arquivos_verificados, arquivos_copiados, bytes_transferidos

# Bloco de teste
if __name__ == "__main__":
    # Teste: Sincronizando a pasta atual para uma pasta nova chamada 'meu_backup_teste'
    sincronizar_diretorios('.', './meu_backup_teste')