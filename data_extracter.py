import os
import base64
from pydantic import BaseModel, Field
from typing import List, Optional
from groq import Groq
import instructor


class InvoiceItem(BaseModel):
    """
    A schema representing an individual item in an invoice.
    
    Attributes:
    -----------
    description : str
        The description of the invoice item.
    quantity : int
        The quantity of the item.
    price : float
        The price per item.
    amount : float
        The total amount for the item (quantity * price).
    """
    description: str = Field(..., description="Description of the item")
    quantity: int = Field(..., description="Quantity of the item")
    price: float = Field(..., description="Price of the item")
    amount: float = Field(..., description="Total amount for the item")


class Invoice(BaseModel):
    """
    A schema for the structured invoice data.
    
    Attributes:
    -----------
    billed_from : str
        The sender's name and address.
    billed_to : str
        The recipient's name and address.
    invoice_number : str
        The invoice number.
    date : str
        The invoice date.
    items : List[InvoiceItem]
        A list of invoice items.
    payment_method : Optional[str]
        The payment method used (e.g., cash, check, etc.).
    total : float
        The total amount of the invoice.
    notes : Optional[str]
        Additional notes regarding the invoice.
    """
    billed_from: str = Field(..., description="Sender's name and address")
    billed_to: str = Field(..., description="Recipient's name and address")
    invoice_number: str = Field(..., description="Invoice number")
    date: str = Field(..., description="Invoice date")
    items: List[InvoiceItem] = Field(default_factory=list, description="List of items in the invoice")
    payment_method: Optional[str] = Field(None, description="Payment method used for the transaction")
    total: float = Field(..., description="Total amount of the invoice")
    notes: Optional[str] = Field(None, description="Additional notes about the invoice")


class InvoiceExtractor:
    """
    A class responsible for extracting structured invoice data from images using the Groq API.

    Attributes:
    -----------
    api_key : str
        The API key for Groq authentication.
    client : Groq
        The Groq client initialized with the API key.
    """
    
    def __init__(self, api_key: str):
        """
        Initializes the GroqInvoiceExtractor with the given API key and sets up the Groq client.

        Parameters:
        ----------
        api_key : str
            The API key for authenticating with Groq API.
        """
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)
        self.client = instructor.from_groq(self.client, mode=instructor.Mode.TOOLS)

    def encode_image(self, image_path: str) -> str:
        """
        Encodes an image to base64 format.

        Parameters:
        ----------
        image_path : str
            The local path to the image file to be encoded.

        Returns:
        -------
        str
            The base64 encoded image as a string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_invoice_data(self, image_path: str) -> Invoice:
        """
        Extracts structured invoice data from an image by sending the image to the Groq API.

        Parameters:
        ----------
        image_path : str
            The local path to the invoice image.

        Returns:
        -------
        Invoice
            The extracted and validated invoice data.
        """
        # Encode the image to base64
        base64_image = self.encode_image(image_path)

        # Define the request payload
        resp = self.client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": 
                            "Extract structured invoice data with confidence. "
                            "- 'billed_from' should include the sender's name and address as one field. "
                            "- 'billed_to' should include the recipient's name and address as one field. "
                            "- Include other details like 'items', 'payment_method', 'invoice_number', 'date', and 'total'."
                            "Return the data in JSON format with correct field names and a clear structure in vertical. dont provide any other information."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            response_model=Invoice,  # Validate against the Invoice schema
        )

        # Return the extracted and validated invoice data
        response = resp.model_dump_json(indent=2)
        return response


# # # Example Usage:
if __name__ == "__main__":
    # Initialize the InvoiceExtractor with the API key
    api_key = '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'
    
    invoice_extractor = InvoiceExtractor(api_key=api_key)

    # Path to the invoice image
    image_path = r"C:\Users\vamsh\OneDrive\Pictures\Screenshots\Screenshot 2024-12-21 133011.png"

    # Extract invoice data
    try:
        invoice_data = invoice_extractor.extract_invoice_data(image_path)
        print("Extracted Invoice Data:")
        print(type(invoice_data))
        print(invoice_data)
    except Exception as e:
        print(f"Error extracting invoice data: {e}")
