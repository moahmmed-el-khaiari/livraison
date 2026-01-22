import { AppBar, Toolbar, Typography, Box } from "@mui/material";

export default function TopBar() {
  return (
    <AppBar position="sticky" elevation={0} color="default">
      <Toolbar>
        <Typography variant="h6" sx={{ fontWeight: 700 }}>
          Logistics Platform
        </Typography>
        <Box sx={{ flex: 1 }} />
        <Typography variant="body2" color="text.secondary">
          Local Dev
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
