from fastapi import FastAPI

from . import shop


app = FastAPI()
shop.initialize_app(app)


@app.get('/')
def root():
    return {"Hello": "World!"}
