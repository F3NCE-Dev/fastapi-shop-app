<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { authAPI } from "../services/api";

const router = useRouter();

const isLogin = ref(true);
const credentials = reactive({
  username: "",
  password: "",
});
const error = ref(null);

const onSubmit = async () => {
  error.value = null;
  try {
    if (isLogin.value) {
      const { data } = await authAPI.login(credentials);
      localStorage.setItem("token", data.access_token);
      router.push("/");
    } else {
      await authAPI.register(credentials);
      alert("Registration successful! Please log in.");
      isLogin.value = true;
    }
  } catch (err) {
    console.error(err);
    error.value =
      err.response?.data?.detail || "An error occurred. Please try again.";
  }
};
</script>

<template>
  <div class="flex justify-center items-center h-full -mt-14">
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
      <h2 class="text-2xl font-bold text-center text-gray-900">
        {{ isLogin ? "Sign in to your account" : "Create a new account" }}
      </h2>
      <form class="space-y-6" @submit.prevent="onSubmit">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700"
            >Username</label
          >
          <div class="mt-1">
            <input
              id="username"
              v-model="credentials.username"
              name="username"
              type="text"
              autocomplete="username"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700"
            >Password</label
          >
          <div class="mt-1">
            <input
              id="password"
              v-model="credentials.password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <div v-if="error" class="p-3 bg-red-100 text-red-700 rounded-md">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-slate-800 hover:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500"
          >
            {{ isLogin ? "Sign in" : "Register" }}
          </button>
        </div>
      </form>

      <div class="text-sm text-center">
        <button
          @click="isLogin = !isLogin"
          class="font-medium text-slate-600 hover:text-slate-500"
        >
          {{
            isLogin
              ? "Don't have an account? Register"
              : "Already have an account? Sign in"
          }}
        </button>
      </div>
    </div>
  </div>
</template>
