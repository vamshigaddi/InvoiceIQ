import os
from pydantic import BaseModel, Field
from typing import List, Optional
from groq import Groq
import instructor
import base64


class InvoiceItem(BaseModel):
    """Schema for individual invoice items."""
    description: str = Field(..., description="Description of the item")
    quantity: int = Field(..., description="Quantity of the item")
    price: float = Field(..., description="Price of the item")
    amount: float = Field(..., description="Total amount for the item")


class Invoice(BaseModel):
    """Schema for the structured invoice data."""
    billed_from: str = Field(..., description="billed_from' should include the sender's name and address as one field.")
    billed_to: str = Field(..., description="billed_to' should include the recipient's name and address as one field.")
    invoice_number: str = Field(..., description="Invoice number")
    date: str = Field(..., description="Invoice date")
    items: List[InvoiceItem] = Field(default_factory=list, description="List of items")
    payment_method: Optional[str] = Field(None, description="Payment method used")
    total: float = Field(..., description="Total invoice amount")
    notes: Optional[str] = Field(None, description="Additional notes on the invoice")


# Initialize the Groq client
client = Groq(api_key=')
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

# Encode your image (assuming base64 encoding function is already implemented)
image_path = r"C:\Users\vamsh\OneDrive\Pictures\Screenshots\Screenshot 2024-12-21 133011.png"


def encode_image(image_path: str) -> str:
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

base64_image = encode_image(image_path)  # Replace with your actual encoding function

# Define the prompt and send the request
resp = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract structured invoice data with confidence."
                                        "- 'billed_from' should include the sender's name and address as one field. "
                                        "- 'billed_to' should include the recipient's name and address as one field. "
                                        "- Include other details like 'items', 'payment_method', 'invoice_number', 'date', and 'total'. "},
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

# Print the structured and validated response
print(resp.model_dump_json(indent=2))
