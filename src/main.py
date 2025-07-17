import logging
import asyncio
import os
from downloader import baixar_arquivo
from updater import atualizar_planilha_google

# Configurar logging para Cloud Run
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    """Função principal que orquestra todo o processo"""
    try: 
        logging.info("Iniciando o processo de download e atualização...")
        
        # Verificar variáveis de ambiente essenciais
        if not os.getenv('GOOGLE_SHEET_ID'):
            logging.error("GOOGLE_SHEET_ID não encontrado nas variáveis de ambiente")
            return
        
        logging.info(f"Planilha alvo: {os.getenv('GOOGLE_SHEET_ID')}")

        # 1. Download de todos os arquivos
        arquivos_baixados = await baixar_arquivo()

        # 2. Atualizar a planilha do Google
        if arquivos_baixados:
            await atualizar_planilha_google(arquivos_baixados)
        else:
            logging.warning("Nenhum arquivo foi baixado. Pulando atualização da planilha.")

        logging.info("Processo concluído com sucesso!")

    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())