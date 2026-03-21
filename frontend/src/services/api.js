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
  editUsername(data) {
    return apiClient.patch("/profile/username", data);
  },
  editPassword(data) {
    return apiClient.patch("/profile/password", data);
  },
  editProfilePicture(data) {
    return apiClient.post("/profile/picture", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  getProfilePicture() {
    return apiClient.get("/profile/picture");
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
    return apiClient.delete(`/cart/items/${productId}/${quantity}`);
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
    return apiClient.post("/products", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  deleteProduct(productId) {
    return apiClient.delete(`/products/${productId}`);
  },
  updateProduct(productId, data) {
    return apiClient.patch(`/products/${productId}`, data);
  },
  updateProductImage(productId, formData) {
    return apiClient.patch(`/products/${productId}/image`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  addCategory(data) {
    return apiClient.post("/category", data);
  },
  deleteCategory(categoryId) {
    return apiClient.delete(`/category/${categoryId}`);
  },
  addProductToCategory(productId, categoryId) {
    return apiClient.patch(
      `/category/${categoryId}/products?product_id=${productId}`,
    );
  },
  updateOrderStatus(orderId, status) {
    return apiClient.patch(`/orders/${orderId}/status?status=${status}`);
  },
  getOrders() {
    return apiClient.get("/orders");
  },
  getOrder(orderId) {
    return apiClient.get(`/orders/${orderId}`);
  },
  updateUserRole(userId, role) {
    return apiClient.patch(`/users/${userId}/role?role=${role}`);
  },
  getUsers(limit = 10, offset = 0) {
    return apiClient.get("/users", { params: { limit, offset } });
  },
  getUser(userId) {
    return apiClient.get(`/users/${userId}`);
  },
};
