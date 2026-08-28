<script lang="ts">
	import BigButton from './BigButton.svelte';
	import Footer from './Footer.svelte';
	
	let { categories, onselect }: { categories: string[]; onselect: (name: string) => void } =
		$props();

	// Regroupe les catégories par famille (Prépa / Ingé / Autres) en se basant sur leur nom,
	// tout en respectant l'ordre déjà renvoyé par le backend (categories arrive pré-triée).
	let groups = $derived.by(() => {
		const prepa = categories.filter((c) => c.includes('Prépa'));
		const inge = categories.filter((c) => c.includes('Ingé'));
		const autres = categories.filter((c) => !c.includes('Prépa') && !c.includes('Ingé'));

		return [
			{ label: "Prépa", items: prepa },
			{ label: "Ingé", items: inge },
			{ label: 'Autres', items: autres }
		].filter((g) => g.items.length > 0);
	});
</script>

<div class="min-h-screen bg-mist p-4 dark:bg-mist-dark">
	<div
		class="mb-4 flex items-baseline justify-center gap-0.5 font-display text-4xl font-bold tracking-tight"
	>
		<span class="text-signal">Esi</span><span class="text-ink dark:text-ink-dark">EDT</span>
	</div>
	<h1 class="mb-6 font-display text-2xl font-bold text-ink dark:text-ink-dark">Choisis ta promo</h1>

	{#each groups as group, i (i)}
		<div class:mt-6={i > 0}>
			<h2 class="mb-2 font-display text-xs font-semibold uppercase tracking-wide text-ink/40 dark:text-ink-dark/40">
				{group.label}
			</h2>
			<div class="grid grid-cols-2 gap-3">
				{#each group.items as name (name)}
					<BigButton label={name} onclick={() => onselect(name)} />
				{/each}
			</div>
		</div>
	{/each}
	<Footer />

</div>