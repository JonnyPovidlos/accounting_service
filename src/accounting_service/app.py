from fastapi import FastAPI

from . import shop, category, operation, account


app = FastAPI()
shop.initialize_app(app)
category.initialize_app(app)
operation.initialize_app(app)
account.initialize_app(app)

