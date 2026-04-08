from fastapi import FastAPI
from app.interfaces.api.vision_api import router as vision_router

app = FastAPI(
    title="Sistema IA de Residuos - Riobamba",
    version="1.0.0"
)

app.include_router(vision_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Sistema IA de residuos funcionando"}