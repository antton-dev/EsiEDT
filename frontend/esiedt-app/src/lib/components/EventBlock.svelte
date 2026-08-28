<script lang="ts">
	import type { ScheduleEvent } from '$lib/types';
	import { minutesSinceMidnight, formatTime, type DayBounds } from '$lib/utils/schedule';

	let {
		event,
		bounds,
		pxPerMin
	}: { event: ScheduleEvent; bounds: DayBounds; pxPerMin: number } = $props();

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

	// Seuils calculés à partir du rendu réel (padding + hauteurs de ligne), pas ajustés à l'œil :
	// Colonne (titre + 2 lignes empilées) : 24 (padding) + 28 (titre) + 2 (gap) + 20 + 20 (2 lignes) = 94px
	// Ligne compacte (titre + 1 ligne) : 24 (padding) + 28 (titre) + 2 (gap) + 20 (1 ligne) = 74px
	// En dessous : uniquement le titre, pas assez de place pour salle/prof sans les couper
	const COLUMN_THRESHOLD = 95;
	const COMPACT_THRESHOLD = 74;

	let isTiny = $derived(blockHeight < 55);
</script>

<div
	class="absolute left-14 right-2 overflow-hidden rounded-md border-l-4 border-signal bg-white shadow-sm dark:bg-surface-dark"
	class:p-2={isTiny}
	class:p-3={!isTiny}
	style="top: {top}px; height: {blockHeight}px"
>
	<div class="flex h-full flex-col">
		<div class="flex items-center justify-between gap-2">
			<h3
				class="truncate font-display font-bold text-ink dark:text-ink-dark"
				class:text-sm={isTiny}
				class:text-base={!isTiny}
			>
				{event.title}
			</h3>
			{#if event.start_time && event.end_time}
				<span class="shrink-0 font-mono text-xs font-medium text-signal">
					{formatTime(event.start_time)}–{formatTime(event.end_time)}
				</span>
			{/if}
		</div>

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