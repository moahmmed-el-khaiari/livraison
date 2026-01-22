import { useQuery } from "@tanstack/react-query";
import { Grid, Typography, Alert, CircularProgress } from "@mui/material";
import { getDashboard } from "../services/reporting.api";
import StatCard from "../component/StatCard";

export default function DashboardPage() {
  const q = useQuery({ queryKey: ["dashboard"], queryFn: getDashboard });

  if (q.isLoading) return <CircularProgress />;
  if (q.isError) return <Alert severity="error">Erreur: {String((q.error as any)?.message ?? q.error)}</Alert>;

  const d = q.data!;
  return (
    <>
      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>Dashboard</Typography>
      <Grid container spacing={2} sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", md: "repeat(4, 1fr)" }, gap: 2 }}>
        <StatCard title="Orders" value={d.orders.total} />
        <StatCard title="Deliveries" value={d.deliveries.total} />
        <StatCard title="Tracking Events" value={d.tracking.total_events} />
        <StatCard title="POD" value={d.pods?.total ?? 0} />
      </Grid>
    </>
  );
}

