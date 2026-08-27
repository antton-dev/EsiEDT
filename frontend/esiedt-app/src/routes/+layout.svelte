<script lang="ts">
	import { browser } from '$app/environment';
	import './layout.css'; // garde cette ligne si elle existe déjà (import Tailwind)
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
