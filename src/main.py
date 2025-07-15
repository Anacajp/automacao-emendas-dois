import os
from downloader import download_file
import logging

url = "https://www.governo.sp.gov.br/transferencias-voluntarias-2023-dep-estaduais/"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
    # Define o diretório de download
        download_dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(download_dir, exist_ok=True)

        download_file(url, download_dir)
        logging.info("Download concluído com sucesso.")

    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")

    finally:
        logging.info("Processo finalizado.")

if __name__ == "__main__":
    main()