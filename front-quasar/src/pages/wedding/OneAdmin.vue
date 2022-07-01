<template>
  <div class="q-pl-lg row justify-center">
    <div class="full-width row">
      <div
        class="col-xs-12 col-sm-6 col-md-4 col-lg-3"
        v-for="(image, index) in imagesAdmin"
        :key="`images_${index}`"
      >
        <q-card flat bordered class="full-height">
          <q-card-section v-if="image.thumb?.$binary?.base64">
            <q-img
              :src="`data:image/${image.filename.split('.')[1]};base64,${
                image.thumb.$binary.base64
              }`"
            />
          </q-card-section>
          <q-card-section class="full-height row">
            <div class="col-xs-6">
              <q-checkbox
                :model-value="image.is_approved"
                @update:model-value="
                  (v) => {
                    $api
                      .request({
                        method: 'POST',
                        url: `/weddings/${$state.$get(
                          'weddings.wedding._id'
                        )}/images/${image._id.$oid}/approve`,
                        data: {
                          is_approved: v,
                        },
                      })
                      .then((r) => (imagesAdmin[index] = r.data));
                  }
                "
                :label="image.is_approved ? 'Approved' : 'Not Approved'"
              ></q-checkbox>
            </div>
            <div class="col-xs-6 text-right">
              &nbsp;
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, getCurrentInstance, ref } from "vue";
import { useQuasar } from "quasar";

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
    const imagesAdmin = ref([]);

    return {
      uploadMode,
      imagesAdmin,
    };
  },
  methods: {
    loadimagesAdmin() {
      this.$api
        .request({
          method: "GET",
          url: `/weddings/${this.$route.params.wedding}/images/admin`,
          data: {},
        })
        .then((response) => {
          this.imagesAdmin = response.data;
        })
        .catch((error) => {
          console.error(error);
          this.imagesAdmin = [];
        });
    },
  },
  created() {
    this.loadimagesAdmin();
  },
});
</script>
