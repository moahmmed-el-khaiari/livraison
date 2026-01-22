import { http } from "./http";
import { endpoints } from "./endpoints";

const api = http(endpoints.order);

export type ApiErrorResponse = {
  timestamp?: string;
  status?: number;
  error?: string;
  message?: string;
  path?: string;
};

// helper pour récupérer message (Spring ErrorResponse)
function extractErrorMessage(err: any): string {
  const data: ApiErrorResponse | undefined = err?.response?.data;
  if (data?.message) return data.message;
  if (typeof err?.message === "string") return err.message;
  return "Request failed";
}

// ===== LIST =====
export async function listOrders() {
  try {
    const { data } = await api.get("/api/orders");
    return data;
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}

// ===== GET ONE =====
export async function getOrderByNumber(orderNumber: string) {
  try {
    const { data } = await api.get(`/api/orders/${orderNumber}`);
    return data;
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}

// ===== CREATE =====
// ⚠️ le type exact dépend de ton CreateOrderRequest (je garde "any" pour ne pas te bloquer)
export async function createOrder(payload: any) {
  try {
    const { data } = await api.post("/api/orders", payload);
    return data;
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}

// ===== UPDATE STATUS =====
export async function updateOrderStatus(orderNumber: string, status: string) {
  try {
    const { data } = await api.patch(`/api/orders/${orderNumber}/status`, { status });
    return data;
  } catch (e: any) {
    throw new Error(extractErrorMessage(e));
  }
}
