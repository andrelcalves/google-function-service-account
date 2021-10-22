import json

#google SDK
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

#AWS SDK
import boto3
from botocore.exceptions import ClientError


# Secret manager que contém as informações para autenticação do GCP
secret_name = "arn:aws:secretsmanager:us-east-1:720414165514:secret:app/gdem/srv/gcp-YphkPd"
region_name = "us-east-1"

# Utilização do AWS SDK (Boto) para criar um client com o serviço do Secrets Manager
session = boto3.session.Session()
client = session.client(service_name='secretsmanager',region_name=region_name)

try:
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
except ClientError as e:
    raise e
else:
    secret = get_secret_value_response['SecretString']

resp_dict  = json.loads(secret)

# api da google function ou de outro service da google
url = 'https://us-central1-sandbox-gdem-migracao.cloudfunctions.net/function-poc-andre'

# preparar as credencias para geracao da session de autenticacao
creds = service_account.IDTokenCredentials.from_service_account_info(resp_dict,target_audience=url)

# Esta classe(AuhotizedSession) é utilizada para peformar requests para API endpoints que requerem autorização.
authed_session = AuthorizedSession(creds)

function_payload = '{"message":"Payload da google function GDEM"}'

# carregar o retorno da secret em formato json
json_payload = json.loads(function_payload)

#envio da requisicao POST
resp = authed_session.post(url,json= json_payload)

# token gerado na GCP
print(creds.token)

#retorno da google function
print("Retorno da Google Function andre_poc : ",resp.content)
