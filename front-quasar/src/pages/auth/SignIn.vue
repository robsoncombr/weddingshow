<template>
  <q-page>
    <div
      class="row"
      style="margin-bottom: 8px; padding: 8px; color: #bb8d37; background-color: transparent"
    >
      <div class="flex flex-center">
        <q-btn
          dense
          flat
          no-caps
          icon="home"
          label="Home"
          @click="$router.push('/')"
        />
        &nbsp;> &nbsp;
        <b>Login</b>
      </div>
    </div>

    <div class="row">
      <div class="col-xs-12 text-center">
        <img
          alt="Wedding Show"
          src="~assets/logo.png"
          style="width: 250px; height: 250px"
        />
        <h5 style="margin: 0px">
          Sharing your memories with
          <br />
          control, privacy and security.
        </h5>
      </div>
      <div
        class="col-xs-12 row justify-center"
        style="margin-top: 30px"
        v-if="!$auth?.isLogged()"
      >
        <q-form>
          <b>Welcome back!</b>
          <q-input
            label="Email"
            name="email"
            v-model="email"
            type="email"
            placeholder="Email"
          />
          <q-input
            label="Password"
            name="password"
            v-model="password"
            type="password"
            placeholder="Password"
          />
          <div class="q-ma-lg">
            <q-btn no-caps color="primary" @click="signin">Login</q-btn>
            <q-btn
              flat
              no-caps
              label="I need to create an account"
              class="text-green-8 q-ml-md"
              style="text-decoration: underline"
              @click="$router.push('/auth/signup')"
            ></q-btn>
          </div>
        </q-form>
      </div>
      <div class="col-xs-12 row justify-center" style="margin-top: 30px" v-else>
        <q-btn
          no-caps
          color="orange-1"
          class="row text-orange-10"
          style="width: 300px; height: 100px; margin: 20px"
          @click="$router.push('/weddings')"
        >
          <div class="col-xs-12" style="font-size: 15px">
            You are already logged in
          </div>
          <div
            class="col-xs-12 text-bold bg-orange-2"
            style="padding: 8px; font-size: 14px"
          >
            Go to Weddings Dashboard
          </div>
        </q-btn>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    const email = ref("robson@robson.com.br");
    const password = ref("test");

    const signin = () => {
      // console.log(email, password); // debug

      vm.$api
        .request({
          method: "POST",
          url: "/auth/signin",
          data: {
            email: email.value,
            password: password.value,
          },
        })
        .then((response) => {
          // console.log(response); // debug
          vm.$auth.setToken(response.data.token);
          vm.$auth.loadUser(() => {
            vm.$router.push("/weddings");
          });
        })
        .catch((error) => {
          console.log(error); // debug
          vm.$q.notify({ message: error?.response?.data || 'Error', color: "negative" });
          vm.$auth.logout();
        });
    };

    return {
      email,
      password,
      signin,
    };
  },
});
</script>
