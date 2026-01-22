import { http } from "./http";
import { endpoints } from "./endpoints";
import type { Pod } from "../types/models";

const api = http(endpoints.pod);

export async function createPod(payload: {
  tracking_number: string;
  receiver_name: string;
  receiver_id_number?: string;
  signature_base64?: string;
  photo_url?: string;
  note?: string;
}): Promise<Pod> {
  const { data } = await api.post("/pod", payload);
  return data;
}

export async function getPod(trackingNumber: string): Promise<Pod> {
  const { data } = await api.get(`/pod/${trackingNumber}`);
  return data;
}

export async function listPods(): Promise<Pod[]> {
  const { data } = await api.get("/pod/pods");
  return data;
}
