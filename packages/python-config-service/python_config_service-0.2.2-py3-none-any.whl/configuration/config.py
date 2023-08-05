import requests
import json

def get_vault_config(iden, token, url=None):
    if url:
        vault_url = url
    else:
        vault_url = "https://configuration.rancher.cloud-h.net/api/configuration"

    payload = {"id": iden, "token": token}
    headers = {'content-type': 'application/json'}

    response = requests.request("POST", vault_url, data=json.dumps(payload), headers=headers)
    response_content = json.loads(response.content.decode('utf-8'))
    
    if response_content['status'] == 'success':
        return response_content['data']
    
    return None