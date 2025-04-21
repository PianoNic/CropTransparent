class ImageProcessor {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultSection = document.getElementById('resultSection');
        this.previewImage = document.getElementById('previewImage');
        this.originalSize = document.getElementById('originalSize');
        this.croppedSize = document.getElementById('croppedSize');
        this.croppedFilename = document.getElementById('croppedFilename');
        this.percentageSaved = document.getElementById('percentageSaved');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.newImageBtn = document.getElementById('newImageBtn');

        this.processedImage = null;
        this.processedFilename = null;

        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.dropZone.addEventListener('click', () => {
            this.fileInput.click();
        });

        this.dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.dropZone.classList.add('active');
        });

        this.dropZone.addEventListener('dragleave', () => {
            this.dropZone.classList.remove('active');
        });

        this.dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.dropZone.classList.remove('active');

            if (e.dataTransfer.files.length > 0) {
                this.handleFile(e.dataTransfer.files[0]);
            }
        });

        this.fileInput.addEventListener('change', () => {
            if (this.fileInput.files.length > 0) {
                this.handleFile(this.fileInput.files[0]);
            }
        });

        this.newImageBtn.addEventListener('click', () => {
            this.resetUI();
        });

        this.downloadBtn.addEventListener('click', () => {
            this.downloadImage();
        });

        document.addEventListener('themeChanged', (e) => {
            console.log('Theme changed to:', e.detail.theme);
        });
    }

    resetUI() {
        this.resultSection.classList.add('hidden');
        this.dropZone.classList.remove('hidden');
        this.fileInput.value = '';
        this.processedImage = null;
        this.processedFilename = null;
    }

    async handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        this.dropZone.classList.add('hidden');
        this.loadingSection.classList.remove('hidden');
        this.resultSection.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.displayResult(result);
            } else {
                alert(result.error || 'Processing failed');
                this.dropZone.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the image');
            this.dropZone.classList.remove('hidden');
        } finally {
            this.loadingSection.classList.add('hidden');
        }
    }

    displayResult(result) {
        this.previewImage.src = result.image;
        this.originalSize.textContent = result.original_size;
        this.croppedSize.textContent = result.cropped_size;
        this.croppedFilename.textContent = result.filename;

        const origDims = result.original_size.split('x');
        const cropDims = result.cropped_size.split('x');
        const origArea = origDims[0] * origDims[1];
        const cropArea = cropDims[0] * cropDims[1];
        const savePercent = Math.round((1 - cropArea / origArea) * 100);
        this.percentageSaved.textContent = `${savePercent}%`;

        this.processedImage = result.image;
        this.processedFilename = result.filename;

        this.resultSection.classList.remove('hidden');
    }

    async downloadImage() {
        if (!this.processedImage || !this.processedFilename) return;

        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: this.processedImage,
                    filename: this.processedFilename
                }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = this.processedFilename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                console.error('Download failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('currentYear').textContent = new Date().getFullYear();
    window.imageProcessor = new ImageProcessor();
});