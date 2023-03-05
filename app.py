import os

import openai
from flask import Flask, render_template, request, url_for


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    result = ""

    if request.method == "POST":
        form_prompt = request.form["prompt"]
        temperature = float(request.form["temperature"])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{form_prompt}"}
            ],
            temperature=temperature,
            n=1,
            max_tokens=1000
        )
        result = response.choices[0].message.content

    return render_template("index.html", result=result)


@app.route("/images", methods=("GET", "POST"))
def images():
    image_url = ""

    if request.method == "POST":
        image_prompt = request.form.get("image_prompt", "error image")

        response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']

    return render_template("images.html", image_url=image_url)


@app.route("/flashcards", methods=("GET", "POST"))
def flashcards():
    flashcard_list = ""

    if request.method == "POST":
        flashcard_prompt = request.form["flashcard_prompt"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "You are a tutor for busy college students. Summarize the following text as flashcards [front : back]."},
                {"role": "user", "content": f"{flashcard_prompt}"}
            ],
            temperature=0,
            n=1,
            max_tokens=1500
        )
        flashcard_list = response.choices[0].message.content.lstrip().split(
            '\n')
        print(flashcard_list)

    return render_template("flashcards.html", flashcards=flashcard_list)


if __name__ == "__main__":
    app.run(debug=True)
