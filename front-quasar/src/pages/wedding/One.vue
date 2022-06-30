<template>
  <q-page v-if="$state.$get('weddings.hasAccess')">
    <div
      class="row"
      style="
        margin-bottom: 8px;
        padding: 8px;
        color: #bb8d37;
        background-color: transparent;
      "
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
        <q-btn
          dense
          flat
          no-caps
          label="Weddings"
          @click="$router.push('/weddings')"
        />
        &nbsp;> &nbsp;
        <b>{{ $state.$get("weddings.wedding.name") }}</b>
      </div>
    </div>

    <q-tabs v-model="tab" dense style="color: #bb8d37">
      <q-tab
        no-caps
        name="images"
        icon="photo_library"
        label="Wedding Gallery"
      />
      <q-tab
        no-caps
        name="myimages"
        icon="contact_emergency"
        label="My Images"
      />
      <q-tab no-caps name="admin" icon="task_alt" label="Manage Images"
        v-if="$auth?.user?._id === $state.$get('weddings.wedding.user') || $state.$get('weddings.wedding.users', []).filter(f => f.email === $auth?.user?.email).some(s => s.is_admin)"
      />
      <q-tab no-caps name="acl" icon="lock" label="Access Control"
        v-if="$auth?.user?._id === $state.$get('weddings.wedding.user') || $state.$get('weddings.wedding.users', []).filter(f => f.email === $auth?.user?.email).some(s => s.is_admin)"
      />
      <q-tab no-caps name="details" icon="save_as" label="Wedding Details"
        v-if="$auth?.user?._id === $state.$get('weddings.wedding.user') || $state.$get('weddings.wedding.users', []).filter(f => f.email === $auth?.user?.email).some(s => s.is_admin)"
      />
    </q-tabs>

    <div class="q-pa-lg">
      <div v-show="tab === 'images'">all approved images</div>
      <div v-show="tab === 'myimages'">
        each user see and can manage its own images
      </div>
      <div v-show="tab === 'admin'">
        only owner and admins, can approve images, see separated per user,
        expansion item
      </div>
      <div v-show="tab === 'acl'">
        only owner and admins, can manage access control
      </div>
      <OneDetails v-show="tab === 'details'"></OneDetails>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

import OneDetails from './OneDetails.vue';

export default defineComponent({
  components: {
    OneDetails,
  },
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    if (!vm.$auth.isLogged()) vm.$router.push("/");

    vm.$state.$set("weddings.hasAccess", false);
    vm.$state.$set("weddings.wedding", null);
    vm.$api
      .request({
        method: "GET",
        url: `/weddings/${vm.$route.params.wedding}`,
        data: {},
      })
      .then((response) => {
        vm.$state.$set("weddings.hasAccess", true);
        vm.$state.$set("weddings.wedding", response.data);
      })
      .catch((error) => {
        console.error(error);
        vm.$router.push("/");
      });

    const tab = ref("images");

    return {
      tab,
    };
  },
});
</script>
