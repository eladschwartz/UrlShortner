class URLShortener {
    constructor() {
        this.urlForm = document.getElementById('urlForm');
        this.urlInput = document.getElementById('urlInput');
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

    async shortenUrl(url) {
        try {
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({
                    target_url: url
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

        if (!this.isValidUrl(url)) {
            this.urlInput.classList.add('is-invalid');
            this.urlError.style.display = 'block';
            return;
        }

        this.urlInput.classList.remove('is-invalid');
        this.urlError.style.display = 'none';

        try {
            const data = await this.shortenUrl(url);
            const shortUrl = `${window.location.origin}/api/${data.short_code}`;
            this.shortUrlInput.value = shortUrl;
            this.resultCard.style.display = 'block';
            this.resultCard.scrollIntoView({ behavior: 'smooth' });
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

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.urlShortener = new URLShortener();
});