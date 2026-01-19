from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from contextlib import asynccontextmanager
from src.config import settings
from src.engine import DetectionEngine
from src.clients.blue_onyx import BlueOnyxClient
from src.inference.speciesnet_wrapper import SpeciesNetWrapper
import uvicorn
import logging

# Setup logging
# logging.basicConfig(level=logging.INFO) # Handled by server.py or uvicorn
logger = logging.getLogger(__name__)

# Initialize singletons
blue_onyx = BlueOnyxClient(settings.BLUE_ONYX_URL)
speciesnet = SpeciesNetWrapper()
engine = DetectionEngine(blue_onyx, speciesnet)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing dependencies...")
    # Pre-warm SpeciesNet?
    yield
    # Shutdown
    logger.info("Shutting down dependencies...")
    # nothing to clean up explicitly for now

app = FastAPI(lifespan=lifespan)

# Root Endpoint
@app.get("/")
async def root():
    return {"status": "running", "service": "AI-Vision-Relay", "gpu": speciesnet.device_name}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/v1/vision/detection")
async def detect(image: UploadFile = File(...)):
    # Determine which client sent the request (Blue Iris usually checks /v1/vision/detection)
    # Just forward to engine
    try:
        image_data = await image.read()
        result = await engine.process_image(image_data)
        return result
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=False)
