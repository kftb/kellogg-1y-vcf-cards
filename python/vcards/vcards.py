import vobject
import base64
import os
import pandas as pd
from datetime import datetime

img_url = "../image_scraper/images/"

print(os.getcwd())

# Read data from survey data
df = pd.read_table("../../r/output/1y_dir_output.csv",sep=",", dtype={'phone_final': str, 'wa_final': str, 'employer_clean': str,})


# Get system time
now = datetime.now()
timestamp = now.strftime("%y%m%d_%H%M%S")

# define the name of the directory to be created
wd = os.getcwd()
print(wd)

path = wd + "/output_"+timestamp
print(path)

access_rights = 0o755

try:
    os.mkdir(path, access_rights)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

path = wd + "/output_"+timestamp + "/single"
try:
    os.mkdir(path, access_rights)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)




# Iterate over each row
for index, row in df.iterrows():

    if (pd.notna(row["netID"])):
       netID = row["netID"]
    else:
        netID = row["first_name"]+ row["last_name"]
    print(netID)


    # Try to find picture from downloaded pictures
    try:
        with open(img_url + netID + ".jpg", "rb") as image_file:
            
                img = base64.b64encode(image_file.read())
                img = img.decode("utf-8")
    except: 
        img = ""
   
   # Start vcard object
    vCard = vobject.vCard()
    
    # Add Name
    vCard.add('N').value = vobject.vcard.Name(family=row['last_name'], given=row['first_name'])
    vCard.add('FN').value = row['first_name'] + " " + row['last_name']

    # Email address
    o = vCard.add('email')
    o.type_param = "INTERNET"
    o.value = row['perm_email_corr']
    o.pref_param = "PREF"

    # Check if kellogg email exists
    if (pd.notna(row["kellogg_email"])):
        k = vCard.add('email')
        k.type_param = "INTERNET"
        k.value = str(row['kellogg_email'])
        kellogg = str(row['kellogg_email'])
    else:
        kellogg = ""

    # Checks if different entries exist or not
    if (row["geo_country"] == "USA"):
        city = row["geo_city_primary"]
    else:
        city = row["geo_city_primary"] + ", " + row["geo_country"]
    
    if (pd.notna(row["geo_city_secondary"])) :
        city = city + "\n" + "Secondary: " + row["geo_city_secondary"]

    if (pd.notna(row["wa_final"])):
        wa = "WhatsApp: " + str(row["wa_final"])
    else:
        wa = ""

    if (pd.notna(row["phone_final"])):
        phone = "Mobile: " + str(row["phone_final"])
    else:
        phone = ""

    if (row["employer_clean"] == "TBD"): 
        employer = ""
    elif (pd.notna(row["employer_clean"])):
       employer = row["employer_clean"]
    else:
        employer = ""
   
    # Composing the notes section
    vCard.add("NOTE")
    note = row['first_name'] + " " + row['last_name'] + \
    "\n" + "\n" + \
    employer + "\n" + \
    "Function: " + str(row['function']) + "\n" + \
    "Industry: " + str(row['industry']) + "\n" + "\n" + \
    city + "\n" + \
    row['perm_email_corr'] + "\n" + \
    kellogg + "\n" + "\n" + \
    str(phone) + "\n" + \
    str(wa) + "\n" + "\n" \
    "Kellogg 1Ys 2021"

    # Add JV marker
    if (row["student_jv"] == "JV"):
        note = note + " (JV)"
 
    # Putting the note in
    vCard.note.value = note

    # Add IMG Only when img exists
    if (img != ""):
        m = vCard.add('PHOTO;ENCODING=b;TYPE=image/jpeg')
        m.value = img

    # Address
    vCard.add('ADR')
    vCard.adr.value = vobject.vcard.Address(city = row['geo_city_primary'], country= row['geo_country'])
    vCard.adr.type_param = 'HOME'

    # Employer (has to be in brackets if string with spaces)
    o = vCard.add('ORG')
    o.value = [employer]

    # Add phone numbers
    if (pd.notna(row["phone_final"])):
        o = vCard.add('tel')
        o.type_param = "cell"
        o.value = str(row['phone_final'])

    if (pd.notna(row["wa_final"])):
        o = vCard.add('tel')
        o.type_param = "whatsapp"
        o.value = str(row['wa_final'])

    vCard.add('CATEGORIES')
    vCard.categories.value = ["Kellogg 1Y 2021"]

    # Write output
    filename = path + "/" + netID + ".vcf"
    with open(filename, 'w') as writer:
            writer.write(vCard.serialize())

# Write into single VCF file
path = wd + "/output_"+timestamp
print(path)

single_path = wd + "/output_"+timestamp + "/single"
file_list = os.listdir(single_path)
file_list = sorted(file_list, key=str.lower)
print(file_list)


with open(path+"/1y.vcf", 'w') as outfile:
    for fname in file_list:
        with open(single_path +"/"+ fname) as infile:
            outfile.write(infile.read())