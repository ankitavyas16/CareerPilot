    async loadApplications() {
        try {
            const response = await this.apiClient.get('/applications');
            const appsList = document.getElementById('applications-list');

            if (response.length === 0) {
                appsList.innerHTML = '<p>No applications tracked yet.</p>';
                return;
            }

            appsList.innerHTML = response
                .map(app => `
                    <div class="app-card">
                        <h4>${app.role}</h4>
                        <p class="match-company">${app.company}</p>
                        <div class="job-meta">
                            <span class="meta-tag">📅 Applied: ${new Date(app.created_at).toLocaleDateString()}</span>
                            <span class="meta-tag">👤 ${app.recruiter_name || 'N/A'}</span>
                        </div>
                        <span class="app-status ${app.status}">${app.status.toUpperCase()}</span>
                    </div>
                `)
                .join('');
        } catch (error) {
            document.getElementById('applications-list').innerHTML = '<p>Error loading applications</p>';
        }
    }

    testAPIConnection() {
        this.apiClient.get('/health')
            .then(response => {
                if (response.status === 'ok') {
                    this.showSuccess('✓ API Connection successful!');
                } else {
                    this.showError('✗ API returned unexpected response');
                }
            })
            .catch(error => {
                this.showError('✗ Cannot connect to API: ' + error.message);
            });
    }

    showSuccess(message) {
        const msg = document.createElement('div');
        msg.className = 'success-message';
        msg.textContent = message;
        document.body.insertBefore(msg, document.body.firstChild);
        setTimeout(() => msg.remove(), 4000);
    }

    showError(message) {
        const msg = document.createElement('div');
        msg.className = 'error-message';
        msg.textContent = message;
        document.body.insertBefore(msg, document.body.firstChild);
        setTimeout(() => msg.remove(), 4000);
    }
}

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CareerPilotApp();
});
