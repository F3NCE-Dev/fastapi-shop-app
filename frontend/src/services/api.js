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
