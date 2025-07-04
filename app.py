import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional
import streamlit.components.v1 as components

article_id = st.text_input('Enter Article ID')

if st.button('Fetch'):
    with st.spinner('Fetching article …'):

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
            
            json_str = json.dumps(exporter_json, indent=2)
            st.text_area("JSON Output", json_str, height=300)

            components.html(f"""
                <script>
                  function copyJSON() {{
                    navigator.clipboard.writeText(`{json_str}`);
                    alert("JSON copied to clipboard!");
                  }}
                </script>
            """, height=0)

            if st.button("JSON kopieren"):
                components.html("<script>copyJSON()</script>", height=0)