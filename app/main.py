from fastapi import FastAPI

app = FastAPI()

# Static Files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
# templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root():
    return {"Hello": "World"}
