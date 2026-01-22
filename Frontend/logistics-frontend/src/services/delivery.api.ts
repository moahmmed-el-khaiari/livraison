import { http } from "./http";
import { endpoints } from "./endpoints";
import type { DeliveryTask } from "../types/models";

const api = http(endpoints.delivery);

export async function listDeliveries(): Promise<DeliveryTask[]> {
  const { data } = await api.get("/delivery/deliveries");
  return data;
}

export async function startDelivery(trackingNumber: string, payload: { lat?: number; lng?: number; city?: string }) {
  const { data } = await api.patch(`/delivery/${trackingNumber}/start`, payload);
  return data;
}

export async function failAttempt(trackingNumber: string, payload: { lat?: number; lng?: number; reason: string }) {
  const { data } = await api.patch(`/delivery/${trackingNumber}/attempt-failed`, payload);
  return data;
}

export async function completeDelivery(trackingNumber: string, payload: { lat?: number; lng?: number; city?: string; note?: string }) {
  const { data } = await api.patch(`/delivery/${trackingNumber}/complete`, payload);
  return data;
}
