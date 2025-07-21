# app.py
import requests
from bs4 import BeautifulSoup
import openai
from flask import Flask, request, render_template

openai.api_key = "Your API Key"

app = Flask(__name__)

def extract_text(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)[:4000]
    except Exception as e:
        return str(e)

def summarize(text):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4
        messages=[
            {"role": "system", "content": "Summarize the following web content:"},
            {"role": "user", "content": text}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        url = request.form["url"]
        text = extract_text(url)
        summary = summarize(text)
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
