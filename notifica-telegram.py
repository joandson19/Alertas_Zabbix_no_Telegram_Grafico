#!/usr/bin/python3

import requests
import base64
import urllib3
import sys
import re
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pyzabbix import ZabbixAPI
from telegram import Bot

urllib3.disable_warnings()

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
CAPTION_TEMPLATE = "Tit: {TITULO}\nDat: {NOW}\n{MENSAGEM}"  # Adicionamos o campo {MENSAGEM}

# Cria o objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Cria um handler de arquivo com rollover e controle de tamanho
file_handler = RotatingFileHandler(filename=log_file, maxBytes=max_log_size, backupCount=log_count)
file_handler.setLevel(logging.INFO)

# Cria um formatter para o handler de arquivo
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Adiciona o handler de arquivo ao logger
logger.addHandler(file_handler)

def get_cookie():
    s = requests.session().get(
        f"{URL_ZABBIX}/index.php?login=1&name={USER}&password={PASS}&enter=Enter"
    )
    return s.cookies

def extract_item_id(mensagem):
    match = re.search(r'Item ID:\s*(\d+)', mensagem)
    if match:
        item_id = match.group(1)
        return item_id
    else:
        return None

def get_image(item_id, item_name, color_code):
    r = requests.get(
        f"{URL_ZABBIX}/chart3.php?name={item_name}&period={PERIOD}&items[0][itemid]={item_id}&items[0][drawtype]={DRAW_TYPE}&items[0][color]={color_code}&width={WIDTH}&height={HEIGHT}",
        cookies=get_cookie()
    )
    return r.content

if __name__ == "__main__":
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
                api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": mensagem_completa,
                    "parse_mode": "Markdown"  # Indica que estamos usando formatação Markdown
                }
                files = {
                    "photo": ("image.png", image_data)
                }
                
                response = requests.post(api_url, data=payload, files=files)
                
                logger.info(f"Item '{item_name}' enviado para o Telegram. Resposta: {response.text}")
            else:
                logger.error(f"Item ID '{item_id}' não encontrado no Zabbix.")
        else:
            logger.error("Item ID não encontrado na mensagem.")
    except Exception as e:
        logger.exception("Ocorreu um erro:", exc_info=e)
