<?xml version='1.0' encoding='utf-8'?>
<wsdl:definitions xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="http://ws1.postescanada-canadapost.ca/">
  <wsdl:types>
    <xs:schema elementFormDefault="qualified" targetNamespace="http://ws1.postescanada-canadapost.ca/">
      <xs:element name="AddressComplete_Interactive_Find_v2_10">
        <xs:complexType>
          <xs:sequence>
            <xs:element minOccurs="0" maxOccurs="1" name="Key" type="s:string" />
            <xs:element minOccurs="0" maxOccurs="1" name="SearchTerm" type="s:string" />
            <xs:element minOccurs="0" maxOccurs="1" name="LastId" type="s:string" />
            <xs:element minOccurs="0" maxOccurs="1" name="SearchFor" type="s:string" />
            <xs:element minOccurs="0" maxOccurs="1" name="Country" type="s:string" />
            <xs:element minOccurs="0" maxOccurs="1" name="LanguagePreference" type="s:string" />
            <xs:element minOccurs="1" maxOccurs="1" name="MaxSuggestions" type="s:int" />
            <xs:element minOccurs="1" maxOccurs="1" name="MaxResults" type="s:int" />
            <xs:element minOccurs="0" maxOccurs="1" name="Origin" type="s:string" />
            <xs:element minOccurs="1" maxOccurs="1" name="Bias" type="s:boolean" />
            <xs:element minOccurs="0" maxOccurs="1" name="Filters" type="s:string" />
            <xs:element minOccurs="0" maxOccurs="1" name="GeoFence" type="s:string" />
          </xs:sequence>
        </xs:complexType>
      </xs:element>
      <xs:element name="AddressComplete_Interactive_Find_v2_10_Response">
        <xs:complexType>
          <xs:sequence>
            <xs:element minOccurs="0" maxOccurs="1" name="AddressComplete_Interactive_Find_v2_10_Result" type="tns:AddressComplete_Interactive_Find_v2_10_ArrayOfResults" />
          </xs:sequence>
        </xs:complexType>
      </xs:element>
      <xs:complexType name="AddressComplete_Interactive_Find_v2_10_ArrayOfResults">
        <xs:sequence>
          <xs:element minOccurs="0" maxOccurs="unbounded" name="AddressComplete_Interactive_Find_v2_10_Results" type="tns:AddressComplete_Interactive_Find_v2_10_Results" />
        </xs:sequence>
      </xs:complexType>
      <xs:complexType name="AddressComplete_Interactive_Find_v2_10_Results">
        <xs:sequence>
          <xs:element minOccurs="0" maxOccurs="1" name="Id" type="s:string" />
          <xs:element minOccurs="0" maxOccurs="1" name="Text" type="s:string" />
          <xs:element minOccurs="0" maxOccurs="1" name="Highlight" type="s:string" />
          <xs:element minOccurs="1" maxOccurs="1" name="Cursor" type="s:int" />
          <xs:element minOccurs="0" maxOccurs="1" name="Description" type="s:string" />
          <xs:element minOccurs="0" maxOccurs="1" name="Next" type="s:string" />
        </xs:sequence>
      </xs:complexType>
    </xs:schema>
  </wsdl:types>
  <wsdl:message name="AddressComplete_Interactive_Find_v2_10_SoapIn">
    <wsdl:part name="parameters" element="tns:AddressComplete_Interactive_Find_v2_10" />
  </wsdl:message>
  <wsdl:message name="AddressComplete_Interactive_Find_v2_10_SoapOut">
    <wsdl:part name="parameters" element="tns:AddressComplete_Interactive_Find_v2_10_Response" />
  </wsdl:message>
  <wsdl:portType name="PostcodeAnywhere_Soap">
    <wsdl:operation name="AddressComplete_Interactive_Find_v2_10">
      <wsdl:input message="tns:AddressComplete_Interactive_Find_v2_10_SoapIn" />
      <wsdl:output message="tns:AddressComplete_Interactive_Find_v2_10_SoapOut" />
    </wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="PostcodeAnywhere_Soap" type="tns:PostcodeAnywhere_Soap">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http" />
    <wsdl:operation name="AddressComplete_Interactive_Find_v2_10">
      <soap:operation soapAction="http://ws1.postescanada-canadapost.ca/AddressComplete_Interactive_Find_v2_10" style="document" />
      <wsdl:input>
        <soap:body use="literal" />
      </wsdl:input>
      <wsdl:output>
        <soap:body use="literal" />
      </wsdl:output>
    </wsdl:operation>
  </wsdl:binding>
  <wsdl:service name="PostcodeAnywhere_Soap"><wsdl:port name="PostcodeAnywhere_Soap" binding="tns:PostcodeAnywhere_Soap"><soap:address location="https://can-post-proxy.onrender.com/AddressComplete/Interactive/Find/v2.10/soap12.ws" /></wsdl:port></wsdl:service></wsdl:definitions>
