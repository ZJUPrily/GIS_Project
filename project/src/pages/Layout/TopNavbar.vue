<template>
  <div>
    <md-toolbar md-elevation="0" class="md-transparent">
      <div class="md-toolbar-row">
        <div class="md-toolbar-section-start">
          <h3 class="md-title" v-if="$store.state.conditionSelectSign">{{ $store.state.views[$store.state.NowViewIndex].name }}</h3>
          <h3 class="md-title" v-else>{{ $route.name }}</h3>
        </div>
        <div class="md-toolbar-section-end">
          <md-button
            class="md-just-icon md-simple md-toolbar-toggle"
            :class="{ toggled: $sidebar.showSidebar }"
            @click="toggleSidebar"
          >
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </md-button>

          <div
            class="md-collapse"
            v-on:click="function(){
                updatename()
                }"
          >
            <div class="md-autocomplete">
              <md-autocomplete class="search" :md-options="layernames">
                <label>Search...</label>
              </md-autocomplete>
            </div>

            <li class="md-list-item">
              <div class="md-list-item-content" :close-on-click-modal="false">
                <drop-down :mdCloseOnClick="false">
                  <md-button
                    slot="title"
                    class="md-button md-just-icon md-simple"
                    data-toggle="dropdown"
                    id="LayerShowButton"
                    v-on:click=" function () {
                        update()
                        }
                        "
                  >
                    <md-icon>camera</md-icon>
                    <span class="map"></span>
                    <p class="hidden-lg hidden-md">Cameras</p>
                  </md-button>
                  <ul class="dropdown-menu dropdown-menu-right" :mdCloseOnClick="false">
                    <li>
                      <a
                        v-for="(item, index) in views = this.$store.state.views"
                        v-if="index!=0"
                        style="width:200px"
                      >
                        {{item.name}}
                        <md-icon-button
                          class="md-button-toggle md-simple btn-sm"
                          v-on:click="function(){
                            FocusView(index)}"
                        >
                          <md-icon>center_focus_strong</md-icon>
                        </md-icon-button>
                        <md-icon-button
                          class="md-button-toggle"
                          style="float:right"
                          v-on:click="function(){DeleteView(index)
                            }"
                        >
                          <md-icon>delete</md-icon>
                        </md-icon-button>
                        <md-icon-button
                          class="md-button-toggle"
                          style="float:right"
                          v-on:click="function(){UpdateView(index)
                            }"
                        >
                          <md-icon>edit</md-icon>
                        </md-icon-button>
                      </a>
                      <a @click="function(){AddViewShown()}" style="width:200px">Add New Condition</a>
                    </li>
                  </ul>
                </drop-down>
              </div>
            </li>

            <!--<md-list-item href="#/notifications" class="dropdown">
              <drop-down>
                <a slot="title" class="dropdown-toggle" data-toggle="dropdown">
                  <i class="material-icons">notifications</i>
                  <span class="notification">5</span>
                  <p class="hidden-lg hidden-md">Notifications</p>
                </a>
                <ul class="dropdown-menu dropdown-menu-right">
                  <li><a href="#">Mike John responded to your email</a></li>
                  <li><a href="#">You have 5 new tasks</a></li>
                  <li><a href="#">You're now friend with Andrew</a></li>
                  <li><a href="#">Another Notification</a></li>
                  <li><a href="#">Another One</a></li>
                </ul>
              </drop-down>
            </md-list-item>-->

            <li class="md-list-item" :mdCloseOnClick="false">
              <div class="md-list-item-content" :close-on-click-modal="false">
                <drop-down :mdCloseOnClick="false">
                  <md-button
                    slot="title"
                    class="md-button md-just-icon md-simple"
                    data-toggle="dropdown"
                    id="LayerShowButton"
                    v-on:click=" function () {
                        update()
                        }
                        "
                  >
                    <md-icon>map</md-icon>
                    <span class="map"></span>
                    <p class="hidden-lg hidden-md">Maps</p>
                  </md-button>
                  <ul class="dropdown-menu dropdown-menu-right" :mdCloseOnClick="false">
                    <li>
                      <a
                        v-for="(item, index) in layers = this.$store.state.layers"
                        style="width:300px"
                        @mouseenter="function(){UpdateStyle(index)}"
                        @mouseleave="function(){UpdateStyle(index)}"
                      >
                        {{item.name}}
                        <md-icon-button
                          class="md-button-toggle md-simple btn-sm"
                          v-on:click="function(){
                            LayerShow(index)}"
                          v-if="item.show == true"
                        >
                          <md-icon>visibility</md-icon>
                        </md-icon-button>
                        <md-icon-button
                          class="md-button-toggle md-simple btn-sm"
                          v-on:click="function(){
                            LayerShow(index)}"
                          v-else
                        >
                          <md-icon>visibility_off</md-icon>
                        </md-icon-button>
                        <md-icon-button class="md-button-toggle" v-on:click="showDialogStyle=true">
                          <md-icon>style</md-icon>
                        </md-icon-button>
                        <md-icon-button
                          class="md-button-toggle"
                          style="float:right"
                          v-on:click="function(){
                            LayerUp(index)}"
                          v-if="index != 0"
                        >
                          <md-icon>arrow_upward</md-icon>
                        </md-icon-button>
                        <md-icon-button
                          class="md-button-toggle md-simple btn-sm"
                          style="float:right"
                          v-on:click="function(){
                            LayerDown(index)}"
                          v-if="index != layers.length - 1"
                        >
                          <md-icon>arrow_downward</md-icon>
                        </md-icon-button>
                      </a>
                    </li>
                  </ul>
                </drop-down>
              </div>
            </li>

            <!--<md-list-item href="#/user">
              <i class="material-icons">person</i>
              <p class="hidden-lg hidden-md">Profile</p>
            </md-list-item>-->
          </div>
        </div>
      </div>
    </md-toolbar>
    <md-dialog :md-active.sync="showDialogStyle" class="md-scrollbar">
      <style-meum></style-meum>
      <md-icon-button
        class="md-button-toggle"
        v-on:click="showDialogStyle=false"
        style="position: absolute;top: 5px;right: 5px;"
      >
        <md-icon>close</md-icon>
      </md-icon-button>
    </md-dialog>
    <md-dialog :md-active.sync="showDialogView" class="md-scrollbar">
      <view-meum></view-meum>
      <md-icon-button
        class="md-button-toggle"
        v-on:click="showDialogView=false"
        style="position: absolute;top: 5px;right: 5px;"
      >
        <md-icon>close</md-icon>
      </md-icon-button>
    </md-dialog>
  </div>
