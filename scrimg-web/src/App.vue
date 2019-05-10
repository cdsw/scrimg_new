<template>
  <div id="app">
    <NavBar/>
    <router-view></router-view>
    <!-- <Welcome/> -->
    <!-- <upload/> -->
    <!-- <Process/> -->
    <!-- <Output/> -->
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import NavBar from "./components/NavBar.vue";
import Welcome from "./components/Welcome.vue";
// import Upload from "./components/Upload.vue";
// import Process from "./components/Process.vue";
// import Output from "./components/Output.vue";

export default {
  name: "app",
  components: {
    NavBar,
    Welcome
  }
};
</script>

<style>
#app {
  font-family: LemonMilk;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  align-items: center;

  /* font-family: 'Avenir', Helvetica, Arial, sans-serif; */
  /* margin-top: 60px; */
}
</style>
