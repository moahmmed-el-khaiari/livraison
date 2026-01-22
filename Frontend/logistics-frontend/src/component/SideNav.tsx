import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Toolbar } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import ListAltIcon from "@mui/icons-material/ListAlt";
import TravelExploreIcon from "@mui/icons-material/TravelExplore";
import FactCheckIcon from "@mui/icons-material/FactCheck";
import NotificationsIcon from "@mui/icons-material/Notifications";
import { useLocation, useNavigate } from "react-router-dom";

const drawerWidth = 260;

const items = [
  { label: "Dashboard", path: "/", icon: <DashboardIcon /> },
  { label: "Orders", path: "/orders", icon: <ListAltIcon /> },
  { label: "Deliveries", path: "/deliveries", icon: <LocalShippingIcon /> },
  { label: "Tracking", path: "/tracking", icon: <TravelExploreIcon /> },
  { label: "POD", path: "/pod", icon: <FactCheckIcon /> },
  { label: "Notifications", path: "/notifications", icon: <NotificationsIcon /> },
];

export default function SideNav() {
  const nav = useNavigate();
  const loc = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: "border-box" },
      }}
    >
      <Toolbar />
      <List>
        {items.map((it) => (
          <ListItemButton
            key={it.path}
            selected={loc.pathname === it.path}
            onClick={() => nav(it.path)}
          >
            <ListItemIcon>{it.icon}</ListItemIcon>
            <ListItemText primary={it.label} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}
