document.getElementById('ocr-button').addEventListener('click', async () => {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file!');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    document.getElementById('processing-text').style.display = 'block';
    document.getElementById('results-container').style.display = 'none';

    try {
        const response = await fetch('/extract-invoice/', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            // Display results
            document.getElementById('uploaded-image').src = result.image_url;
            document.getElementById('extracted-text').value = JSON.stringify(result.extracted_text, null, 2);
            document.getElementById('results-container').style.display = 'block';
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error during fetch:', error);
        alert('An error occurred while processing your request.');
    } finally {
        document.getElementById('processing-text').style.display = 'none';
    }
});
