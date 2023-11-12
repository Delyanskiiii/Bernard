from openai import OpenAI
from tokens import API_KEY

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=API_KEY,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)