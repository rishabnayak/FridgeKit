<template>
<main role="main">
  <div class="container">
    <div class="jumbotron">
      <h2 class="text-center"> Fridge Inventory</h2>
    </div>
    <masonry :cols="{default: 3, 991: 2, 767: 1}" :gutter="{default: '30px', 767: '15px'}">
      <div v-for="stuff in inventory" :key="stuff.id" class="card mb-4 box-shadow text-center">
        <div class="card-header">
          <h2 class="my-0 font-weight-normal">{{stuff}}</h2>
          <a class="btn text-right" style="font-size: 0.8rem; display: block" @click="deleteItem(stuff)">Delete</a>
        </div>
      </div>
    </masonry>
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
  name: 'inventory',
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  data() {
    return {
      inventory: null
    }
  },
  methods: {
    deleteItem: async function(stuff){
      let dataref = db.collection('users').doc(this.user.uid)
      let data = await dataref.get()
      this.inventory = data.data().Inventory.filter(item => item != stuff)
      await dataref.update({
        Inventory: this.inventory
      })
    }
  },
  async mounted() {
    let ref = await db.collection('users').doc(this.user.uid).get()
    this.inventory = ref.data().Inventory
  }
}
</script>

<style>
.container {
  padding-top: 40px;
  padding-bottom: 40px;
}

.material-icons.green {
  color: green;
}

.material-icons.red {
  color: red;
}

.availability {
  padding-top: 6px;
  padding-left: 3px;
}

.section-head {
  padding-left: 8px
}

.content {
  padding-left: 12px
}

.green {
  color: green;
}

.red {
  color: red;
}
</style>
