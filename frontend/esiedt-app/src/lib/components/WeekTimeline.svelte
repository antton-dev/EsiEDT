<script lang="ts">
	import type { DayGroup } from '$lib/utils/schedule';
	import { getWeekBounds, toDateKey, formatDayShort } from '$lib/utils/schedule';
	import EventBlock from './EventBlock.svelte';

	let { days, now }: { days: DayGroup[]; now: Date } = $props();

	const PX_PER_MIN = 1.4;
	const MIN_COLUMN_WIDTH = 152;
	const HEADER_HEIGHT = 30;

	let bounds = $derived(getWeekBounds(days));
	let totalHeight = $derived((bounds.endMinutes - bounds.startMinutes) * PX_PER_MIN);
	let hours = $derived.by(() => {
		const list: number[] = [];
		for (let m = bounds.startMinutes; m <= bounds.endMinutes; m += 60) list.push(m);
		return list;
	});

	let todayKey = $derived(toDateKey(now));
	let nowMinutes = $derived(now.getHours() * 60 + now.getMinutes());
	let nowOffset = $derived((nowMinutes - bounds.startMinutes) * PX_PER_MIN);
</script>

<div class="flex max-h-[calc(100vh-220px)] overflow-auto">
	<div
		class="sticky left-0 top-0 z-20 w-10 shrink-0 bg-mist dark:bg-mist-dark"
		style="height: {totalHeight + HEADER_HEIGHT}px"
	>
		<div class="sticky top-0 z-20 bg-mist dark:bg-mist-dark" style="height: {HEADER_HEIGHT}px"></div>

		{#each hours as minutes (minutes)}
			<span
				class="absolute -translate-y-1/2 text-right font-mono text-xs text-ink/40 dark:text-ink-dark/40"
				style="top: {HEADER_HEIGHT + (minutes - bounds.startMinutes) * PX_PER_MIN}px; width: 2.5rem"
			>
				{String(Math.floor(minutes / 60)).padStart(2, '0')}h
			</span>
		{/each}
	</div>

	{#each days as day (day.dateKey)}
		{@const isToday = day.dateKey === todayKey}
		{@const showNowLine =
			isToday && nowMinutes >= bounds.startMinutes && nowMinutes <= bounds.endMinutes}
		<div
			class="min-w-[152px] flex-1 shrink-0 border-l border-lilac/20 dark:border-lilac-dark/10"
			style="max-width: none"
		>
			<div
				class="sticky top-0 z-10 bg-mist text-center font-body text-xs font-semibold dark:bg-mist-dark"
				style="height: {HEADER_HEIGHT}px; line-height: {HEADER_HEIGHT}px"
				class:text-signal={isToday}
				class:text-ink={!isToday}
				class:dark:text-ink-dark={!isToday}
			>
				{formatDayShort(day.date)}
			</div>
			<div class="relative" style="height: {totalHeight}px">
				{#each hours as minutes (minutes)}
					<div
						class="absolute left-0 right-0 h-px bg-lilac/20 dark:bg-lilac-dark/10"
						style="top: {(minutes - bounds.startMinutes) * PX_PER_MIN}px"
					></div>
				{/each}

				{#each day.events as event (event.title + event.start_time)}
					<EventBlock {event} {bounds} pxPerMin={PX_PER_MIN} compact />
				{/each}

				{#if showNowLine}
					<div class="absolute left-0 right-0 z-10 h-0.5 bg-signal" style="top: {nowOffset}px"></div>
				{/if}
			</div>
		</div>
	{/each}
</div>