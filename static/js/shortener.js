class URLShortener {
    constructor() {
        this.urlForm = document.getElementById('urlForm');
        this.urlInput = document.getElementById('urlInput');
        this.passwordInput = document.getElementById('passwordInput');
        this.urlError = document.getElementById('urlError');
        this.resultCard = document.getElementById('resultCard');
        this.shortUrlInput = document.getElementById('shortUrl');
        this.copyButton = document.getElementById('copyButton');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.urlForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.urlInput.addEventListener('input', () => this.handleInput());
        this.copyButton.addEventListener('click', () => this.copyUrl());
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    async shortenUrl(url, password) {
        try {
            const customCode = document.getElementById('customCodeInput').value.trim();
            
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({
                    target_url: url,
                    password: password || null,
                    custom_code: customCode || null  // Include custom code if provided
                })
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to shorten URL');
            }
    
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        const url = this.urlInput.value.trim();
        const password = this.passwordInput?.value.trim();

        if (!this.isValidUrl(url)) {
            this.urlInput.classList.add('is-invalid');
            this.urlError.style.display = 'block';
            return;
        }

        this.urlInput.classList.remove('is-invalid');
        this.urlError.style.display = 'none';

        try {
            const data = await this.shortenUrl(url, password);
            const shortUrl = `${window.location.origin}/api/${data.short_code}`;
            this.shortUrlInput.value = shortUrl;
            this.resultCard.style.display = 'block';
            this.resultCard.scrollIntoView({ behavior: 'smooth' });

            // Clear the form fields
            this.urlInput.value = '';
            document.getElementById('customCodeInput').value = '';
            if (this.passwordInput) {
                this.passwordInput.value = '';
                // Hide the password note when clearing the form
                document.getElementById('passwordNote').classList.add('d-none');
            }
        } catch (error) {
            alert(error.message || 'Failed to shorten URL. Please try again.');
        }
    }

    handleInput() {
        if (this.urlInput.value.trim() && !this.isValidUrl(this.urlInput.value.trim())) {
            this.urlInput.classList.add('is-invalid');
            this.urlError.style.display = 'block';
        } else {
            this.urlInput.classList.remove('is-invalid');
            this.urlError.style.display = 'none';
        }
    }

    async copyUrl() {
        try {
            await navigator.clipboard.writeText(this.shortUrlInput.value);
            const copyIcon = this.copyButton.querySelector('i');
            copyIcon.classList.remove('fa-copy');
            copyIcon.classList.add('fa-check');
            setTimeout(() => {
                copyIcon.classList.remove('fa-check');
                copyIcon.classList.add('fa-copy');
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    }
}

    // Add password visibility toggle functionality
    document.getElementById('togglePassword').addEventListener('click', function() {
        const passwordInput = document.getElementById('passwordInput');
        const icon = this.querySelector('i');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });

    // Show password note if password is set
    document.getElementById('passwordInput').addEventListener('input', function() {
        const passwordNote = document.getElementById('passwordNote');
        if (this.value.trim()) {
            passwordNote.classList.remove('d-none');
        } else {
            passwordNote.classList.add('d-none');
        }
    });

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.urlShortener = new URLShortener();
});