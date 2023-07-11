import requests
from datetime import datetime, timedelta
import pandas as pd
import json

slack_token = ''       # your Slack Token
slack_channel = ''     # your Slack Channel
slack_icon_emoji = ''  # your Slack emoji
slack_user_name = ''   # your Slack username

def post_message_to_slack(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()	
    

td = datetime.today().strftime('%Y-%m-%d') #get today
ytd = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d') # get yesterday
nif_1 = '' #Fiscal Number you want to search
text_2 = '' #you text
district = '' #check in base.gov.pt for your district code (Lisbon is 12)
city = '' #check in base.gov.pt for your city code (Lisbon is 0)

url_1 = 'https://www.base.gov.pt/Base4/pt/resultados/?type=csv_contratos&texto=' + nif_1 + '&tipo=0&tipocontrato=0&desdedatapublicacao=' + ytd + '&atedatapublicacao=' + td +'&pais=187&distrito=' + district + '&concelho=' + city + '&sort(-publicationDate)'

url_2 = 'https://www.base.gov.pt/Base4/pt/resultados/?type=csv_contratos&texto=' + text_2 + '&tipo=0&tipocontrato=0&desdedatapublicacao=' + ytd + '&atedatapublicacao=' + td +'&pais=187&distrito=' + district + '&concelho=' + city + '&sort(-publicationDate)'

#headers = {
#"Accept-Language" : pt-PT,
#"User-Agent": "Defined",
#}

response_nif_1 = requests.get(url_1)
response_text_2 = requests.get(url_2)

open("contratos_emel.csv", "wb").write(response_nif_1.content)
open("contratos_ciclovia.csv", "wb").write(response_text_2.content)

df_nif_1 = pd.read_csv('contratos_emel.csv', sep=';', header = None)
df_text_2 = pd.read_csv('contratos_ciclovia.csv', sep=';', header = None)

i = 1

if (len(df_nif_1) == 1 and len(df_text_2) == 1):
    msg_nif_1 = "Nothing new today"
    post_message_to_slack(msg_nif_1)
else:
    while i < len(df_nif_1):

        ''' here you must config your message depending of your CSV'''
        msg_nif_1 = '############New contract for ' + nif_1 + '############\nObjeto: ' + df_nif_1.iat[i,0] + "\nTipo de Procedimento: " + df_nif_1.iat[i,1] + "\nTipo de Contrato: " + df_nif_1.iat[i,2] + "\nCPV: " + df_nif_1.iat[i,5] + "\nAdjucante: " + df_nif_1.iat[i,7] + "\nAdjucatária: " + df_nif_1.iat[i,8] + "\nPreço: " + df_nif_1.iat[i,9] + "\nData Contrato: " + df_nif_1.iat[i,10] + "\nData Publicação: " + df_nif_1.iat[i,11] + "\nPrazo: " + df_nif_1.iat[i,12] + "\nLocal: " + df_nif_1.iat[i,13] + "\n"
        
        post_message_to_slack(msg_nif_1)	
        i += 1

    i = 1
    while i < len(df_text_2):

        msg_text_2 = '############New contract for ' + text_2 + '############\nObjeto: ' + df_text_2.iat[i,0] + "\nTipo de Procedimento: " + df_text_2.iat[i,1] + "\nTipo de Contrato: " + df_text_2.iat[i,2] + "\nCPV: " + df_text_2.iat[i,5] + "\nAdjucante: " + df_text_2.iat[i,7] + "\nAdjucatária: " + df_text_2.iat[i,8] + "\nPreço: " + df_text_2.iat[i,9] + "\nData Contrato: " + df_text_2.iat[i,10] + "\nData Publicação: " + df_text_2.iat[i,11] + "\nPrazo: " + df_text_2.iat[i,12] + "\nLocal: " + df_text_2.iat[i,13] + "\n"
        
        post_message_to_slack(msg_text_2)	
        i += 1