<template>
  <div>
    <img class="logo" alt="s logo" src="../assets/the-s.png">
    <div class="description">
      Identifying Writing Systems
      <br>using Image Recognition and
      <br>Neural Network
    </div>
    <b-button class="trans" onclick="window.location.href='../upload'">EXPLORE</b-button>
  </div>
</template>

<script>
export default {
  name: "Welcome"
};
</script>

<style>
.description {
  height: 100px;
  margin-top: 100px;
  font-family: Menlo;
  font-size: 20px;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.14;
  letter-spacing: normal;
  text-align: center;
  color: #727272;
}

.logo {
  margin-top: 100px;
  height: 60px;
}

@media (max-width: 576px) {
  .description {
    font-size: 14px;
    margin-top: 50px;
  }
  .logo {
    height: 40px;
    margin-top: 50px;
  }
}

.btn.trans.btn-secondary {
  background-color: #ffffff00;
  color: #ff7e7e;
  border: solid 2px #ff7e7e;
}

.btn.btn.trans.btn-secondary:hover {
  color: white;
  background-color: #ff7e7e;
  border-color: #ff7e7e;
}
</style>
