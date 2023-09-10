import configparser
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from api_handlers import PeJobSearchHandler
from llm.request_chain import get_openapi_llm

config = configparser.ConfigParser()
config.read("config.ini")
client_id = config['credentials']['pe_client_id']
client_secret = config['credentials']['pe_client_secret']
openai_api_key = config['credentials']['open_ai_api_key']

# pe_job_search_api_manager = PeJobSearchHandler(client_id, client_secret)
# response = pe_job_search_api_manager.get_offers_for_commune('51418')
# print(response.status_code, response.text)

openai_model = ChatOpenAI(openai_api_key=openai_api_key, model_name='gpt-3.5-turbo')
keyword_prompt = ChatPromptTemplate.from_template("Retourne une liste de mots-clés (métier, compétence ou contraintes) \
                                                  permettant de rechercher des offres d'emploi liées \
                                                    à la requête utilisateur suivante:\n\n{query}.")
pe_api_chain = get_openapi_llm(spec="src/pe-openapi-spec.json", llm=openai_model, prompt=keyword_prompt)
