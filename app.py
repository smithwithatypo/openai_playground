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
            max_tokens=1500
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
                    "content": "You are a professional tutor for a college student who prefers visual analogies. Summarize the following text with bullet points of only the most important points. Use analogies when possible."},
                {"role": "user", "content": f"{flashcard_prompt}"}
            ],
            temperature=.1,
            n=1,
            max_tokens=(1500)
        )
        flashcard_list = response.choices[0].message.content.lstrip().split(
            '\n')

    return render_template("flashcards.html", flashcards=flashcard_list)


@app.route("/resume", methods=("GET", "POST"))
def resume():
    result_list = ""

    if request.method == "POST":
        temperature = float(request.form["temperature"])
        role = request.form["role"]
        duties = request.form["duties"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "You are a professional resume writer for an early career software engineer."},
                {"role": "user",
                    "content": f"Write bullet points for a resume using buzzwords that recruiters look for with the job title {role}, and the duties: {duties}:"},
            ],
            temperature=temperature,
            n=1,
            max_tokens=1000
        )
        result_list = response.choices[0].message.content.lstrip().split(
            '\n')

    return render_template("resume.html", result=result_list)


if __name__ == "__main__":
    app.run(debug=True)
