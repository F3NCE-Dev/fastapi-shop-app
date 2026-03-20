<script setup>
import { RouterLink } from "vue-router";
import { ref } from "vue";
import { cartAPI } from "../services/api";

const props = defineProps({
  id: Number,
  imageUrl: String,
  name: String,
  price: Number,
});

const isAdding = ref(false);

const addToCart = async () => {
  if (isAdding.value) return;
  isAdding.value = true;
  try {
    await cartAPI.addToCart({ product_id: props.id, quantity: 1 });
  } catch (err) {
    console.error(err);
  } finally {
    isAdding.value = false;
  }
};
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
      <div class="flex items-center gap-2">
        <button
          @click="addToCart"
          class="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 cursor-pointer disabled:opacity-50"
          :disabled="isAdding"
        >
          Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>
