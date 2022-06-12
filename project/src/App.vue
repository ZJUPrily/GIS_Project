<template>
  <router-view v-if="isRouterAlive"></router-view>
</template>

<script>
header("Access-Control-Allow-Origin: *");
export default {};
</script>


<script>
import store from "./vuex/store.js";
export default {

  store,
  provide() {
    return {
      reload: this.reload
    };
  },
  data() {
    return {
      isRouterAlive: true
    };
  },
  mounted() {
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(function() {
        this.isRouterAlive = true;
      });
    },
  },
  components: { undefined },
};
</script>
