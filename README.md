# Alertas_Zabbix_no_Telegram_Grafico

* Adicione o script notifica-telegram.py dentro de /usr/lib/zabbix/alertscripts/ e crie a pasta log.
```
mkdir /usr/lib/zabbix/alertscripts/log
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

### Este script é uma adaptação do script do [MarreraTech](https://github.com/MarreraTech/Zabbix/tree/main)
