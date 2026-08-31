export interface ScheduleEvent {
    title: string;
    location: string;
    professor: string;
    start_time: string | null;
    end_time: string | null;
}

export interface ScheduleResponse {
    status: string;
    resource_id: string;
    total_events: number;
    fetched_at: string;
    events: ScheduleEvent[];
}

export interface SearchResult {
    name: string;
    id: string;
}

export interface SearchResponse {
    status: string;
    query: string;
    total_results: number;
    results: SearchResult[];
}

export interface ResourceGroup {
    full_name: string;
    short_name: string;
    id: string;
}

export interface GroupsResponse {
    status: string;
    categories_count: number;
    data: Record<string, ResourceGroup[]>;
}

export interface MaintenanceAnnouncement {
    starts_at: string;
    ends_at: string;
}


export interface MaintenanceResponse {
    announcement: MaintenanceAnnouncement | null;
}