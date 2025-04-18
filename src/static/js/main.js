document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const loadingSection = document.getElementById('loadingSection');
    const resultSection = document.getElementById('resultSection');
    const previewImage = document.getElementById('previewImage');
    const originalSize = document.getElementById('originalSize');
    const croppedSize = document.getElementById('croppedSize');
    const croppedFilename = document.getElementById('croppedFilename');
    const percentageSaved = document.getElementById('percentageSaved');
    const downloadBtn = document.getElementById('downloadBtn');
    const newImageBtn = document.getElementById('newImageBtn');
    
    let processedImage = null;
    let processedFilename = null;
    
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('active');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('active');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('active');
        
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });
    
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
        }
    });
    
    newImageBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        dropZone.classList.remove('hidden');
        fileInput.value = '';
    });
    
    downloadBtn.addEventListener('click', async () => {
        if (!processedImage || !processedFilename) return;
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: processedImage,
                    filename: processedFilename
                }),
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = processedFilename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                console.error('Download failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
    
    async function handleFile(file) {
        // Check if file is an image
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }
        
        // Show loading
        dropZone.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        resultSection.classList.add('hidden');
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Display result
                previewImage.src = result.image;
                originalSize.textContent = result.original_size;
                croppedSize.textContent = result.cropped_size;
                croppedFilename.textContent = result.filename;
                
                // Calculate savings
                const origDims = result.original_size.split('x');
                const cropDims = result.cropped_size.split('x');
                const origArea = origDims[0] * origDims[1];
                const cropArea = cropDims[0] * cropDims[1];
                const savePercent = Math.round((1 - cropArea / origArea) * 100);
                percentageSaved.textContent = `${savePercent}%`;
                
                // Store for download
                processedImage = result.image;
                processedFilename = result.filename;
                
                // Show result section
                resultSection.classList.remove('hidden');
            } else {
                alert(result.error || 'Processing failed');
                dropZone.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the image');
            dropZone.classList.remove('hidden');
        }
        
        loadingSection.classList.add('hidden');
    }
});