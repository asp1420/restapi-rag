from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import rag
from .utils.customapischema import CustomizerOpenAPI

app = FastAPI()

origins = ['*']

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=rag.router)
app.openapi = CustomizerOpenAPI(app=app).custom_openapi