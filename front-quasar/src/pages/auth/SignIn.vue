<template>
  <q-page>
    <q-form>
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
      <q-btn color="primary" @click="signin">Signin</q-btn>
    </q-form>
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    const email = ref("r@r.r");
    const password = ref("test");

    const signin = () => {
      // console.log(email, password); // debug

      vm.$api.request({
        method: "POST",
        url: "/auth/signin",
        data: {
          email: email.value,
          password: password.value,
        }
      })
        .then(response => {
          // console.log(response); // debug
          vm.$auth.setToken(response.data.token);
          vm.$auth.loadUser();
        })
        .catch(error => {
          console.log(error); // debug
          vm.$q.notify({ message: error?.response?.data, color: 'negative' });
          vm.$auth.logout();
        });
    };

    return {
      email,
      password,
      signin
    };
  }
});
</script>
