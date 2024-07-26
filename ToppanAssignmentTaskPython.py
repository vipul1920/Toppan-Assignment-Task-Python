import re
from lxml import etree
from datetime import datetime

# Function to create XML elements
def create_element(tag, text):
    element = etree.Element(tag)
    element.text = text if text and text != '|' else ''
    return element

# Function to prettify the XML output
def prettify(element):
    return etree.tostring(element, pretty_print=True, encoding='unicode')

# File paths
input_file = "C:/Users/Vipul Potdar/Desktop/Toppan Assignment Task Python/orderform.txt"
output_file = "C:/Users/Vipul Potdar/Desktop/Toppan Assignment Task Python/Generated_Output.xml"

# Read the input file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Create the root XML element
order_form = etree.Element("OrderForm")

# Variables to store data
customer_name = "!CUSTOMER_NAME__!!"
mask_supplier = ""
date = ""
site_of = ""
orderform_number = ""
revision = ""
page = ""
technology_name = ""
status = ""
mask_set_name = ""
fab_unit = ""
email_address = ""
device = ""
levels = []
cdinfo = []
po_numbers = ""
site_to_send_masks_to = ""
site_to_send_invoice_to = ""
technical_contact = ""
shipping_method = ""
additional_information = ""

# Hash to map month abbreviations to numbers
months = {
    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
    'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
    'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
}

# Parse the input file content
for line in lines:
    line = line.strip()
    if re.search(r'MASK SUPPLIER : (\w+)', line):
        mask_supplier = re.search(r'MASK SUPPLIER : (\w+)', line).group(1)
    if re.search(r'DATE : (\d{2})\/(\d{2})\/(\d{4})', line):
        date_match = re.search(r'DATE : (\d{2})\/(\d{2})\/(\d{4})', line)
        date = f"{date_match.group(3)}-{date_match.group(1)}-{date_match.group(2)}"
    if re.search(r'SITE OF : (\w+)', line):
        site_of = re.search(r'SITE OF : (\w+)', line).group(1)
    if re.search(r'ORDERFORM NUMBER : (IP \d+)', line):
        orderform_number = re.search(r'ORDERFORM NUMBER : (IP \d+)', line).group(1)
    if re.search(r'REVISION : (\d+)', line):
        revision = re.search(r'REVISION : (\d+)', line).group(1)
    if re.search(r'PAGE : (\d+)', line):
        page = re.search(r'PAGE : (\d+)', line).group(1)
    if re.search(r'DEVICE\s*:\s*(.+?)\s*\|', line):
        device = re.search(r'DEVICE\s*:\s*(.+?)\s*\|', line).group(1).strip()
    if re.search(r'TECHNOLOGY NAME : (.+?)\s+STATUS\s*:', line):
        technology_name = re.search(r'TECHNOLOGY NAME : (.+?)\s+STATUS\s*:', line).group(1).strip()
    if re.search(r'STATUS\s*:\s*(N0)', line):
        status = re.search(r'STATUS\s*:\s*(N0)', line).group(1)
    if re.search(r'MASK SET NAME : (\w+)', line):
        mask_set_name = re.search(r'MASK SET NAME : (\w+)', line).group(1)
    if re.search(r'FAB UNIT\s*:\s*(.+?)\s+EMAIL\s*:', line):
        fab_unit = re.search(r'FAB UNIT\s*:\s*(.+?)\s+EMAIL\s*:', line).group(1).strip()
    if re.search(r'EMAIL : (\S+)', line):
        email_address = re.search(r'EMAIL : (\S+)', line).group(1)
    if re.search(r'LEVEL\s+MASK CODIFICATION\s+GRP\s+CYCL\s+QTY\s+SHIP DATE', line):
        continue  # Skip the header line
    if re.search(r'(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d{2})([A-Z]{3})(\d{2})', line):
        level_match = re.search(r'(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|\s*(\d{2})([A-Z]{3})(\d{2})', line)
        num = level_match.group(1)
        mask_codification = level_match.group(2).strip()
        group = level_match.group(3)
        cycle = level_match.group(4)
        quantity = level_match.group(5)
        day = level_match.group(6)
        month = months[level_match.group(7)]
        year = f"20{level_match.group(8)}"
        ship_date = f"{year}-{month}-{day}"
        levels.append({
            'num': num,
            'mask_codification': mask_codification,
            'group': group,
            'cycle': cycle,
            'quantity': quantity,
            'ship_date': ship_date,
        })
    if re.search(r'P\.O\. NUMBERS : (\S+)', line):
        po_numbers = re.search(r'P\.O\. NUMBERS : (\S+)', line).group(1)
    if re.search(r'SITE TO SEND MASKS TO : (\w+)', line):
        site_to_send_masks_to = re.search(r'SITE TO SEND MASKS TO : (\w+)', line).group(1)
    if re.search(r'SITE TO SEND INVOICE TO : (\w+ SITE)', line):
        site_to_send_invoice_to = re.search(r'SITE TO SEND INVOICE TO : (\w+ SITE)', line).group(1)
    if re.search(r'TECHNICAL CONTACT : (.+?)\s+', line):
        technical_contact = re.search(r'TECHNICAL CONTACT : (.+?)\s+', line).group(1)
    if re.search(r'SHIPPING METHOD\s*:\s*(\S.*)', line):
        shipping_method = re.search(r'SHIPPING METHOD\s*:\s*(\S.*)', line).group(1).strip()
    if re.search(r'ADDITIONAL INFORMATION\s*:\s*(.+)', line):
        additional_information = re.search(r'ADDITIONAL INFORMATION\s*:\s*(.+)', line).group(1).strip()
    if re.search(r'(\d+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\d+\.\d+)\s*\|\s*(\d+\.\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)', line):
        cd_match = re.search(r'(\d+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\d+\.\d+)\s*\|\s*(\d+\.\d+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)', line)
        cdinfo.append({
            'revision': cd_match.group(2),
            'cd_number': cd_match.group(7),
            'cd_name': cd_match.group(8),
            'feature': cd_match.group(9),
            'tone': cd_match.group(10),
            'polarity': cd_match.group(11),
        })

