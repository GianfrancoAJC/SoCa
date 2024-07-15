import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/UserHome.vue";
import Auth from "../components/UserAuth.vue";
import Questionnaire from "../components/UserQuestionnaire.vue";
import ChatApp from "../components/ChatApp.vue";
import Dashboard from "../components/UserDashboard.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/auth",
    name: "auth",
    component: Auth,
  },
  {
    path: "/questionnaire",
    name: "questionnaire",
    component: Questionnaire,
  },
  {
    path: "/chat",
    name: "chat",
    component: ChatApp,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
