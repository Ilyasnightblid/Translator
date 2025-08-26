class FileTranslation {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.translateBtn = document.getElementById('translateFileBtn');
        
        this.bindEvents();
    }
    
    bindEvents() {
        if (!this.uploadArea || !this.fileInput) return;
        
        // Click to select file
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            this.handleFileSelection(e.target.files[0]);
        });
        
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelection(files[0]);
            }
        });
    }
    
    handleFileSelection(file) {
        if (!file) return;
        
        // Validate file type
        const allowedTypes = ['text/plain', 'application/json'];
        const allowedExtensions = ['.txt', '.json'];
        
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
            this.showError('Type de fichier non autorisé. Seuls les fichiers .txt et .json sont acceptés.');
            return;
        }
        
        // Validate file size (16MB)
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showError('Le fichier est trop volumineux. Taille maximale: 16MB.');
            return;
        }
        
        // Update UI
        this.displayFileInfo(file);
        this.translateBtn.disabled = false;
    }
    
    displayFileInfo(file) {
        if (!this.fileInfo || !this.fileName || !this.fileSize) return;
        
        this.fileName.textContent = file.name;
        this.fileSize.textContent = `(${this.formatFileSize(file.size)})`;
        this.fileInfo.style.display = 'block';
        
        // Update upload area
        this.uploadArea.classList.add('has-file');
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.file-translation-container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new FileTranslation();
});
