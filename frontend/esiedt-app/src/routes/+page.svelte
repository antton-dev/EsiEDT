<script lang="ts">
	import { onMount } from 'svelte';
	import CategoryScreen from '$lib/components/CategoryScreen.svelte';
	import GroupScreen from '$lib/components/GroupScreen.svelte';
	import ScheduleView from '$lib/components/ScheduleView.svelte';
	import { groupStore, clearGroup, selectGroup } from '$lib/stores/selectedGroup.svelte';
	import { fetchGroups } from '$lib/api';
	import type { ResourceGroup } from '$lib/types';

	let view = $state<'category' | 'group'>('category');
	let categoriesData = $state<Record<string, ResourceGroup[]>>({});
	let selectedCategory = $state<string | null>(null);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		try {
			const data = await fetchGroups();
			categoriesData = data.data;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Erreur de chargement';
		} finally {
			loading = false;
		}
	});

	function openCategory(name: string) {
		selectedCategory = name;
		view = 'group';
	}

	function backToCategories() {
		view = 'category';
		selectedCategory = null;
	}

	function pickGroup(group: ResourceGroup) {
		selectGroup({ id: group.id, name: group.full_name });
	}
</script>

{#if groupStore.current}
	<div class="flex items-center justify-between bg-mist p-4 pb-0">
		<h1 class="font-display text-lg font-bold text-ink">{groupStore.current.name}</h1>
		<button onclick={clearGroup} class="text-sm font-semibold text-signal">Changer</button>
	</div>
	{#key groupStore.current.id}
		<ScheduleView resourceId={groupStore.current.id} />
	{/key}
{:else if loading}
	<div class="flex min-h-screen items-center justify-center bg-mist">
		<p class="font-body text-ink/60">Chargement des promos...</p>
	</div>
{:else if error}
	<div class="flex min-h-screen items-center justify-center bg-mist p-4">
		<p class="text-coral">{error}</p>
	</div>
{:else if view === 'category'}
	<CategoryScreen categories={Object.keys(categoriesData)} onselect={openCategory} />
{:else if selectedCategory}
	<GroupScreen
		categoryName={selectedCategory}
		groups={categoriesData[selectedCategory]}
		onselect={pickGroup}
		onback={backToCategories}
	/>
{/if}