from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root():
	return {"message": "Hello, this is the test webhook endpoint!"}


@app.post("/webhook")
async def webhook(request: Request):
	data = await request.json()
	
	return JSONResponse(content = {"status": "ok", "data": data})
