import { useMutation, useQuery } from "@tanstack/react-query";
import { Alert, Button, CircularProgress, Stack, TextField, Typography } from "@mui/material";
import { listDeliveries, startDelivery, failAttempt, completeDelivery } from "../services/delivery.api";
import { queryClient } from "../app/queryClient";
import { useState } from "react";

export default function DeliveriesPage() {
  const [tracking, setTracking] = useState("");
  const [reason, setReason] = useState("Customer not available");

  const q = useQuery({ queryKey: ["deliveries"], queryFn: listDeliveries });

  const mStart = useMutation({
    mutationFn: () => startDelivery(tracking, { city: "Tanger" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["deliveries"] }),
  });
  const mFail = useMutation({
    mutationFn: () => failAttempt(tracking, { reason }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["deliveries"] }),
  });
  const mDone = useMutation({
    mutationFn: () => completeDelivery(tracking, { city: "Tanger", note: "Delivered successfully" }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["deliveries"] }),
  });

  return (
    <>
      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>Deliveries</Typography>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mb: 2 }}>
        <TextField label="Tracking number" value={tracking} onChange={(e) => setTracking(e.target.value)} fullWidth />
        <Button variant="contained" onClick={() => mStart.mutate()} disabled={!tracking}>Start</Button>
        <TextField label="Fail reason" value={reason} onChange={(e) => setReason(e.target.value)} fullWidth />
        <Button variant="outlined" onClick={() => mFail.mutate()} disabled={!tracking}>Attempt Failed</Button>
        <Button variant="contained" color="success" onClick={() => mDone.mutate()} disabled={!tracking}>Complete</Button>
      </Stack>

      {q.isLoading && <CircularProgress />}
      {q.isError && <Alert severity="error">{String((q.error as any)?.message ?? q.error)}</Alert>}

      {q.data && (
        <Stack spacing={1}>
          {q.data.map((t) => (
            <Alert key={t.id} severity="info">
              <b>{t.tracking_number}</b> — {t.status} — courier: {t.courier_id ?? "-"}
            </Alert>
          ))}
        </Stack>
      )}
    </>
  );
}
