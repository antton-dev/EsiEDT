<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchMaintenance } from '$lib/api';
	import { formatDateTime, formatTime, formatDateTimeFull } from '$lib/utils/schedule';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';

	const HIDE_AFTER_HRS = 2;
	let announcement = $state<{ starts_at: string; ends_at: string } | null>(null);

	onMount(async () => {
		try {
			const data = await fetchMaintenance();
			if (!data.announcement) return;
			
			const ends_at = new Date(data.announcement.ends_at);
			const starts_at = new Date(data.announcement.starts_at);

			const hideAfter = new Date(ends_at.getTime() + HIDE_AFTER_HRS*60*60*1000);

			if (new Date() >= hideAfter) return;

			announcement = data.announcement;
			
		} catch {
			// non bloquant
		}
	});

	let isOnGoing = $derived.by(() => {
		if (!announcement) return false;
		const now = new Date();
		return now >= new Date(announcement.starts_at) && now < new Date(announcement.ends_at)
	});
</script>

{#if announcement}
	<div
		class="flex items-start gap-2 border-b border-coral/30 bg-coral/10 px-4 py-2.5 text-sm text-coral dark:bg-coral/15"
	>
		<FontAwesomeIcon icon={faTriangleExclamation} class="mt-0.5 shrink-0" />
		<p>
			{#if isOnGoing}
				<span class="font-bold">Maintenance en cours</span>. Le site peut subir des perturbations ou des interruptions. Fin estimée : <span class="font-mono">{formatDateTimeFull(announcement.ends_at)} </span>
			{:else}
			Maintenance prévue entre le <span class="font-mono"> {formatDateTimeFull(announcement.starts_at)}</span>
			et <span class="font-mono">{formatDateTimeFull(announcement.ends_at)}</span>. EsiEDT pourra être
			inaccessible pendant cette période.
			{/if}
		</p>
	</div>
{/if}