<template>
  <div>
    <form>
      <md-dialog :md-active.sync="showDialogSucceed">
        <md-dialog-title>Succeed!</md-dialog-title>
        <p md-label="General" style="margin: 10px 50px">
          Succeed in adding layer!
        </p>
        <md-dialog-actions>
          <md-button class="md-primary" @click="showDialogSucceed = false"
            >OK</md-button
          >
        </md-dialog-actions>
      </md-dialog>
      <md-dialog :md-active.sync="showDialogFail">
        <md-dialog-title>Fail!</md-dialog-title>
        <p md-label="General" style="margin: 10px 50px">
          Error! Information is not completed!
        </p>
        <md-dialog-actions>
          <md-button class="md-primary" @click="showDialogFail = false"
            >OK</md-button
          >
        </md-dialog-actions>
      </md-dialog>
      <md-card>
        <md-card-header :data-background-color="dataBackgroundColor">
          <h4 class="title">Add Layer</h4>
          <p class="category">Complete Layer Information</p>
          <p class="category">Depends on GeoServer</p>
        </md-card-header>

        <md-card-content>
          <div class="md-layout">
            <div class="md-layout-item md-small-size-100 md-size-100">
              <md-field md-clearable>
                <label>Name</label>
                <md-input v-model="name" type="text"></md-input>
                <span class="md-helper-text">Name of Layer</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
              <md-field md-clearable>
                <label>Layer Name</label>
                <md-input v-model="layername" type="text"></md-input>
                <span class="md-helper-text">Layer Source Name</span>
              </md-field md-clearable>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-33">
              <md-field md-clearable>
                <label>Layer Type</label>
                <md-input v-model="layertype" type="text"></md-input>
                <span class="md-helper-text">Type of Layer</span>
              </md-field md-clearable>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-33">
              <md-field>
                <label>Format</label>
                <md-input v-model="format" type="text"></md-input>
                <span class="md-helper-text">Format of Layer</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-33">
              <md-field :class="ServiceError" md-clearable>
                <label>Service</label>
                <md-input v-model="service" type="text"></md-input>
                <span class="md-error">Service Not Supposed!</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
              <md-field md-clearable>
                <label>URL</label>
                <md-input v-model="url" type="text"></md-input>
                <span class="md-helper-text">URL of Layer</span>
              </md-field>
            </div>
            <div class="md-layout-item md-size-100 text-right">
              <md-button class="md-raised md-success" v-on:click="AddLayer()"
                >Submit</md-button
              >
            </div>
          </div>
        </md-card-content>
      </md-card>
    </form>
  </div>
</template>
<script>
export default {
  name: "edit-profile-form",
  props: {
    dataBackgroundColor: {
      type: String,
      default: "green",
    },
  },
  data() {
    return {
      name: null,
      layername: null,
      layertype: null,
      format: null,
      service: null,
      url: null,
      showDialogSucceed: false,
      showDialogFail: false,
      ServiceList: [],
      ServiceErrorShow: false,
      NowIndex: 1,
    };
  },
  methods: {
    AddLayer() {
      if (
        !this.layername ||
        !this.layertype ||
        !this.service ||
        !this.url ||
        !this.format ||
        !this.name
      ) {
        this.showDialogFail = true;
        return;
      }
      var NewLayer = new Object();
      NewLayer.name = this.name;
      NewLayer.layer = this.layername;
      NewLayer.type = this.layertype;
      NewLayer.service = this.service;
      NewLayer.url = this.url;
      NewLayer.format = this.format;
      NewLayer.show = true;
      NewLayer.style = "";
      NewLayer.transparency = 0;
      NewLayer.size = 1;
      NewLayer.color = "#ff0000";
      NewLayer.propertyNames = [];
      NewLayer.LabelShow = false;
      NewLayer.LabelProperty = 0;
      NewLayer.OutLineWidth = 1;
      NewLayer.OutLineColor = "#ff0000";
      NewLayer.OutLineTransparency = 0;
      NewLayer.IconShow = false;
      NewLayer.IconIndex = 0;
      NewLayer.IconWidth = 20;
      NewLayer.IconHeight = 20;
      NewLayer.IconRotation = 0;
      NewLayer.IconTransparency = 0;
      NewLayer.IconColor = "#ff0000";
      NewLayer.EntityLat = 0;
      NewLayer.EntityLon = 0;
      NewLayer.EntityAl = 0;
      NewLayer.EntityRoll = 0;
      NewLayer.EntityPitch = 0;
      NewLayer.EntityHpr = 0;
      NewLayer.ModelColorSet=[
          "#ff0000",
          "#00ff00",
          "#0000ff",
        ];
      NewLayer.ModelSplitHeightSet=[
          50,
        ];
      var year = new Date().getFullYear();
      var month = new Date().getMonth() + 1;
      var date = new Date().getDate();
      NewLayer.time = year + "-" + month + "-" + date;
      this.$store.commit("AddLayersToStore", NewLayer);
      this.showDialogSucceed = true;
      this.layername = "";
      this.layertype = "";
      this.service = "";
      this.url = "";
      this.format = "";
      this.name = "";
    },
  },
  computed: {
    monitor() {
      return this.$store.state.layers;
    },
    ServiceError() {
      return {
        "md-invalid": this.ServiceErrorShow,
      };
    },
  },
  watch: {
    service(val, oldVal) {
      for (let i = 0; i < this.ServiceList.length; i++)
        if (this.ServiceList[i] == this.service) {
          this.ServiceErrorShow = false;
          return;
        }
      this.ServiceErrorShow = true;
    },
  },
  mounted() {
    this.ServiceList = this.$store.state.ServiceList;
  },
};
</script>
<style>
</style>
