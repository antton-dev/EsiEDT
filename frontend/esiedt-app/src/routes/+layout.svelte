<script lang="ts">
	import { applyTheme } from '$lib/stores/theme.svelte';
	import { browser } from '$app/environment';
	import './layout.css'; 
	import InstallButton from '$lib/components/InstallButton.svelte';

	let { children } = $props();

	if (browser) {
		import('virtual:pwa-register').then(({ registerSW }) => {
			registerSW({ immediate: true });
		});
	}
</script>

{@render children()}
<InstallButton />
