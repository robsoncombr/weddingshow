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
        @click="$state.$get('wedings.methods.loadGallery', () => {})()"
      />
      <q-tab
        no-caps
        name="myimages"
        icon="upload"
        label="Your Gallery"
        @click="$state.$get('wedings.methods.loadGalleryUser', () => {})()"
      />
      <q-tab
        no-caps
        name="admin"
        icon="task_alt"
        label="Manage Images"
        @click="$state.$get('wedings.methods.loadAdmin', () => {})()"
        v-if="
          $auth?.user?._id === $state.$get('weddings.wedding.user') ||
          $state
            .$get('weddings.wedding.users', [])
            .filter((f) => f.email === $auth?.user?.email)
            .some((s) => s.is_admin)
        "
      />
      <q-tab
        no-caps
        name="acl"
        icon="lock"
        label="Access Control"
        @click="$state.$get('wedings.methods.loadOne', () => {})()"
        v-if="
          $auth?.user?._id === $state.$get('weddings.wedding.user') ||
          $state
            .$get('weddings.wedding.users', [])
            .filter((f) => f.email === $auth?.user?.email)
            .some((s) => s.is_admin)
        "
      />
      <q-tab
        no-caps
        name="details"
        icon="save_as"
        label="Wedding Details"
        @click="$state.$get('wedings.methods.loadOne', () => {})()"
        v-if="
          $auth?.user?._id === $state.$get('weddings.wedding.user') ||
          $state
            .$get('weddings.wedding.users', [])
            .filter((f) => f.email === $auth?.user?.email)
            .some((s) => s.is_admin)
        "
      />
    </q-tabs>

    <div class="q-pa-lg">
      <OneGallery
        :loadAll="loadAll"
        :loadOne="loadOne"
        v-if="tab === 'images'"
      />
      <OneGalleryUser
        :loadAll="loadAll"
        :loadOne="loadOne"
        v-if="tab === 'myimages'"
      ></OneGalleryUser>
      <OneAdmin
        :loadAll="loadAll"
        :loadOne="loadOne"
        v-if="tab === 'admin'"
      ></OneAdmin>
      <OneAcl
        :loadAll="loadAll"
        :loadOne="loadOne"
        v-if="tab === 'acl'"
      ></OneAcl>
      <OneDetails
        :loadAll="loadAll"
        :loadOne="loadOne"
        v-if="tab === 'details'"
      ></OneDetails>
    </div>
    <q-page-scroller position="bottom-right" :scroll-offset="50" :offset="[18, 18]">
      <q-btn fab icon="keyboard_arrow_up" color="primary" />
    </q-page-scroller>
  </q-page>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

import OneGallery from "./OneGallery.vue";
import OneGalleryUser from "./OneGalleryUser.vue";
import OneAdmin from "./OneAdmin.vue";
import OneAcl from "./OneAcl.vue";
import OneDetails from "./OneDetails.vue";

export default defineComponent({
  components: {
    OneGallery,
    OneGalleryUser,
    OneAdmin,
    OneAcl,
    OneDetails,
  },
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    if (!vm.$auth.isLogged()) vm.$router.push("/");

    vm.$state.$set("weddings.hasAccess", false);
    vm.$state.$set("weddings.wedding", null);
    const loadOne = async () => {
      vm.$state.$doLoading();
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
        })
        .finally(() => vm.$state.$doneLoading());
    };
    loadOne();

    const loadAll = async () => {
      vm.$api
        .request({
          method: "GET",
          url: "/weddings",
          data: {},
        })
        .then((response) => {
          vm.$state.$set("weddings.all", response.data);
        })
        .catch((error) => {
          console.error(error);
          vm.$router.push("/");
        });
    };

    const tab = ref("images");

    return {
      loadAll,
      loadOne,
      tab,
    };
  },
});
</script>
