import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import DashboardPage from "../pages/DashboardPage";
import OrdersPage from "../pages/OrdersPage";
import DeliveriesPage from "../pages/DeliveriesPage";
import TrackingPage from "../pages/TrackingPage";
import PodPage from "../pages/PodPage";
import NotificationsPage from "../pages/NotificationsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "orders", element: <OrdersPage /> },
      { path: "deliveries", element: <DeliveriesPage /> },
      { path: "tracking", element: <TrackingPage /> },
      { path: "pod", element: <PodPage /> },
      { path: "notifications", element: <NotificationsPage /> },
    ],
  },
]);
