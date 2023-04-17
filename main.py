from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nmap_api.routers import router as nmap_router

app = FastAPI(
    title="Scanner as a Service",
    version="1.0.0"
)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(nmap_router)
