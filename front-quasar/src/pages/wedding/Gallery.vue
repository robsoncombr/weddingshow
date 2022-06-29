<template>
  <q-page>
    <div
      class="row"
      style="padding: 8px; color: #bb8d37; background-color: transparent"
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

    <div>
      - button to manage users with access, I will use only the e-mail to match
      as the ACL in back-end - Users.vue
      <br /><br />
      - gallery with list of pictures - upload button that opens a Dialog -
      Upload.vue
      <br /><br />
      - tab 1: approved pictures - GalleryApproved.vue
      <br />
      - tab2: your pictures - pictures that was sent by the user, approved or
      not - GalleryUser.vue
      <br />
      - when click on a image open a Dialog - Zoom.vue
    </div>
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    if (!vm.$auth.isLogged()) vm.$router.push("/");

    return {};
  },
});
</script>
