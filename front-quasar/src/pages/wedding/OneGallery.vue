<template>
  <div class="q-pl-lg row justify-center">
    <div class="full-width row">
      <div class="col-xs-12 q-ma-lg text-center" v-if="!imagesGallery.length">
        <b>No images yet.</b>
        <br /><br />
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
            <q-tooltip> Zoom In </q-tooltip>
          </q-card-section>
          <q-card-section class="full-height row">
            <div class="col-xs-7">
              <q-rating
                :model-value="
                  $lib
                    .$get(image, 'ratings', [])
                    .find((f) => f.user === $auth.user._id)?.rating || 0
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
                size="1.20em"
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
              <span
                class="text-bold text-yellow-10 q-ml-xs text-no-wrap"
                style="font-size: 12px"
              >
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
            <div class="col-xs-5 text-right">
              <q-btn-dropdown
                flat
                dense
                size="sm"
                color="blue"
                icon="chat"
                style="top: -3px; font-size: 12px"
              >
                <div
                  class="row no-wrap q-pa-md bg-grey-2"
                  style="min-width: 350px; border: 1px solid #9e9e9e"
                >
                  <div class="column">
                    <div class="text-h6 q-mb-md">Messages</div>
                    <q-input
                      clearable
                      counter
                      v-model="leaveMessage"
                      label="Type a message"
                      type="text"
                      maxlength="150"
                    >
                      <template v-slot:append>
                        <q-btn
                          flat
                          dense
                          color="blue"
                          icon="send"
                          :disable="!leaveMessage"
                          @click="
                            $api
                              .request({
                                method: 'POST',
                                url: `/weddings/${$state.$get(
                                  'weddings.wedding._id'
                                )}/images/${image._id.$oid}/messages`,
                                data: {
                                  message: leaveMessage,
                                },
                              })
                              .then((r) => (imagesGallery[index] = r.data))
                              .finally(() => leaveMessage = null)
                          "
                        />
                      </template>
                    </q-input>
                    <div class="q-mb-md">
                      <div class="full-width flex flex-center text-orange-9" v-if="!$lib.$get(image, 'messages', []).length">
                        Be the first to send a message to this image.
                      </div>
                      <q-chat-message
                        :name="message.user_email"
                        :text="[message.message, message.date]"
                        :stamp="message.date.format('YYYY/MM/DD HH:mm:ss')"
                        text-color="white"
                        bg-color="primary"
                        class="full-width"
                        v-for="(message, index) in $lib.$get(image, 'messages', []).map(m => { return { ...m, date: $lib.moment(m.date.$date) } }).sort((a, b) => b.date - a.date)"
                        :key="`messages_${index}`"
                      />
                    </div>
                  </div>
                </div>
              </q-btn-dropdown>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
  <q-dialog v-model="zoomShow" @show="zoomLoad(zoomImageThumb)">
    <div
      class="flex flex-center bg-white"
      style="min-width: 90vw; min-height: 90vh"
    >
      <q-btn
        icon="close"
        label="Close"
        class="fixed-top bg-grey-8 text-white"
        @click="zoomShow = false"
      />
      <img :src="zoomImage" class="bg-white fit" />
    </div>
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
    const leaveMessage = ref("");

    return {
      uploadMode,
      imagesGallery,
      zoomShow,
      zoomImageThumb,
      zoomImage,
      leaveMessage,
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
      this.zoomImage = null;
      this.zoomImageThumb = image;
      this.zoomShow = true;
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
