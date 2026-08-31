import type { ScheduleResponse, SearchResponse, GroupsResponse, MaintenanceResponse } from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function apiFetch<T>(path: string): Promise<T> {
    const res = await fetch(`${BASE_URL}${path}`);

    if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail ?? `Erreur API ${res.status}`);
    }

    return res.json()
}



export function fetchGroups(): Promise<GroupsResponse> {
    return apiFetch('/api/groups');
}

export function searchResources(query: string): Promise<SearchResponse> {
    return apiFetch(`/api/search?q=${encodeURIComponent(query)}`);
}

export function fetchSchedule(resourceId: string): Promise<ScheduleResponse> {
    return apiFetch(`/api/schedule/${resourceId}`);
}

export function fetchMaintenance() : Promise<MaintenanceResponse> {
    return apiFetch("/api/maintenance")
}