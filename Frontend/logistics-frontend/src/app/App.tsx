import { Outlet } from "react-router-dom";
import { Box } from "@mui/material";
import TopBar from "../component/TopBar";
import SideNav from "../component/SideNav";

export default function App() {
  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <SideNav />
      <Box sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <TopBar />
        <Box component="main" sx={{ p: 3, flex: 1, bgcolor: "background.default" }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}
