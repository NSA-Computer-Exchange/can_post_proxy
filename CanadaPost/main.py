from flask import Flask, request, Response
import requests

app = Flask(__name__)
API_KEY = 'JZ99-DZ73-UD52-DF19'
SOAP_ENDPOINT = "https://ws1.postescanada-canadapost.ca/addresscomplete/interactive/find/v2.10/soap12.ws"

SOAP_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                 xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <Find xmlns="http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10">
      <Key>{key}</Key>
      <SearchTerm>{term}</SearchTerm>
      <LanguagePreference>en</LanguagePreference>
      <Country>CAN</Country>
      <MaxSuggestions>5</MaxSuggestions>
    </Find>
  </soap12:Body>
</soap12:Envelope>"""

@app.route('/', methods=['POST','GET'])
def find_address():
    term = request.args.get('term')
    if not term:
        return {"error": "Missing search term (?term=...)"}, 400

    soap_payload = SOAP_TEMPLATE.format(key=API_KEY, term=term)
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

    res = requests.post(SOAP_ENDPOINT, data=soap_payload.encode('utf-8'), headers=headers)

    return Response(res.content, content_type='application/xml', status=res.status_code)

if __name__ == '__main__':
    app.run(debug=True)
