from fastapi import FastAPI, UploadFile, File
from contextlib import asynccontextmanager
from src.config import settings
from src.proxy import DetectionProxy
from src.clients.blue_onyx import BlueOnyxClient
from src.inference.speciesnet_wrapper import SpeciesNetWrapper
import uvicorn
import logging

# Setup logging
# Setup logging
# logging.basicConfig(level=logging.INFO) # Handled by server.py or uvicorn
logger = logging.getLogger("AiVisionRelay")

# Global instances
proxy: DetectionProxy = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting SpeciesNet AI Proxy...")
    
    blue_onyx = BlueOnyxClient(base_url=settings.BLUE_ONYX_URL)
    
    speciesnet = SpeciesNetWrapper(region=settings.SPECIESNET_REGION)
    # Warm up / Load model
    speciesnet.initialize()
    
    global proxy
    proxy = DetectionProxy(blue_onyx, speciesnet)
    
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "service": "AI-Vision-Relay"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/v1/vision/detection")
async def detect(image: UploadFile = File(...)):
    if not proxy:
        return {"success": False, "error": "Service not initialized"}
    
    image_data = await image.read()
    result = await proxy.process_image(image_data)
    return result

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=False)
