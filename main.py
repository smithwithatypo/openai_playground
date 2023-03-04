import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

openai.Image.create(
    prompt="A cute baby sea otter",
    n=1,
    size="256x256"
)
