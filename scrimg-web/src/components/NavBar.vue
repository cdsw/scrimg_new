<template>
  <div>
    <!-- Image and text -->
    <b-navbar variant="faded" type="light">
      <b-navbar-brand href="#">
        <img alt="icon" height="30" src="../assets/icon.png">
        SCRIMG
      </b-navbar-brand>

      <b-navbar-nav class="ml-auto">
        <b-navbar-brand href="#" align="right">
          <!-- <img v-bind:src="git" alt="git"> -->
          <img alt="git logo" height="26" src="../assets/git.png">
        </b-navbar-brand>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "NavBar"
};
</script>

<style>
.navbar {
  font-family: LemonMilk;
  background-color: white;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
}
</style>

