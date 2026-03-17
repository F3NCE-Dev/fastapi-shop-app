<script setup>
import { ref, onMounted } from "vue";
import { profileAPI, API_BASE_URL } from "../services/api";

const username = ref("");
const password = ref("");
const file = ref(null);
const feedback = ref({ message: "", type: "" });
const profilePictureUrl = ref("");

const fetchProfilePicture = async () => {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    const { data } = await profileAPI.getProfilePicture();
    if (data) {
      profilePictureUrl.value = `${API_BASE_URL}/${data}`;
    }
  } catch (err) {
    console.error("Error fetching profile picture:", err);
  }
};

onMounted(fetchProfilePicture);

const handleFileChange = (e) => {
  file.value = e.target.files[0];
};

const showFeedback = (msg, type = "success") => {
  feedback.value = { message: msg, type };
  setTimeout(() => (feedback.value = { message: "", type: "" }), 3000);
};

const updateUsername = async () => {
  if (!username.value) return;
  try {
    const { data } = await profileAPI.editUsername({
      new_name: username.value,
    });
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
    }
    showFeedback("Username updated successfully");
    username.value = "";
  } catch (err) {
    console.error(err);
    showFeedback("Failed to update username", "error");
  }
};

const updatePassword = async () => {
  if (!password.value) return;
  try {
    const { data } = await profileAPI.editPassword({
      password: password.value,
    });
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
    }
    showFeedback("Password updated successfully");
    password.value = "";
  } catch (err) {
    console.error(err);
    showFeedback("Failed to update password", "error");
  }
};

const uploadPicture = async () => {
  if (!file.value) return;
  try {
    const formData = new FormData();
    formData.append("file", file.value);
    await profileAPI.editProfilePicture(formData);
    await fetchProfilePicture();
    showFeedback("Profile picture uploaded successfully");
    file.value = null;
  } catch (err) {
    console.error(err);
    showFeedback("Failed to upload picture", "error");
  }
};
</script>

<template>
  <div class="p-10">
    <h2 class="text-3xl font-bold mb-8">Profile Management</h2>

    <div
      v-if="feedback.message"
      class="mb-6 p-4 rounded-lg border"
      :class="
        feedback.type === 'error'
          ? 'bg-red-50 border-red-200 text-red-600'
          : 'bg-green-50 border-green-200 text-green-600'
      "
    >
      {{ feedback.message }}
    </div>

    <div class="flex flex-col gap-8 max-w-xl">
      <div class="border rounded-xl p-6 shadow-sm bg-white">
        <h3 class="text-xl font-semibold mb-4">Update Username</h3>
        <div class="flex gap-4">
          <input
            v-model="username"
            type="text"
            placeholder="New username"
            class="flex-1 border rounded-md py-2 px-3 outline-none focus:border-gray-400"
          />
          <button
            @click="updateUsername"
            class="bg-slate-900 text-white px-4 py-2 rounded-md hover:bg-slate-800 transition"
          >
            Save
          </button>
        </div>
      </div>

      <div class="border rounded-xl p-6 shadow-sm bg-white">
        <h3 class="text-xl font-semibold mb-4">Update Password</h3>
        <div class="flex gap-4">
          <input
            v-model="password"
            type="password"
            placeholder="New password"
            class="flex-1 border rounded-md py-2 px-3 outline-none focus:border-gray-400"
          />
          <button
            @click="updatePassword"
            class="bg-slate-900 text-white px-4 py-2 rounded-md hover:bg-slate-800 transition"
          >
            Save
          </button>
        </div>
      </div>

      <div class="border rounded-xl p-6 shadow-sm bg-white">
        <h3 class="text-xl font-semibold mb-4">Profile Picture</h3>
        <div class="flex items-center gap-4">
          <img
            v-if="profilePictureUrl"
            :src="profilePictureUrl"
            alt="Current profile"
            class="w-16 h-16 rounded-full object-cover border border-slate-200"
          />
          <input
            type="file"
            @change="handleFileChange"
            class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
          />
          <button
            @click="uploadPicture"
            class="bg-slate-900 text-white px-4 py-2 rounded-md hover:bg-slate-800 transition whitespace-nowrap"
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
