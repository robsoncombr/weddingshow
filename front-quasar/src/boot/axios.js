import { boot } from "quasar/wrappers";
import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.16.200:5000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { api };
