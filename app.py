from flask import Flask, render_template_string
import jwt
import time

app = Flask(__name__)

# CONFIGURAÇÕES DO METABASE
METABASE_SITE_URL = "http://localhost:3000"
METABASE_SECRET_KEY = "2ced173cb455b161b5b38cd5b5fa45b912e353e316dbb8d4c753fa75d5764553"

@app.route('/')
def dashboard():
    payload = {
        "resource": {"dashboard": 33},
        "params": {},
        "exp": round(time.time()) + (60 * 10)  # expira em 10 min
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    # compatibilidade com versões mais recentes do PyJWT
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    iframeUrl = f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"

    # Renderiza diretamente o HTML com iframe
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Embutido</title>
        <style>
            iframe {{
                width: 100%;
                height: 90vh;
                border: 0;
            }}
        </style>
    </head>
    <body>
        <h1>Case Técnico</h1>
        <iframe src="{iframeUrl}" allowfullscreen></iframe>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
