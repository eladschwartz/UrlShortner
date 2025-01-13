document.addEventListener('DOMContentLoaded', function() {
    // Handle copy buttons
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const input = this.previousElementSibling;
            await navigator.clipboard.writeText(input.value);
            
            const icon = this.querySelector('i');
            icon.classList.remove('fa-copy');
            icon.classList.add('fa-check');
            setTimeout(() => {
                icon.classList.remove('fa-check');
                icon.classList.add('fa-copy');
            }, 2000);
        });
    });

    // Handle status toggles
    document.querySelectorAll('.status-toggle').forEach(toggle => {
        toggle.addEventListener('change', async function() {
            const urlId = this.dataset.urlId;
            const isActive = this.checked;

            try {
                const response = await fetch(`/api/urls/${urlId}/toggle`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ is_active: isActive })
                });

                if (!response.ok) {
                    throw new Error('Failed to update status');
                }
            } catch (error) {
                console.error('Error:', error);
                this.checked = !isActive; // Revert the toggle
                alert('Failed to update URL status');
            }
        });
    });

    // Handle delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async function() {
            if (!confirm('Are you sure you want to delete this URL?')) {
                return;
            }

            const urlId = this.dataset.urlId;
            try {
                const response = await fetch(`/api/urls/${urlId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    throw new Error('Failed to delete URL');
                }

                // Remove the row from the table
                this.closest('tr').remove();
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to delete URL');
            }
        });
    });

    // Handle password protection
    let currentUrlId = null;

    document.querySelectorAll('.password-btn').forEach(button => {
        button.addEventListener('click', function() {
            currentUrlId = this.dataset.urlId;
            document.getElementById('passwordInput').value = '';
        });
    });

    document.getElementById('savePasswordBtn').addEventListener('click', async function() {
        if (!currentUrlId) return;

        const password = document.getElementById('passwordInput').value;
        try {
            const response = await fetch(`/api/urls/${currentUrlId}/password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password })
            });

            if (!response.ok) {
                throw new Error('Failed to update password');
            }

            const data = await response.json();
            
            // Update the password button appearance
            const passwordBtn = document.querySelector(`.password-btn[data-url-id="${currentUrlId}"]`);
            if (data.is_protected) {
                passwordBtn.classList.remove('btn-outline-warning');
                passwordBtn.classList.add('btn-warning');
            } else {
                passwordBtn.classList.remove('btn-warning');
                passwordBtn.classList.add('btn-outline-warning');
            }

            // Close the modal
            bootstrap.Modal.getInstance(document.getElementById('passwordModal')).hide();
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to update password');
        }
    });
});