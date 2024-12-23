document.addEventListener("DOMContentLoaded", function () {
    const ocrButton = document.getElementById("ocr-button");
    const fileInput = document.getElementById("file-input");
    const processingText = document.getElementById("processing-text");
    const resultsContainer = document.getElementById("results-container");
    const extractedTextArea = document.getElementById("extracted-text");
    const uploadedImage = document.getElementById("uploaded-image");
    const submitButton = document.getElementById("submit-button");

    // Helper function to handle the OCR request with timeout
    async function performOCRWithTimeout(formData, timeout = 25000) {
        // Create an abort controller for the fetch request
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch("/extract-invoice/", {
                method: "POST",
                body: formData,
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Processing timeout');
            }
            throw error;
        }
    }

    // Event listener for OCR button
    ocrButton.addEventListener("click", async function (event) {
        event.preventDefault();

        // Check if a file is selected
        if (fileInput.files.length === 0) {
            alert("Please select an invoice image.");
            return;
        }

        const file = fileInput.files[0];

        // Show the "Processing" message
        processingText.style.display = "block";

        // Clear previous results
        resultsContainer.style.display = "none";
        extractedTextArea.value = "";

        try {
            // Create a FormData object to send the file to the server
            const formData = new FormData();
            formData.append("file", file);

            // Perform OCR with 25-second timeout
            const data = await performOCRWithTimeout(formData);

            if (data.image_url) {
                // Display the uploaded image
                uploadedImage.src = data.image_url;

                // Display the extracted text
                extractedTextArea.value = JSON.stringify(data.extracted_text, null, 2);

                // Show the results section
                resultsContainer.style.display = "block";
            } else {
                alert("Error extracting data: " + data.error);
            }
        } catch (error) {
            console.error("Error during the extraction process:", error);
            
            // Custom message for timeout
            if (error.message === 'Processing timeout') {
                processingText.textContent = "Processing is taking longer than expected. Please try again after some time.";
                setTimeout(() => {
                    processingText.textContent = "Processing... Please wait";
                    processingText.style.display = "none";
                }, 3000);
            } else {
                alert("An error occurred while processing the invoice.");
                processingText.style.display = "none";
            }
        }
    });
});