import argparse
from sync_engine import sincronizar_diretorios
from database import registrar_execucao

def main():
    # 1. Configurando o interpretador de linha de comando (argparse)
    parser = argparse.ArgumentParser(
        description="PySync CLI - Ferramenta de Sincronização Incremental",
        epilog="Exemplo de uso: python3 main.py --origem ./minha_pasta --destino ./meu_backup"
    )
    
    # 2. Definindo os argumentos que o nosso programa vai aceitar
    parser.add_argument('--origem', required=True, help="Caminho da pasta que contém os arquivos originais")
    parser.add_argument('--destino', required=True, help="Caminho da pasta onde o backup será salvo")
    
    # Captura o que o usuário digitou no terminal
    args = parser.parse_args()

    # 3. Executando a lógica principal
    try:
        # Chama a função do os/shutil e guarda os números retornados
        resultados = sincronizar_diretorios(args.origem, args.destino)
        
        if resultados:
            arquivos_verificados, arquivos_copiados, bytes_transferidos = resultados
            
            # Manda os dados para o SQLite
            registrar_execucao(arquivos_verificados, arquivos_copiados, bytes_transferidos, status="Sucesso")
        else:
            # Se retornou vazio (ex: pasta de origem não existe)
            registrar_execucao(0, 0, 0, status="Erro: Origem não encontrada")
            
    except Exception as e:
        print(f"Erro crítico durante a execução: {e}")
        registrar_execucao(0, 0, 0, status=f"Erro: {str(e)}")

if __name__ == "__main__":
    main()