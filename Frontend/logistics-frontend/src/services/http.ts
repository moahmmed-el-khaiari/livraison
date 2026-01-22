import axios from "axios";

export function http(baseURL: string) {
  const instance = axios.create({ baseURL, timeout: 300000 });

  // Si tu actives JWT plus tard, tu peux injecter ici:
  // instance.interceptors.request.use((config) => {
  //   const token = localStorage.getItem("access_token");
  //   if (token) config.headers.Authorization = `Bearer ${token}`;
  //   return config;
  // });

  return instance;
}
