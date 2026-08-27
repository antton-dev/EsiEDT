<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { dev } from '$app/environment';
	import { fetchSchedule } from '$lib/api';
	import { groupEventsByDay, formatDayLabel, toDateKey, type DayGroup } from '$lib/utils/schedule';
	import DayNavigator from './DayNavigator.svelte';
	import DayTimeline from './DayTimeline.svelte';

	let { resourceId }: { resourceId: string } = $props();

	let days = $state<DayGroup[]>([]);
	let selectedKey = $state('');
	let loading = $state(true);
	let error = $state('');
	let now = $state(new Date());
	let nowTimer: ReturnType<typeof setInterval>;

	onMount(() => {
		load();
		const debugDate = dev ? new URLSearchParams(window.location.search).get('debugDate') : null;
		if (!debugDate) {
			nowTimer = setInterval(() => (now = new Date()), 60_000);
		}
	});

	onDestroy(() => clearInterval(nowTimer));

	function selectClosestToToday() {
		const todayKey = toDateKey(now);
		const upcoming = days.find((d) => d.dateKey >= todayKey);
		selectedKey = upcoming ? upcoming.dateKey : (days[0]?.dateKey ?? '');
	}

	async function load() {
		loading = true;
		error = '';
		try {
			const data = await fetchSchedule(resourceId);
			days = groupEventsByDay(data.events);

			const debugDate = dev ? new URLSearchParams(window.location.search).get('debugDate') : null;
			now = debugDate ? new Date(debugDate) : new Date();

			selectClosestToToday();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Erreur de chargement';
		} finally {
			loading = false;
		}
	}

	let selectedDay = $derived(days.find((d) => d.dateKey === selectedKey));
	let selectedIndex = $derived(days.findIndex((d) => d.dateKey === selectedKey));
	let isOnToday = $derived(selectedKey === toDateKey(now));

	function goToPreviousDay() {
		if (selectedIndex > 0) selectedKey = days[selectedIndex - 1].dateKey;
	}
	function goToNextDay() {
		if (selectedIndex >= 0 && selectedIndex < days.length - 1)
			selectedKey = days[selectedIndex + 1].dateKey;
	}
</script>

{#if loading}
	<p class="p-4 font-body text-ink/60">Chargement de l'emploi du temps...</p>
{:else if error}
	<div class="p-4">
		<p class="text-coral">{error}</p>
		<button onclick={load} class="mt-2 text-sm font-semibold text-signal">Réessayer</button>
	</div>
{:else if days.length === 0}
	<p class="p-4 font-body text-ink/60">Aucun cours trouvé.</p>
{:else}
	<DayNavigator {days} {selectedKey} onselect={(key) => (selectedKey = key)} />

	{#if selectedDay}
		<div class="px-4 pb-24 pt-2">
			<h2 class="mb-3 font-display text-sm font-semibold uppercase tracking-wide text-ink/50">
				{formatDayLabel(selectedDay.date)}
			</h2>
			<DayTimeline events={selectedDay.events} day={selectedDay.date} {now} />
		</div>

		<div class="fixed inset-x-0 bottom-0 border-t border-lilac/30 bg-white/95 p-4 backdrop-blur">
			<div class="mx-auto flex max-w-md items-center gap-3">
				<button
					onclick={goToPreviousDay}
					disabled={selectedIndex <= 0}
					class="flex-1 rounded-lg bg-signal px-4 py-2.5 text-sm font-semibold text-mist shadow-sm transition active:bg-ink disabled:cursor-not-allowed disabled:bg-lilac/40 disabled:text-ink/40 disabled:shadow-none"
				>
					← Précédent
				</button>
				<button
					onclick={selectClosestToToday}
					disabled={isOnToday}
					aria-label="Revenir à aujourd'hui"
					class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border-2 border-signal font-display text-xs font-bold text-signal transition active:bg-signal active:text-mist disabled:cursor-not-allowed disabled:border-lilac/40 disabled:text-ink/30"
				>
					Auj.
				</button>
				<button
					onclick={goToNextDay}
					disabled={selectedIndex >= days.length - 1}
					class="flex-1 rounded-lg bg-signal px-4 py-2.5 text-sm font-semibold text-mist shadow-sm transition active:bg-ink disabled:cursor-not-allowed disabled:bg-lilac/40 disabled:text-ink/40 disabled:shadow-none"
				>
					Suivant →
				</button>
			</div>
		</div>
	{/if}
{/if}