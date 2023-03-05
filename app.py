import os

import openai
from flask import Flask, redirect, render_template, request, url_for


# from jinja2 import Environment, PackageLoader, BaseLoader
# env = Environment(
#     loader=PackageLoader(BaseLoader()),
#     keep_trailing_newline=True
# )
# template = env.get_template("flashcards.html")

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    result = ""

    if request.method == "POST":
        form_prompt = request.form["prompt"]
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=form_prompt,
            temperature=0,
            max_tokens=100,
        )
        result = response.choices[0].text.replace('\n', '\n \n \n')
        # return redirect(url_for("index", result=response.choices[0].text))

    # result = request.args.get(f"{result}")
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
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=generate_flashcards(flashcard_prompt),
            temperature=0,
            max_tokens=400
        )
        flashcard_list = response.choices[0].text.lstrip().split('\n')
        # print(flashcard_list)

    return render_template("flashcards.html", flashcards=flashcard_list)
    # return template.render(flashcards=flashcards)


def generate_flashcards(flashcard_prompt):
    return """Pretend to be a professional tutor.
            Summarize the following text in as few words as possible and make a list of [Topic: Summary] flashcards:
            {}:""".format(flashcard_prompt)


if __name__ == "__main__":
    app.run(debug=True)


# Archive / Trash

# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         animal = request.form["animal"]
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=generate_prompt(animal),
#             temperature=0.6,
#         )
#         return redirect(url_for("index", result=response.choices[0].text))

#     result = request.args.get("result")
#     return render_template("index.html", result=result)


# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.
# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(animal.capitalize())
