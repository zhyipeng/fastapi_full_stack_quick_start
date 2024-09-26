import { createRouter, createWebHashHistory } from "vue-router";
import IndexView from "./views/IndexView.vue";
import LoginView from "./views/LoginView.vue";

const routes = [
  {
    path: "/",
    component: IndexView,
  },
  { path: "/login", component: LoginView },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, _, next) => {
  if (to.path === "/login") {
    next();
  } else {
    const token = sessionStorage.getItem("access_token");
    if (token) {
      next();
    } else {
      next("/login");
    }
  }
});

export default router;
