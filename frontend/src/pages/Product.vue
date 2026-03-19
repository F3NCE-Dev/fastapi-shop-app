<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { productsAPI, API_BASE_URL } from "../services/api";

const route = useRoute();
const product = ref(null);

onMounted(async () => {
  try {
    const productId = route.params.id;
    const { data } = await productsAPI.getProduct(productId);
    product.value = data;
  } catch (err) {
    console.error(err);
  }
});
</script>

<template>
  <div v-if="product" class="py-12 px-6 max-w-7xl mx-auto">
    <div class="grid md:grid-cols-2 gap-16 items-start">
      <img
        :src="`${API_BASE_URL}/${product.image_url}`"
        :alt="product.name"
        class="w-full h-[500px] object-cover rounded-xl"
      />

      <div class="flex flex-col h-full">
        <h1 class="text-5xl font-bold mb-6">
          {{ product.name }}
        </h1>

        <p class="text-gray-500 text-lg leading-relaxed mb-10 max-w-xl">
          {{ product.description }}
        </p>

        <div class="mt-auto flex items-center justify-between">
          <span class="text-4xl font-bold"> ${{ product.price }} </span>

          <button
            class="bg-black text-white py-3 px-10 rounded-xl hover:bg-gray-800 transition text-lg"
          >
            Add to cart
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="py-20 text-center text-gray-500 text-lg">Loading...</div>
</template>
