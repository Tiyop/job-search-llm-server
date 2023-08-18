import requests

class PeJobSearchHandler():
    def __init__(self, c_id, c_secret):
        self.c_id = c_id
        self.c_secret = c_secret
        self.access_token, self.expires_in = self.update_access_token_for_api_oe()

    def update_access_token_for_api_oe(self) -> tuple:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.c_id,
            "client_secret": self.c_secret,
            "scope": "api_offresdemploiv2 o2dsoffre"
        }
        token_json = requests.post(f"https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire", 
                                    data=data).json()
        return token_json["access_token"], token_json["expires_in"]

    def get_offers_for_commune(self, commune):
        headers = {"Authorization": "Bearer " + self.access_token}
        response = requests.get(f"https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?commune={commune}", headers=headers)
        return response