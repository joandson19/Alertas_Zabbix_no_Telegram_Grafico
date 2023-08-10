
# Alertas_Zabbix_no_Telegram_Grafico

* Instale as dependencias para o script
```
sudo -H -u zabbix python3 -m pip requests pyzabbix python-telegram-bot
```
* Adicione o script notifica-telegram.py dentro de /usr/lib/zabbix/alertscripts/ e crie a pasta log.
```
# cd /tmp
# git clone https://github.com/joandson19/Alertas_Zabbix_no_Telegram_Grafico.git
# cd Alertas_Zabbix_no_Telegram_Grafico
# mv * /usr/lib/zabbix/alertscripts/
```
* dê as permissões necessárias
```
chown zabbix. -R /usr/lib/zabbix/alertscripts/*
chmod  +x /usr/lib/zabbix/alertscripts/notifica-telegram.py
```
* Importante falar que o "Item ID: {ITEM.ID1}" é obrigatorio no corpo da mensagem para que o grafico funcione.
Segue um modelo de mensagem, o titulo fica live a sua escolha.
```
⏰ Inicio do problema às {EVENT.TIME} em {EVENT.DATE}
Host: {HOST.NAME}
Serveridade: {EVENT.SEVERITY}
Último valor: {ITEM.VALUE1}
Item ID: {ITEM.ID1}
```

### Este script é uma adaptação do script de envio do [MarreraTech](https://github.com/MarreraTech/Zabbix/tree/main) que no caso dele é usado para enviar o alerta com grafico para o WhatsApp com a API da MarreraTech.
