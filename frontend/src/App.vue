<script setup>
import { onMounted } from "vue";
import { authAPI } from "./services/api";
import Header from "./components/Header.vue";

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get("code");
  if (code) {
    try {
      const { data } = await authAPI.googleCallback(code);
      localStorage.setItem("token", data.access_token);
      window.location.href = "/";
    } catch (err) {
      console.error(err);
    }
  }
});
</script>

<template>
  <div class="bg-white w-4/5 m-auto rounded-xl shadow-xl mt-14">
    <Header />
    <router-view></router-view>
  </div>
</template>
