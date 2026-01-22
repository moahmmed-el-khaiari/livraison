export type DashboardReport = {
  generated_at: string;
  orders: { total: number; by_status: Record<string, number> };
  deliveries: { total: number; by_status: Record<string, number> };
  tracking: { total_events: number; latest_status_count: Record<string, number> };
  pods?: { total: number } | null;
};

export type DeliveryTask = {
  id: string;
  tracking_number: string;
  status: string;
  courier_id?: string | null;
  last_lat?: number | null;
  last_lng?: number | null;
  note?: string | null;
  created_at: string;
  updated_at: string;
};

export type TrackingResponse = {
  tracking_number: string;
  latest_status?: string;
  status?: string;
  events?: Array<{
    id: string;
    tracking_number: string;
    status: string;
    source: string;
    city?: string | null;
    message?: string | null;
    lat?: number | null;
    lng?: number | null;
    event_time: string;
  }>;
};

export type Pod = {
  id: string;
  tracking_number: string;
  receiver_name: string;
  receiver_id_number?: string | null;
  signature_base64?: string | null;
  photo_url?: string | null;
  note?: string | null;
  created_at: string;
};

export type NotificationItem = {
  id: string;
  event_type: string;
  channel: string;
  recipient?: string | null;
  tracking_number?: string | null;
  order_id?: string | null;
  title: string;
  message: string;
  status: string;
  sent: boolean;
  created_at: string;
  sent_at?: string | null;
};
