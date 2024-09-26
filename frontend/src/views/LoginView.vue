<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { AuthService, LoginRsp, OpenAPI } from "../client";

const formData = reactive({
  username: "",
  password: "",
});

const router = useRouter();

const login = async () => {
  try {
    const resp = await AuthService.loginApiAuthLoginPost(formData);
    afterLogin(resp);
    await router.push("/");
  } catch (e) {
    console.log(e);
  }
};

const afterLogin = (resp: LoginRsp) => {
  sessionStorage.setItem("access_token", resp.access_token);
  sessionStorage.setItem("refresh_token", resp.refresh_token);
  OpenAPI.TOKEN = resp.access_token;
};
</script>

<template>
  <div class="h-screen w-screen flex justify-center items-center">
    <div
      class="w-[350px] h-[200px] flex flex-col p-10 justify-center items-center"
    >
      <div>
        <label for="username">账号</label>
        <input
          type="text"
          id="username"
          v-model="formData.username"
          class="input"
        />
      </div>
      <div class="mt-5">
        <label for="password">密码</label>
        <input
          class="input"
          type="password"
          name="password"
          id="password"
          v-model="formData.password"
        />
      </div>
      <div class="mt-5">
        <button @click="login">Login</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.input {
  margin-left: 10px;
}
</style>
