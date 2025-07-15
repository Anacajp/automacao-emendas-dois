import logging
import asyncio
from downloader import baixar_arquivo
from updater import atualizar_planilha_google

logging.basicConfig(level=logging.INFO)

async def main():
        """Função principal que orquestra todo o processo"""
        try: 
            logging.info("Iniciando o processo de download e atualização...")

            # 1. Download de todos os arquivos
            arquivo_baixados = await baixar_arquivo()

            # 2. Atualizar a planilha do Google
            #await atualizar_planilha_google(arquivo_baixados)

            logging.info("Processo concluído com sucesso!")

        except Exception as e:
            logging.error(f"Ocorreu um erro: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(main())