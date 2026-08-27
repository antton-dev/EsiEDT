<script lang="ts">
	let { compact = false }: { compact?: boolean } = $props();
</script>

<footer
	class="mt-8 border-t border-lilac/30 px-4 pt-4 text-center font-body text-xs text-ink/40"
	class:pb-28={compact}
	class:pb-6={!compact}
>
	<p>Données ADE mises en cache toutes les 2h</p>
	<p class="mt-0.5">Fait par <a href="https://anttonc.fr" target="_blank" rel="noopener noreferrer" class="font-semibold text-signal underline decoration-signal/30 underline-offset-2">anttonc.fr</a></p>
</footer>