# InvoiceIQ

This project is designed to perform Optical Character Recognition (OCR) on invoice images and extract structured data from them using the LLaMA 3.2 Vision model through the Groq API. The system extracts relevant invoice details and displays them in a user-friendly format, making it easy to analyze and store invoice data.

## Features

- **Invoice OCR Extraction**: Uses the LLaMA 3.2 Vision model via the Groq API to extract textual and structured data from invoice images.
- **Structured Data Output**: The extracted data is processed and formatted using **Pydantic** to ensure a structured and consistent output, including fields like invoice number, vendor details, date, and total amount.
- **FastAPI Backend**: The server is built using FastAPI, which handles file uploads, extraction requests, and interaction with the Groq API.

## Technologies Used

- **LLaMA 3.2 Vision Model** (via Groq API) for OCR and structured data extraction.
- **FastAPI** for backend API services.
- **Pydantic** for data validation and structured output formatting.
- **JavaScript, HTML, CSS** for the frontend UI.
- **Groq API** for invoking the LLaMA model for vision-based OCR tasks.

## Installation

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.8 or above
- MongoDB (running locally or using a cloud service)
- A **Groq API key** to access the LLaMA 3.2 Vision model (obtainable from Groq)

### Clone the repository

```bash
git clone https://github.com/vamshigaddi/InvoiceIQ.git
cd InvoiceIQ
```

###  Install dependencies
- pip install -r requirements.txt

### Setup Environment Variables
- Create a .env file in the root directory and add the following variables:
  ```bash
  GROQ_API_KEY="your_groq_api_key"
  ```
### Run the Application
```bash
uvicorn main:app --reload
```
- The application will be accessible at http://127.0.0.1:8000/

### Image
![InvoiceIQ](https://github.com/vamshigaddi/InvoiceIQ/blob/main/InvoiceIQ.png)

### API Endpoints
#### GET /
Render the homepage to upload invoice images for OCR processing.

#### POST /extract-invoice/
- Description: Upload an invoice image, and the system will extract textual and structured data from it.
- Request Body: A multipart file upload with the invoice image.

