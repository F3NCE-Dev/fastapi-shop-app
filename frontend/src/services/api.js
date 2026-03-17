import axios from "axios";

export const API_BASE_URL = "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const productsAPI = {
  getProducts(params) {
    return apiClient.get("/products", { params });
  },
};
