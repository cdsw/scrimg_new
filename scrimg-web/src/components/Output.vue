<template>
  <div>
    <div class="bold-text">OUTPUT</div>
    <img class="img-input" alt="input" src="../assets/ex-input.jpg">
    <br>
    <b-button>SAVE OUTPUT</b-button>
    <br>
    <b-button class="trans">DO AGAIN</b-button>
  </div>
</template>

<script>
export default {
  name: "Output"
};
</script>

<style>
.bold-text {
  margin-top: 100px;
  margin-bottom: 10px;
  font-family: LemonMilkBold;
  font-size: 30px;
  font-weight: normal;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.14;
  letter-spacing: normal;
  text-align: center;
  color: #ff7e7e;
}

@media (max-width: 576px) {
  .bold-text {
    font-size: 20px;
    margin-top: 50px;
  }
}

.img-input {
  height: 250px;
  width: 250px;
}
</style>
