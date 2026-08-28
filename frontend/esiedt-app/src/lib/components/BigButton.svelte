<script lang="ts">
	let { label, onclick }: { label: string; onclick: () => void } = $props();
</script>

<button
	{onclick}
	class="rounded-2xl border border-lilac/50 bg-white px-4 py-6 text-center font-display text-base font-semibold text-ink shadow-sm transition active:scale-95 active:border-signal active:bg-signal active:text-mist dark:border-lilac-dark/20 dark:bg-surface-dark dark:text-ink-dark dark:active:bg-signal dark:active:text-mist-dark"
>
	{label}
</button>