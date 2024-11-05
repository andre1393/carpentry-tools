import os
from mangum import Mangum
from fastapi import FastAPI, HTTPException
import traceback

from tools.quote_generator import generate_quote
from tools.logger_config import logger
from tools.api.models import RequestParams


app = FastAPI(
    title="Document processing API",
    description="API to generate quote and contracts"
)


@app.post("/generate-quote/")
async def generate_quote_endpoint(params: RequestParams):
    try:
        result = await generate_quote(params)
        return {"message": "Orçamento gerado com sucesso", "result": result}
    except Exception as e:
        logger.error(f"Error generating quote: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Ocorreu um erro gerando o orçamento")


@app.get("/health")
def health():
    return {"message": "Welcome to the Document Processing API!"}


@app.get("/version")
def version():
    return {"git_commit": os.getenv("GIT_COMMIT")}


handler = Mangum(app)
