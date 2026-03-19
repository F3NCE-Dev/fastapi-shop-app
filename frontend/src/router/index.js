import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Auth from "../pages/Auth.vue";
import Profile from "../pages/Profile.vue";
import Product from "../pages/Product.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/auth",
    name: "Auth",
    component: Auth,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/products/:id",
    name: "Product",
    component: Product,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
