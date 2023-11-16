from lxml import etree



def build_dividend_xml(data, year, config):
    # Define namespaces
    ns_main = "http://edavki.durs.si/Documents/Schemas/Doh_Div_3.xsd"
    ns_edp = "http://edavki.durs.si/Documents/Schemas/EDP-Common-1.xsd"

    root = etree.Element("Envelope", xmlns=ns_main, nsmap={'edp': ns_edp})
    
    # Create child elements
    header = etree.SubElement(root, etree.QName(ns_edp, "Header"))
    taxpayer = etree.SubElement(header, etree.QName(ns_edp, "taxpayer"))
    
    taxpayernumber = etree.SubElement(taxpayer, etree.QName(ns_edp, "taxNumber"))
    taxpayernumber.text = config["tax_payer_number"]
    
    taxpayertype = etree.SubElement(taxpayer, etree.QName(ns_edp, "taxpayerType"))
    taxpayertype.text = config["tax_payer_type"]
    
    name = etree.SubElement(taxpayer, etree.QName(ns_edp, "name"))
    name.text = config["name"]
    
    address1 = etree.SubElement(taxpayer, etree.QName(ns_edp, "address1"))
    address1.text = config["address1"]
    
    
    city = etree.SubElement(taxpayer, etree.QName(ns_edp, "city"))
    city.text =config["city"]
    
    post_number = etree.SubElement(taxpayer, etree.QName(ns_edp, "postNumber"))
    post_number.text = config["post_number"]
    
    post_name = etree.SubElement(taxpayer, etree.QName(ns_edp, "postName"))
    post_name.text = config["post_name"]
    
    workflow = etree.SubElement(header, etree.QName(ns_edp, "Workflow"))
    document_workflow_id = etree.SubElement(workflow, etree.QName(ns_edp, "DocumentWorkflowID"))
    document_workflow_id.text = config["document_workflow_id"]
    document_workflow_name = etree.SubElement(workflow, etree.QName(ns_edp, "DocumentWorkflowName"))

    # attachment_list =    etree.SubElement(root, "AttachmentList")
    signatures = etree.SubElement(root, etree.QName(ns_edp, "Signatures"))
    body = etree.SubElement(root, "body")   
    doh_div = etree.SubElement(body, "Doh_Div")
    period = etree.SubElement(doh_div, "Period")
    period.text = f"{year}"
    
    

    for _, row in data.iterrows():
        dividend = etree.SubElement(body, "Dividend")
        # Add logic to build XML elements based on DataFrame rows
        date = etree.SubElement(dividend, "Date")
        date.text = row['Datum.1'].strftime("%Y-%m-%d")
        payer_tax_num = etree.SubElement(dividend, "PayerTaxNumber")
        # PayerTaxNumber.text = row[""]
        payer_ident_num = etree.SubElement(dividend, "PayerIdentificationNumber")
        payer_ident_num.text = f"{(_+1)}"
        
        payer_name = etree.SubElement(dividend, "PayerName")
        payer_name.text = config["payer_name"]
        
        payer_address = etree.SubElement(dividend, "PayerAddress")
        payer_address.text = config["payer_address"]
        
        payer_country = etree.SubElement(dividend, "PayerCountry")
        payer_country.text = config["payer_country"]
        
        type = etree.SubElement(dividend, "Type")
        type.text = config["type"]
        
        value = etree.SubElement(dividend, "Value")
        value.text = str(round(row["transaction_eur"], 2))
        
        ForeignTax = etree.SubElement(dividend, "ForeignTax")
        ForeignTax.text = str(round((row["transaction_eur"]*100/(100-config["foreign_tax_percent"]))-row["transaction_eur"], 2))
        
        source_country = etree.SubElement(dividend, "SourceCountry")
        source_country.text = config["source_country"]
        
        relief_statement = etree.SubElement(dividend, "ReliefStatement")
        relief_statement.text = config["relief_statement"]

    # corp_data = etree.SubElement(body, "CorpData")
    # corp_data_detail = etree.SubElement(body, "CorpDataDetail")
    # subseqsubmissdecision = etree.SubElement(body, "SubseqSubmissDecision")
    # subseqsubmissproposal = etree.SubElement(body, "SubseqSubmissProposal")
    
    # Serialize the ElementTree to a string
    xml_string = etree.tostring(root, xml_declaration=True, encoding='utf-8').decode('utf-8')
    
    # Print the generated XML
    print(xml_string)

    # Save the XML to a file
    return xml_string
    