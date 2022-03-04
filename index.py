import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import routes.GetAccessToken.getaccesstoken as getaccesstoken
import routes.cert_gen.certificate_gen as certificate_gen

param = st.experimental_get_query_params()



def main():
    add_selectbox = st.sidebar.selectbox(
        "Select Choice",
        ("Send Certificate","Get Access Token"),
    )

    if add_selectbox == "Get Access Token":
        getaccesstoken.main()
        pass    
    else:
        certificate_gen.main()
    
    
if param == {}:
    main()
else:
    st.subheader('Authorization Code')
    st.write(param['code'][0])