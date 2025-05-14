# Article Hörbar Synthesis App

This is a Streamlit-based web application that allows users to convert news articles into audio-friendly summaries using OpenAI's language models. The app is designed to support auditory accessibility and convenience by transforming long-form text into concise, spoken-word-friendly formats.

## ✨ Features

- 🔐 Secure integration with the Exporter API via Basic Auth
- 📄 Automatic parsing of article `title` and `text`
- 🤖 Summarization and adaptation using OpenAI API
- 📢 Optimized output for text-to-speech applications
- 🛠 Error handling and loading animations for better UX

## 🚀 Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/article-hoerbar-synthesis.git
cd article-hoerbar-synthesis
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your secrets to `.streamlit/secrets.toml` (do not commit this file):

```toml
[api_tokens]
exporter_auth_token = "your_exporter_token"
openai_token = "your_openai_token"
exporter_api_base_url = "https://your-exporter-api-url/"
```

4. Run the app:

```bash
streamlit run app.py
```

## 🧠 How it works

- Users input an `articleId`.
- The app calls the Exporter API to fetch the article.
- If successful, the app sends the `title` and `text` to the OpenAI API with a specific summarization prompt.
- The response is cleaned of HTML and presented in a text area.

## 🛡 Security

- All API keys are managed using Streamlit's secrets system and excluded via `.gitignore`.

## 🖥 Deployment

To deploy on [Streamlit Cloud](https://streamlit.io/cloud), set the same secrets in the Cloud UI under *App Settings → Secrets*.