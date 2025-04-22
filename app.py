import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json
import re

# Title of the app
st.title('Hörbar Articly Synthesis')

# Input field for articleId
article_id = st.text_input('Enter Article ID')

# Button to trigger the API calls
if st.button('Fetch and Process'):
    with st.spinner('Processing article …'):

        # First API call (Exporter API)
        exporter_api_url = f"{st.secrets['api_tokens']['exporter_api_base_url']}{article_id}/"
        
        exporter_auth_token = st.secrets["api_tokens"]["exporter_auth_token"]
        headers_exporter = {
            "Authorization": f"Basic {exporter_auth_token}",
            "Content-Type": "application/json"
        }

        exporter_response = requests.get(exporter_api_url, headers=headers_exporter)

        if exporter_response.status_code != 200:
            # Error handling for exporter API
            st.error("Error retrieving article from Exporter API.")
        else:
            # Parse response from exporter API
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
            
            # Prepare payload for OpenAI API
            openai_api_url = "https://api.openai.com/v1/chat/completions"
            openai_model = "ft:gpt-4o-2024-08-06:noz-digital-audio:dpo:BAykzAcO"  # replace with your specific model
            openai_token = st.secrets["api_tokens"]["openai_token"]
            headers_openai = {
                "Authorization": f"Bearer {openai_token}",
                "Content-Type": "application/json"
            }

            payload_openai = {
                "model": openai_model,
                "temperature": 0.3,
                "top_p": 0.50,
                "metadata": {
                    "manual-testing": "false",
                    "streamlit-app": "active"
                },
                "store": True,
                "response_format": {
                    "type": "text"
                },
                "messages": [
                    {
                        "role": "developer",
                        "content": "ROLLE: Du optimierst geschriebene Artikel zum Hören. KONTEXT: Die Artikel wurden von Redakteurinnen verfasst und sind primär fürs Lesen konzipiert. Deine optimierten Texte sollen anschließend von Text-To-Speech vertont werden und somit Menschen für mehr Convenience dienen und Menschen mit Sehbehinderungen. AUFGABE: 1. Überschrift/Hook - Beginne mit einer prägnanten Überschrift (Frage oder kurze Aussage), die den Kern des Artikels widerspiegelt und in den ersten zehn Sekunden direkt Aufmerksamkeit erzeugt. 2. Struktur & Format - Verfasse einen Fließtext ohne Absätze, der so klingt, wie man spricht. - Halte den Text auf maximal zweihundert Wörter begrenzt. 3. Sprachstil & Verständlichkeit - Nutze kurze, aktive Sätze, alltagssprachliche Formulierungen und gegebenenfalls emotionale Sprache. - Formuliere inklusive, leicht verständliche Texte. Verzichte auf überflüssige Fachbegriffe oder erkläre diese, falls unvermeidbar. - Halte dich an das Originaltempus des Artikels. 4. Kerninformationen nach W-Fragen - Beantworte klar die Fragen WER, WAS, WO, WANN, WARUM und ggf. WIE. - Streiche Unwichtiges und reduziere die Inhalte auf rund ein Viertel des Originaltextes (maximal aber zweihundert Wörter), um die Hörversion kompakt zu halten. 5. Zahlen & Daten - Schreibe Zahlen, Daten und Maßeinheiten aus und setze sie ggf. in Relation (z.B. 'fast jede zweite Person' statt 'siebenundvierzig Komma drei Prozent'). - Nutze Wiederholungen anstelle von Synonymen, wenn ein Begriff besonders wichtig ist. - Erwähne keine Kontaktdaten, wie z.B. E-Mail Adressen, Postadressen, Telefonnummern. 6. Zitate & Quellen - Nur wenn es unbedingt nötig ist, verwende kurze Zitate – mit klarem Sprecherhinweis (z. B. „laut Trainer:“). 7. Audiotauglichkeit & Hörfluss - Gestalte die Interpunktion so, dass natürliche Pausen deutlich werden (Kommas für kurze Atempausen, Punkte für Stopps). - Achte darauf, dass beim Hören keine inhaltlichen Brüche entstehen. 8. Lokale Relevanz & Monetarisierung - Falls relevant, betone den lokalen Bezug (z. B. regionale Ereignisse oder Besonderheiten), um die Nähe zum Publikum zu stärken. 9. Best Practices - Kürze Inhalte für die auditive Nutzung, statt sie nur vorzulesen. Reduziere den Inhalt auf ca. ein Viertel des Originaltextes – maximal aber auf zweihundert Wörter – und streiche überflüssige Details, damit das Ganze auditiv kompakt bleibt. - Achte auf konsistente Wiederholung wichtiger Begriffe und einprägsame Formulierungen für ein besseres Hörerlebnis. Erstelle schließlich genau ein optimiertes Audioskript mit exakt einer Überschrift und darunter einem zusammenhängenden Text (ohne Absätze) von maximal zweihundert Wörtern, in dem du alle oben genannten Punkte berücksichtigst. Stelle sicher, dass das Zuhören Spaß macht und den Kern des Artikels transportiert."  # Replace with your actual prompt if needed
                    },
                    {
                        "role": "user",
                        "content": f"'title': '{title}', 'text': '{text}'"
                    }
                ]
            }

            # Send request to OpenAI API
            openai_response = requests.post(openai_api_url, headers=headers_openai, json=payload_openai)

            if openai_response.status_code != 200:
                # Error handling for OpenAI API
                st.error("Error retrieving response from OpenAI API.")
            else:
                # Successful OpenAI response
                openai_json = openai_response.json()
                result_content = openai_json['choices'][0]['message']['content']

                # Remove HTML tags from the result (simple approach)
                result_text_clean = re.sub('<[^<]+?>', '', result_content)

                # Display the result
                st.success("Hörbar Article Version:")
                st.text_area("Response:", value=result_text_clean, height=400)
