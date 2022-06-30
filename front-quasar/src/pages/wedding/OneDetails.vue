<template>
  <div class="q-pl-lg">
    <q-input
      :modelValue="$state.$get('weddings.wedding.name')"
      @update:modelValue="$state.$set('weddings.wedding.name', $event)"
      label="Name"
    />
    <q-btn
      color="green"
      label="Save"
      class="q-ma-md"
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
            loadOne();
          });
        }
      "
    />
  </div>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";

export default defineComponent({
  props: {
    loadAll: {
      type: Function,
      required: true,
    },
    loadOne: {
      type: Function,
      required: true,
    },
  },
  setup() {
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    return {
    };
  },
});
</script>
