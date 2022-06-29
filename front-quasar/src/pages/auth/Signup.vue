<template>
  <q-page>
    <q-form>
      <q-input
        label="Name"
        name="name"
        v-model="name"
        type="text"
        placeholder="Name"
      />
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
      <q-btn color="primary" @click="signup">Signup</q-btn>
    </q-form>
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    const name = ref("r");
    const email = ref("r@r.r");
    const password = ref("test");

    const signup = () => {
      // console.log(name, email, password); // debug

      vm.$api
        .request({
          method: "POST",
          url: "/auth/signup",
          data: {
            name: name.value,
            email: email.value,
            password: password.value,
          },
        })
        .then((response) => {
          // console.log(response); // debug
          vm.$q.sessionStorage.set(
            "weddingshow_access_token",
            response.data.token
          );
          vm.$api.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${response.data.token}`;
          vm.$auth.user = response.data.user;
          // const token_decoded = vm.$lib.jwtParse(response.data.token);
        })
        .catch((error) => {
          console.log(error); // debug
          vm.$q.sessionStorage.remove("weddingshow_access_token");
          delete vm.$api.defaults.headers.common["Authorization"];
        });
    };

    return {
      name,
      email,
      password,
      signup,
    };
  },
});
</script>
