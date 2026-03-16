<script setup>
defineProps({
  imageUrl: String,
  title: String,
  price: Number,
});
</script>

<template>
  <div class="border rounded-md p-4 shadow-md">
    <img
      :src="imageUrl"
      alt="Product Image"
      class="w-full h-48 object-cover mb-4 rounded"
    />
    <h3 class="text-lg font-semibold mb-2">{{ title }}</h3>
    <p class="text-gray-600 mb-4">{{ price }} $</p>
    <button
      class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 cursor-pointer"
    >
      Add to Cart
    </button>
  </div>
</template>
