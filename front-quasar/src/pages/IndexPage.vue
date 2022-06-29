<template>
  <q-page class="q-mt-xl">
    <div id="log"></div>
    <br />
    <form id="form">
      <label for="text">Input: </label>
      <input type="text" id="text" autofocus />
    </form>
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
      <div
        class="col-xs-12 row justify-center"
        style="margin-top: 30px"
        v-if="!$auth?.isLogged()"
      >
        <q-btn
          no-caps
          color="green"
          class="row"
          style="width: 200px; height: 100px; margin: 20px"
          @click="$router.push('/auth/signup')"
        >
          <div class="col-xs-12" style="font-size: 15px">Need an account?</div>
          <div
            class="col-xs-12 text-bold bg-green-5"
            style="padding: 8px; font-size: 14px"
          >
            Register
          </div>
        </q-btn>
        <q-btn
          no-caps
          color="blue"
          class="row"
          style="width: 200px; height: 100px; margin: 20px"
          @click="$router.push('/auth/signin')"
        >
          <div class="col-xs-12" style="font-size: 15px">I have an account</div>
          <div
            class="col-xs-12 text-bold bg-blue-5"
            style="padding: 8px; font-size: 14px"
          >
            Login
          </div>
        </q-btn>
      </div>
      <div class="col-xs-12 row justify-center" style="margin-top: 30px" v-else>
        <q-btn
          no-caps
          color="orange-1"
          class="row text-orange-10"
          style="width: 300px; height: 100px; margin: 20px"
          @click="$router.push('/auth/signin')"
        >
          <div class="col-xs-12" style="font-size: 15px">
            You are already logged in
          </div>
          <div
            class="col-xs-12 text-bold bg-orange-2"
            style="padding: 8px; font-size: 14px"
            @click="$router.push('/weddings')"
          >
            Go to Weddings Dashboard
          </div>
        </q-btn>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "IndexPage",

  mounted() {
    const log = (text, color) => {
      document.getElementById(
        "log"
      ).innerHTML += `<span style="color: ${color}">${text}</span><br>`;
    };

    // const socket = new WebSocket("ws://" + location.host + "/echo");
    const socket = new WebSocket("ws://" + location.hostname + ":5000/ws/echo");

    socket.addEventListener("message", (ev) => {
      log("<<< " + ev.data, "blue");
    });
    document.getElementById("form").onsubmit = (ev) => {
      ev.preventDefault();
      const textField = document.getElementById("text");
      log(">>> " + textField.value, "red");
      socket.send(textField.value);
      textField.value = "";
    };
  },
});
</script>
