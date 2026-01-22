import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Alert, Button, CircularProgress, Stack, TextField, Typography } from "@mui/material";
import { getTracking } from "../services/tracking.api";

export default function TrackingPage() {
  const [tracking, setTracking] = useState("");
  const [go, setGo] = useState<string | null>(null);

  const q = useQuery({
    queryKey: ["tracking", go],
    queryFn: () => getTracking(go!),
    enabled: !!go,
  });

  return (
    <>
      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>Tracking</Typography>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mb: 2 }}>
        <TextField label="Tracking number" value={tracking} onChange={(e) => setTracking(e.target.value)} fullWidth />
        <Button variant="contained" onClick={() => setGo(tracking)} disabled={!tracking}>Search</Button>
      </Stack>

      {q.isLoading && <CircularProgress />}
      {q.isError && <Alert severity="error">{String((q.error as any)?.message ?? q.error)}</Alert>}

      {q.data && (
        <Stack spacing={1}>
          <Alert severity="success">
            Latest: <b>{q.data.latest_status ?? q.data.status ?? "UNKNOWN"}</b>
          </Alert>
          {(q.data.events ?? []).map((ev) => (
            <Alert key={ev.id} severity="info">
              <b>{ev.status}</b> — {ev.source} — {ev.city ?? "-"} — {ev.message ?? "-"} — {ev.event_time}
            </Alert>
          ))}
        </Stack>
      )}
    </>
  );
}
