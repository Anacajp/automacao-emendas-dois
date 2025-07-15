from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configurações do driver do Chrome
def setup_driver(download_dir=None):
    options = Options()
    
    if download_dir:
        prefs = {
            "download.default_directory": download_dir, # Caminho exato onde salvar os arquivos baixados
            "download.prompt_for_download": False, # Não mostrar caixa de confirmação de download
            "download.directory_upgrade": True, # Atualiza o diretório de download se mudar
            "safebrowsing.enabled": True # Habilita o modo de navegação segura
        }
        options.add_experimental_option("prefs", prefs)
    
    # options.add_argument("--headless")  # Executa o Chrome em modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def download_file(url, download_dir):
    driver = setup_driver(download_dir)
    
    try:
        driver.get(url)
        logging.info(f"Processando seção: {url}")
        
        wait = WebDriverWait(driver, 10)
        
        # Entra no iframe do Power BI
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id=\"page\"]/div/div[2]/div/div[2]/div/iframe')))
        logging.info("Iframe do dashboard Power BI encontrado e switch realizado.")
        
        # Conta arquivos .xlsx existentes antes do download
        if not os.path.exists(download_dir):
            os.makedirs(download_dir, exist_ok=True)
        arquivos_antes = len([f for f in os.listdir(download_dir) if f.endswith('.xlsx')])
        
        # Localiza e clica no botão de download
        botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Baixar os dados')]")))
        logging.info("Botão 'Baixar os dados' encontrado.")
        driver.execute_script("arguments[0].click();", botao)
        logging.info("Botão 'Baixar os dados' clicado com sucesso (VIA JAVASCRIPT).")
        
        # Espera um novo arquivo ser baixado
        WebDriverWait(driver, 30).until(
            lambda d: len([f for f in os.listdir(download_dir) if f.endswith('.xlsx')]) > arquivos_antes
        )
        logging.info(f"Arquivo baixado com sucesso para {download_dir}")
            
    except Exception as e:
        logging.error(f"Erro durante o processo de download: {e}")
        
    finally:
        # Garante que o driver sempre seja fechado
        driver.quit()
        logging.info("Driver do Chrome fechado.")