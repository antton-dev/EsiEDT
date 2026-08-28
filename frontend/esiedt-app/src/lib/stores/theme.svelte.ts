import { browser } from '$app/environment';

type ThemeMode = 'system' | 'light' | 'dark';

const STORAGE_KEY = 'esiedt-theme';

function loadInitial(): ThemeMode {
	if (!browser) return 'system';
	const stored = localStorage.getItem(STORAGE_KEY);
	return stored === 'light' || stored === 'dark' ? stored : 'system';
}

export const themeStore = $state<{ mode: ThemeMode }>({ mode: loadInitial() });

function systemPrefersDark(): boolean {
	return browser && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

export function isDarkActive(): boolean {
	if (themeStore.mode === 'dark') return true;
	if (themeStore.mode === 'light') return false;
	return systemPrefersDark();
}

export function setTheme(mode: ThemeMode) {
	themeStore.mode = mode;
	localStorage.setItem(STORAGE_KEY, mode);
	applyTheme();
}

export function applyTheme() {
	if (!browser) return;
	document.documentElement.classList.toggle('dark', isDarkActive());
}

export function cycleTheme() {
	const next: Record<ThemeMode, ThemeMode> = { system: 'light', light: 'dark', dark: 'system' };
	setTheme(next[themeStore.mode]);
}

if (browser) {
	applyTheme();
	window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
		if (themeStore.mode === 'system') applyTheme();
	});
}