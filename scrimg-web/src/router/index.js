import Vue from "vue";
import Router from "vue-router";

import Welcome from "@/components/Welcome.vue";
import Upload from "@/components/Upload.vue";
import Process from "@/components/Process.vue";
import Output from "@/components/Output.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "welcome",
      component: Welcome
    },
    {
      path: "/upload",
      name: "upload picture",
      component: Upload,
      props: true
    },
    {
      path: "/process",
      name: "process or not",
      component: Process,
      props: true
    },
    {
      path: "/output",
      name: "image with output",
      component: Output,
      props: true
    }
  ]
});
