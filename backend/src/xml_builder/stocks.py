from lxml import etree

from src.parser.stocks import get_historical_ticker_transactions

def build_popisni_list(id, ticker_transactions):
    root = etree.Element("KDVPItem")
    item_id = etree.SubElement(root, "ItemID")
    item_id.text = str(id)
    
    
    inventory_list_type = etree.SubElement(root, "InventoryListType")
    inventory_list_type.text = "PLVP"
    name = etree.SubElement(root, "Name")
    name.text = ticker_transactions.iloc[0,3]
    has_foreign_tax = etree.SubElement(root, "HasForeignTax")
    has_foreign_tax.text = "false"
    has_loss_transfer = etree.SubElement(root, "HasLossTransfer")
    has_loss_transfer.text = "false"
    foreign_transfer = etree.SubElement(root, "ForeignTransfer")
    foreign_transfer.text = "false"
    tax_decrease_conformance = etree.SubElement(root, "TaxDecreaseConformance")
    tax_decrease_conformance.text = "false"
    securities = etree.SubElement(root, "Securities")
    isin = etree.SubElement(securities, "ISIN")
    isin.text = ticker_transactions.iloc[0,3]
    is_fond = etree.SubElement(securities, "IsFond")
    is_fond.text = "false"
    
    for _, row in ticker_transactions.iterrows():
        row2 = etree.SubElement(securities, "Row")
        id = etree.SubElement(row2, "ID")
        id.text = str(_+1)
        # nakup
        if row.iloc[6] > 0:
            purchase = etree.SubElement(row2, "Purchase")
            f1 = etree.SubElement(purchase, "F1")
            f1.text = str(row.iloc[0].date())
            f2 = etree.SubElement(purchase, "F2")
            f2.text = "B"
            f3 = etree.SubElement(purchase, "F3")
            f3.text = str(abs(round(row.iloc[6],4)))
            f4 = etree.SubElement(purchase, "F4")
            f4.text = str(abs(round(row["transaction_eur"], 4)))
        else:
            purchase = etree.SubElement(row2, "Sale")
            f6 = etree.SubElement(purchase, "F6")
            f6.text = str(row.iloc[0].date())
            f7 = etree.SubElement(purchase, "F7")
            f7.text = str(abs(round(row.iloc[6],4)))
            f9 = etree.SubElement(purchase, "F9")
            f9.text = str(abs(round(row["transaction_eur"], 4)))
            f10 = etree.SubElement(purchase, "F10")
            f10.text = "false"
            
        
    return root

def build_stock_xml(data, sold_products, year, config):
     
    # Define namespaces
    ns_main = "http://edavki.durs.si/Documents/Schemas/Doh_KDVP_9.xsd"
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
    
    

    # attachment_list =    etree.SubElement(root, "AttachmentList")
    signatures = etree.SubElement(root, etree.QName(ns_edp, "Signatures"))
    body = etree.SubElement(root, "body") 
    
    body_content =   etree.SubElement(body, etree.QName(ns_edp, "bodyContent")) 
    doh_kdvp = etree.SubElement(body, "Doh_KDVP")
    
    
    kdvp = etree.SubElement(doh_kdvp, "KDVP") 
    document_workflow_id = etree.SubElement(kdvp, "DocumentWorkflowID")
    document_workflow_id.text = config["document_workflow_id"]
    year_2 = etree.SubElement(kdvp, "Year")
    year_2.text = str(year)
    period_start = etree.SubElement(kdvp, "PeriodStart")
    period_start.text = f"{year}-01-01"
    period_end = etree.SubElement(kdvp, "PeriodEnd")
    period_end.text = f"{year}-12-31"
    security_count = etree.SubElement(kdvp, "SecurityCount")
    security_count.text =  str(1)
    security_short_count = etree.SubElement(kdvp, "SecurityShortCount")
    security_short_count.text =  str(0)
    security_with_contract_count = etree.SubElement(kdvp, "SecurityWithContractCount")
    security_with_contract_count.text =  str(0)
    security_with_contract_short_count = etree.SubElement(kdvp, "SecurityWithContractShortCount")
    security_with_contract_short_count.text =  str(0)
    share_count = etree.SubElement(kdvp, "ShareCount")
    share_count.text =  str(0)
    
    for _, row in sold_products.iterrows():
        
        ticker_transactions = get_historical_ticker_transactions(data, row["ISIN"], year)
        
        kdvp_item = build_popisni_list(_, ticker_transactions)
        
        
        doh_kdvp.append(kdvp_item)
        
        

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
    