</template>


<script>
import StyleMeum from "./StyleMeum.vue";
import ViewMeum from "./ViewMeum.vue";
export default {
  components: {
    StyleMeum,
    ViewMeum,
  },
  inject: ["reload"],
  data() {
    return {
      layers: [],
      layernames: [],
      StyleShow: [false],
      showDialogStyle: false,
      showDialogView: false,
      view: null,
    };
  },
  computed: {
    StyleMeumMonitor() {
      return this.$store.state.StyleChange;
    },
  },
  watch: {
    StyleMeumMonitor() {
      this.$forceUpdate();
    },
  },
  methods: {
    update() {
      this.layers = this.$store.state.layers;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    updatename() {
      this.layernames.splice(0, this.layernames.length);
      for (let index = 0; index < this.$store.state.layers.length; index++) {
        this.layernames.push(this.$store.state.layers[index].name);
      }
    },
    LayerShow(index) {
      if (this.layers[index].show) this.layers[index].show = false;
      else this.layers[index].show = true;
      this.$store.commit("UpdateLayersToStore", this.layers);
      var change = this.$store.state.CesiumChange;
      this.$store.commit("SituationChange", !change);
    },
    InitStyle() {
      this.StyleShow = this.$store.state.StyleMeum;
    },
    UpdateStyle(index) {
      if (this.$store.state.StyleBarChange == true) {
        this.StyleShow[index] = !this.StyleShow[index];
        this.$store.commit("NowLayerIndexSubmit", index);
        this.$store.commit("StyleMeumSubmit", this.StyleShow);
        var change = this.$store.state.StyleChange;
        this.$store.commit("StyleChangeSubmit", !change);
      }
    },
    ReturnStyle(index) {
      return this.StyleShow[index];
    },
    LayerUp(index) {
      var temp = this.layers[index];
      this.layers[index] = this.layers[index - 1];
      this.layers[index - 1] = temp;
      this.$store.commit("UpdateLayersToStore", this.layers);
      var change = this.$store.state.CesiumChange;
      this.$store.commit("SituationChange", !change);
    },
    LayerDown(index) {
      var temp = this.layers[index];
      this.layers[index] = this.layers[index + 1];
      this.layers[index + 1] = temp;
      this.$store.commit("UpdateLayersToStore", this.layers);
      var change = this.$store.state.CesiumChange;
      this.$store.commit("SituationChange", !change);
    },
    AddViewShown() {
      this.$store.commit("AddViewSignSubmit", true);
      this.showDialogView = true;
    },
    FocusView(index) {
      this.$store.commit("NowViewIndexSubmit", index);
      this.$store.commit("ViewChangeSubmit", !this.$store.state.ViewChange);
    },
    DeleteView(index) {
      this.$store.state.views.splice(index, 1);
      this.$store.state.conditions.splice(index, 1);
      this.$forceUpdate();
    },
    UpdateView(index){
      this.$store.commit("NowViewIndexSubmit", index);
      this.showDialogView = true;
    }
  },
  mounted() {
    this.update();
    this.updatename();
    this.InitStyle();
  },
};
</script>

<style lang="css">
.custom-btn-sm {
  min-height: 1px;
  height: 1px;
  line-height: 2rem;
  padding: 0 2px;
  font-size: 1px;
  min-width: 0px;
  margin: 0%;
}
</style>
