from dotenv import load_dotenv

load_dotenv()

from nemoguardrails import LLMRails, RailsConfig

config = RailsConfig.from_path("./guardrails")
print("CONFIG LOADED:")
print(config)

rails = LLMRails(config)

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def business_chat(message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are BizAssist, an enterprise business assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content




async def security_check(message: str):
    response = await rails.generate_async(
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    print("SECURITY RESPONSE:", response)

    return response["content"]

