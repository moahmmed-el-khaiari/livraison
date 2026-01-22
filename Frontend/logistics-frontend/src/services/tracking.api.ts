import { http } from "./http";
import { endpoints } from "./endpoints";
import type { TrackingResponse } from "../types/models";

const api = http(endpoints.tracking);

export async function getTracking(trackingNumber: string): Promise<TrackingResponse> {
  const { data } = await api.get(`/tracking/${trackingNumber}`);
  return data;
}

export async function addTrackingEvent(payload: {
  tracking_number: string;
  status: string;
  source?: string;
  city?: string;
  message?: string;
  lat?: number;
  lng?: number;
}) {
  const { data } = await api.post("/tracking/events", payload);
  return data;
}
