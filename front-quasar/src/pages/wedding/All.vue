<template>
  <q-page>
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
        <b>Weddings</b>
        &nbsp;
        <q-btn dense flat round icon="refresh" @click="loadAll()"
          ><q-tooltip>Reload List</q-tooltip></q-btn
        >
      </div>
    </div>
    <div class="q-pl-lg">
      <q-btn
        no-caps
        size="sm"
        color="blue"
        label="Add a New Wedding"
        style="font-size: 12px"
        @click="
          () => {
            $q.dialog({
              title: 'Creating Wedding',
              message: 'Pick your best name for this moment.',
              prompt: {
                model: '',
                type: 'text', // optional
              },
              cancel: true,
              persistent: true,
            })
              .onOk((data) => {
                $api
                  .request({
                    method: 'POST',
                    url: '/weddings',
                    data: {
                      name: data,
                      users: [],
                    },
                  })
                  .then((r) => {
                    $q.notify({
                      message: 'Wedding created!',
                      color: 'positive',
                    });
                    loadAll();
                    $router.push('/weddings/' + r.data._id);
                  });
              })
              .onCancel(() => {
                // console.log('>>>> Cancel')
              })
              .onDismiss(() => {
                // console.log('I am triggered on both OK and Cancel')
              });
          }
        "
      />
    </div>
    <div class="q-pa-lg">
      <div
        class="q-mt-md"
        v-for="(wedding, index) in $state.$get('weddings.all', [])"
        :key="`weddings_${index}`"
      >
        <q-btn
          no-caps
          rounded
          size="sm"
          style="font-size: 12px"
          @click="$router.push(`/weddings/${wedding._id.$oid}`)"
          >View</q-btn
        >
        {{ wedding.name }} -
        {{
          wedding.user.$oid === $auth.user._id
            ? "(owner)"
            : wedding.users.find((f) => f.email === $auth.user.email).is_admin
            ? "(admin)"
            : "(guest)"
        }}
        <br />
        {{ new Date(wedding.dt_created.$date) }}
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

    if (!vm.$auth.isLogged()) vm.$router.push("/");

    vm.$state.$set("weddings.all", []);
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
    loadAll();

    return {
      loadAll,
    };
  },
});
</script>
