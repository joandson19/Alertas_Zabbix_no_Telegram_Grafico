#!/usr/bin/python3
# Reescrito e Adaptado por Joandson Bezerra 

import sys
import re
from datetime import datetime
from loguru import logger
import httpx
from pyzabbix import ZabbixAPI
from telegram import Bot
from telegram.constants import ParseMode

# Suas configurações e constantes
TELEGRAM_TOKEN = sys.argv[1]
TELEGRAM_CHAT_ID = sys.argv[2]
URL_ZABBIX = "https://URL DO ZABBIX"
USER = "login do zabbix"
PASS = "senha do zabbix"
log_file = '/usr/lib/zabbix/alertscripts/log/zabbix_telegram.log'
max_log_size = 10 * 1024 * 1024
log_count = 1

# Outras configurações
WIDTH = "800"
HEIGHT = "250"
DRAW_TYPE = "5"
PERIOD = "3600"
NOW = datetime.now()

# Configuração do logger
logger.add(log_file, rotation=max_log_size, retention=log_count)

def get_cookie():
    with httpx.Client() as client:
        response = client.get(
            f"{URL_ZABBIX}/index.php?login=1&name={USER}&password={PASS}&enter=Enter"
        )
        return response.cookies

def extract_item_id(mensagem):
    match = re.search(r'Item ID:\s*(\d+)', mensagem)
    if match:
        item_id = match.group(1)
        return item_id
    else:
        return None

def get_image(item_id, item_name, color_code):
    with httpx.Client() as client:
        response = client.get(
            f"{URL_ZABBIX}/chart3.php?name={item_name}&period={PERIOD}&items[0][itemid]={item_id}&items[0][drawtype]={DRAW_TYPE}&items[0][color]={color_code}&width={WIDTH}&height={HEIGHT}",
            cookies=get_cookie()
        )
        return response.content

async def main():
    try:
        assunto = sys.argv[3]  # Captura o assunto do argv[2]
        mensagem = sys.argv[4]
        item_id = extract_item_id(mensagem)
        
        color_code_match = re.search(r'#(.*?)#', mensagem)
        if color_code_match:
            color_code = color_code_match.group(1)
            # Remover o código de cor da mensagem original
            mensagem = mensagem.replace(color_code_match.group(0), "")
        else:
            color_code = "00C800"  # Cor padrão
        
        if item_id:
            zapi = ZabbixAPI(URL_ZABBIX)
            zapi.session.verify = False
            zapi.login(USER, PASS)
            item = zapi.item.get(filter={"itemid": item_id})
            
            if item:
                item_name = item[0]["name"]
                image_data = get_image(item_id, item_name, color_code)
                
                # Montar a mensagem que será enviada para o Telegram com formatação Markdown
                mensagem_completa = f"{assunto}\n\n{mensagem}"
                
                # Enviar a imagem e a mensagem formatada para o Telegram usando URL
                bot = Bot(token=TELEGRAM_TOKEN)
                await bot.send_photo(
                    TELEGRAM_CHAT_ID,
                    photo=image_data,
                    caption=mensagem_completa,
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"Item '{item_name}' enviado para o Telegram.")
            else:
                logger.error(f"Item ID '{item_id}' não encontrado no Zabbix.")
        else:
            logger.error("Item ID não encontrado na mensagem.")
    except Exception as e:
        logger.exception("Ocorreu um erro:", exc_info=e)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
