from zeep import Client
from zeep.wsse.username import UsernameToken
from pprint import pprint

wsdl = "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/wsdlnew.ws"
client = Client(wsdl=wsdl, wsse=UsernameToken('JZ99-DZ73-UD52-DF19', ''))


# List available services
print("\nServices:")
for service_name, service in client.wsdl.services.items():
    print(f"  Service: {service_name}")
    for port_name, port in service.ports.items():
        print(f"    Port: {port_name}")
        print(f"      Operations: {list(port.binding._operations.keys())}")


# Replace 'CorrectServiceName' and 'CorrectPortName' with actual names from the above
binding = client.wsdl.services['PostcodeAnywhere'].ports['PostcodeAnywhere_Soap'].binding
operation = binding._operations['AddressComplete_Interactive_Find_v2_10']

# Show the expected request fields
print("\nExpected input elements:")
pprint(operation.input.body.type.elements)





