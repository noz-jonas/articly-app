# 🗣️ Article Hörbar Synthesis App

This is a Streamlit-based web application that transforms news articles into audio-friendly summaries using OpenAI's language models — with built-in support for real-time evaluation and feedback collection through the OpenAI Evals API.

---

## ✨ Features

- 🔐 Secure integration with an internal Exporter API (Basic Auth)
- 📄 Automatic parsing of article `title` and `text`
- 🤖 Summarization and optimization using OpenAI models
- 🧪 User-correctable output with automatic feedback submission to OpenAI Evals
- 🔁 Editable result fields and live updates
- 📤 Optional local JSONL logging
- 📢 Optimized for text-to-speech playback
- 🛠️ Error handling, loading animations, and evaluation toggles

---

## 🚀 Usage

1. **Clone the repository**

```bash
git clone https://github.com/your-username/article-hoerbar-synthesis.git
cd article-hoerbar-synthesis
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Add secrets to `.streamlit/secrets.toml`**

```toml
[api_tokens]
exporter_auth_token = "your_exporter_token"
openai_token = "your_openai_api_key"
openai_organization_id = "org-..."  # Optional, for Evals API
exporter_api_base_url = "https://your-exporter-api-url/"
evals_enabled = true
```

4. **Run the app locally**

```bash
streamlit run app.py
```

---

## 🧠 How it works

- User enters an `articleId` from the internal CMS.
- The app fetches the article via the Exporter API.
- It extracts `title` and `text`, and sends them to OpenAI for summarization.
- The summarized result is shown in a text area.
- If Evals mode is enabled (via checkbox or `secrets.toml`), users can:
  - Edit the AI-generated text
  - Submit corrections directly to OpenAI's Evals API
  - View confirmation of Eval + Run IDs

---

## 🔁 Feedback Collection and Evals

- User edits are submitted as `ideal_response` evaluations
- Evals are automatically created and run using OpenAI’s `/evals` endpoint
- App displays success or error messages per submission
- Local backup in `evals_log.jsonl` is optional and used for redundancy

---

## 🛡 Security

- Secrets like tokens and URLs are stored securely in `.streamlit/secrets.toml`
- This file is excluded from version control via `.gitignore`
- No user-submitted data is shared unless Evals is explicitly enabled

---

## 🖥 Deployment

To deploy on [Streamlit Cloud](https://streamlit.io/cloud):

1. Push this repo to GitHub
2. Create a new Streamlit app
3. Paste your secrets into the *App Settings → Secrets* section of the Cloud UI