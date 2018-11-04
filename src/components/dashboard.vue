<template>
<main role="main">
  <div class="container">
    <div class="row">
      <div class="col-sm">
        <div class="jumbotron text-center">
          <p class="text-muted">Your Total Calorie Consumption Today</p>
          {{cal}}
        </div>
      </div>
    </div>
    <div class="row text-center">
      <div class="col-sm">
        <button class="btn btn-primary btn-lg" @click="visualize()">Visualize Calorie Intake</button>
      </div>
      <div class="col-sm">
        <button class="btn btn-primary btn-lg" @click="openInventory()">Fridge Inventory</button>
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
import firebase from 'firebase'
import firebaseui from 'firebaseui'
import db from '@/firebase/init.js'
import axios from 'axios'
export default {
  name: 'dashboard',
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  data() {
    return {
      cal: null
    }
  },
  methods: {
    visualize: function(){

    },
    openInventory: function(){
      this.$router.push({
        name: "inventory"
      })
    }
  },
  async mounted() {
    var todayTime = new Date();
    var date = ("0" + (todayTime.getMonth() + 1).toString()).substr(-2) + ("0" + todayTime.getDate().toString()).substr(-2) + (todayTime.getFullYear().toString()).substr(2)
    let ref = await db.collection('users').doc(this.user.uid).get()
    this.cal = Math.round(Number((Object.values(ref.data().CalInt))));
  }
}
</script>
