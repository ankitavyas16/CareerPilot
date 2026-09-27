const utils = {
	showToast(message, type = 'info') {
		console[type === 'error' ? 'error' : 'log'](message);
	},
};
