from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

try:
	from openai import OpenAI
except Exception:
	OpenAI = None

client = None
if OpenAI:
	api_key = os.getenv("OPENAI_API_KEY")
	if api_key:
		client = OpenAI(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_bot_reply(message: str) -> str:
	if client:
		response = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": message},
			],
		)
		return response.choices[0].message.content

	return f"You said: {message}. I'm running locally without AI API."


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_class=HTMLResponse)
def chat(request: Request, message: str = Form(...)):
	reply = get_bot_reply(message)
	return templates.TemplateResponse(
		"index.html", {"request": request, "user": message, "bot": reply}
	)


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="127.0.0.1", port=8000)
