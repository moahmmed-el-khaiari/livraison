import { useMemo, useState } from "react";
import {
  Alert,
  Button,
  Chip,
  Divider,
  MenuItem,
  Paper,
  Stack,
  TextField,
  Typography,
  CircularProgress,
} from "@mui/material";
import { useMutation } from "@tanstack/react-query";
import {
  listNotificationsByRecipient,
  listNotificationsByTracking,
  sendNotificationEvent,
} 
from "../services/notifications.api";
import type { NotificationOut } from "../services/notifications.api";

type Mode = "recipient" | "tracking";

const CHANNELS = ["IN_APP", "EMAIL", "SMS", "PUSH"];
const EVENT_TYPES = ["ORDER_CREATED", "PICKED_UP", "IN_TRANSIT", "OUT_FOR_DELIVERY", "DELIVERED", "EXCEPTION"];

function StatusChip({ n }: { n: NotificationOut }) {
  const label = n.sent ? "SENT" : n.status || "PENDING";
  return <Chip size="small" label={label} />;
}

export default function NotificationsPage() {
  const [mode, setMode] = useState<Mode>("recipient");
  const [q, setQ] = useState("me");
  const [limit, setLimit] = useState(50);

  // create event form
  const [recipient, setRecipient] = useState("me");
  const [trackingNumber, setTrackingNumber] = useState("");
  const [orderId, setOrderId] = useState("");
  const [channel, setChannel] = useState("IN_APP");
  const [eventType, setEventType] = useState("ORDER_CREATED");
  const [title, setTitle] = useState("New update");
  const [message, setMessage] = useState("Your shipment status has been updated.");

  const [items, setItems] = useState<NotificationOut[]>([]);
  const [error, setError] = useState<string>("");

  const mSearch = useMutation({
  mutationFn: async () => {
    const value = q.trim();
    if (!value) throw new Error("Value is required");
    if (mode === "tracking") {
      return await listNotificationsByTracking(value, limit); // ✅ array
    }
    return await listNotificationsByRecipient(value, limit); // ✅ array
  },
  onSuccess: (data) => {
    setError("");
    setItems(data ?? []);
  },
  onError: (e: any) => {
    setItems([]);
    setError(String(e?.message ?? e));
  },
});

  const mSend = useMutation({
    mutationFn: async () =>
      sendNotificationEvent({
        event_type: eventType,
        channel,
        recipient: recipient.trim() || undefined,
        tracking_number: trackingNumber.trim() || undefined,
        order_id: orderId.trim() || undefined,
        title: title.trim(),
        message: message.trim(),
      }),
    onSuccess: (created) => {
      // prepend in list
      setItems((prev) => [created, ...prev]);
    },
  });

  const busy = mSearch.isPending || mSend.isPending;

  const headerLabel = useMemo(() => {
    return mode === "tracking" ? "Search by tracking number" : "Search by recipient";
  }, [mode]);

  return (
    <>
      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>
        Notifications
      </Typography>

      <Paper variant="outlined" sx={{ p: 2, borderRadius: 3, mb: 2 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 800, mb: 1 }}>
          Search
        </Typography>

        <Stack direction={{ xs: "column", md: "row" }} spacing={1}>
          <TextField
            select
            label="Mode"
            value={mode}
            onChange={(e) => setMode(e.target.value as Mode)}
            sx={{ minWidth: 220 }}
          >
            <MenuItem value="recipient">Recipient</MenuItem>
            <MenuItem value="tracking">Tracking</MenuItem>
          </TextField>

          <TextField
            label={headerLabel}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            fullWidth
          />

          <TextField
            label="Limit"
            type="number"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value || 50))}
            sx={{ width: 140 }}
            inputProps={{ min: 1, max: 200 }}
          />

          <Button variant="contained" onClick={() => mSearch.mutate()} disabled={busy || !q.trim()}>
            {mSearch.isPending ? "Searching..." : "Search"}
          </Button>
        </Stack>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      <Paper variant="outlined" sx={{ p: 2, borderRadius: 3, mb: 2 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 800, mb: 1 }}>
          Create Notification Event
        </Typography>

        <Stack spacing={1}>
          <Stack direction={{ xs: "column", md: "row" }} spacing={1}>
            <TextField
              select
              label="Event type"
              value={eventType}
              onChange={(e) => setEventType(e.target.value)}
              sx={{ minWidth: 240 }}
            >
              {EVENT_TYPES.map((x) => (
                <MenuItem key={x} value={x}>
                  {x}
                </MenuItem>
              ))}
            </TextField>

            <TextField
              select
              label="Channel"
              value={channel}
              onChange={(e) => setChannel(e.target.value)}
              sx={{ minWidth: 180 }}
            >
              {CHANNELS.map((x) => (
                <MenuItem key={x} value={x}>
                  {x}
                </MenuItem>
              ))}
            </TextField>

            <TextField
              label="Recipient"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              fullWidth
            />
          </Stack>

          <Stack direction={{ xs: "column", md: "row" }} spacing={1}>
            <TextField
              label="Tracking number (optional)"
              value={trackingNumber}
              onChange={(e) => setTrackingNumber(e.target.value)}
              fullWidth
            />
            <TextField
              label="Order id (optional)"
              value={orderId}
              onChange={(e) => setOrderId(e.target.value)}
              fullWidth
            />
          </Stack>

          <TextField label="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
          <TextField
            label="Message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            multiline
            minRows={3}
          />

          <Button variant="outlined" onClick={() => mSend.mutate()} disabled={busy || !title.trim() || !message.trim()}>
            {mSend.isPending ? "Sending..." : "Send Event"}
          </Button>

          {mSend.isError && (
            <Alert severity="error">{String((mSend.error as any)?.message ?? mSend.error)}</Alert>
          )}
          {mSend.isSuccess && (
            <Alert severity="success">Event created (201)</Alert>
          )}
        </Stack>
      </Paper>

      <Paper variant="outlined" sx={{ p: 2, borderRadius: 3 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h6" sx={{ fontWeight: 800 }}>
            Results
          </Typography>
          {busy && <CircularProgress size={18} />}
        </Stack>

        <Divider sx={{ my: 2 }} />

        {items.length === 0 ? (
          <Alert severity="info">No notifications loaded yet.</Alert>
        ) : (
          <Stack spacing={1}>
            {items.map((n) => (
              <Paper key={n.id} variant="outlined" sx={{ p: 1.5, borderRadius: 2 }}>
                <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={1}>
                  <Typography sx={{ fontWeight: 800 }}>{n.title}</Typography>
                  <StatusChip n={n} />
                </Stack>

                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                  {n.event_type} • {n.channel} • {n.created_at}
                </Typography>

                <Typography sx={{ mt: 1 }}>{n.message}</Typography>

                <Stack direction="row" spacing={1} sx={{ mt: 1, flexWrap: "wrap" }}>
                  {n.recipient && <Chip size="small" label={`recipient: ${n.recipient}`} />}
                  {n.tracking_number && <Chip size="small" label={`tracking: ${n.tracking_number}`} />}
                  {n.order_id && <Chip size="small" label={`order: ${n.order_id}`} />}
                </Stack>
              </Paper>
            ))}
          </Stack>
        )}
      </Paper>
    </>
  );
}
