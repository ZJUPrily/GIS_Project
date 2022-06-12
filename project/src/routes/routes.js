import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import UserProfile from "@/pages/UserProfile.vue";
import TableList from "@/pages/TableList.vue";
import Maps from "@/pages/Maps.vue";
import chart from "@/pages/Chart.vue";
import conStyle from "@/pages/ConditionStyle.vue";

const routes = [
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/maps",
    children: [
      {
        path: "chart",
        name: "Condition Analyze",
        component: chart,
      },
      {
        path: "style",
        name: "Condition Style",
        component: conStyle,
      },
      {
        path: "user",
        name: "Add Layer",
        component: UserProfile,
      },
      {
        path: "table",
        name: "Layer List",
        component: TableList,
      },
      {
        path: "maps",
        name: "Map",
        meta: {
          hideFooter: true,
        },
        component: Maps,
      },
    ],
  },
];

export default routes;
