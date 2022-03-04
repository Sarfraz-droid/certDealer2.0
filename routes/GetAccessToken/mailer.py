import asyncio
from copyreg import constructor


import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
import os

params = st.experimental_get_query_params()
if params:
    print(params['code'][0])

"## Configuration"
client= None
client_id= None
client_secret= None
redirect_uri= None

def main ():
    st.title("Google OAuth2 flow")
    client_id = st.text_input("Client ID")
    client_secret = st.text_input("Client secret")
    redirect_uri = st.text_input("Redirect URI", "http://localhost:8501/")

    if client_id and client_secret and redirect_uri:
        client = GoogleOAuth2(client_id, client_secret)
    else:
        client = None
        
    async def write_authorization_url():
        authorization_url = await client.get_authorization_url(
            redirect_uri,
            scope=["profile", "email"],
            extras_params={"access_type": "offline"},
        )
        st.write(authorization_url)

    if client:
        asyncio.run(write_authorization_url())
    else:
        "Waiting client configuration..."

    "## Callback"

    if client:
        code = st.text_input("Authorization code")
    else:
        code = None
    "Waiting client configuration..."

    "## Access token"

    async def write_access_token(code):
        token = await client.get_access_token(code, redirect_uri)
        file = open("token.json", "w")
        file.write(str(token))
        file.close()
        st.write(token)        
        with open("token.json", "rb") as file:
            btn = st.download_button(
                label="Download token.json",
                data=file,
                file_name="token.json",
                mime="application/json",
            )
            pass
        

        
        

    if code:
        asyncio.run(write_access_token(code))
    else:
        "Waiting authorization code..."

    
"## Authorization URL"
