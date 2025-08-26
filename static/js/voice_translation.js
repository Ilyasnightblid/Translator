class VoiceTranslation {
    constructor() {
        this.recognition = null;
        this.isRecording = false;
        this.transcribedText = '';
        
        this.startBtn = document.getElementById('startRecording');
        this.stopBtn = document.getElementById('stopRecording');
        this.statusDiv = document.getElementById('recordingStatus');
        this.transcribedDiv = document.getElementById('transcribedText');
        this.translateBtn = document.getElementById('translateBtn');
        this.hiddenInput = document.querySelector('input[name="transcribed_text"]');
        
        this.initSpeechRecognition();
        this.bindEvents();
    }
    
    initSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('Votre navigateur ne supporte pas la reconnaissance vocale.');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'fr-FR';
        
        this.recognition.onstart = () => {
            this.isRecording = true;
            this.updateUI();
        };
        
        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            this.transcribedText = finalTranscript;
            this.transcribedDiv.innerHTML = finalTranscript + '<span class="text-muted">' + interimTranscript + '</span>';
            this.hiddenInput.value = finalTranscript;
            
            if (finalTranscript.trim()) {
                this.translateBtn.disabled = false;
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.showError('Erreur de reconnaissance vocale: ' + event.error);
            this.stopRecording();
        };
        
        this.recognition.onend = () => {
            this.isRecording = false;
            this.updateUI();
        };
    }
    
    bindEvents() {
        if (this.startBtn) {
            this.startBtn.addEventListener('click', () => this.startRecording());
        }
        
        if (this.stopBtn) {
            this.stopBtn.addEventListener('click', () => this.stopRecording());
        }
    }
    
    startRecording() {
        if (!this.recognition) {
            this.showError('Reconnaissance vocale non disponible.');
            return;
        }
        
        try {
            this.transcribedText = '';
            this.transcribedDiv.textContent = '';
            this.hiddenInput.value = '';
            this.translateBtn.disabled = true;
            
            this.recognition.start();
        } catch (error) {
            this.showError('Impossible de démarrer l\'enregistrement: ' + error.message);
        }
    }
    
    stopRecording() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
        }
    }
    
    updateUI() {
        if (this.isRecording) {
            this.startBtn.style.display = 'none';
            this.stopBtn.style.display = 'inline-block';
            this.statusDiv.style.display = 'block';
            this.statusDiv.className = 'alert alert-danger';
            this.statusDiv.innerHTML = '<i class="fas fa-circle text-danger blink"></i> Enregistrement en cours...';
        } else {
            this.startBtn.style.display = 'inline-block';
            this.stopBtn.style.display = 'none';
            this.statusDiv.style.display = 'none';
            
            if (this.transcribedText.trim()) {
                this.transcribedDiv.innerHTML = this.transcribedText;
            } else {
                this.transcribedDiv.textContent = 'Cliquez sur "Commencer l\'enregistrement" pour parler...';
            }
        }
    }
    
    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.voice-translation-container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new VoiceTranslation();
});
