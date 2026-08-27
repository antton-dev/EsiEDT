import { browser } from '$app/environment';

const STORAGE_KEY = 'esiedt-selected-group';

export interface SelectedGroup {
	id: string;
	name: string;
}

function loadInitial(): SelectedGroup | null {
	if (!browser) return null; // pas de localStorage côté serveur (SSR)
	const raw = localStorage.getItem(STORAGE_KEY);
	return raw ? JSON.parse(raw) : null;
}

export const groupStore = $state<{ current: SelectedGroup | null }>({
	current: loadInitial()
});

export function selectGroup(group: SelectedGroup) {
	groupStore.current = group;
	localStorage.setItem(STORAGE_KEY, JSON.stringify(group));
}

export function clearGroup() {
	groupStore.current = null;
	localStorage.removeItem(STORAGE_KEY);
}