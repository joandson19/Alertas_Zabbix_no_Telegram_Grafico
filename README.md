# Alertas_Zabbix_no_Telegram_Grafico

## Adicione o script notifica-telegram.py dentro de /usr/lib/zabbix/alertscripts/ e crie a pasta log.
```
mkdir /usr/lib/zabbix/alertscripts/log
```
## dê as permissões necessárias
```
chown zabbix. -R /usr/lib/zabbix/alertscripts/*
chmod  +x /usr/lib/zabbix/alertscripts/notifica-telegram.py
```
### Importante falar que o "Item ID: {ITEM.ID1}" é obrigatorio no corpo da mensagem para que o grafico funcione.
