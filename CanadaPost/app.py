from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
API_KEY = 'JZ99-DZ73-UD52-DF19'
FIND_URL = "https://ws1.postescanada-canadapost.ca/addresscomplete/interactive/find/v2.10/soap12.ws"
RETRIEVE_URL = "https://ws1.postescanada-canadapost.ca/addresscomplete/interactive/retrieve/v2.11/soap12.ws"

FIND_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                 xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <Find xmlns="http://ws1.postescanada-canadapost.ca/addresscomplete/interactive/find/v2.10">
      <Key>{key}</Key>
      <SearchTerm>{term}</SearchTerm>
      <LanguagePreference>en</LanguagePreference>
      <Country>{country}</Country>
      <MaxSuggestions>1</MaxSuggestions>
    </Find>
  </soap12:Body>
</soap12:Envelope>"""

RETRIEVE_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                 xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <Retrieve xmlns="http://ws1.postescanada-canadapost.ca/addresscomplete/interactive/retrieve/v2.11">
      <Key>{key}</Key>
      <Id>{id}</Id>
    </Retrieve>
  </soap12:Body>
</soap12:Envelope>"""

CORS(app, supports_credentials=True, origins=["https://sxe12.inforcloudsuite.com"])


@app.route('/addresscomplete/interactive/find/v2.10/soap12.ws', methods=['GET'])
def serve_wsdl():
    with open('static/wsdl/AddressComplete.wsdl', 'r') as f:
        wsdl_content = f.read()
    return Response(wsdl_content, mimetype='text/xml')


# @app.route('/AddressComplete/Interactive/Find/v2.10/soap12.ws')
# def serve_wsdl():
#     return send_from_directory('static/wsdl', 'addresscomplete.wsdl', mimetype='text/xml')

@app.route('/AddressComplete/Interactive/Find/v2.10/soap12.ws', methods=['POST'])
def handle_find():
    response_xml = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <AddressComplete_Interactive_Find_v2_10_Result xmlns="http://ws1.postescanada-canadapost.ca/">
      <AddressComplete_Interactive_Find_v2_10_Results>
        <Id>CA|CP|A|16236336</Id>
        <Text>97 Rue Champlain</Text>
        <Description>Les Cèdres, QC, J7T 0C6</Description>
        <Next>Retrieve</Next>
      </AddressComplete_Interactive_Find_v2_10_Results>
    </AddressComplete_Interactive_Find_v2_10_Result>
  </soap12:Body>
</soap12:Envelope>'''
    return Response(response_xml, mimetype='application/soap+xml')



@app.route('/AddressComplete/Interactive/Retrieve/v2.11/soap12.ws', methods=['POST'])
def handle_retrieve():
    response_xml = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <RetrieveResponse xmlns="http://schemas.postcodeanywhere.com/">
      <Line1>97 Rue Champlain</Line1>
      <City>Les Cèdres</City>
      <Province>QC</Province>
      <PostalCode>J7T 0C6</PostalCode>
      <CountryName>Canada</CountryName>
    </RetrieveResponse>
  </soap12:Body>
</soap12:Envelope>'''
    return Response(response_xml, mimetype='application/soap+xml')
  

@app.route('/AddressComplete/Interactive/Find/v2.10/wsdlnew.ws', methods=['GET'])
def serve_wsdl_find():
    return send_from_directory('static/wsdl', 'wsdlnew.ws', mimetype='text/xml')

@app.route('/AddressComplete/Interactive/Retrieve/v2.11/wsdlnew.ws', methods=['GET'])
def serve_wsdl_retrieve():
    return send_from_directory('static/wsdl', 'wsdlnew.ws', mimetype='text/xml')


@app.route('/proxy', methods=['POST'])
def proxy_infor_request():
    payload = request.get_json()
    if not payload or 'ttbladdrverifycriteria' not in payload:
        return jsonify({"error": "Invalid payload"}), 400

    criteria = payload['ttbladdrverifycriteria']
    street = " ".join(filter(None, [
        criteria.get('streetaddr', ''),
        criteria.get('streetaddr2', ''),
        criteria.get('streetaddr3', '')
    ]))

    search_term = f"{street}, {criteria.get('city', '')}, {criteria.get('state', '')} {criteria.get('zipcd', '')}"
    country_code = criteria.get("country", "CA").upper()

    soap_payload = FIND_TEMPLATE.format(key=API_KEY, term=search_term, country=country_code)
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

    # Step 1: Find
    find_res = requests.post(FIND_URL, data=soap_payload, headers=headers)
    if find_res.status_code != 200:
        return jsonify({"error": "Find call failed"}), 502

    root = ET.fromstring(find_res.content)
    ns_find = {'soap': 'http://www.w3.org/2003/05/soap-envelope', 'f': 'http://schemas.postcodeanywhere.com/'}
    item = root.find('.//f:Result/f:Results', ns_find)

    if item is None or item.find('f:Id', ns_find) is None:
        return jsonify({"ttblmessaging": [{"error": "No matches found"}], "ttbladdrverifyresults": {}}), 200

    result_id = item.find('f:Id', ns_find).text
    next_action = item.find('f:Next', ns_find)
    if next_action is None or next_action.text != "Retrieve":
        return jsonify({"error": "Unexpected Find result format"}), 500

    # Step 2: Retrieve
    retrieve_payload = RETRIEVE_TEMPLATE.format(key=API_KEY, id=result_id)
    retrieve_res = requests.post(RETRIEVE_URL, data=retrieve_payload, headers=headers)
    if retrieve_res.status_code != 200:
        return jsonify({"error": "Retrieve call failed"}), 502

    rroot = ET.fromstring(retrieve_res.content)
    ns_retrieve = {'soap': 'http://www.w3.org/2003/05/soap-envelope', 'r': 'http://schemas.postcodeanywhere.com/'}

    addresses = rroot.findall('.//r:Results', ns_retrieve)

    if not addresses:
        print("DEBUG: Retrieve response:")
        print(retrieve_res.text)
        return jsonify({"error": "No address returned from Retrieve"}), 500

    address = addresses[0]  # take the first suggestion

    def get(tag):
        el = address.find(f"r:{tag}", ns_retrieve)
        return el.text if el is not None else ""

    city = get("City")
    state = get("ProvinceName")
    postal = get("PostalCode")
    street_line = get("Line1")
    country = get("CountryName")

    return jsonify({
        "ttblmessaging": [],
        "ttbladdrverifyresults": {
            "doctype": criteria.get("doctype", "geo"),
            "primarykey": criteria.get("primarykey", ""),
            "secondarykey": criteria.get("secondarykey", ""),
            "streetaddr": street_line,
            "streetaddr2": "",
            "streetaddr3": "",
            "city": city,
            "state": state,
            "zipcd": postal,
            "zipcdext": "",
            "country": country,
            "county": "",
            "addressoverfl": False,
            "geocd": 0,
            "retmsg": "",
            "userfield": ""
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4567)
