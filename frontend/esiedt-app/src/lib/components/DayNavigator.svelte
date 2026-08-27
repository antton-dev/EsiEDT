<script lang="ts">
	import type { DayGroup } from '$lib/utils/schedule';
	import { formatDayShort } from '$lib/utils/schedule';

	let {
		days,
		selectedKey,
		onselect
	}: { days: DayGroup[]; selectedKey: string; onselect: (key: string) => void } = $props();

	let container: HTMLDivElement;

	$effect(() => {
		const activeButton = container?.querySelector<HTMLButtonElement>(
			`[data-day-key="${selectedKey}"]`
		);
		activeButton?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
	});
</script>

<div bind:this={container} class="flex gap-2 overflow-x-auto px-4 pb-2 pt-3">
	{#each days as day (day.dateKey)}
		<button
			data-day-key={day.dateKey}
			onclick={() => onselect(day.dateKey)}
			class="shrink-0 rounded-full px-4 py-2 font-body text-sm font-semibold transition
				{day.dateKey === selectedKey ? 'bg-signal text-mist' : 'bg-white text-ink/70'}"
		>
			{formatDayShort(day.date)}
		</button>
	{/each}
</div>