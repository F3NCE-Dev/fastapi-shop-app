import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Auth from "../pages/Auth.vue";
import Profile from "../pages/Profile.vue";
import Product from "../pages/Product.vue";
import Cart from "../pages/Cart.vue";
import Admin from "../pages/Admin.vue";
import { authAPI } from "../services/api";

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
  {
    path: "/cart",
    name: "Cart",
    component: Cart,
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.name === "Admin") {
    const token = localStorage.getItem("token");
    if (!token) {
      return next({ name: "Auth" });
    }
    try {
      const { data } = await authAPI.getMe();
      if (data.role !== "admin") {
        return next({ name: "Home" });
      }
    } catch (e) {
      return next({ name: "Auth" });
    }
  }
  next();
});

export default router;
