from fastapi import FastAPI

from . import shop, category, operation


app = FastAPI()
shop.initialize_app(app)
category.initialize_app(app)
operation.initialize_app(app)


@app.get('/')
def root():
    return {"Hello": "World!"}
