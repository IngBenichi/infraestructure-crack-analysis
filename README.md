# Simulador de Detección de Grietas en Infraestructura Civil

Este proyecto es una aplicación web construida con FastAPI que permite subir imágenes de infraestructura civil para detectar grietas estructurales usando un modelo YOLO entrenado. Además, la imagen anotada con las detecciones se sube a Cloudinary para ser visualizada en línea.

---

## Características

- Subida de imágenes para análisis.
- Detección automática de grietas usando YOLO.
- Generación y visualización de imágenes anotadas.
- Almacenamiento de imágenes anotadas en Cloudinary con URL pública.
- Respuesta JSON con la cantidad de grietas detectadas y URL de la imagen anotada.

---

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- PIL (Pillow)
- ultralytics (YOLO)
- Cloudinary SDK para Python
- python-dotenv

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/IngBenichi/infraestructure-crack-analysis.git
cd infraestructure-crack-analysis
````

2. Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` en la raíz con tus credenciales de Cloudinary:

```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

5. Asegúrate de tener el modelo YOLO en la carpeta `models/best.pt`. Puedes entrenar uno propio o usar uno preentrenado.

---

## Uso

Para correr la aplicación en modo desarrollo con recarga automática:

```bash
uvicorn main:app --reload
```

Luego abre en el navegador: `http://127.0.0.1:8000`

---

## Estructura

```
.
├── main.py                # Código backend FastAPI
├── templates/
│   └── index.html         # Frontend con formulario y resultados
├── static/
│   ├── uploads/           # Imágenes subidas temporalmente
│   └── ...                # Otros archivos estáticos (CSS, JS)
├── models/
│   └── best.pt            # Modelo YOLO
├── .env                   # Variables de entorno (no subir a GitHub)
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

---

## Endpoints

* `GET /`
  Renderiza el formulario para subir imágenes.

* `POST /analyze/`
  Recibe la imagen, analiza grietas, sube la imagen anotada a Cloudinary y devuelve JSON con:

```json
{
  "annotated_image_url": "https://res.cloudinary.com/...",
  "report": {
    "cracks_detected": 3
  }
}
```

---

## Licencia

Este proyecto está bajo la licencia MIT.
