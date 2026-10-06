import { browser } from '$app/environment';

export type ViewMode = 'day' | 'week';

const STORAGE_KEY = 'esiedt-view-mode';

function loadInitial(): ViewMode {
	if (!browser) return 'day';
	try {
		return localStorage.getItem(STORAGE_KEY) === 'week' ? 'week' : 'day';
	} catch {
		return 'day';
	}
}

export const viewModeStore = $state<{ mode: ViewMode }>({ mode: loadInitial() });

export function setViewMode(mode: ViewMode) {
	viewModeStore.mode = mode;
	try {
		localStorage.setItem(STORAGE_KEY, mode);
	} catch {
		// stockage indisponible (navigation privée...) : on garde juste la valeur en mémoire
	}
}

export function toggleViewMode() {
	setViewMode(viewModeStore.mode === 'day' ? 'week' : 'day');
}