# Add the parsed data to the XML
order_form.append(create_element("Customer", customer_name))
order_form.append(create_element("Device", device))
order_form.append(create_element("MaskSupplier", mask_supplier))
order_form.append(create_element("Date", date))
order_form.append(create_element("SiteOf", site_of))
order_form.append(create_element("OrderFormNumber", orderform_number))
order_form.append(create_element("Revision", revision))
order_form.append(create_element("Page", page))
order_form.append(create_element("TechnologyName", technology_name))
order_form.append(create_element("Status", status))
order_form.append(create_element("MaskSetName", mask_set_name))
order_form.append(create_element("FabUnit", fab_unit))
order_form.append(create_element("EmailAddress", email_address))

levels_element = etree.Element("Levels")
for level in levels:
    level_element = etree.Element("Level", {"num": level['num']})
    level_element.append(create_element("MaskCodification", level['mask_codification']))
    level_element.append(create_element("Group", level['group']))
    level_element.append(create_element("Cycle", level['cycle']))
    level_element.append(create_element("Quantity", level['quantity']))
    level_element.append(create_element("ShipDate", level['ship_date']))
    levels_element.append(level_element)
order_form.append(levels_element)

cdinfo_element = etree.Element("Cdinformation")
for cd in cdinfo:
    cd_element = etree.Element("Level")
    cd_element.append(create_element("Revision", cd['revision']))
    cd_element.append(create_element("CDNumber", cd['cd_number']))
    cd_element.append(create_element("CDName", cd['cd_name']))
    cd_element.append(create_element("Feature", cd['feature']))
    cd_element.append(create_element("Tone", cd['tone']))
    cd_element.append(create_element("Polarity", cd['polarity']))
    cdinfo_element.append(cd_element)
order_form.append(cdinfo_element)

order_form.append(create_element("PONumbers", po_numbers))
order_form.append(create_element("SiteToSendMasksTo", site_to_send_masks_to))
order_form.append(create_element("SiteToSendInvoiceTo", site_to_send_invoice_to))
order_form.append(create_element("TechnicalContact", technical_contact))
order_form.append(create_element("ShippingMethod", shipping_method))
order_form.append(create_element("AdditionalInformation", additional_information))

# Write the XML to the output file with proper formatting
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(prettify(order_form))

print(f"XML file generated successfully as {output_file}.")