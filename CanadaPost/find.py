from zeep import Client
from zeep.wsse.username import UsernameToken

wsdl = "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/wsdlnew.ws"
client = Client(wsdl=wsdl, wsse=UsernameToken('JZ99-DZ73-UD52-DF19', ''))

response = client.service.AddressComplete_Interactive_Find_v2_10(
    Key='JZ99-DZ73-UD52-DF19',
    SearchTerm='97 Champlain Les Cedres Quebec J7T 0C6',
    Country='CAN',
    LanguagePreference='en',
    MaxSuggestions=1,
    MaxResults=10,
    Bias=True
)

print(response)