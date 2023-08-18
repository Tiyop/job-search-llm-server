import configparser

from api_handlers import PeJobSearchHandler

config = configparser.ConfigParser()
config.read("config.ini")
client_id = config['credentials']['pe_client_id']
client_secret = config['credentials']['pe_client_secret']

pe_job_search_api_manager = PeJobSearchHandler(client_id, client_secret)
response = pe_job_search_api_manager.get_offers_for_commune('51418')

print(response.status_code, response.text)