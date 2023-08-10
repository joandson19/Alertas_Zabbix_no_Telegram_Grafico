
# Alertas_Zabbix_no_Telegram_Grafico

* Instale as dependencias para o script
```
# sudo -H -u zabbix python3 -m pip requests pyzabbix python-telegram-bot
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
# chown zabbix. -R /usr/lib/zabbix/alertscripts/*
# chmod  +x /usr/lib/zabbix/alertscripts/notifica-telegram.py
```
* Importante falar que o "Item ID: {ITEM.ID1}" é obrigatorio no corpo da mensagem para que o grafico funcione.
Segue um modelo de mensagem, o assunto fica live a sua escolha.
```
⏰ Inicio do problema às {EVENT.TIME} em {EVENT.DATE}
Host: {HOST.NAME}
Serveridade: {EVENT.SEVERITY}
Último valor: {ITEM.VALUE1}
Item ID: {ITEM.ID1}
```
* Segue abaixo modo que tem que ficar o "Tipo de Mídia"

![image](https://github.com/joandson19/Alertas_Zabbix_no_Telegram_Grafico/assets/36518985/6017affa-8811-4ddc-9bb6-851e9ee309f6)

* Segue configuração de Midia do Usuario!

![image](https://github.com/joandson19/Alertas_Zabbix_no_Telegram_Grafico/assets/36518985/3d70d58a-149e-474a-892d-6a296afb4afe)


* Segue exemplo para incidente
  
![image](https://github.com/joandson19/Alertas_Zabbix_no_Telegram_Grafico/assets/36518985/a6f09bb1-888d-42cb-9dad-02528d823876)
* Segue exemplo para resolvido
  
![image](https://github.com/joandson19/Alertas_Zabbix_no_Telegram_Grafico/assets/36518985/5ee6f68b-3212-4fe4-b51c-879448e1ff4b)

### Este script é uma adaptação do script de envio do [MarreraTech](https://github.com/MarreraTech/Zabbix/tree/main) que no caso dele é usado para enviar o alerta com grafico para o WhatsApp com a API da MarreraTech.

