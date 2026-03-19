<script setup>
import { RouterLink } from "vue-router";

defineProps({
  id: Number,
  imageUrl: String,
  name: String,
  price: Number,
});
</script>

<template>
  <div class="border rounded-md p-4 shadow-md">
    <RouterLink :to="`/products/${id}`">
      <img
        :src="imageUrl"
        alt="Product Image"
        class="w-full h-48 object-cover mb-4 rounded"
      />
      <h3 class="text-lg font-semibold mb-2">{{ name }}</h3>
    </RouterLink>
    <div class="flex justify-between items-center">
      <p class="text-gray-600">{{ price }} $</p>
      <button
        class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 cursor-pointer"
      >
        Add to Cart
      </button>
    </div>
  </div>
</template>
