<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { orderAPI, productsAPI, API_BASE_URL } from "../services/api";

const route = useRoute();
const router = useRouter();
const order = ref(null);
const loading = ref(true);

const fetchOrder = async () => {
  try {
    const { data } = await orderAPI.getOrders();
    const foundOrder = data.find((o) => o.id === Number(route.params.id));
    if (foundOrder) {
      if (foundOrder.items) {
        await Promise.all(
          foundOrder.items.map(async (item) => {
            if (!item.product && item.product_id) {
              try {
                const { data: productData } = await productsAPI.getProduct(
                  item.product_id,
                );
                item.product = productData;
              } catch (e) {
                console.error(
                  "Failed to fetch product details for order item:",
                  item,
                );
              }
            }
          }),
        );
      }
      order.value = foundOrder;
    } else {
      router.push({ name: "Home" });
    }
  } catch (error) {
    console.error("Failed to fetch order:", error);
    router.push({ name: "Auth" });
  } finally {
    loading.value = false;
  }
};

const cancelOrder = async () => {
  if (confirm("Are you sure you want to cancel this order?")) {
    try {
      await orderAPI.deleteOrder(order.value.id);
      alert("Order cancelled successfully");
      router.push({ name: "Profile" });
    } catch (error) {
      alert("Failed to cancel order");
    }
  }
};

onMounted(fetchOrder);
</script>

<template>
  <div class="p-10">
    <h1 class="text-3xl font-bold mb-10">Order Details</h1>

    <div v-if="loading" class="flex justify-center items-center py-20">
      <p class="text-slate-400 font-medium">Loading order information...</p>
    </div>

    <div
      v-else-if="order"
      class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm"
    >
      <div
        class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4"
      >
        <div>
          <p
            class="text-slate-400 text-sm mb-1 uppercase tracking-wider font-semibold"
          >
            Order Number
          </p>
          <h2 class="text-2xl font-bold">#{{ order.id }}</h2>
          <p class="text-slate-500 mt-1">
            Placed on {{ new Date(order.created_at).toLocaleDateString() }}
          </p>
        </div>
        <div class="flex flex-col items-end">
          <p
            class="text-slate-400 text-sm mb-1 uppercase tracking-wider font-semibold"
          >
            Status
          </p>
          <span
            class="px-4 py-1.5 rounded-full text-sm font-bold capitalize shadow-sm border"
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
        </div>
      </div>

      <div class="space-y-4 mb-8">
        <h3 class="text-lg font-bold border-b border-slate-100 pb-2">
          Ordered Items
        </h3>
        <div
          v-for="item in order.items"
          :key="item.id"
          class="flex justify-between items-center py-4 border-b border-slate-50 last:border-0"
        >
          <div class="flex items-center gap-4">
            <img
              v-if="item.product && item.product.image_url"
              :src="`${API_BASE_URL}/${item.product.image_url}`"
              class="w-20 h-20 object-cover rounded-xl border border-slate-100"
            />
            <div>
              <p class="font-bold text-lg">
                {{ item.product?.name || "Product #" + item.product_id }}
              </p>
              <p class="text-slate-400 text-sm">
                Quantity: {{ item.quantity }} × ${{ item.price_at_purchase }}
              </p>
            </div>
          </div>
          <p class="font-bold text-xl">
            ${{ (item.price_at_purchase * item.quantity).toFixed(2) }}
          </p>
        </div>
      </div>

      <div
        class="border-t border-slate-100 pt-6 flex flex-col md:flex-row justify-between items-center gap-6"
      >
        <button
          v-if="order.status === 'pending'"
          @click="cancelOrder"
          class="text-red-500 hover:text-red-600 font-bold transition-colors"
        >
          Cancel this order
        </button>
        <div class="md:ml-auto text-right">
          <p class="text-slate-400 text-sm font-semibold">TOTAL AMOUNT</p>
          <p class="text-3xl font-black text-lime-600">
            ${{ order.total_price.toFixed(2) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
