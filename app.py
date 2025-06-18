import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional

article_id = st.text_input('Enter Article ID')

if st.button('Fetch and Process'):
    with st.spinner('Processing article …'):

        exporter_api_url = f"{st.secrets['api_tokens']['exporter_api_base_url']}{article_id}/"
        
        exporter_auth_token = st.secrets["api_tokens"]["exporter_auth_token"]
        headers_exporter = {
            "Authorization": f"Basic {exporter_auth_token}",
            "Content-Type": "application/json"
        }

        exporter_response = requests.get(exporter_api_url, headers=headers_exporter)

        if exporter_response.status_code != 200:
            st.error("Error retrieving article from Exporter API.")
        else:
            exporter_json = exporter_response.json()
            try:
                title = exporter_json.get('title', '')
                text = exporter_json.get('text', '')
            except json.JSONDecodeError:
                st.error("Failed to decode JSON from Exporter API.")
                st.stop()
            
            if not title or not text:
                st.warning("Exporter API returned empty title or text.")
                st.stop()
            
            # Display full JSON from Exporter API
            st.json(exporter_json)