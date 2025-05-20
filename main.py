from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from PIL import Image
import io
import uuid
import os
from fastapi import Request
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()


# Configura aquí tus credenciales Cloudinary o usa variables de entorno
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Carga el modelo YOLO (ajusta la ruta si es necesario)
model = YOLO("models/best.pt")

def analyze_cracks_with_yolo(image_path: str):
    results = model(image_path)
    # Guarda imagen anotada
    save_path = str(Path(image_path).parent / f"annotated_{Path(image_path).name}")
    results[0].save(save_path)

    num_cracks = len(results[0].boxes.data)
    return save_path, num_cracks

def upload_file_to_cloudinary(file_path: str, resource_type="image") -> str:
    res = cloudinary.uploader.upload(file_path, resource_type=resource_type)
    return res.get("secure_url")


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))
    img_path = UPLOAD_DIR / f"{uuid.uuid4().hex}.jpg"
    img.save(img_path)

    # Análisis con YOLO
    annotated_path, cracks_detected = analyze_cracks_with_yolo(str(img_path))

    # Generar reporte PDF

    # Subir imagen anotada y pdf a Cloudinary
    image_url = upload_file_to_cloudinary(annotated_path, resource_type="image")

    return {
        "annotated_image_url": image_url,
        "report": {
            "cracks_detected": cracks_detected
        }
    }
