<template>
  <q-layout view="hHh lpr fFf" v-if="$state.$get('loadedUser')">
    <q-header
      bordered
      style="height: 80px; color: #d1aa62; background-color: #faf9f8"
      v-if="$auth?.isLogged()"
    >
      <q-toolbar style="min-height: unset">
        <q-btn
          flat
          dense
          icon="menu"
          aria-label="Menu"
          style="
            width: 45px;
            height: 45px;
            color: #000000;
            background-color: #d1aa62;
            margin-bottom: 8px;
            padding: 8px;
          "
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <img
            alt="Quasar logo"
            src="~assets/logo.png"
            style="width: 80px; height: 80px"
          />
        </q-toolbar-title>

        <div>
          <q-btn flat round>
            <q-icon name="account_circle" style="font-size: 45px"></q-icon>
            <q-popup-proxy>
              <q-list dense style="min-width: 250px; padding-bottom: 8px">
                <q-item-label header class="bg-grey-1 text-right text-bold">{{ $auth.user.email }}</q-item-label>
                <q-separator spaced />
                <q-item clickable v-ripple @click="$auth.logout(() => { $router.push('/') })">
                  <q-item-section>
                    <q-item-label>Sign Out</q-item-label>
                  </q-item-section>
                  <q-item-section thumbnail>
                    <q-icon name="logout" class="text-red" style="font-size: 30px"></q-icon>
                  </q-item-section>
                </q-item>
                <q-separator spaced />
              </q-list>
            </q-popup-proxy>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      v-if="$auth?.user"
    >
      <q-list>
        <q-item-label header> Menu Map </q-item-label>
        <q-item clickable to="/auth/signup">
          <q-item-label> Auth / Register </q-item-label>
        </q-item>
        <q-item clickable to="/auth/signin">
          <q-item-label> Auth / Login </q-item-label>
        </q-item>
        <q-item clickable to="/weddings">
          <q-item-label> Weddings Dashboard </q-item-label>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, getCurrentInstance, reactive, ref } from "vue";

export default defineComponent({
  name: "MainLayout",

  components: {},

  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    const $env = {
      // $dev atualmente baseado no hostname
      isDev: [
        "localhost",
        "127.0.0.1",
        "192.168.0.200",
        "192.168.16.200",
      ].includes(location.hostname),
    };
    app.appContext.config.globalProperties.$env = $env;

    const auth = reactive({
      token: null,
      user: null,
      isLogged: () => {
        return vm.$auth.token && vm.$auth.user;
      },
      setToken: async (token = null) => {
        if (!token) {
          token =
            vm.$q.sessionStorage.getItem("weddingshow_access_token") ||
            vm.$api.defaults.headers.common.Authorization?.split(" ")[1];
        }
        if (token) {
          vm.$q.sessionStorage.set("weddingshow_access_token", token);
          vm.$api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
          vm.$auth.token = token;
        } else {
          vm.$auth.logout();
        }
      },
      logout: async (cb) => {
        vm.$q.sessionStorage.remove("weddingshow_access_token");
        delete vm.$api.defaults.headers.common["Authorization"];
        vm.$auth.token = null;
        vm.$auth.user = null;
        if (typeof cb === "function") {
          cb();
        }
      },
      loadUser: async (cb = null) => {
        vm.$auth.setToken();
        //
        if (vm.$auth.token) {
          app.appContext.config.globalProperties.$auth.user = await vm.$api
            .request({
              method: "GET",
              url: "/auth/user",
              // headers: headers,
              data: {},
            })
            .then((r) => {
              // console.debug(r); // debug
              return r.data;
            })
            .catch((e) => {
              console.error(e);
              return null;
            });
        }
        //
        if (typeof cb === "function") {
          cb(vm.$auth.user);
        }
        //
        vm.$state.$set('loadedUser', true)
      },
      refreshToken: async () => {
        vm.$auth.setToken();
        //
        if (vm.$auth.token) {
          app.appContext.config.globalProperties.$auth.token = await vm.$api
            .request({
              method: "GET",
              url: "/auth/user/token_refresh",
              // headers: headers,
              data: {},
            })
            .then((r) => {
              // console.debug(r); // debug
              return r.data.token;
            })
            .catch((e) => {
              console.error(e);
              return null;
            });
        }
      },
    });
    app.appContext.config.globalProperties.$auth = auth;

    const state = reactive({
      data: {},
      $reset(data = {}) {
        app.appContext.config.globalProperties.$lib.setWith(
          app.appContext.config.globalProperties.$state,
          "data",
          data
        );
      },
      $set(target, value = {}) {
        if (!target) {
          /*
          app.appContext.config.globalProperties.$lib.x(
            "state.$set() !target"
          );
          */
        } else {
          app.appContext.config.globalProperties.$lib.setWith(
            app.appContext.config.globalProperties.$state,
            `data.${target}`,
            value
          );
        }
      },
      $get(target, defaultValue = null) {
        if (!target) {
          /*
          return app.appContext.config.globalProperties.$lib.$debug(
            "state.$get() !target"
          );
          */
        } else {
          return app.appContext.config.globalProperties.$lib.$get(
            app.appContext.config.globalProperties.$state,
            `data.${target}`,
            defaultValue
          );
        }
      },
      //
      loading: {},
      $doLoading(target = app.appContext.config.globalProperties.$route.path) {
        app.appContext.config.globalProperties.$lib.setWith(
          app.appContext.config.globalProperties.$state,
          `loading.${target}`,
          true
        );
      },
      $isLoading(target = app.appContext.config.globalProperties.$route.path) {
        return app.appContext.config.globalProperties.$lib.$get(
          app.appContext.config.globalProperties.$state,
          `loading.${target}`,
          false
        );
      },
      $doneLoading(
        target = app.appContext.config.globalProperties.$route.path
      ) {
        app.appContext.config.globalProperties.$lib.setWith(
          app.appContext.config.globalProperties.$state,
          `loading.${target}`,
          false
        );
      },
    });
    app.appContext.config.globalProperties.$state = state;

    const leftDrawerOpen = ref(false);

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },

  created() {
    /*
    if (this.$env.isDev) {
      window.wedding = this
    }
    */
    // i will leave this instance in production for demonstration needs during the process, but it is not recommended for real production
    window.wedding = this;

    // always load user info on create to initialize the ui
    this.$auth.loadUser();
  },
});
</script>
