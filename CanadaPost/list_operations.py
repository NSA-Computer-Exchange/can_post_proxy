from zeep import Client
from zeep.wsse.username import UsernameToken

wsdl = "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/wsdlnew.ws"
client = Client(wsdl=wsdl, wsse=UsernameToken('JZ99-DZ73-UD52-DF19', ''))

print("Available operations:")
for service in client.wsdl.services.values():
    for port in service.ports.values():
        operations = sorted(port.binding._operations.keys())
        print(f"{port.name}: {operations}")
