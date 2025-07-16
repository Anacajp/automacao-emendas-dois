import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Configurações do Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Mapeamento dos arquivos para abas específicas
MAPEAMENTO_ABAS = {
    'emendas_voluntarias_2023': 'BASE - VOLUNTÁRIAS - 2023',
    'emendas_voluntarias_2024': 'BASE - VOLUNTÁRIAS - 2024', 
    'emendas_voluntarias_2025': 'BASE - VOLUNTÁRIAS - 2025',
    'emendas_impositivas_2025': 'BASE - IMPOSITIVAS - 2025'
}

def autenticar_google_sheets():
    """Autentica e retorna o cliente do Google Sheets"""
    try:
        # Caminho para o arquivo de credenciais
        credentials_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'config', 
            'google_credentials.json'
        )
        
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credentials_path}")
        
        # Configurar credenciais
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        
        # Conectar ao Google Sheets
        gc = gspread.authorize(creds)
        logging.info("Autenticação com Google Sheets realizada com sucesso!")
        
        return gc
        
    except Exception as e:
        logging.error(f"Erro na autenticação com Google Sheets: {e}")
        raise

def identificar_tipo_arquivo(nome_arquivo):
    """Identifica o tipo do arquivo baseado no nome"""
    nome_arquivo = os.path.basename(nome_arquivo).lower()
    
    for tipo, aba in MAPEAMENTO_ABAS.items():
        if tipo in nome_arquivo:
            return aba
    
    # Fallback baseado em palavras-chave
    if 'impositivas' in nome_arquivo:
        return 'BASE - IMPOSITIVAS - 2025'
    elif '2025' in nome_arquivo:
        return 'BASE - VOLUNTÁRIAS - 2025'
    elif '2024' in nome_arquivo:
        return 'BASE - VOLUNTÁRIAS - 2024'
    elif '2023' in nome_arquivo:
        return 'BASE - VOLUNTÁRIAS - 2023'
    
    return 'Dados Gerais'  # Aba padrão

def atualizar_aba_planilha(worksheet, df, nome_aba):
    """Substitui TODOS os dados da aba pela planilha Excel"""
    try:
        logging.info(f"Substituindo dados da aba '{nome_aba}'...")
        
        # Limpa TODA a aba
        worksheet.clear()
        
        # Substitui NaN por string vazia
        df = df.fillna('')
        
        # Prepara cabeçalhos + dados
        headers = [df.columns.tolist()]
        dados = df.values.tolist()
        todos_os_dados = headers + dados
        
        if todos_os_dados:
            # Calcula dimensões necessárias
            num_linhas = len(todos_os_dados)
            num_colunas = len(todos_os_dados[0])
            
            # Garante que a planilha tem colunas suficientes
            if worksheet.col_count < num_colunas:
                worksheet.add_cols(num_colunas - worksheet.col_count)
            
            # Cola TUDO a partir de A1
            range_to_update = f"A1:{gspread.utils.rowcol_to_a1(num_linhas, num_colunas)}"
            worksheet.update(range_to_update, todos_os_dados)
            
            logging.info(f"Aba '{nome_aba}' substituída com {num_linhas-1} linhas de dados!")
        else:
            logging.warning(f"Nenhum dado para colar na aba '{nome_aba}'")
            
    except Exception as e:
        logging.error(f"Erro ao atualizar aba '{nome_aba}': {e}")
        raise

async def atualizar_planilha_google(arquivos_baixados, sheet_id=None):
    """Função principal para atualizar a planilha Google"""
    if not arquivos_baixados:
        logging.warning("Nenhum arquivo foi fornecido para atualização")
        return
    
    try:
        # Autentica com Google Sheets
        gc = autenticar_google_sheets()
        
        # Obtém o ID da planilha das variáveis de ambiente ou configuração
        if not sheet_id:
            sheet_id = os.getenv('GOOGLE_SHEET_ID')
            if not sheet_id:
                raise ValueError("ID da planilha não encontrado. Configure GOOGLE_SHEET_ID")
        
        # Abre a planilha
        spreadsheet = gc.open_by_key(sheet_id)
        logging.info(f"Planilha '{spreadsheet.title}' aberta com sucesso!")
        
        # Processa cada arquivo
        for arquivo in arquivos_baixados:
            try:
                logging.info(f"Processando arquivo: {os.path.basename(arquivo)}")
                
                # Lê o arquivo Excel
                df = pd.read_excel(arquivo)
                
                # Identifica qual aba usar
                nome_aba = identificar_tipo_arquivo(arquivo)
                
                # Tenta abrir a aba ou cria uma nova
                try:
                    worksheet = spreadsheet.worksheet(nome_aba)
                except gspread.WorksheetNotFound:
                    logging.info(f"Aba '{nome_aba}' não encontrada. Criando nova aba...")
                    worksheet = spreadsheet.add_worksheet(title=nome_aba, rows=1000, cols=26)
                
                # Substitui TODOS os dados da aba
                atualizar_aba_planilha(worksheet, df, nome_aba)
                
            except Exception as e:
                logging.error(f"Erro ao processar arquivo {arquivo}: {e}")
                continue
        
        logging.info("Atualização da planilha Google concluída com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro geral na atualização da planilha Google: {e}")
        raise

