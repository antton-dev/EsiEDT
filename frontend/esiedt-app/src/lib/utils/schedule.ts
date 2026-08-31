import type { ScheduleEvent } from '$lib/types';

export interface DayGroup {
	dateKey: string;
	date: Date;
	events: ScheduleEvent[];
}

export function toDateKey(date: Date): string {
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0');
	const day = String(date.getDate()).padStart(2, '0');
	return `${year}-${month}-${day}`;
}

export function groupEventsByDay(events: ScheduleEvent[]): DayGroup[] {
	const map = new Map<string, ScheduleEvent[]>();

	for (const event of events) {
		if (!event.start_time) continue;
		const date = new Date(event.start_time);
		const dateKey = toDateKey(date);

		if (!map.has(dateKey)) map.set(dateKey, []);
		map.get(dateKey)!.push(event);
	}

	const groups: DayGroup[] = Array.from(map.entries()).map(([dateKey, dayEvents]) => ({
		dateKey,
		date: new Date(dateKey),
		events: dayEvents.sort((a, b) => (a.start_time ?? '').localeCompare(b.start_time ?? ''))
	}));

	return groups.sort((a, b) => a.dateKey.localeCompare(b.dateKey));
}

export function formatTime(iso: string): string {
	return new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}

export function formatDayLabel(date: Date): string {
	return date.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
}

export function formatDayShort(date: Date): string {
	return date.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' });
}

export function formatDateTimeFull(iso: string): string {
	return new Date(iso).toLocaleDateString("fr-FR", {day: 'numeric', month: 'long', hour: '2-digit', minute:"2-digit"});
}

export function formatDateTime(iso: string): string {
	return new Date(iso).toLocaleString('fr-FR', {
		day: 'numeric',
		month: 'short',
		hour: '2-digit',
		minute: "2-digit"
	})
}

// --- Nouveau pour la frise chronologique ---

export function minutesSinceMidnight(iso: string): number {
	const d = new Date(iso);
	return d.getHours() * 60 + d.getMinutes();
}

export interface DayBounds {
	startMinutes: number;
	endMinutes: number;
}

export function getDayBounds(events: ScheduleEvent[]): DayBounds {
	let min = Infinity;
	let max = -Infinity;

	for (const event of events) {
		if (!event.start_time || !event.end_time) continue;
		min = Math.min(min, minutesSinceMidnight(event.start_time));
		max = Math.max(max, minutesSinceMidnight(event.end_time));
	}

	if (min === Infinity) return { startMinutes: 8 * 60, endMinutes: 18 * 60 };

	return {
		startMinutes: Math.floor(min / 60) * 60,
		endMinutes: Math.ceil(max / 60) * 60
	};
}