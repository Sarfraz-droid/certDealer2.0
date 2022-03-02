import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from import_data import import_data
from display_data import display_data

st.title('Certificate Dealer and Generator')



cert_template = st.file_uploader("Choose Template", accept_multiple_files=False)

if cert_template != None :
    image = Image.open(cert_template)
    st.image(image, caption='Template', use_column_width=True)
    state,df,heading,para = import_data()
    
    if state != False:
        st.caption("Data imported successfully")
        display_data(df,heading,para, cert_template)
    else: 
        st.caption("No data uploaded")

    
    
    
    
