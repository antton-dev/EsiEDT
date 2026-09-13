<script lang="ts">
	import type { ScheduleEvent } from '$lib/types';
	import { minutesSinceMidnight, formatTime, type DayBounds } from '$lib/utils/schedule';

	let {
		event,
		bounds,
		pxPerMin,
		compact = false
	}: { event: ScheduleEvent; bounds: DayBounds; pxPerMin: number; compact?: boolean } = $props();

	let top = $derived(
		event.start_time
			? (minutesSinceMidnight(event.start_time) - bounds.startMinutes) * pxPerMin
			: 0
	);
	let height = $derived(
		event.start_time && event.end_time
			? (minutesSinceMidnight(event.end_time) - minutesSinceMidnight(event.start_time)) * pxPerMin
			: 40
	);
	let blockHeight = $derived(Math.max(height - 4, 36));

	const COLUMN_THRESHOLD = 95;
	const COMPACT_THRESHOLD = 74;

	let isTiny = $derived(blockHeight < 55 || compact);
</script>

<div
	class="absolute overflow-hidden rounded-md border-l-4 border-signal bg-white shadow-sm dark:bg-surface-dark"
	class:left-14={!compact}
	class:right-2={!compact}
	class:left-1={compact}
	class:right-1={compact}
	class:p-2={isTiny}
	class:p-3={!isTiny}
	style="top: {top}px; height: {blockHeight}px"
>
	<div class="flex h-full flex-col">
		{#if compact}
			<h3 class="truncate font-display text-sm font-bold text-ink dark:text-ink-dark">
				{#if event.lesson_type}<span class="text-signal">{event.lesson_type}</span>{' '}{/if}{event.title}
			</h3>
			{#if event.start_time && event.end_time}
				<span class="shrink-0 font-mono text-xs font-medium text-signal">
					{formatTime(event.start_time)}–{formatTime(event.end_time)}
				</span>
			{/if}
		{:else}
			<div class="flex items-center justify-between gap-2">
				<h3
					class="truncate font-display font-bold text-ink dark:text-ink-dark"
					class:text-sm={isTiny}
					class:text-base={!isTiny}
				>
					{#if event.lesson_type}<span class="text-signal">{event.lesson_type}</span>{' '}{/if}{event.title}
				</h3>
				{#if event.start_time && event.end_time}
					<span class="shrink-0 font-mono text-xs font-medium text-signal">
						{formatTime(event.start_time)}–{formatTime(event.end_time)}
					</span>
				{/if}
			</div>
		{/if}

		{#if blockHeight > COLUMN_THRESHOLD}
			<div class="flex min-w-0 flex-col gap-0.5 font-body text-sm text-ink/70 dark:text-ink-dark/70">
				{#if event.location}<span class="break-words">{event.location}</span>{/if}
				{#if event.professor}<span class="break-words">{event.professor}</span>{/if}
			</div>
		{:else if blockHeight > COMPACT_THRESHOLD}
			<div class="mt-0.5 truncate font-body text-sm text-ink/70 dark:text-ink-dark/70">
				{#if event.location}<span>{event.location}</span>{/if}
				{#if event.location && event.professor}<span class="mx-1.5">•</span>{/if}
				{#if event.professor}<span>{event.professor}</span>{/if}
			</div>
		{/if}
	</div>
</div>