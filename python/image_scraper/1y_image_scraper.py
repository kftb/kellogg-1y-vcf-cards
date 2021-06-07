import pandas as pd
import requests
import urllib.request
import PIL

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

mytable = pd.read_table("input/netids.csv",sep=",")
mytable = mytable

for index, row in mytable.iterrows():

    # Define base URL format   
    url = "https://www.kellogg.northwestern.edu/images/students/all/"+row['netID']+".jpg"
    try:
        # Construct relative filename
        filename = "images/"+row['netID'].lower()+".jpg"

        # Download file from Kellogg servers
        urllib.request.urlretrieve(url, filename)
        
        # Reformat picture to smaller size
        img = Image.open(filename)
        basewidth = 400
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        width, height = img.size

        # Write image back out
        img.save(filename)

    except Exception as e: # work on python 3.x
        print(str(e))
        
       


