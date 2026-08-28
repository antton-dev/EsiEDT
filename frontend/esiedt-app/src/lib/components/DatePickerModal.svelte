<script lang="ts">
	import { DatePicker } from 'date-picker-svelte';
	import { toDateKey, type DayGroup } from '$lib/utils/schedule';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faXmark } from '@fortawesome/free-solid-svg-icons';

	let {
		open = $bindable(false),
		days,
		onselect
	}: { open?: boolean; days: DayGroup[]; onselect: (key: string) => void } = $props();

	let dialogEl: HTMLDialogElement;
	let availableKeys = $derived(new Set(days.map((d) => d.dateKey)));
	let pickedDate = $state(new Date());

	$effect(() => {
		if (open) dialogEl?.showModal();
		else dialogEl?.close();
	});

	function isDisabledDate(date: Date): boolean {
		const disabled = !availableKeys.has(toDateKey(date));
        return disabled;
	}

	function confirm() {
        const key = toDateKey(pickedDate);
		if (availableKeys.has(key)) {
			onselect(key);
			open = false;
		}
	}

	// Déclenché par <dialog> lui-même : Échap, ou fermeture programmatique
	function handleClose() {
		open = false;
	}

	// Clic sur le fond (le <dialog> couvre tout l'espace ; un clic hors du contenu = sur le <dialog> lui-même)
	function handleBackdropClick(e: MouseEvent) {
		if (e.target === dialogEl) open = false;
	}
</script>

<dialog
	bind:this={dialogEl}
	onclose={handleClose}
	onclick={handleBackdropClick}
	class="m-auto w-full max-w-sm rounded-2xl bg-white p-4 pb-6 shadow-lg backdrop:bg-ink/40 backdrop:backdrop-blur-sm"
>
	<div class="mb-3 flex items-center justify-between">
		<h2 class="font-display text-lg font-bold text-ink">Choisir une date</h2>
		<button
			onclick={() => (open = false)}
			aria-label="Fermer"
			class="flex h-8 w-8 items-center justify-center rounded-full text-ink/50 active:bg-lilac/30"
		>
        <FontAwesomeIcon icon={faXmark} />
        </button>
	</div>

	<div class="flex justify-center">
		<DatePicker bind:value={pickedDate} />
	</div>

	<button
		onclick={confirm}
		disabled={isDisabledDate(pickedDate)}
		class="mt-4 w-full rounded-lg bg-signal px-4 py-2.5 text-sm font-semibold text-mist shadow-sm transition active:bg-ink disabled:cursor-not-allowed disabled:bg-lilac/40 disabled:text-ink/40"
	>
		Voir ce jour
	</button>
	{#if isDisabledDate(pickedDate)}
		<p class="mt-2 text-center text-xs text-ink/40">Pas de cours ce jour-là</p>
	{/if}
</dialog>
