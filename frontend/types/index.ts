export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Monitor {
  id: string;
  user_id: string;
  name: string;
  url: string;
  interval: number;
  timeout: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_status: 'UP' | 'DOWN' | 'UNKNOWN';
  last_response_time: number | null;
  last_checked_at: string | null;
}

export interface HealthCheck {
  id: string;
  monitor_id: string;
  status: 'UP' | 'DOWN';
  status_code: number | null;
  response_time: number;
  error_message: string | null;
  checked_at: string;
}

export interface Incident {
  id: string;
  monitor_id: string;
  started_at: string;
  resolved_at: string | null;
  reason: string;
}

export interface DashboardSummary {
  total_monitors: number;
  up_monitors: number;
  down_monitors: number;
  paused_monitors: number;
  overall_uptime_percentage: number;
  monitors: Monitor[];
}

export interface MonitorDetailResponse {
  monitor: Monitor;
  uptime_percentage: number;
  recent_checks: HealthCheck[];
  incidents: Incident[];
}
