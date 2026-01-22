import { http } from "./http";
import { endpoints } from "./endpoints";
import type { DashboardReport } from "../types/models";

const api = http(endpoints.reporting);

export async function getDashboard(): Promise<DashboardReport> {
  const { data } = await api.get("/reports/dashboard");
  return data;
}
