<template>
  <div>
    <div class="step">Click 'PROCESS' to continue</div>
    <img class="img-input" alt="input" src="../assets/ex-input.jpg">
    <br>
    <b-button>PROCESS</b-button>
    <br>
    <b-button class="trans" onclick="window.location.href='../upload'">GO BACK</b-button>
  </div>
</template>

<script>
export default {
  name: "Process"
};
</script>

<style>
@media (max-width: 576px) {
  .step {
    font-size: 14px;
    margin-top: 50px;
  }
}

.img-input {
  height: 250px;
  width: 250px;
}
</style>
