<script lang="ts">
	import BigButton from './BigButton.svelte';
	import Footer from './Footer.svelte';

	let { categories, onselect }: { categories: string[]; onselect: (name: string) => void } =
		$props();
</script>

<div class="flex min-h-screen flex-col bg-mist p-4">
	<div
		class="mb-4 flex items-baseline justify-center gap-0.5 font-display text-4xl font-bold tracking-tight"
	>
		<span class="text-signal">Esi</span><span class="text-ink">EDT</span>
	</div>
	<h1 class="mb-6 font-display text-2xl font-bold text-ink">Choisis ta promo</h1>
	<div class="grid grid-cols-2 gap-3">
		{#each categories as name (name)}
			<BigButton label={name} onclick={() => onselect(name)} />
		{/each}
	</div>
	<div class="mt-auto">
		<Footer />
	</div>
</div>