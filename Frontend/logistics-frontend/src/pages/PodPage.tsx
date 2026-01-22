import { useState } from "react";
import { Button, TextField, Typography, Alert } from "@mui/material";
import { getPod } from "../services/pod.api";

export default function PodPage() {
  const [tracking, setTracking] = useState("");
  const [pod, setPod] = useState<any>(null);

  const search = async () => {
    const res = await getPod(tracking);
    setPod(res);
  };

  return (
    <>
      <Typography variant="h5" fontWeight={800} mb={2}>
        Proof Of Delivery
      </Typography>

      <TextField
        label="Tracking number"
        value={tracking}
        onChange={(e) => setTracking(e.target.value)}
        sx={{ mr: 2 }}
      />

      <Button variant="contained" onClick={search}>
        Search
      </Button>

      {pod && (
        <Alert severity="info" sx={{ mt: 2 }}>
          Receiver: {pod.receiver_name}
        </Alert>
      )}
    </>
  );
}
