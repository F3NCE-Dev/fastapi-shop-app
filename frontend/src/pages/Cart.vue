<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { cartAPI, productsAPI, orderAPI, API_BASE_URL } from "../services/api";

const router = useRouter();
const cart = ref(null);
const loading = ref(true);

const loadCart = async () => {
  try {
    const { data } = await cartAPI.getCart();

    if (data.items) {
      await Promise.all(
        data.items.map(async (item) => {
          if (!item.product && item.product_id) {
            try {
              const { data: productData } = await productsAPI.getProduct(
                item.product_id,
              );
              item.product = productData;
            } catch (e) {
              console.error("Failed to fetch product details for item:", item);
            }
          }
        }),
      );
    }

    cart.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const increaseQuantity = async (item) => {
  try {
    const productId = item.product ? item.product.id : item.product_id;
    await cartAPI.addToCart({ product_id: productId, quantity: 1 });
    await loadCart();
  } catch (err) {
    console.error(err);
  }
};

const decreaseQuantity = async (item) => {
  try {
    const productId = item.product ? item.product.id : item.product_id;
    await cartAPI.decreaseQuantity(productId, 1);
    await loadCart();
  } catch (err) {
    console.error(err);
  }
};

const removeItem = async (productId) => {
  try {
    await cartAPI.removeFromCart(productId);
    await loadCart();
  } catch (err) {
    console.error(err);
  }
};

const clearCart = async () => {
  try {
    await cartAPI.clearCart();
    await loadCart();
  } catch (err) {
    console.error(err);
  }
};

const checkout = async () => {
  try {
    const { data } = await orderAPI.setOrder();
    if (data.success) {
      router.push({ name: "Orders" });
    }
  } catch (err) {
    console.error(err);
  }
};

onMounted(loadCart);
</script>

<template>
  <div class="py-12 px-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-8">Shopping Cart</h1>

    <div v-if="loading" class="text-center text-gray-500 text-lg">
      Loading...
    </div>

    <div
      v-else-if="!cart || !cart.items || cart.items.length === 0"
      class="text-center text-gray-500 text-lg"
    >
      Your cart is empty.
    </div>

    <div v-else>
      <div class="space-y-6">
        <div
          v-for="item in cart.items"
          :key="item.id"
          class="flex items-center gap-6 border border-slate-200 p-4 rounded-xl shadow-sm"
        >
          <div v-if="item.product" class="flex items-center gap-6 flex-1">
            <img
              :src="`${API_BASE_URL}/${item.product.image_url}`"
              :alt="item.product.name"
              class="w-24 h-24 object-cover rounded-lg"
            />
            <div>
              <h3 class="text-xl font-semibold">{{ item.product.name }}</h3>
              <p class="text-gray-500">Price: ${{ item.product.price }}</p>
            </div>
          </div>
          <div v-else class="flex-1 text-gray-400 italic">
            Product information unavailable
          </div>

          <div class="flex flex-col items-end gap-2 min-w-[100px]">
            <div
              class="flex items-center border border-gray-300 rounded-lg overflow-hidden"
            >
              <button
                @click="decreaseQuantity(item)"
                class="px-3 py-1 bg-gray-50 hover:bg-gray-100 border-r border-gray-300 text-gray-600 cursor-pointer"
              >
                -
              </button>
              <span class="px-3 py-1 text-sm font-medium text-gray-900">{{
                item.quantity
              }}</span>
              <button
                @click="increaseQuantity(item)"
                class="px-3 py-1 bg-gray-50 hover:bg-gray-100 border-l border-gray-300 text-gray-600 cursor-pointer"
              >
                +
              </button>
            </div>
            <span class="text-lg font-bold" v-if="item.product">
              ${{ item.product.price * item.quantity }}
            </span>
            <button
              @click="
                removeItem(item.product ? item.product.id : item.product_id)
              "
              class="text-red-500 hover:text-red-700 font-medium cursor-pointer"
            >
              Remove
            </button>
          </div>
        </div>
      </div>

      <div
        class="mt-8 flex justify-between items-center border-t border-slate-200 pt-6"
      >
        <button
          @click="clearCart"
          class="text-red-600 hover:text-red-800 font-medium cursor-pointer"
        >
          Clear Cart
        </button>
        <div class="flex items-center gap-8">
          <div class="text-2xl font-bold">Total: ${{ cart.total_price }}</div>
          <button
            @click="checkout"
            class="bg-lime-600 text-white py-3 px-8 rounded-xl font-bold hover:bg-lime-700 transition cursor-pointer"
          >
            Buy Now
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
