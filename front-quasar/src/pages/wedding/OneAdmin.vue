<template>
  <div class="q-pl-lg row justify-center">
    <div class="full-width row">
      <div class="col-xs-12 q-ma-lg text-center" v-if="!imagesAdmin.length">
        <b>No images yet.</b>
        <br /><br />
        Upload images to fill the gallery.
      </div>

      <q-list class="col-xs-12">
        <q-expansion-item
          expand-separator
          icon="perm_identity"
          group="users"
          :label="user_email"
          :caption="`${imagesAdminGrouped[user_email].length} image(s)`"
          v-for="user_email in Object.keys(imagesAdminGrouped)"
          :key="user_email"
        >
          <template v-slot:header>
            <div class="full-width bg-grey-2 row q-pa-sm">
              <q-item-section avatar>
                <q-icon name="photo" class="text-yellow-10" />
              </q-item-section>

              <q-item-section>
                {{ user_email }}
              </q-item-section>

              <q-item-section side>
                <div class="row items-center">
                  {{ imagesAdminGrouped[user_email].length }} image(s) / {{ imagesAdminGrouped[user_email].filter(f => f.is_approved).length }} approved
                </div>
              </q-item-section>
            </div>
          </template>
          <div class="full-width row">
            <div
              class="col-xs-12 col-sm-6 col-md-4 col-lg-3"
              v-for="image in imagesAdminGrouped[user_email]"
              :key="image._id.$oid"
            >
              <q-card flat bordered class="full-height" v-if="image.thumb?.$binary?.base64">
                <q-card-section>
                  <q-img
                    :src="`data:image/${image.filename.split('.')[1]};base64,${
                      image.thumb.$binary.base64
                    }`"
                  />
                </q-card-section>
                <q-card-section class="full-height row">
                  <div class="col-xs-6">
                    <q-checkbox
                      v-model="image.is_approved"
                      @update:model-value="
                        (v) => {
                          $state.$doLoading();
                          $api
                            .request({
                              method: 'POST',
                              url: `/weddings/${$state.$get(
                                'weddings.wedding._id'
                              )}/images/${image._id.$oid}/approve`,
                              data: {
                                is_approved: v,
                              },
                            }).finally(() => $state.$doneLoading());
                        }
                      "
                      :label="image.is_approved ? 'Approved' : 'Not Approved'"
                    ></q-checkbox>
                  </div>
                  <div class="col-xs-6 text-right">&nbsp;</div>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </q-expansion-item>
      </q-list>
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
  computed: {
    imagesAdminGrouped() {
      return this.imagesAdmin.reduce((group, image) => {
        const { user_email } = image;
        group[user_email] = group[user_email] ?? [];
        group[user_email].push(image);
        return group;
      }, {});
    },
  },
  methods: {
    loadimagesAdmin() {
      this.$state.$doLoading()
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
        })
        .finally(() => this.$state.$doneLoading());
    },
  },
  created() {
    this.loadimagesAdmin();
  },
});
</script>
