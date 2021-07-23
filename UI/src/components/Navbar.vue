<template>
      <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Samsung Logo"
          class="shrink mr-2"
          contain
          :src="require('@/assets/logo.png')"
          transition="scale-transition"
          width="100"
        />
            <v-btn v-if="this.$store.getters['auth/loggedIn']" right absolute @click="logout()">logout</v-btn>
      </div>
    </v-app-bar>
</template>

<script>
export default {
    methods: {
        logout(){
      this.$store.dispatch('auth/logoutUser')
        .then((res) => {
          console.log(res);
          console.log("Logged Out Sucessfuly")
          this.$router.push({ name: 'login' })
        })
        .catch(err=>{
            console.log(err);
            this.$router.push({ name: 'login' });
        })
    }
}
}
</script>
