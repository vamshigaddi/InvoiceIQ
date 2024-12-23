from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from data_extracter import InvoiceExtractor
import logging

# Initialize FastAPI app
app = FastAPI()

# MongoDB client setup
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = mongo_client["invoice_data"]
invoices_collection = db["invoices"]

# Initialize invoice extractor
api_key = os.getenv("GROQ_API_KEY")
invoice_extractor = InvoiceExtractor(api_key)

# Serve static files (for images, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)

# Logger configuration
logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the homepage for invoice extraction.
    """
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request URL: {request.url}")
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/extract-invoice/")
async def extract_invoice(file: UploadFile = File(...)):
    """
    Process a single invoice image and return extracted data.
    """
    try:
        logging.info(f"Received file: {file.filename}")
        # Save uploaded file to the static directory
        file_path = os.path.join("static", file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Extract data using the invoice extractor
        extracted_data = invoice_extractor.extract_invoice_data(file_path)
        extracted_text = json.loads(extracted_data) if extracted_data else {"error": "No data extracted"}

        # Return the image URL and extracted data
        return {
            "image_url": f"/static/{file.filename}",
            "extracted_text": extracted_text
        }
    except Exception as e:
        logging.error(f"Error in extract_invoice: {e}")
        return {"error": str(e)}





