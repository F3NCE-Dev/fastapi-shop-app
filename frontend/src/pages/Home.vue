<script setup>
import { onMounted, ref, reactive, watch } from "vue";
import ProductCard from "../components/ProductCard.vue";
import { productsAPI, categoriesAPI, API_BASE_URL } from "../services/api";

const products = ref([]);
const categories = ref([]);

const filters = reactive({
  sortBy: "name",
  searchQuery: "",
  categoryId: null,
});

const fetchCategories = async () => {
  try {
    const { data } = await categoriesAPI.getCategories();
    categories.value = data;
  } catch (err) {
    console.log(err);
  }
};

const fetchProducts = async () => {
  try {
    const params = {
      sort: filters.sortBy,
    };
    if (filters.searchQuery) {
      params.search = filters.searchQuery;
    }
    if (filters.categoryId) {
      params.category_id = filters.categoryId;
    }
    const { data } = await productsAPI.getProducts(params);
    products.value = data;
  } catch (err) {
    console.log(err);
  }
};
onMounted(async () => {
  await Promise.all([fetchCategories(), fetchProducts()]);
});
watch(filters, fetchProducts);
</script>

<template>
  <div class="flex">
    <div class="p-10 border-r">
      <h3 class="text-2xl font-bold mb-4">Categories</h3>
      <ul>
        <li
          @click="filters.categoryId = null"
          :class="{ 'font-bold': !filters.categoryId }"
          class="cursor-pointer hover:text-gray-500 mb-2"
        >
          All
        </li>
        <li
          v-for="category in categories"
          :key="category.id"
          @click="filters.categoryId = category.id"
          :class="{ 'font-bold': filters.categoryId === category.id }"
          class="cursor-pointer hover:text-gray-500 mb-2"
        >
          {{ category.name }}
        </li>
      </ul>
    </div>
    <div class="w-3/4 p-10">
      <div class="flex justify-between items-center mb-8">
        <h2 class="text-3xl font-bold">Our products</h2>
        <div class="flex gap-4">
          <select
            v-model="filters.sortBy"
            class="py-2 px-3 border rounded-md outline-none"
          >
            <option value="name">By name</option>
            <option value="price">By price (cheap)</option>
            <option value="-price">By price (expensive)</option>
          </select>
          <input
            v-model="filters.searchQuery"
            class="border rounded-md py-2 px-3 outline-none focus:border-gray-400"
            placeholder="Search..."
          />
        </div>
      </div>
      <div class="grid grid-cols-3 gap-5">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :id="product.id"
          :name="product.name"
          :price="product.price"
          :imageUrl="
            product.image_url ? `${API_BASE_URL}/${product.image_url}` : ''
          "
        />
      </div>
    </div>
  </div>
</template>
