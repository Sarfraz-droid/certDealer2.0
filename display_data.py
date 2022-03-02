import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import base64

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.fontSize = 0

def addHeading(heading,draw,fontHead,x,y, imageWidth, isRightAligned):
  w,h = draw.textsize(heading,font=fontHead);
  if isRightAligned :
      x -= w;
  draw.text((x,y),heading,(0,0,0),font=fontHead)

def addPara(designation,draw,fontPara,x,y, imageWidth, isRightAligned):
  w,h = draw.textsize(designation,font=fontPara);
  if isRightAligned :
      x -= w;
  draw.text((x,y),designation,(0,0,0),font=fontPara)



def generate_cert_image(df, head_pos, para_pos,headtext,paratext, cert_template, fontHead, fontBody, isRightAligned):
    certificate = Image.open(cert_template)
    draw = ImageDraw.Draw(certificate)
    imageWidth = certificate.size[0]
    
    st.caption('Image Width: ' + str(imageWidth))
    
    addHeading(headtext,draw,fontHead,head_pos.x,head_pos.y, imageWidth, isRightAligned)
    addPara(paratext,draw,fontBody,para_pos.x,para_pos.y, imageWidth, isRightAligned)
    st.image(certificate, caption="Certificate")
    
    certificate.save('certificate.png')
    
    with open('certificate.png', 'rb') as file:
        st.download_button(label="Download Certificate", file_name="certificate.png", data=file)

    return


def display_data(df,heading,para, cert_template):
    st.subheader("Certificate Generator")
    
    font_head = st.file_uploader("Choose Head Font", accept_multiple_files=False)
    font_para = st.file_uploader("Choose Para Font", accept_multiple_files=False)
    if font_head != None and font_para != None:
        st.caption("Font uploaded successfully")
        
        st.caption("Head Info")
        head_pos = Position()
        
        head_pos.x = st.number_input("Head X",min_value=0,max_value=8000,value=3140)
        head_pos.y = st.number_input("Head Y",min_value=0,max_value=8000,value=1130)
        head_pos.fontSize = st.number_input("Head Font Size",min_value=0,max_value=3152,value=100)
        
        para_pos = Position()
        
        st.caption("Para X/Y Pos")
        para_pos.x = st.number_input("Para X",min_value=0,max_value=3152,value=3140)
        para_pos.y = st.number_input("Para Y",min_value=0,max_value=3152,value=1359)
        para_pos.fontSize = st.number_input("Para Font Size",min_value=0,max_value=3152,value=50)
        
        isRightAligned = st.checkbox("Right Aligned",value=True)
        
        head_arr = np.array(df[heading])
        para_arr = np.array(df[para])
        
        pos = st.slider('Select Index',0,len(head_arr)-1,0)
        
        
        if st.button('Generate Demo'):
            fontHead = ImageFont.truetype(font_head, head_pos.fontSize)
            fontPara = ImageFont.truetype(font_para, para_pos.fontSize)
            generate_cert_image(df, head_pos, para_pos,head_arr[pos],para_arr[pos], cert_template, fontHead, fontPara, isRightAligned)
        else:
            st.write("No data uploaded")