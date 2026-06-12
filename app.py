from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from security.auth import verify_api_key

from dotenv import load_dotenv

load_dotenv()

from guardrails_service import security_check, business_chat

app=FastAPI(
    title="BizAssist AI Security chatbot",
    version="1.0"
)

class ChatRequest(BaseModel):
    message:str

@app.get("/")
def health_check():
    return{
        "status":"running",
        "message":"BizAssist API is alive"

    }


@app.post("/chat")
async def chat(request:ChatRequest, _: bool =Depends(verify_api_key)):
    result = await security_check(request.message)

    if result == "SECURITY_BLOCKED":
        return {
            "assistant": "Request blocked due to security policy."
        }


    answer = await business_chat(request.message)


    return{
        "assistant":answer
    }

