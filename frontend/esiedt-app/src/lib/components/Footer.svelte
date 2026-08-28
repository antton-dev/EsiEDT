<script lang="ts">
	import { formatDateTime } from '$lib/utils/schedule';
	import { themeStore, cycleTheme } from '$lib/stores/theme.svelte';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faSun, faMoon, faCircleHalfStroke } from '@fortawesome/free-solid-svg-icons';

	let { compact = false, fetchedAt = null }: { compact?: boolean; fetchedAt?: string | null } =
		$props();

	const icons = { system: faCircleHalfStroke, light: faSun, dark: faMoon };
	const labels = { system: 'Système', light: 'Clair', dark: 'Sombre' };
</script>

<footer
	class=" border-t border-lilac/30 px-4 pt-4 text-center font-body text-xs text-ink/40 dark:border-lilac-dark/20 dark:text-ink-dark/40"
	class:pb-28={compact}
	class:pb-6={!compact}
>
	<button
		onclick={cycleTheme}
		class="mx-auto mb-3 flex items-center gap-1.5 rounded-full border border-lilac/50 px-3 py-1.5 text-xs font-semibold text-ink/60 transition active:bg-lilac/20 dark:border-lilac-dark/30 dark:text-ink-dark/60 dark:active:bg-surface-dark"
	>
		<FontAwesomeIcon icon={icons[themeStore.mode]} />
		{labels[themeStore.mode]}
	</button>

	<p class="text-xxs">Données ADE mises en cache tous les jours à 7h00, puis à la demande pendant 2h.</p>
	<p>
		{#if fetchedAt}
			Dernière synchronisation avec ADE : <span class="font-mono">{formatDateTime(fetchedAt)}</span>
		{/if}
	</p>
	<p class="mt-0.5">
		Fait par
			<a
			href="https://anttonc.fr"
			target="_blank"
			rel="noopener noreferrer"
			class="font-semibold text-signal underline decoration-signal/30 underline-offset-2"
		>
			anttonc.fr
		</a>
	</p>
</footer>