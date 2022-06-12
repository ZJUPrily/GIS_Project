<template>
  <div>
    <md-dialog :md-active.sync="showDialogRevise">
      <md-card>
        <md-card-header :data-background-color="tableHeaderColor">
          <h4 class="title">Revise Layer</h4>
        </md-card-header>
        <md-card-content>
          <div class="md-layout">
            <div class="md-layout-item md-small-size-100 md-size-100">
              <md-field>
                <label>Name</label>
                <md-input v-model="name" type="text"></md-input>
                <span class="md-helper-text">Name of Layer</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
              <md-field>
                <label>Layer Name</label>
                <md-input v-model="layername" type="text"></md-input>
                <span class="md-helper-text">Layer Source Name</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-33">
              <md-field>
                <label>Layer Type</label>
                <md-input v-model="layertype" type="text"></md-input>
                <span class="md-helper-text">Type of Layer</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-33">
              <md-field>
                <label>Format</label>
                <md-input v-model="format" type="text"></md-input>
                <span class="md-helper-text">Format of Layer</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-33">
              <md-field :class="ServiceError">
                <label>Service</label>
                <md-input v-model="service" type="text"></md-input>
                <span class="md-error">Service Not Supposed!</span>
              </md-field>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-100">
              <md-field>
                <label>URL</label>
                <md-input v-model="url" type="text"></md-input>
                <span class="md-helper-text">URL of Layer</span>
              </md-field>
            </div>
          </div>
        </md-card-content>
      </md-card>
      <md-dialog-actions>
        <md-button class="md-primary" @click="showDialogRevise = false"
          >Close</md-button
        >
        <md-button class="md-primary" @click="function(){SubmitReviseLayer();}"
          >Submit</md-button
        >
      </md-dialog-actions>
    </md-dialog>
    <md-dialog :md-active.sync="showDialogSucceed">
      <md-dialog-title>Succeed!</md-dialog-title>
      <p md-label="General" style="margin: 10px 50px">
        Succeed in revising layer!
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
    <md-dialog :md-active.sync="showDialogDelete">
      <md-dialog-title>Succeed!</md-dialog-title>
      <p md-label="General" style="margin: 10px 50px">
        Succeed in deleting layer!
      </p>
      <md-dialog-actions>
        <md-button class="md-primary" @click="showDialogDelete = false"
          >OK</md-button
        >
      </md-dialog-actions>
    </md-dialog>
    <div>
      <md-table v-model="layers" :table-header-color="tableHeaderColor">
        <md-table-row slot="md-table-row" slot-scope="{ item, index }">
          <md-table-cell md-label="Layer">{{ item.name }}</md-table-cell>
          <md-table-cell md-label="Type">{{ item.type }}</md-table-cell>
          <md-table-cell md-label="Service">{{ item.service }}</md-table-cell>
          <md-table-cell md-label="Format">{{ item.format }}</md-table-cell>
          <md-table-cell md-label="Time">{{ item.time }}</md-table-cell>
          <md-table-cell class="md-layout-item md-small-size-20 text-right">
            <md-button
              class="md-raised md-success"
              @click="
                function () {
                  ReviseLayer(index);
                }
              "
              >Revise</md-button
            >
          </md-table-cell>
          <md-table-cell class="md-layout-item md-small-size-20 text-right">
            <md-button
              class="md-raised md-success"
              v-on:click="
                function () {
                  DeleteLayer(index);
                }
              "
              >Delete</md-button
            >
          </md-table-cell>
        </md-table-row>
      </md-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "simple-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      showDialogRevise: false,
      showDialogSucceed: false,
      showDialogFail: false,
      showDialogDelete: false,
      selected: [],
      layers: [],
      ServiceList: [],
      name: null,
      layername: null,
      layertype: null,
      format: null,
      service: null,
      url: null,
      NowIndex: 1,
    };
  },
  methods: {
    update() {
      this.layers = this.$store.state.layers;
    },
    DeleteLayer(index) {
      this.layers.splice(index, 1);
      this.$store.commit("UpdateLayersToStore", this.layers);
      this.showDialogDelete = true;
    },
    ReviseLayer(i) {
      this.NowIndex = i;
      this.layername = this.layers[i].layer;
      this.layertype = this.layers[i].type;
      this.service = this.layers[i].service;
      this.url = this.layers[i].url;
      this.format = this.layers[i].format;
      this.name = this.layers[i].name;
      this.showDialogRevise = true;
    },
    SubmitReviseLayer() {
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
      this.layers[this.NowIndex].name = this.name;
      this.layers[this.NowIndex].layer = this.layername;
      this.layers[this.NowIndex].type = this.layertype;
      this.layers[this.NowIndex].service = this.service;
      this.layers[this.NowIndex].url = this.url;
      this.layers[this.NowIndex].format = this.format;
      this.layers[this.NowIndex].name = this.name;
      this.$store.commit("UpdateLayersToStore", this.layers);
      var change = this.$store.state.CesiumChange;
      this.$store.commit("SituationChange", !change);
      this.showDialogSucceed = true;
      this.showDialogRevise = false;
    },
  },
  mounted() {
    this.update();
    this.ServiceList = this.$store.state.ServiceList;
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
};
</script>
