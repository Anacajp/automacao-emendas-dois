import asyncio
from playwright.async_api import async_playwright
import logging

logging.basicConfig(level=logging.INFO)

async def baixar_arquivo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto("https://www.governo.sp.gov.br/transferencias-voluntarias-2023-dep-estaduais/")
        logging.info("Página carregada com sucesso.")

        # Seletor específico do iframe do Power BI
        iframe = page.frame_locator('iframe[title="Emendas_TV_2023"]')
        logging.info("Iframe do dashboard Power BI encontrado.")

        # Espera a renderização do terceiro g.tile
        botao_visual = iframe.locator("g.tile").nth(2)
        await botao_visual.wait_for(state="visible")
        logging.info("Elemento visual do botão 'Baixar os dados' localizado.")

        # Aguarda e clica com confirmação de download
        async with page.expect_download() as download_info:
            logging.info("Clicando no botão 'Baixar os dados' (g.tile #3)...")
            await botao_visual.click(force=True)
        logging.info("Aguardando download...")

        # Salva o arquivo baixado
        download = await download_info.value
        filename = "dados_emendas_2023.xlsx"
        await download.save_as(filename)
        logging.info(f"Download concluído com sucesso! Arquivo salvo como {filename}")

        await browser.close()
        logging.info("Navegador fechado.")

# Execução segura
asyncio.run(baixar_arquivo())
