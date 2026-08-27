<script lang="ts">
	import type { ScheduleEvent } from '$lib/types';
	import { formatTime } from '$lib/utils/schedule';

	let { event }: { event: ScheduleEvent } = $props();
</script>

<div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
	<div class="flex items-baseline justify-between gap-2">
		<h3 class="font-medium text-gray-900">{event.title}</h3>
		{#if event.start_time && event.end_time}
			<span class="whitespace-nowrap text-sm text-gray-500">
				{formatTime(event.start_time)} – {formatTime(event.end_time)}
			</span>
		{/if}
	</div>
	<div class="mt-1 flex flex-col text-sm text-gray-500">
		{#if event.location}
			<span>{event.location}</span>
		{/if}
		{#if event.professor}
			<span>{event.professor}</span>
		{/if}
	</div>
</div>