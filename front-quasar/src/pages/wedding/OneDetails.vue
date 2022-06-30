<template>
  <div>
    <q-input
      :modelValue="$state.$get('weddings.wedding.name')"
      @update:modelValue="$state.$set('weddings.wedding.name', $event)"
    />
    <q-btn
      label="Save"
      @click="
        () => {
          $api.request({
            method: 'PUT',
            url: '/weddings/' + $state.$get('weddings.wedding._id'),
            data: {
              name: $state.$get('weddings.wedding.name'),
              users: $state.$get('weddings.wedding.users', []),
            },
          }).then((r) => {
            $q.notify({ message: 'Wedding updated!', color: 'positive' });
            loadAll();
          });
        }
      "
    />
  </div>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    vm.$state.$set("weddings.all", []);
    const loadAll = async () => {
      vm.$api
        .request({
          method: "GET",
          url: '/weddings',
          data: {},
        })
        .then((response) => {
          vm.$state.$set("weddings.all", response.data);
        })
        .catch((error) => {
          console.error(error);
          vm.$router.push("/");
        });
    }

    return {
      loadAll,
    };
  },
});
</script>
