import os
import base64
from groq import Groq
from dotenv import load_dotenv
import json
# Load environment variables from .env file
load_dotenv()

class GroqInvoiceExtractor:
    """
    A class to interact with Groq API to extract invoice data from an image using Llama Vision model.
    
    Attributes:
    ----------
    api_key : str
        API key for Groq API authentication.
    model : str
        The Groq model to use for image analysis (default is "llama-3.2-11b-vision-preview").
    client : Groq
        The Groq client initialized with the API key.
    
    Methods:
    -------
    encode_image(image_path: str) -> str
        Encodes the provided image into a base64 string.
    extract_invoice_data(image_path: str) -> dict
        Extracts invoice data from an image using the Groq Llama model and returns the results in JSON format.
    """
    
    def __init__(self, api_key: str, model: str = "llama-3.2-11b-vision-preview"):
        """
        Initializes the GroqInvoiceExtractor with the API key and model.
        
        Parameters:
        ----------
        api_key : str
            The API key to authenticate with Groq API.
        model : str, optional
            The model used for extraction, default is "llama-3.2-11b-vision-preview".
        """
        self.api_key = api_key
        os.environ['GROQ_API_KEY'] = self.api_key
        self.client = Groq(api_key=self.api_key)
        self.model = model

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
    
    def extract_invoice_data(self, image_path: str) -> dict:
        """
        Extracts invoice data from an image by sending the image to the Groq API for processing.
        The image is first encoded to base64, then passed to the Llama model for analysis.
        
        Parameters:
        ----------
        image_path : str
            The local path to the image file (invoice).
        
        Returns:
        -------
        dict
            The extracted invoice data in JSON format.
        """
        # Encode the image to base64
        base64_image = self.encode_image(image_path)

        # Create the prompt for the model to extract invoice data
        prompt = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                "Extract detailed invoice data from this image. "
                "Ensure that all information is organized as follows: "
                "- 'billed_from' should include the sender's name and address as one field. "
                "- 'billed_to' should include the recipient's name and address as one field. "
                "- Include other details like 'items', 'payment_method', 'invoice_number', 'date', and 'total'. "
                "Return the data in JSON format with correct field names and a clear structure in vertical. dont provide any other information."
                )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }

        # Send the request to the Groq API
        chat_completion = self.client.chat.completions.create(
            messages=[prompt],
            temperature=0.4,
            model=self.model
        )

        # Return the extracted data in JSON format  
        response_content= chat_completion.choices[0].message.content
        return response_content

# Example usage of the GroqInvoiceExtractor class

# # API Key for Groq (make sure to set the correct API key)
# api_key = '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'

# # # Initialize the invoice extractor object
# invoice_extractor = GroqInvoiceExtractor(api_key)

# # Path to the invoice image
# image_path = r"C:\Users\vamsh\OneDrive\Pictures\Screenshots\Screenshot 2024-12-21 155315.png"

# # Extract invoice data from the image
# invoice_data = invoice_extractor.extract_invoice_data(image_path)

# # Print the extracted invoice data
# print(invoice_data)
