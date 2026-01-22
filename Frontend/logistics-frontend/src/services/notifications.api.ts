import { http } from "./http";
import { endpoints } from "./endpoints";

const api = http(endpoints.notifications);

export type NotificationOut = {
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

export type NotificationEventIn = {
  event_type: string;
  channel?: string;
  recipient?: string | null;
  tracking_number?: string | null;
  order_id?: string | null;
  title: string;
  message: string;
};

function extractErrorMessage(err: any): string {
  const data = err?.response?.data;
  if (typeof data?.detail === "string") return data.detail; // FastAPI
  if (typeof data?.message === "string") return data.message;
  if (typeof err?.message === "string") return err.message;
  return "Request failed";
}

// ✅ Normalizer: accepte {items:[...]} OU [...] OU {data:{items:[...]}}
function normalizeList(payload: any): NotificationOut[] {
  if (!payload) return [];
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload.items)) return payload.items;
  if (payload.data && Array.isArray(payload.data.items)) return payload.data.items;
  return [];
}

export async function listNotificationsByTracking(trackingNumber: string, limit = 50): Promise<NotificationOut[]> {
  try {
    const { data } = await api.get(`/notifications/tracking/${encodeURIComponent(trackingNumber)}`, {
      params: { limit },
    });
    return normalizeList(data);
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}

export async function listNotificationsByRecipient(recipient: string, limit = 50): Promise<NotificationOut[]> {
  try {
    const { data } = await api.get(`/notifications/recipient/${encodeURIComponent(recipient)}`, {
      params: { limit },
    });
    return normalizeList(data);
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}

export async function sendNotificationEvent(payload: NotificationEventIn): Promise<NotificationOut> {
  try {
    const { data } = await api.post(`/notifications/events`, payload);
    return data as NotificationOut;
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}
