<script setup>
import { onMounted, ref, reactive, watch } from "vue";
import Header from "../components/Header.vue";
import ProductCard from "../components/ProductCard.vue";
import { productsAPI, API_BASE_URL } from "../services/api";

const products = ref([]);

const filters = reactive({
  sortBy: "title",
  searchQuery: "",
});

const fetchProducts = async () => {
  try {
    const params = {
      sort: filters.sortBy,
    };

    if (filters.searchQuery) {
      params.search = filters.searchQuery;
    }

    const { data } = await productsAPI.getProducts(params);
    products.value = data;
  } catch (err) {
    console.log(err);
  }
};

onMounted(fetchProducts);

watch(filters, fetchProducts);
</script>

<template>
  <div class="bg-white w-4/5 m-auto h-screen rounded-xl shadow-xl mt-14">
    <Header />

    <div class="p-10">
      <div class="flex justify-between items-center mb-8">
        <h2 class="text-3xl font-bold">Our products</h2>
        <div class="flex gap-4">
          <select
            v-model="filters.sortBy"
            class="py-2 px-3 border rounded-md outline-none"
          >
            <option value="title">By name</option>
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

      <div class="grid grid-cols-4 gap-5">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :title="product.title"
          :price="product.price"
          :imageUrl="
            product.image_url ? `${API_BASE_URL}/${product.image_url}` : ''
          "
        />
      </div>
    </div>
  </div>
</template>
