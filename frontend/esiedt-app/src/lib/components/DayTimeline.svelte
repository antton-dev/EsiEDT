<script lang="ts">
	import type { ScheduleEvent } from '$lib/types';
	import { getDayBounds, toDateKey } from '$lib/utils/schedule';
	import EventBlock from './EventBlock.svelte';

	let { events, day, now }: { events: ScheduleEvent[]; day: Date; now: Date } = $props();

	const PX_PER_MIN = 1.4;

	let bounds = $derived(getDayBounds(events));
	let totalHeight = $derived((bounds.endMinutes - bounds.startMinutes) * PX_PER_MIN);
	let hours = $derived.by(() => {
		const list: number[] = [];
		for (let m = bounds.startMinutes; m <= bounds.endMinutes; m += 60) list.push(m);
		return list;
	});

	let isToday = $derived(toDateKey(day) === toDateKey(now));
	let nowMinutes = $derived(now.getHours() * 60 + now.getMinutes());
	let nowOffset = $derived((nowMinutes - bounds.startMinutes) * PX_PER_MIN);
	let showNowLine = $derived(
		isToday && nowMinutes >= bounds.startMinutes && nowMinutes <= bounds.endMinutes
	);
</script>

<div class="relative" style="height: {totalHeight}px">
	{#each hours as minutes (minutes)}
		<div class="absolute left-0 right-0 flex items-start" style="top: {(minutes - bounds.startMinutes) * PX_PER_MIN}px">
			<span class="w-10 -translate-y-1/2 text-right font-mono text-xs text-ink/40 dark:text-ink-dark/40">
				{String(Math.floor(minutes / 60)).padStart(2, '0')}h
			</span>
			<div class="ml-2 h-px flex-1 bg-lilac/30 dark:bg-lilac-dark/20"></div>
		</div>
	{/each}

	{#each events as event (event.title + event.start_time)}
		<EventBlock {event} {bounds} pxPerMin={PX_PER_MIN} />
	{/each}

	{#if showNowLine}
		<div class="absolute left-9 right-0 z-10 flex items-center gap-0" style="top: {nowOffset}px">
			<span class="pulse-dot h-2.5 w-2.5 rounded-full bg-signal"></span>
			<div class="h-0.5 flex-1 bg-signal"></div>
		</div>
	{/if}
</div>

<style>
	.pulse-dot {
		position: relative;
	}
	.pulse-dot::after {
		content: '';
		position: absolute;
		inset: -6px;
		border-radius: 9999px;
		background: var(--color-signal);
		opacity: 0.35;
		animation: pulse-ring 2s ease-out infinite;
	}
	@media (prefers-reduced-motion: reduce) {
		.pulse-dot::after {
			animation: none;
		}
	}
	@keyframes pulse-ring {
		0% {
			transform: scale(0.6);
			opacity: 0.5;
		}
		100% {
			transform: scale(1.8);
			opacity: 0;
		}
	}
</style>