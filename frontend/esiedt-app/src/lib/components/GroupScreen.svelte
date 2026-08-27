<script lang="ts">
	import BigButton from './BigButton.svelte';
	import Footer from './Footer.svelte';
	import type { ResourceGroup } from '$lib/types';

	let {
		categoryName,
		groups,
		onselect,
		onback
	}: {
		categoryName: string;
		groups: ResourceGroup[];
		onselect: (group: ResourceGroup) => void;
		onback: () => void;
	} = $props();
</script>

<div class="flex min-h-screen flex-col bg-mist p-4">
	<div
		class="mb-4 flex items-baseline justify-center gap-0.5 font-display text-4xl font-bold tracking-tight"
	>
		<span class="text-signal">Esi</span><span class="text-ink">EDT</span>
	</div>
	<div class="mb-6 flex items-center gap-3">
		<button
			onclick={onback}
			class="flex h-9 w-9 items-center justify-center rounded-full text-signal transition active:bg-lilac/30"
			aria-label="Retour"
		>
			←
		</button>
		<h1 class="font-display text-2xl font-bold text-ink">{categoryName}</h1>
	</div>
	<div class="grid grid-cols-2 gap-3">
		{#each groups as group (group.id)}
			<BigButton label={group.short_name} onclick={() => onselect(group)} />
		{/each}
	</div>
	<div class="mt-auto">
		<Footer />
	</div>
</div>