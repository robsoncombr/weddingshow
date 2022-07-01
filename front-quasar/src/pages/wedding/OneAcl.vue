<template>
  <div class="text-center q-pa-lg">
    <q-btn
      round
      size="sm"
      color="green"
      icon="add"
      @click="
        () => {
          one = $lib.lodash.cloneDeep(oneModel);
          oneMode = true;
        }
      "
      v-if="!oneMode"
    >
      <q-tooltip class="text-no-wrap"> Add a new User </q-tooltip>
    </q-btn>

    <div
      class="text-center q-pa-lg"
      v-if="!oneMode && !$state.$get('weddings.wedding.users', []).length"
    >
      No users yet, click on the button above to add one.
    </div>

    <div class="row justify-center" v-if="!oneMode && !$state.$get('weddings.wedding.users', []).length">
      <q-card class="card-info q-mt-xl" flat bordered>
        <q-card-section horizontal>
          <q-icon
            name="info"
            class="col-3 text-yellow-9"
            style="font-size: 40px"
          />
          <q-card-section style="font-size: 13px">
            <li>Allow users to see your wedding gallery and upload their images, by
            indicating their e-mail address.</li>
            <li>If you mark an user as admin, they will be able to manage the
            wedding and users as well.</li>
          </q-card-section>
        </q-card-section>
      </q-card>
    </div>
    <div v-if="oneMode">
      <q-btn
        outline
        size="sm"
        color="green"
        label="Save"
        style="font-size: 12px"
        class="q-ma-md"
        :disable="!one.email"
        @click="save()"
      />
      <q-btn
        outline
        size="sm"
        color="red-4"
        label="Cancel"
        class="q-ma-md"
        style="font-size: 12px"
        @click="oneMode = false"
      />
      <q-input v-model="one.email" label="User's e-mail" clearable />
      <q-checkbox v-model="one.is_admin" label="Admin" />
    </div>

    <div
      class="q-pa-lg text-left"
      v-if="$state.$get('weddings.wedding.users', []).length"
    >
      <table>
        <tr class="text-bold">
          <td>E-mail</td>
          <td>Admin</td>
          <td>Remove</td>
        </tr>
        <tr
          v-for="(user, index) in $state.$get('weddings.wedding.users', [])"
          :key="`users_${index}`"
        >
          <td>
            {{ user.email }}
          </td>
          <td>
            {{ user.is_admin ? "Yes" : "No" }}
          </td>
          <td width="1%">
            <q-btn
              flat
              round
              size="sm"
              color="red"
              icon="delete"
              style="font-size: 12px"
              @click="del(user.email)"
            />
          </td>
        </tr>
      </table>
    </div>
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

    return {};
  },
  data() {
    return {
      oneMode: false,
      oneModel: {
        email: "",
        is_admin: false,
      },
      one: {
        email: "",
        is_admin: false,
      },
    };
  },
  methods: {
    save() {
      const users = this.$lib.lodash.cloneDeep(
        this.$state.$get("weddings.wedding.users", [])
      );
      users.push(this.one);
      this.$api
        .request({
          method: "PUT",
          url: "/weddings/" + this.$state.$get("weddings.wedding._id"),
          data: {
            users,
          },
        })
        .then((r) => {
          this.$q.notify({
            message: "Access Control updated!",
            color: "positive",
          });
          this.oneMode = false;
          this.loadAll();
          this.loadOne();
        });
    },
    del(email) {
      const users = this.$lib.lodash.cloneDeep(
        this.$state
          .$get("weddings.wedding.users", [])
          .filter((f) => f.email !== email)
      );
      this.$api
        .request({
          method: "PUT",
          url: "/weddings/" + this.$state.$get("weddings.wedding._id"),
          data: {
            users,
          },
        })
        .then((r) => {
          this.$q.notify({
            message: "Access Control updated!",
            color: "positive",
          });
          this.oneMode = false;
          this.loadAll();
          this.loadOne();
        });
    },
  },
});
</script>

<style lang="sass" scoped>
.card-info
  width: 100%
  max-width: 500px
</style>
