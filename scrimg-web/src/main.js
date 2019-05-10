import Vue from "vue";
import App from "./App.vue";
import BootstrapVue from "bootstrap-vue";
import VueRouter from "vue-router";
import router from "./router";
import jQuery from "jquery";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

global.jQuery = jQuery;

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(VueRouter);

/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App)
  // render: function(h) {
  //   return h(App);
  // }
}).$mount("#app");
