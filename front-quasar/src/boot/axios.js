import { boot } from "quasar/wrappers";
import axios from "axios";

const api = axios.create({
  // baseURL: `http://${location.hostname}:5000`,
  baseURL: 'http://weddingshow.robson.com.br:5000',
  headers: {
    "Content-Type": "application/json",
  },
});

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { api };
