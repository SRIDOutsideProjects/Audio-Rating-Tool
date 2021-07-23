//// action async hota hai aur mutations sync hota hai
import axios from "@/plugins/axios";

export default {
  namespaced: true, // dispatch me auth/<action-name> likh sakte namespaced True rakhne pe
  state: {
    accessToken: localStorage.getItem("access_token") || null, // use this token to make authenticated api calls
    refreshToken: localStorage.getItem("refresh_token") || null,
    endPoints: {
      obtainToken: "auth/obtain_token_pair/",
      refreshToken: "auth/refresh_token/",
      logout:"logout/"
    },
  },
  getters: {
    loggedIn(state) {
      return state.accessToken != null;
    },
  },
  mutations: {
    updateTokens(state, { access, refresh }) {
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      state.accessToken = access;
      state.refreshToken = refresh;
    },
    updateAccessToken(state, access) {
      localStorage.setItem("access_token", access);
      state.accessToken = access;
    },
    destroyTokens(state) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      state.accessToken = null;
      state.refreshToken = null;
    },
  },
  actions: {
    // run the below action to get a new access token on expiration
    //https://stackoverflow.com/questions/40165766/returning-promises-from-vuex-actions
    refreshToken(context) {
      return new Promise((resolve, reject) => {
        axios
          .post(context.state.endPoints.refreshToken, {
            refresh: context.state.refreshToken,
          }) // send the stored refresh token to the backend API
          .then((response) => {
            // if API sends back new access and refresh token update the store
            console.log("New access successfully generated");
            context.commit("updateAccessToken", response.data.access);
            resolve(response.data.access);
          })
          .catch((err) => {
            console.log("Could not refresh token. Logging out.");
            context.dispatch("logoutUser");
            reject(err); // error generating new access and refresh token because refresh token has expired
          });
      });
    },

    registerUser(context, data) {
      return new Promise((resolve, reject) => {
        axios
          .post("/register/", {
            name: data.name,
            email: data.email,
            username: data.username,
            password: data.password,
            confirm: data.confirm,
          })
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },

    logoutUser(context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve) => {
          axios
            .post(context.state.endPoints.logout,{refresh_token:context.state.refreshToken})
            .then((response) => {
              context.commit("destroyTokens");
              console.log("Logout sucessful");
              resolve(response);///  // Let the calling function know that http is done. You may send some data back
              //https://stackoverflow.com/questions/40165766/returning-promises-from-vuex-actions
            })
            .catch((err) => {
              context.commit("destroyTokens");
              console.log(err);
              resolve(err);
            });
        });
      }
    },

    obtainTokens(context, credentials) {
      return new Promise((resolve, reject) => {
        /// agar koi async activity karte hai taab promise banate hai and return karte hai.. agar promise sucessful hoti hai taab resolve call karte hai aur unsucessful hone pe reject
        // send the username and password to the backend API:
        axios
          .post(context.state.endPoints.obtainToken, {
            username: credentials.username,
            password: credentials.password,
          })
          // if successful update local storage:
          .then((response) => {
            context.commit("updateTokens", {
              access: response.data.access,
              refresh: response.data.refresh,
            }); // store the access and refresh token in localstorage
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
  },
};
