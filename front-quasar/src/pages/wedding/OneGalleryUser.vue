<template>
  <q-dialog v-model="uploadMode">
    <q-uploader
      multiple
      batch
      :url="`${$api.defaults.baseURL}/weddings/${$route.params.wedding}/images`"
      :headers="[{ name: 'Authorization', value: `Bearer ${$auth.token}` }]"
      label="Select Your Images! - Batch upload, max file size 5MB"
      max-file-size="5620000"
      accept=".jpg, .jpeg, .gif, .png"
      color="green-6"
      class="full-width"
      @rejected="onRejected"
    />
  </q-dialog>
  <div class="q-pl-lg row justify-center">
    <q-btn
      rounded outline
      color="green"
      icon="upload"
      label="Upload Images"
      @click="uploadMode = true"
    />
  </div>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";
import { useQuasar } from 'quasar'

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
    const $q = useQuasar()
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;

    const uploadMode = ref(false);

    function onRejected (rejectedEntries) {
      // Notify plugin needs to be installed
      // https://quasar.dev/quasar-plugins/notify#Installation
      $q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
      })
    }

    return {
      uploadMode,
      onRejected,
    };
  },
});
</script>
