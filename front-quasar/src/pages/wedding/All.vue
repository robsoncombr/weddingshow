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
        <b>Weddings</b>
      </div>
    </div>

    List and Add
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    if (!vm.$auth.isLogged()) vm.$router.push("/");

    return {
    };
  },
});
</script>
