import axios from "axios";

export const API_BASE_URL = "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const productsAPI = {
  getProducts(params) {
    return apiClient.get("/products", { params });
  },
  getProduct(id) {
    return apiClient.get(`/products/${id}`);
  },
};

export const categoriesAPI = {
  getCategories() {
    return apiClient.get("/categories");
  },
};

export const authAPI = {
  register(credentials) {
    return apiClient.post("/register", credentials);
  },
  login(credentials) {
    const params = new URLSearchParams();
    params.append("username", credentials.username);
    params.append("password", credentials.password);

    return apiClient.post("/login", params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },
  getMe() {
    return apiClient.get("/users/me");
  },
};

export const profileAPI = {
  editProfile(formData) {
    return apiClient.patch("/profile", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  editProfilePicture(data) {
    return apiClient.patch("/profile/image", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export const cartAPI = {
  getCart() {
    return apiClient.get("/cart/items");
  },
  addToCart(data) {
    return apiClient.post("/cart/items", data);
  },
  decreaseQuantity(productId, quantity) {
    return apiClient.delete(`/cart/items/${productId}`, {
      params: { quantity },
    });
  },
  removeFromCart(productId) {
    return apiClient.delete(`/cart/items/${productId}`);
  },
  clearCart() {
    return apiClient.delete("/cart/items");
  },
};

export const adminAPI = {
  addProduct(formData) {
    return apiClient.post("/admin/products", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  deleteProduct(productId) {
    return apiClient.delete(`/admin/products/${productId}`);
  },
  updateProduct(productId, data) {
    return apiClient.patch(`/admin/products/${productId}`, data);
  },
  addCategory(data) {
    return apiClient.post("/admin/category", data);
  },
  deleteCategory(categoryId) {
    return apiClient.delete(`/admin/category/${categoryId}`);
  },
  updateOrderStatus(orderId, status) {
    return apiClient.patch(`/admin/orders/${orderId}?status=${status}`);
  },
  getOrders() {
    return apiClient.get("/admin/orders");
  },
  getOrder(orderId) {
    return apiClient.get(`/admin/orders/${orderId}`);
  },
  updateUserRole(userId, role) {
    return apiClient.patch(`/admin/users/${userId}?role=${role}`);
  },
  getUsers(limit = 10, offset = 0) {
    return apiClient.get("/admin/users", { params: { limit, offset } });
  },
  getUser(userId) {
    return apiClient.get(`/admin/users/${userId}`);
  },
};

export const orderAPI = {
  setOrder() {
    return apiClient.post("/orders");
  },
  getOrders() {
    return apiClient.get("/orders");
  },
  deleteOrder(orderId) {
    return apiClient.delete(`/orders/${orderId}`);
  },
};
