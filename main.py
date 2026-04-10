import argparse
from sync_engine import sincronizar_diretorios
from database import registrar_execucao

def main():
    parser = argparse.ArgumentParser(
        description="PySync CLI - Ferramenta de Sincronização Incremental",
        epilog="Exemplo: python3 main.py --origem ./minha_pasta --destino ./meu_backup"
    )
    
    parser.add_argument('--origem', required=True, help="Caminho da pasta original")
    parser.add_argument('--destino', required=True, help="Caminho da pasta de backup")
    
    # NOVA FLAG ADICIONADA:
    parser.add_argument('--dry-run', action='store_true', help="Simula a execução sem copiar nenhum arquivo")
    
    args = parser.parse_args()

    try:
        # Passamos a flag dry_run para o motor
        resultados = sincronizar_diretorios(args.origem, args.destino, dry_run=args.dry_run)
        
        if resultados:
            arquivos_verificados, arquivos_copiados, bytes_transferidos = resultados
            
            # Ajustamos o status no banco de dados se for simulação
            status = "Sucesso (Simulação)" if args.dry_run else "Sucesso"
            
            registrar_execucao(arquivos_verificados, arquivos_copiados, bytes_transferidos, status=status)
        else:
            registrar_execucao(0, 0, 0, status="Erro: Origem não encontrada")
            
    except Exception as e:
        print(f"Erro crítico: {e}")
        registrar_execucao(0, 0, 0, status=f"Erro: {str(e)}")

if __name__ == "__main__":
    main()