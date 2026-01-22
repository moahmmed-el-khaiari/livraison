import { useMemo, useState } from "react";
import {
  Alert,
  Button,
  CircularProgress,
  MenuItem,
  Paper,
  Stack,
  TextField,
  Typography,
  Divider,
} from "@mui/material";
import { useMutation, useQuery } from "@tanstack/react-query";
import { queryClient } from "../app/queryClient";
import {
  getOrderByNumber,
  listOrders,
  updateOrderStatus,
} from "../services/orders.api";

const STATUS_OPTIONS = [
  "CREATED",
  "SHIPMENT_CREATED",
  "TRACKING_INIT_FAILED",
  "CANCELLED",
  "FAILED",
];

export default function OrdersPage() {
  const [orderNumber, setOrderNumber] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("CANCELLED");

  // LIST
  const qList = useQuery({
    queryKey: ["orders"],
    queryFn: listOrders,
  });

  // GET ONE (manual)
  const [one, setOne] = useState<any | null>(null);
  const [oneError, setOneError] = useState<string>("");

  const mGetOne = useMutation({
    mutationFn: async () => getOrderByNumber(orderNumber.trim()),
    onSuccess: (data) => {
      setOneError("");
      setOne(data);
    },
    onError: (e: any) => {
      setOne(null);
      setOneError(String(e?.message ?? e));
    },
  });

  // UPDATE STATUS
  const mUpdate = useMutation({
    mutationFn: async () =>
      updateOrderStatus(orderNumber.trim(), selectedStatus),
    onSuccess: (data) => {
      setOne(data);
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });

  const isBusy = mGetOne.isPending || mUpdate.isPending;

  const smallOrderLine = useMemo(() => {
    if (!one) return null;
    return `orderNumber=${one.order_number ?? one.orderNumber ?? "-"} | status=${
      one.status ?? "-"
    } | tracking=${one.tracking_number ?? one.trackingNumber ?? "-"}`;
  }, [one]);

  return (
    <>
      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>
        Orders
      </Typography>

      <Paper variant="outlined" sx={{ p: 2, borderRadius: 3, mb: 2 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={1}>
          <TextField
            label="Order number"
            value={orderNumber}
            onChange={(e) => setOrderNumber(e.target.value)}
            fullWidth
          />

          <Button
            variant="contained"
            onClick={() => mGetOne.mutate()}
            disabled={!orderNumber.trim() || isBusy}
          >
            {mGetOne.isPending ? "Searching..." : "Search"}
          </Button>

          <TextField
            select
            label="New status"
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            sx={{ minWidth: 220 }}
          >
            {STATUS_OPTIONS.map((s) => (
              <MenuItem key={s} value={s}>
                {s}
              </MenuItem>
            ))}
          </TextField>

          <Button
            variant="outlined"
            onClick={() => mUpdate.mutate()}
            disabled={!orderNumber.trim() || isBusy}
          >
            {mUpdate.isPending ? "Updating..." : "Update Status"}
          </Button>
        </Stack>

        <Divider sx={{ my: 2 }} />

        {oneError && <Alert severity="error">{oneError}</Alert>}

        {mUpdate.isError && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {String((mUpdate.error as any)?.message ?? mUpdate.error)}
          </Alert>
        )}

        {one && (
          <Alert severity="success" sx={{ mt: 1 }}>
            {smallOrderLine}
          </Alert>
        )}
      </Paper>

      <Paper variant="outlined" sx={{ p: 2, borderRadius: 3 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h6" sx={{ fontWeight: 800 }}>
            Orders list
          </Typography>
          {qList.isLoading && <CircularProgress size={18} />}
        </Stack>

        {qList.isError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {String((qList.error as any)?.message ?? qList.error)}
          </Alert>
        )}

        {qList.data && Array.isArray(qList.data) && (
          <Stack spacing={1} sx={{ mt: 2 }}>
            {qList.data.map((o: any) => (
              <Alert key={o.id ?? o.orderNumber ?? o.order_number} severity="info">
                <b>{o.order_number ?? o.orderNumber}</b> — {o.status} — tracking:{" "}
                {o.tracking_number ?? o.trackingNumber ?? "-"}
              </Alert>
            ))}
          </Stack>
        )}
      </Paper>
    </>
  );
}
