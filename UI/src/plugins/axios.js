import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import store from "@/store";

const axiosBase = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  headers:{'Content-Type': 'application/json'},
  transformRequest: [
    (data, headers) => {
      const token = store.state.auth.accessToken;
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
      data=JSON.stringify(data);
      return data;
    },
  ],
});


axiosBase.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log(error);
    if (error.config && error.response && error.response.status === 401) {
      store
        .dispatch("auth/refreshToken") // attempt to obtain new access token by running 'refreshToken' action
        .catch((err) => {
          // Could not refresh token. Refresh token may have expired too. It would be better to logout the user.
          return Promise.reject(err);
        });
    } else {
      const { response, message } = error;
      if (response) {
        console.log(error.response.data.message);
      } else if (message) {
        console.log(message);
      }
    }
  }
);

Vue.use(VueAxios, axiosBase);

export default axiosBase;
