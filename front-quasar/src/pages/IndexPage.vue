<template>
  <q-page class="q-mt-xl">
    <div class="row">
      <div class="col-xs-12 text-center">
        <img
          alt="Wedding Show"
          src="~assets/logo.png"
          style="width: 250px; height: 250px"
        />
        <h5 style="margin: 0px">
          Sharing your memories with
          <br />
          control, privacy and security.
        </h5>
      </div>
      <div class="col-xs-12 row justify-center" style="margin-top: 30px">
        <q-btn
          no-caps
          color="green"
          class="row"
          style="width: 200px; height: 100px; margin: 20px"
          @click="$router.push('/auth/signup')"
        >
          <div class="col-xs-12" style="font-size: 15px">Need an account?</div>
          <div class="col-xs-12 text-bold bg-green-5" style="padding: 8px; font-size: 14px">Register</div>
        </q-btn>
        <q-btn
          no-caps
          color="blue"
          class="row"
          style="width: 200px; height: 100px; margin: 20px"
          @click="$router.push('/auth/signin')"
        >
          <div class="col-xs-12" style="font-size: 15px">I have an account</div>
          <div class="col-xs-12 text-bold bg-blue-5" style="padding: 8px; font-size: 14px">Login</div>
        </q-btn>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "IndexPage",
});
</script>
