<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { authAPI, API_BASE_URL } from "../services/api";

const route = useRoute();
const router = useRouter();
const isLoggedIn = ref(false);
const showMenu = ref(false);
const profilePictureUrl = ref("");
const isAdmin = ref(false);

const checkLoginStatus = async () => {
  const token = localStorage.getItem("token");
  if (token) {
    isLoggedIn.value = true;
    try {
      const userResponse = await authAPI.getMe();
      isAdmin.value = userResponse.data.role === "admin";
      if (userResponse.data.profile_picture_url) {
        profilePictureUrl.value = `${API_BASE_URL}/${userResponse.data.profile_picture_url}`;
      } else {
        profilePictureUrl.value = "";
      }
    } catch (e) {
      console.error("Error fetching user data:", e);
    }
  } else {
    isLoggedIn.value = false;
    profilePictureUrl.value = "";
    isAdmin.value = false;
  }
};

const logout = () => {
  localStorage.removeItem("token");
  isLoggedIn.value = false;
  showMenu.value = false;
  router.push("/auth");
};

onMounted(checkLoginStatus);
watch(() => route.path, checkLoginStatus);
</script>

<template>
  <header
    class="flex justify-between items-center border-b border-slate-200 px-10 py-8"
  >
    <router-link to="/">
      <h1 class="text-xl font-bold text-slate-900">Shop App</h1>
    </router-link>
    <nav class="flex items-center gap-10">
      <ul class="flex space-x-6">
        <li>
          <router-link to="/" class="text-slate-700 hover:text-slate-900"
            >Home</router-link
          >
        </li>
        <li>
          <a href="#" class="text-slate-700 hover:text-slate-900">About</a>
        </li>
        <li>
          <a href="#" class="text-slate-700 hover:text-slate-900">Contact</a>
        </li>
        <li>
          <router-link to="/cart" class="text-slate-700 hover:text-slate-900"
            >Cart</router-link
          >
        </li>
        <li v-if="isAdmin">
          <router-link
            to="/admin"
            class="text-slate-700 hover:text-slate-900 font-bold"
            >Admin</router-link
          >
        </li>
      </ul>

      <div v-if="!isLoggedIn" class="flex items-center gap-4">
        <router-link
          to="/auth"
          class="text-slate-700 hover:text-slate-900 font-medium"
        >
          login/register
        </router-link>
      </div>

      <div v-else class="relative">
        <button
          @click="showMenu = !showMenu"
          class="flex items-center gap-2 focus:outline-none"
        >
          <img
            :src="profilePictureUrl || 'https://via.placeholder.com/40'"
            alt="Avatar"
            class="w-10 h-10 rounded-full object-cover border border-slate-200 cursor-pointer"
          />
        </button>

        <div
          v-if="showMenu"
          class="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-xl shadow-xl z-20 overflow-hidden"
        >
          <div class="py-1">
            <router-link
              to="/profile"
              class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
              @click="showMenu = false"
            >
              My Profile
            </router-link>
            <router-link
              to="/orders"
              class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
              @click="showMenu = false"
            >
              My Orders
            </router-link>
          </div>
          <div class="border-t border-slate-100"></div>
          <button
            @click="logout"
            class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  </header>
</template>
>
