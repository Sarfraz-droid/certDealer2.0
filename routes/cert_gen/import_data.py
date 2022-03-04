import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw

def import_data():
    st.caption("Setup Certificate data")
    dataset = st.file_uploader("Upload CSV", accept_multiple_files=False)
    
    df = None
    heading = None
    para = None
    
    if dataset != None:
        df = pd.read_csv(dataset)

        st.dataframe(df)
        arr = np.array(df.keys())
        heading = st.selectbox("Select Heading", arr)
        para= st.selectbox("Enter Paragraph", arr)
        email= st.selectbox("Enter Email", arr)
        
        return True ,df, heading, para, email
    
    else: 
        st.write("No data uploaded")
        
    return False ,df, heading, para
        
    