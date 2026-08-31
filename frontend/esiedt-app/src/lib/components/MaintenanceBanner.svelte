<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchMaintenance } from '$lib/api';
	import { formatDateTime, formatTime, formatDateTimeFull } from '$lib/utils/schedule';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';

	let announcement = $state<{ starts_at: string; ends_at: string } | null>(null);

	onMount(async () => {
		try {
			const data = await fetchMaintenance();
			if (data.announcement) {
				announcement = data.announcement;
			}
		} catch {
			// Si cet appel échoue, on ignore silencieusement — pas la peine de bloquer
			// l'affichage du reste de l'app pour une bannière d'info non critique.
		}
	});
</script>

{#if announcement}
	<div
		class="flex items-start gap-2 border-b border-coral/30 bg-coral/10 px-4 py-2.5 text-sm text-coral dark:bg-coral/15"
	>
		<FontAwesomeIcon icon={faTriangleExclamation} class="mt-0.5 shrink-0" />
		<p>
			Maintenance prévue entre le <span class="font-mono">{formatDateTimeFull(announcement.starts_at)}</span>
			et <span class="font-mono">{formatDateTimeFull(announcement.ends_at)}</span>. EsiEDT pourra être
			inaccessible pendant cette période.
		</p>
	</div>
{/if}