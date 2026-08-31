<script lang="ts">
	import BigButton from './BigButton.svelte';
	import Footer from './Footer.svelte';
	import type { ResourceGroup } from '$lib/types';

	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faArrowLeft } from '@fortawesome/free-solid-svg-icons';

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

	function handleSelect(group: ResourceGroup) {
	if (typeof umami !== 'undefined') {
		umami.track('group_selected', { category: categoryName, group: group.short_name });
	}
	onselect(group);
}
</script>

<div class="flex min-h-screen flex-col bg-mist p-4 dark:bg-mist-dark">
	<div class="mb-4 flex items-baseline justify-center gap-0.5 font-display text-4xl font-bold tracking-tight">
		<span class="text-signal">Esi</span><span class="text-ink dark:text-ink-dark">EDT</span>
	</div>
	<div class="mb-6 flex items-center gap-3">
		<button
			onclick={onback}
			class="flex h-9 w-9 items-center justify-center rounded-full text-signal transition active:bg-lilac/30 dark:active:bg-surface-dark"
			aria-label="Retour"
		>
			<FontAwesomeIcon icon={faArrowLeft} class="mx-1" />
		</button>
		<h1 class="font-display text-2xl font-bold text-ink dark:text-ink-dark">{categoryName}</h1>
	</div>
	<div class="grid grid-cols-2 gap-3">
		{#each groups as group (group.id)}
			<BigButton label={group.short_name} onclick={() => handleSelect(group)} />
		{/each}
	</div>
	<div class="mt-auto">
		<Footer />
	</div>
</div>