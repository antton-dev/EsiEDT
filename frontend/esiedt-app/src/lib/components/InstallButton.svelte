<script lang="ts">
	import { installState, promptInstall } from '$lib/stores/installPrompt.svelte';

    
</script>

{#if installState.deferredPrompt && !installState.installed}
	<button
		onclick={promptInstall}
		class="fixed bottom-20 right-4 z-50 rounded-full bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg"
	>
		Installer l'app
	</button>
{/if}