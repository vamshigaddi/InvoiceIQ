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


@app.get("/dashboard/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Render the dashboard page for viewing saved invoices.
    """
    logging.info(f"Rendering dashboard.")
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/extract-invoice/")
async def extract_invoice(file: UploadFile = File(...)):
    """
    Process a single invoice image and return extracted data.
    """
    try:
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


@app.post("/submit-invoice/")
async def submit_invoice(image_url: str = Form(...), extracted_text: str = Form(...)):
    """
    Submit the final data to MongoDB.
    """
    try:
        # Save invoice data to MongoDB
        invoice_doc = {
            "image_url": image_url,
            "data": json.loads(extracted_text),
            "edited": False
        }
        invoices_collection.insert_one(invoice_doc)
        logging.info(f"Invoice data saved: {invoice_doc}")
        return {"message": "Data submitted successfully!"}
    except Exception as e:
        logging.error(f"Error in submit_invoice: {e}")
        return {"error": str(e)}


@app.get("/get-data/")
async def get_data():
    """
    Fetch all saved invoices from MongoDB.
    """
    try:
        # Retrieve all invoices
        invoices = list(invoices_collection.find({}, {"_id": 0}))
        logging.info(f"Fetched {len(invoices)} invoices from the database.")
        return {"data": invoices}
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return {"error": str(e)}
