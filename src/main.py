import requests
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
client_id = config['credentials']['pe_client_id']
client_secret = config['credentials']['pe_client_secret']

def get_access_token_for_api_oe() -> tuple:
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    token_json = requests.post(f"https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire", 
                                data=data).json()
    return token_json["access_token"], token_json["expires_in"]

access_token, duration = get_access_token_for_api_oe()
print(access_token, duration)
headers = {"Authorization": "Bearer " + access_token}

response = requests.get("https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?commune=51069", headers=headers)
print(response.status_code, response.text)