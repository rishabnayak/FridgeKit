<template>
<main role="main">
  <div class="container">
    <div class="jumbotron text-center">
      <video class="embed-responsive" ref="video" autoplay playsinline></video>
      <canvas ref="canvas" width="640" height="480" hidden></canvas>
      <br>
      <button class="btn btn-success btn-lg" @click="takeimage()">Take Image</button>
      <br>
      <br>
      <div class="row">
        <div class="column col-sm">
          <button class="btn btn-warning" @click="choosefood(food1)">{{food1}}</button>
        </div>
        <div class="column col-sm">
          <button class="btn btn-warning" @click="choosefood(food2)">{{food2}}</button>
        </div>
        <div class="column col-sm">
          <button class="btn btn-warning" @click="choosefood(food3)">{{food3}}</button>
        </div>
        <div class="column col-sm">
          <button class="btn btn-warning" @click="choosefood(food4)">{{food4}}</button>
        </div>
      </div>
    </div>
  </div>

  <hr class="featurette-divider">

    <footer class="container">
        <p class="float-right"><a href="#">Back to top</a></p>
        <p>© 2018 FridgeKit · <a>
                <router-link :to="{ name: 'privacy'}">Privacy</router-link>
              </a></p>
      </footer>
</main>
</template>

<script>
const Clarifai = require('clarifai');
import firebase from 'firebase'
import firebaseui from 'firebaseui'
import db from '@/firebase/init.js'
import axios from 'axios'
const app = new Clarifai.App({
  apiKey: '1a542634ab0c4bbfab1dcb24afaddaf7'
});
export default {
  name: 'caloriecounter',
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  data() {
    return {
      video: null,
      canvas: null,
      food1: null,
      food2: null,
      food3: null,
      food4: null,
      check: null,
      cal: null
    }
  },
  methods: {
    async checkfx() {
      var todayTime = new Date();
      var date = ("0" + (todayTime.getMonth() + 1).toString()).substr(-2) + ("0" + todayTime.getDate().toString()).substr(-2) + (todayTime.getFullYear().toString()).substr(2)
      let ref = await db.collection('users').doc(this.user.uid).get()
      this.check = (ref.data().CalInt.hasOwnProperty(date));
      this.cal = (Object.values(ref.data().CalInt));
    },
    takeimage() {
      var CANVAS_WIDTH = this.canvas.width;
      var CANVAS_HEIGHT = this.canvas.height;
      var context = this.canvas.getContext('2d');
      let _this = this

      context.drawImage(_this.video, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
      var dataURI = this.canvas.toDataURL("image/png")
      var data = dataURI.split(',')
      app.models.predict(Clarifai.FOOD_MODEL, {
        base64: data[1]
      }).then(
        function(response) {
          // do something with response
          _this.food1 = response.outputs[0].data.concepts[0].name
          _this.food2 = response.outputs[0].data.concepts[1].name
          _this.food3 = response.outputs[0].data.concepts[2].name
          _this.food4 = response.outputs[0].data.concepts[3].name
        },
        function(err) {
          // there was an error
        }
      );
    },
    choosefood(food) {
      let _this = this
      axios.post('https://trackapi.nutritionix.com/v2/natural/nutrients', {
        "query": food
      }, {
        headers: {
          "x-app-id": "8a16bcd4",
          "x-app-key": "c0bdffe387238edff4c9cb14386f4e61"
        }
      }).then((response) => {
        let ref = db.collection('users').doc(this.user.uid)
        var todayTime = new Date();
        var date = ("0" + (todayTime.getMonth() + 1).toString()).substr(-2) + ("0" + todayTime.getDate().toString()).substr(-2) + (todayTime.getFullYear().toString()).substr(2)
        var calories = response.data.foods[0].nf_calories
        if (this.check == true) {
          calories = Number(this.cal) + Number(calories)
          ref.set({
            CalInt: {
              [date]: calories
            }
          }, {
            merge: true
          })
          this.checkfx()
        } else {
          ref.set({
            CalInt: {
              [date]: calories
            }
          }, {
            merge: true
          })
          this.checkfx()
        }
      })
    }
  },
  async mounted() {
    this.checkfx()
    this.video = this.$refs.video;
    this.canvas = this.$refs.canvas;
    if (navigator.mediaDevices) {
      navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: "environment",
            width: {
              exact: 640
            },
            height: {
              exact: 480
            }
          }
        }).then(stream => {
          this.video.srcObject = stream;
        })
        .catch(function(error) {
          document.body.textContent = 'Could not access the camera. Error: ' + error.name;
        });
    }
  }
}
</script>
