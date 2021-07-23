import Vue from "vue";
import Router from "vue-router";
import store from "@/store"; // by default index.js leta hai
import Auth from "@/components/Auth";

Vue.use(Router);
import auth from "./auth"; // This will import array exported in auth.js
import rating from "./rating";

const router = new Router({
  mode: "history",
  routes: [
    {
      path: "/auth",
      component: Auth, // agar sirf /auth dala too yee component open hoga else agar /auth/login daala too chidren wala open hoga
      children: auth,
    },
 // spread operator jo sare dicts joo audio array me hai unko bahar kaar dega
    ...rating
  ],
});

router.beforeEach((to, from, next) => {
  // if any of the routes in ./router.js has a meta named 'requiresAuth: true'
  // then check if the user is logged in before routing to this path:
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.getters["auth/loggedIn"]) {
      ///kyun ki Logged in getter auth module me hai
      next({ path: "/auth/login" });
    } else {
      next();
    }
  } else {
    next(); /// agar kuch pass nhi kiye too joo url pehle bheja tha wahi chal jaenge
  }
});

export default router;
