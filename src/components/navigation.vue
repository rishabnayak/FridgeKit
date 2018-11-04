<template>
<header class="navbar navbar-expand bd-navbar d-flex flex-column flex-md-row bg-white border-bottom shadow-sm">
  <a class="navbar-brand my-0 mr-md-auto" href="/"><img class="d-block" width="181.3" height="72.4" src="@/assets/fridgekit-full.png" />
    <!-- <h5 class="my-0 mr-md-auto font-weight-normal"><router-link to="/">FridgeKit</router-link></h5> -->
  </a>
  <div class="navbar-nav-scroll">
    <ul class="navbar-nav bd-navbar-nav flex-row">
      <li class="nav-item">
        <router-link to="/" class="nav-link">Home</router-link><span class="sr-only">(current)</span>
      </li>
      <li v-if="user" class="nav-item">
        <router-link :to="{ path: dashlink()}" class="nav-link">Dashboard</router-link>
      </li>
      <li v-if="user" class="nav-item">
        <router-link :to="{ path: invlink()}" class="nav-link">Inventory</router-link>
      </li>
      <li v-if="user" class="nav-item">
        <router-link :to="{ path: caloriecounter()}" class="nav-link">Calorie Counter</router-link>
      </li>
      <li v-if="user" class="nav-item">
        <router-link :to="{ path: profilelink()}" class="nav-link">Profile</router-link>
      </li>
    </ul>
  </div>
  <a v-if="user" class="nav-link btn btn-outline" @click="signOut()">Logout</a>
  <a v-else class="nav-link btn btn-outline" @click="login()">Login</a>
</header>
</template>

<script>
import firebase from 'firebase'
import db from '@/firebase/init.js'
export default {
  name: 'navigation',
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  methods: {
    async signOut() {
      await this.$store.dispatch('logOut')
      this.$router.push('/')
    },
    profilelink: function() {
      return "/profile/" + this.user.uname
    },
    dashlink: function() {
      return "/dashboard"
    },
    invlink: function() {
      return "/inventory"
    },
    caloriecounter: function() {
      return "/caloriecounter"
    },
    async login() {
      this.$router.push('/login')
    }
  },
  data() {
    return {}
  }
}
</script>
