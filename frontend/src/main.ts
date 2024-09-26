import axios, { AxiosError, AxiosResponse } from "axios";
import { createApp } from "vue";
import App from "./App.vue";
import { AuthService, OpenAPI } from "./client";
import router from "./router";
import "./style.css";

const app = createApp(App);
app.use(router);
app.mount("#app");

if (import.meta.env.DEV) {
  OpenAPI.BASE = "http://localhost:8000";
}
OpenAPI.TOKEN = sessionStorage.getItem("access_token") || undefined;

axios.interceptors.response.use(
  (resp: AxiosResponse) => {
    if (resp.data?.error_message) {
      console.log(resp.data);
      alert(resp.data.error_message);
      throw new Error(resp.data.error_message);
    }
    return resp;
  },
  (error: AxiosError) => {
    const data: any = error?.response?.data;
    const msg = data.detail || error.message;
    switch (error.response?.status) {
      case 408: {
        // 签名过期错误码
        const refreshToken = sessionStorage.getItem("refresh_token");
        if (refreshToken) {
          OpenAPI.TOKEN = undefined;
          sessionStorage.removeItem("access_token");
          AuthService.refreshApiAuthRefreshPost({ refresh_token: refreshToken })
            .then((resp) => {
              sessionStorage.setItem("access_token", resp.access_token);
              OpenAPI.TOKEN = resp.access_token;
              error.config!.headers.Authorization = `Bearer ${resp.access_token}`;
              // 最多重试2次, 防止异常情况导致死循环
              error.config!.headers["X-Retry-Count"] =
                (error.config!.headers["X-Retry-Count"] || 0) + 1;
              if (error.config!.headers["X-Retry-Count"] > 2) {
                setTimeout(() => {
                  router.push("/login");
                }, 1000);
              }
              return axios(error.config!);
            })
            .catch(() => {
              sessionStorage.removeItem("refresh_token");
              setTimeout(() => {
                router.push("/login");
              }, 1000);
            });
        } else {
          setTimeout(() => {
            router.push("/login");
          }, 500);
        }
        return Promise.reject(error);
      }
      case 401: {
        alert(msg);
        if (router.currentRoute.value.path === "/login") {
          return Promise.reject(error);
        }
        setTimeout(() => {
          router.push("/login");
        }, 1000);
        return Promise.reject(error);
      }
      default: {
        alert(msg);
        return Promise.reject(error);
      }
    }
  },
);
