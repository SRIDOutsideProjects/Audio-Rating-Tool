  
<template>
<div>
  <v-card
    :loading="loading"
    class="mx-auto my-12"
    max-width="374"
    elevation="6"
  >
      <template>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="username"
                  label="User Name"
                  :rules="rules"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  type="password"
                  label="Password"
                  :rules="rules"
                  required
                ></v-text-field>
                <v-btn
                  class="mr-4"
                  :disabled="!valid"
                  @click="loginUser()"
                  color="primary"
                >
                  Login
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </template>
  </v-card>
</div>
</template>

<script>
  export default {
    name: 'login',

    data () {
      return {
        username: '',
        password: '',
      loading:false,
      valid:false,
        wrongCred: false ,// activates appropriate message if set to true
        rules: [
        value => !!value || 'Required.',
      ],
      }
    },
    methods: {
      loginUser () { // call loginUSer action
        this.$store.dispatch('auth/obtainTokens', {  /// because it is in nested Module
          username: this.username,
          password: this.password
        })
            .then(() => {
              this.wrongCred = false
              this.$router.push({ name: 'rating' })
              console.log("sucessful Login and redirected to home")
            })
          .catch(err => {
            console.log(err)
            this.wrongCred = true // if the credentials were wrong set wrongCred to true
          })
        }
      }
  }
</script>