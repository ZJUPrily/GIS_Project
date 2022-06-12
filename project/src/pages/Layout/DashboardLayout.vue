<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">


    <side-bar
      :sidebar-item-color="sidebarBackground"
      :sidebar-background-image="sidebarBackgroundImage"
    >
      <mobile-menu slot="content"></mobile-menu>
      <sidebar-link to="/maps">
        <md-icon>location_on</md-icon>
        <p>Map</p>
      </sidebar-link>
      <sidebar-link to="/user">
        <md-icon>map</md-icon>
        <p>Add Layer</p>
      </sidebar-link>
      <sidebar-link to="/table">
        <md-icon>content_paste</md-icon>
        <p>Layer List</p>
      </sidebar-link>
      <sidebar-link to="/chart">
        <md-icon>pie_chart</md-icon>
        <p>Condition Analyze</p>
      </sidebar-link>
      <sidebar-link to="/style">
        <md-icon>style</md-icon>
        <p>Condition Style</p>
      </sidebar-link>
    </side-bar>

    <div class="main-panel">
      <top-navbar></top-navbar>

      <fixed-plugin
        :color.sync="sidebarBackground"
        :image.sync="sidebarBackgroundImage"
      >
      </fixed-plugin>

      <dashboard-content> </dashboard-content>

      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import FixedPlugin from "./Extra/FixedPlugin.vue";

export default {
  components: {
    TopNavbar,
    DashboardContent,
    ContentFooter,
    FixedPlugin,
  },
  data() {
    return {
      sidebarBackground: "green",
      sidebarBackgroundImage: require("@/assets/img/sidebar-2.jpg"),
    };
  },
};
</script>
