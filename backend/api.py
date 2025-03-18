from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import ALLOWED_ORIGINS

class API:

    _instance = None

    def __init__(self):

        self._app = FastAPI()

        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def app(self):   
        return self._app