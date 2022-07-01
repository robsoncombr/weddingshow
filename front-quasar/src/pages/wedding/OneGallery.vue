<template>
  <div class="q-pl-lg row justify-center">
    <div class="full-width row">
      <div class="col-xs-12 q-ma-lg text-center" v-if="!imagesGallery.length">
        <b>No images yet.</b>
        <br><br>
        Upload images and approve them to fill the gallery.
      </div>
      <div
        class="col-xs-12 col-sm-6 col-md-4 col-lg-3"
        v-for="(image, index) in imagesGallery"
        :key="`images_${index}`"
      >
        <q-card flat bordered class="full-height">
          <q-card-section v-if="image.thumb?.$binary?.base64">
            <q-img
              :src="`data:image/${image.filename.split('.')[1]};base64,${
                image.thumb.$binary.base64
              }`"
              class="cursor-pointer"
              @click="zoomIn(image)"
            />
            <q-tooltip>
              Zoom In
            </q-tooltip>
          </q-card-section>
          <q-card-section class="full-height row">
            <div class="col-xs-6">
              <q-rating
                :model-value="
                  $lib.$get(image, 'ratings', []).find(f => f.user === $auth.user._id)?.rating || 0
                "
                @update:model-value="
                  (v) => {
                    $api
                      .request({
                        method: 'POST',
                        url: `/weddings/${$state.$get(
                          'weddings.wedding._id'
                        )}/images/${image._id.$oid}/rating`,
                        data: {
                          rating: v,
                        },
                      })
                      .then((r) => (imagesGallery[index] = r.data));
                  }
                "
                size="1.5em"
                color="grey"
                :color-selected="[
                  'yellow-4',
                  'yellow-5',
                  'yellow-6',
                  'yellow-7',
                  'yellow-8',
                ]"
              >
              </q-rating>
              <span class="text-bold text-yellow-10 q-ml-xs">
                (
                {{
                  $lib
                    .$get(image, "ratings", [])
                    .reduce((a, n) => a + n.rating, 0) /
                    $lib.$get(image, "ratings", []).length || 0
                }}
                )
              </span>
            </div>
            <div class="col-xs-6 text-right">
              <q-btn
                round
                outline
                size="sm"
                color="blue"
                icon="chat"
                style="top: -6px; font-size: 12px"
              >
              <q-tooltip>
                Join Conversation
              </q-tooltip>
              </q-btn>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
  <q-dialog
    v-model="zoomShow"
    @show="zoomLoad(zoomImageThumb)"
  >
    <q-img :src="zoomImage" class="bg-white" />
  </q-dialog>
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
    const imagesGallery = ref([]);
    const zoomShow = ref(false);
    const zoomImageThumb = ref(null);
    const zoomImage = ref(null);

    return {
      uploadMode,
      imagesGallery,
      zoomShow,
      zoomImageThumb,
      zoomImage,
    };
  },
  methods: {
    loadimagesGallery() {
      this.$api
        .request({
          method: "GET",
          url: `/weddings/${this.$route.params.wedding}/images`,
          data: {},
        })
        .then((response) => {
          this.imagesGallery = response.data;
        })
        .catch((error) => {
          console.error(error);
          this.imagesGallery = [];
        });
    },
    zoomIn(image) {
      this.zoomImage = null
      this.zoomImageThumb = image
      this.zoomShow = true
    },
    zoomLoad(imageThumb) {
      this.$api
        .request({
          method: "GET",
          url: `/weddings/${this.$route.params.wedding}/images/${imageThumb._id.$oid}`,
          data: {},
        })
        .then((response) => {
          this.zoomImage = response.data;
        })
        .catch((error) => {
          console.error(error);
          this.zoomImage = null;
        });
    },
  },
  created() {
    this.loadimagesGallery();
  },
});
</script>
