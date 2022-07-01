<template>
  <div class="q-pl-lg row justify-center">
    <q-btn
      rounded outline
      size="sm"
      color="green"
      icon="upload"
      label="Upload Images"
      style="font-size: 12px"
      @click="uploadMode = true"
    />
    <q-dialog v-model="uploadMode">
      <q-uploader
        multiple
        batch
        :url="`${$api.defaults.baseURL}/weddings/${$route.params.wedding}/images/upload`"
        :headers="[{ name: 'Authorization', value: `Bearer ${$auth.token}` }]"
        label="Select Your Images! - Batch upload, max file size 5MB"
        max-file-size="5620000"
        accept=".jpg, .jpeg, .gif, .png"
        color="green-6"
        class="full-width"
        @finish="onFinish"
        @rejected="onRejected"
      />
    </q-dialog>

    <div class="full-width q-mt-lg row">
      <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3" v-for="(image, index) in imagesUser" :key="`images_${index}`">
        <q-card flat bordered>
          <q-card-section>
            {{ `data:image/jpg;base64,${image.thumb}` }}
            <!--
            <q-img
              :src="`${$api.defaults.baseURL}/weddings/${$route.params.wedding}/images/${image.id}/thumbnail`"
              class="full-width"
            />
            -->
          </q-card-section>
          <q-card-section>
            <q-btn
              color="red-4"
              icon="delete"
              @click="deleteImage(image.id)"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>
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
    const app = getCurrentInstance();
    const vm = app.appContext.config.globalProperties;
    const $q = useQuasar();

    const uploadMode = ref(false);
    const imagesUser = ref([]);

    return {
      uploadMode,
      imagesUser,
    };
  },
  methods: {
    onFinish (e) {
      this.$q.notify({ message: 'Image(s) uploaded!', color: 'positive' });
      this.uploadMode = false;
      this.loadAll();
      this.loadOne();
      this.loadImagesUser();
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
      })
    },
    loadImagesUser () {
      this.$api
        .request({
          method: "GET",
          url: `/weddings/${this.$route.params.wedding}/images/user`,
          data: {},
        })
        .then((response) => {
          this.imagesUser = response.data;
        })
        .catch((error) => {
          console.error(error);
          this.imagesUser = [];
        });
    },
    deleteImage (id) {
      this.$api
        .request({
          method: "DELETE",
          url: `/weddings/${this.$route.params.wedding}/images/${id}`,
          data: {},
        })
        .then((response) => {
          this.$q.notify({ message: 'Image deleted!', color: 'positive' });
          this.loadAll();
          this.loadOne();
          this.loadImagesUser();
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created () {
    this.loadImagesUser();
  },
});
</script>
