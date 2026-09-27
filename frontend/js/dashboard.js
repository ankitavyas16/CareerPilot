// Dashboard-specific functions

async function loadDashboardData() {
	const status = document.getElementById('apiStatus');

	try {
		await api.health();
		status.textContent = 'API connected';
	} catch (error) {
		status.textContent = 'API offline';
		status.classList.add('error');
		console.error('Error loading dashboard data:', error);
	}
}
