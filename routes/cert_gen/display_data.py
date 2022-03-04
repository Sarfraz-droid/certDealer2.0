import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import base64
from zipfile import ZipFile
class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.fontSize = 0

class CertHandler:
    def __init__(self):
        self.Subject = None
        self.Body = None
        self.fontHead = None
        self.fontPara = None
        self.head_pos = None
        self.para_pos = None
        self.isRightAligned = False
        self.head_arr = []
        self.para_arr = []
        self.email_arr= []
        

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

def download_all(cert: CertHandler, cert_template: any):
    
    n = len(cert.head_arr)
    zipObj = ZipFile("Certificates.zip", "w")
    
    for i in range(n):
        generate(cert.head_pos, cert.para_pos, cert.head_arr[i], cert.para_arr[i], cert_template, cert.fontHead, cert.fontPara, cert.isRightAligned)
        zipObj.write(f'certs/{cert.head_arr[i]}.png')

    zipObj.close()

    with open('Certificates.zip', 'rb') as file:
        btn = st.download_button(label="Download Certificates", file_name="Certificates.zip", data=file)
    
    
    
    
    pass

def generate(head_pos: Position, para_pos: Position,headtext,paratext, cert_template, fontHead, fontBody, isRightAligned):
    certificate = Image.open(cert_template)
    draw = ImageDraw.Draw(certificate)
    imageWidth = certificate.size[0]
    
    st.caption('Image Width: ' + str(imageWidth))
    
    addHeading(headtext,draw,fontHead,head_pos.x,head_pos.y, imageWidth, isRightAligned)
    addPara(paratext,draw,fontBody,para_pos.x,para_pos.y, imageWidth, isRightAligned)
    st.image(certificate, caption="Certificate")
    
    certificate.save(f'certs/{headtext}.png')

def generate_cert(head_pos: Position, para_pos: Position,headtext,paratext, cert_template, fontHead, fontBody, isRightAligned):
    certificate = Image.open(cert_template)
    draw = ImageDraw.Draw(certificate)
    imageWidth = certificate.size[0]
    
    st.caption('Image Width: ' + str(imageWidth))
    
    addHeading(headtext,draw,fontHead,head_pos.x,head_pos.y, imageWidth, isRightAligned)
    addPara(paratext,draw,fontBody,para_pos.x,para_pos.y, imageWidth, isRightAligned)
    st.image(certificate, caption="Certificate")
    
    certificate.save('certificate.png')    

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


def display_data(df,heading,para, cert_template, email):
    st.subheader("Certificate Generator")
    
    font_head = st.file_uploader("Choose Head Font", accept_multiple_files=False)
    font_para = st.file_uploader("Choose Para Font", accept_multiple_files=False)
    
    cert = CertHandler()
    
    if font_head != None and font_para != None:
        st.caption("Font uploaded successfully")
        st.caption("Head Info")
        cert.head_pos = Position()
        
        cert.head_pos.x = st.number_input("Head X",min_value=0,max_value=8000,value=3140)
        cert.head_pos.y = st.number_input("Head Y",min_value=0,max_value=8000,value=1130)
        cert.head_pos.fontSize = st.number_input("Head Font Size",min_value=0,max_value=3152,value=100)
        
        cert.para_pos = Position()
        
        st.caption("Para X/Y Pos")
        cert.para_pos.x = st.number_input("Para X",min_value=0,max_value=3152,value=3140)
        cert.para_pos.y = st.number_input("Para Y",min_value=0,max_value=3152,value=1359)
        cert.para_pos.fontSize = st.number_input("Para Font Size",min_value=0,max_value=3152,value=50)
        
        cert.isRightAligned = st.checkbox("Right Aligned",value=True)
        
        cert.head_arr = np.array(df[heading])
        cert.para_arr = np.array(df[para])
        cert.email_arr = np.array(df[email])
        
        pos = st.slider('Select Index',0,len(cert.head_arr)-1,0)
        
        cert.fontHead = ImageFont.truetype(font_head, cert.head_pos.fontSize)
        cert.fontPara = ImageFont.truetype(font_para, cert.para_pos.fontSize)

        if st.button('Generate Demo'):
            generate_cert(cert.head_pos, cert.para_pos, cert.head_arr[pos],cert.para_arr[pos], cert_template, cert.fontHead, cert.fontPara, cert.isRightAligned)
            # st.write("No data uploaded")
        
        if st.button('Download All'):
            download_all(cert, cert_template)
            pass
            
        
        return cert
    else:
        return None