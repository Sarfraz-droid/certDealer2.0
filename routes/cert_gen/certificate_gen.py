import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from routes.cert_gen.import_data import import_data
from routes.cert_gen.display_data import display_data, Position, CertHandler
from routes.cert_gen.send_mail import send_mail

def main():
    st.title('Certificate Dealer and Generator')
    cert_template = st.file_uploader("Choose Template", accept_multiple_files=False)

    if cert_template != None :
        image = Image.open(cert_template)
        st.image(image, caption='Template', use_column_width=True)
        state,df,heading,para,email = import_data()
    
        if state != False:
            st.caption("Data imported successfully")
            result = display_data(df,heading,para, cert_template,email)
            print(result)

            if result != None:
                send_mail(df,result,cert_template)
        
        else: 
            st.caption("No data uploaded")

    
    
    
    
