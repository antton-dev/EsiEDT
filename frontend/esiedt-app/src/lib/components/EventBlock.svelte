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
</script>

<div
    class="absolute left-14 right-2 overflow-hidden rounded-md border-l-4 border-signal bg-white p-3 shadow-sm"
    style="top: {top}px; height: {blockHeight}px"
>
    <div class="flex h-full flex-col">
        <div class="flex items-center justify-between gap-2">
            <h3 class="truncate font-display text-xl font-bold text-ink">{event.title}</h3>
            {#if event.start_time && event.end_time}
                <span class="shrink-0 font-mono text-sm font-medium text-signal">
                    {formatTime(event.start_time)}–{formatTime(event.end_time)}
                </span>
            {/if}
        </div>
        
        {#if blockHeight > 95}
            <!-- Mode Colonne (Par défaut, quand l'espace le permet) -->
            <div class="flex min-w-0 flex-col gap-0.5 font-body text-sm text-ink/70">
                {#if event.location}<span class="break-words">{event.location}</span>{/if}
                {#if event.professor}<span class="break-words">{event.professor}</span>{/if}
            </div>
        {:else if blockHeight > 55}
            <!-- Mode Ligne Compact (S'active pour éviter le débordement sur les cours courts) -->
            <div class="truncate mt-0.5 font-body text-sm text-ink/70">
                {#if event.location}<span>{event.location}</span>{/if}
                {#if event.location && event.professor}<span class="mx-1.5">•</span>{/if}
                {#if event.professor}<span>{event.professor}</span>{/if}
            </div>
        {/if}
    </div>
</div>