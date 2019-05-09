<template>
  <div>
    <div class="step">Upload a file to begin</div>
    <img class="img-input" alt="input" src="../assets/upload.png">
    <br>
    <b-button>CHOOSE A FILE</b-button>
    <br>
    <b-button>TAKE A PHOTO</b-button>
  </div>
</template>

<script>
export default {
  name: "Upload"
};
</script>

<style>
.step {
  margin-top: 100px;
  margin-bottom: 10px;
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

@media (max-width: 576px) {
  .step {
    font-size: 14px;
    margin-top: 50px;
  }
}

.btn.btn-secondary {
  width: 250px;
  margin-top: 10px;
  color: white;
  background-color: #ff7e7e;
  border-color: #ff7e7e;
}

.btn.btn.btn-secondary:hover {
  color: white;
  background-color: #ff7e7e;
  border-color: white;
}

.img-input {
  height: 250px;
  width: 250px;
}
</style>
