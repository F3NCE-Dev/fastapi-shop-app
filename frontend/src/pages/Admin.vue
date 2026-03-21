<script setup>
import { ref, onMounted, reactive } from "vue";
import { adminAPI, productsAPI, categoriesAPI } from "../services/api";

const activeTab = ref("products");
const products = ref([]);
const users = ref([]);
const orders = ref([]);
const categories = ref([]);
const loading = ref(false);

const productForm = reactive({
  name: "",
  description: "",
  price: 0,
  category_id: 1,
  image: null,
});
const categoryForm = reactive({ name: "" });

const fetchData = async () => {
  loading.value = true;
  try {
    if (activeTab.value === "products") {
      const { data } = await productsAPI.getProducts({});
      products.value = data;
    } else if (activeTab.value === "categories") {
      const { data } = await categoriesAPI.getCategories();
      categories.value = data;
    } else if (activeTab.value === "users") {
      const { data } = await adminAPI.getUsers();
      users.value = data;
    } else if (activeTab.value === "orders") {
      const { data } = await adminAPI.getOrders();
      orders.value = data;
    }
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleTabChange = (tab) => {
  activeTab.value = tab;
  fetchData();
};

onMounted(fetchData);

const onFileChange = (e) => {
  productForm.image = e.target.files[0];
};

const addProduct = async () => {
  try {
    const formData = new FormData();
    formData.append("name", productForm.name);
    formData.append("description", productForm.description);
    formData.append("price", productForm.price);
    formData.append("category_id", productForm.category_id);
    if (productForm.image) {
      formData.append("image", productForm.image);
    }
    await adminAPI.addProduct(formData);
    alert("Product added!");
    fetchData();
  } catch (e) {
    alert("Failed to add product");
  }
};

const deleteProduct = async (id) => {
  if (!confirm("Are you sure?")) return;
  try {
    await adminAPI.deleteProduct(id);
    fetchData();
  } catch (e) {
    alert("Failed to delete");
  }
};

const addCategory = async () => {
  try {
    await adminAPI.addCategory({ name: categoryForm.name });
    alert("Category added");
    categoryForm.name = "";
    fetchData();
  } catch (e) {
    alert("Error adding category");
  }
};

const deleteCategory = async (id) => {
  if (!confirm("Are you sure?")) return;
  try {
    await adminAPI.deleteCategory(id);
    alert("Category deleted");
    fetchData();
  } catch (e) {
    alert("Error deleting category");
  }
};

const updateUserRole = async (userId, role) => {
  try {
    await adminAPI.updateUserRole(userId, role);
    alert("Role updated");
    fetchData();
  } catch (e) {
    alert("Error updating role");
  }
};

const updateOrderStatus = async (orderId, status) => {
  try {
    await adminAPI.updateOrderStatus(orderId, status);
    alert("Status updated");
    fetchData();
  } catch (e) {
    alert("Error updating status");
  }
};
</script>

<template>
  <div class="p-10">
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-3xl font-bold">Admin Panel</h2>
      <div class="flex gap-2">
        <button
          v-for="tab in ['products', 'categories', 'users', 'orders']"
          :key="tab"
          @click="handleTabChange(tab)"
          :class="[
            'px-4 py-2 rounded-md font-medium capitalize',
            activeTab === tab
              ? 'bg-slate-800 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
          ]"
        >
          {{ tab }}
        </button>
      </div>
    </div>

    <div v-if="activeTab === 'products'" class="space-y-8">
      <div class="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h3 class="text-lg font-bold mb-4">Add New Product</h3>
        <form @submit.prevent="addProduct" class="grid grid-cols-2 gap-4">
          <input
            v-model="productForm.name"
            placeholder="Product Name"
            class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500"
            required
          />
          <input
            v-model="productForm.price"
            type="number"
            placeholder="Price"
            class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500"
            required
          />
          <input
            v-model="productForm.category_id"
            type="number"
            placeholder="Category ID"
            class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500"
            required
          />
          <input
            type="file"
            @change="onFileChange"
            class="px-3 py-2 border border-gray-300 rounded-md bg-white"
            required
          />
          <textarea
            v-model="productForm.description"
            placeholder="Description"
            class="col-span-2 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500"
            required
          ></textarea>
          <button
            type="submit"
            class="col-span-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-slate-800 hover:bg-slate-900"
          >
            Add Product
          </button>
        </form>
      </div>

      <div>
        <h3 class="text-xl font-bold mb-4">Product List</h3>
        <div class="grid grid-cols-1 gap-4">
          <div
            v-for="product in products"
            :key="product.id"
            class="flex justify-between items-center p-4 border rounded-md bg-white shadow-sm"
          >
            <div>
              <p class="font-bold">{{ product.name }}</p>
              <p class="text-sm text-gray-500">
                ID: {{ product.id }} | ${{ product.price }}
              </p>
            </div>
            <button
              @click="deleteProduct(product.id)"
              class="text-red-600 hover:text-red-800 font-medium"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'categories'" class="space-y-8">
      <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 max-w-md">
        <h3 class="text-lg font-bold mb-4">Add Category</h3>
        <div class="flex gap-2">
          <input
            v-model="categoryForm.name"
            placeholder="Category Name"
            class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500"
          />
          <button
            @click="addCategory"
            class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-slate-800 hover:bg-slate-900"
          >
            Add
          </button>
        </div>
      </div>

      <div>
        <h3 class="text-xl font-bold mb-4">Category List</h3>
        <div class="grid grid-cols-1 gap-4">
          <div
            v-for="category in categories"
            :key="category.id"
            class="flex justify-between items-center p-4 border rounded-md bg-white shadow-sm"
          >
            <div>
              <p class="font-bold">{{ category.name }}</p>
              <p class="text-sm text-gray-500">ID: {{ category.id }}</p>
            </div>
            <button
              @click="deleteCategory(category.id)"
              class="text-red-600 hover:text-red-800 font-medium"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'users'">
      <div class="space-y-4">
        <div
          v-for="user in users"
          :key="user.id"
          class="flex justify-between items-center p-4 border rounded-md bg-white shadow-sm"
        >
          <div>
            <p class="font-bold">{{ user.username }}</p>
            <p class="text-sm text-gray-500">
              ID: {{ user.id }} | Role: {{ user.role }}
            </p>
          </div>
          <div class="flex gap-2">
            <button
              @click="updateUserRole(user.id, 'admin')"
              class="text-blue-600 font-medium"
            >
              Make Admin
            </button>
            <button
              @click="updateUserRole(user.id, 'user')"
              class="text-gray-600 font-medium"
            >
              Make User
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'orders'">
      <div class="space-y-4">
        <div
          v-for="order in orders"
          :key="order.id"
          class="flex justify-between items-center p-4 border rounded-md bg-white shadow-sm"
        >
          <div>
            <p class="font-bold">Order #{{ order.id }}</p>
            <p class="text-sm text-gray-500">
              User ID: {{ order.user_id }} | Status: {{ order.status }}
            </p>
          </div>
          <div class="flex gap-2">
            <select
              @change="updateOrderStatus(order.id, $event.target.value)"
              class="border rounded px-2 py-1"
            >
              <option value="" disabled selected>Change Status</option>
              <option value="pending">Pending</option>
              <option value="shipped">Shipped</option>
              <option value="delivered">Delivered</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
