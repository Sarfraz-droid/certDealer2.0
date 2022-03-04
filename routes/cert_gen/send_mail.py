import json
import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from routes.cert_gen.display_data import generate_cert, CertHandler


def mailer(fromaddr,frompass,toaddr,subject,msgbody,file_name,filepath):
  msg = MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = toaddr
  msg['Subject'] = subject
  body = msgbody
  msg.attach(MIMEText(body, 'plain'))
  filename = file_name
  attachment = open(filepath, "rb")
  p = MIMEBase('application', 'octet-stream')
  p.set_payload((attachment).read())
  encoders.encode_base64(p) 
  p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  msg.attach(p)
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login(fromaddr, frompass)
  text = msg.as_string()
  s.sendmail(fromaddr, toaddr, text)
  st.write("Mail sent successfully")
  s.quit()

def send_mail(df,result: CertHandler, cert_template: any):
    st.subheader("Send Mail")
    
    st.write("TroubleShooting Tips")
    st.write("1. Make sure you have the correct email address and Password")
    st.markdown("2. On Error, [Enable Less Secure Apps](https://myaccount.google.com/lesssecureapps)")
    st.markdown("3. If the error still exists, [Display Unlock Captcha](https://accounts.google.com/b/0/DisplayUnlockCaptcha)")
    
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    subject = st.text_input("Enter Subject")
    body = st.text_area("Enter Body")
    mail_button = st.button("Send Mail")
    
    if mail_button:
        head_arr = result.head_arr
        para_arr = result.para_arr

        n = len(head_arr)

        for i in range(n):
            # pass
            generate_cert(result.head_pos, result.para_pos, head_arr[i], para_arr[i], cert_template, result.fontHead, result.fontPara, result.isRightAligned)
            mailer(email,password,result.email_arr[i],subject,body, f'{i}.png','./certificate.png')
