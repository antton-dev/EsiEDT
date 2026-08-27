import { browser } from '$app/environment';

export const installState = $state<{ deferredPrompt: any; installed: boolean }>({
	deferredPrompt: null,
	installed: false
});

if (browser) {
	window.addEventListener('beforeinstallprompt', (e) => {
		e.preventDefault(); // empêche la mini-barre auto de Chrome, on gère nous-mêmes
		installState.deferredPrompt = e;
	});

	window.addEventListener('appinstalled', () => {
		installState.installed = true;
		installState.deferredPrompt = null;
	});
}

export async function promptInstall() {
	if (!installState.deferredPrompt) return;
	installState.deferredPrompt.prompt();
	await installState.deferredPrompt.userChoice;
	installState.deferredPrompt = null;
}