<script setup>
import { ref, onMounted } from "vue";
import { orderAPI } from "../services/api";

const orders = ref([]);
const loading = ref(true);

const fetchOrders = async () => {
  try {
    const { data } = await orderAPI.getOrders();
    orders.value = data.sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at),
    );
  } catch (error) {
    console.error("Failed to fetch orders:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOrders);
</script>

<template>
  <div class="p-10">
    <h1 class="text-3xl font-bold mb-10">My Orders</h1>

    <div v-if="loading" class="flex justify-center py-20">
      <p class="text-slate-400">Loading your order history...</p>
    </div>

    <div
      v-else-if="orders.length === 0"
      class="text-center py-20 bg-slate-50 rounded-3xl border border-dashed border-slate-300"
    >
      <p class="text-slate-500 text-xl">You haven't placed any orders yet.</p>
      <router-link
        to="/"
        class="text-lime-600 font-bold mt-4 inline-block hover:underline"
      >
        Start Shopping
      </router-link>
    </div>

    <div v-else class="grid gap-6">
      <div
        v-for="order in orders"
        :key="order.id"
        class="bg-white border border-slate-200 rounded-2xl p-6 flex flex-col md:flex-row justify-between items-center hover:shadow-md transition-shadow cursor-pointer"
        @click="$router.push({ name: 'Order', params: { id: order.id } })"
      >
        <div class="flex items-center gap-6">
          <div>
            <h3 class="font-bold text-lg">Order #{{ order.id }}</h3>
            <p class="text-slate-500 text-sm">
              {{ new Date(order.created_at).toLocaleDateString() }}
            </p>
          </div>
        </div>

        <div class="flex items-center gap-8 mt-4 md:mt-0">
          <div class="text-right">
            <p class="text-xs text-slate-400 uppercase font-semibold">Total</p>
            <p class="font-black text-lime-600">
              ${{ order.total_price.toFixed(2) }}
            </p>
          </div>
          <span
            class="px-4 py-1 rounded-full text-xs font-bold capitalize border"
            :class="{
              'bg-yellow-50 text-yellow-600 border-yellow-100':
                order.status === 'pending',
              'bg-green-50 text-green-600 border-green-100':
                order.status === 'completed',
              'bg-red-50 text-red-600 border-red-100':
                order.status === 'cancelled',
            }"
          >
            {{ order.status }}
          </span>
          <button class="text-slate-300 hover:text-slate-600 transition-colors">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="m9 18 6-6-6-6" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
