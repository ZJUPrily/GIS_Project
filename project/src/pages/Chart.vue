<template>
  <div class="md-layout">
    <div class="md-layout-item md-medium-size-100 md-size-66">
      <form>
        <md-dialog :md-active.sync="dataDialogShow" class="md-scrollbar">
          <database></database>
          <md-icon-button
            class="md-button-toggle"
            v-on:click="dataDialogShow=false"
            style="position: absolute;top: 5px;right: 5px;"
          >
            <md-icon>close</md-icon>
          </md-icon-button>
        </md-dialog>
        <md-dialog :md-active.sync="showDialogSucceed">
          <md-dialog-title>Succeed!</md-dialog-title>
          <p md-label="General" style="margin: 10px 50px">Succeed in adding to database!</p>
          <md-dialog-actions>
            <md-button class="md-primary" @click="showDialogSucceed = false">OK</md-button>
          </md-dialog-actions>
        </md-dialog>
        <md-card>
          <md-card-header :data-background-color="dataBackgroundColor">
            <h4 class="title">Condition Analyze</h4>
            <p class="category">Displays a Graphical Analysis of the Condition</p>
          </md-card-header>

          <md-card-content v-show="addSign">
            <md-progress-spinner
              :md-diameter="100"
              :md-stroke="10"
              md-mode="indeterminate"
              style="left:30%"
            ></md-progress-spinner>
            <span
              class="md-headline"
              style="top: 55%;left: 45%;position:absolute"
            >Adding to Database...</span>
            <md-icon
              style="top:53%;left: 33.5%;position:absolute"
              class="md-primary md-size-2x"
            >save</md-icon>
          </md-card-content>
          <md-card-content v-show="!addSign">
            <div class="md-layout">
              <div class="md-layout-item md-small-size-100 md-size-70">
                <md-field>
                  <label for="font">Condition</label>
                  <md-select
                    v-model="NowIndex"
                    name="font"
                    id="font"
                    @input="function(){conditionChangeInit()}"
                  >
                    <md-option
                      v-for="(item, index) in icon = this.views"
                      v-bind:value="index"
                      v-show="index!=0"
                    >{{item.name}}</md-option>
                  </md-select>
                </md-field>
              </div>
              <div class="md-layout-item md-small-size-100 md-size-30">
                <md-button
                  class="md-primary"
                  @click="dataDialogShow=true"
                >Get Condition from Database</md-button>
              </div>
            </div>
            <div md-card-content v-show="!condition.haveComp">
              <div class="md-layout">
                <div class="md-layout-item md-small-size-100 md-size-100">
                  <span class="md-display-1">
                    Sorry, You Need to Compute This Condition First!
                    <md-icon>sentiment_very_dissatisfied</md-icon>
                  </span>
                </div>
              </div>
            </div>

            <div md-card-content v-show="condition.haveComp">
              <div class="md-layout">
                <div class="md-layout-item md-small-size-100 md-size-100">
                  <div id="linechart" style="width:900px;height:500px" ref="linechart"></div>
                </div>
                <div class="md-layout-item md-small-size-100 md-size-100">
                  <div id="piechart" style="width:900px;height:600px"></div>
                  <b>{{"Day: "+pieDay}}</b>
                  <br />
                  <input
                    id="pieday"
                    type="range"
                    v-model.number="pieDay"
                    style="width:900px"
                    @input="function(){pieChart()}"
                  />
                </div>
              </div>
              <div class="md-layout">
                <div class="md-layout-item md-small-size-100 md-size-100">
                  <md-button
                    class="md-primary md-size-100"
                    style="left:35%"
                    @click="function(){submitData()}"
                  >Submit Condition to Database</md-button>
                </div>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </form>
    </div>
  </div>
</template>
<script>
import * as echarts from "echarts";
import axios from "axios";
import Database from "./Layout/Database.vue";
export default {
  name: "chart",
  components: {
    Database,
  },
  props: {
    dataBackgroundColor: {
      type: String,
      default: "green",
    },
  },
  data() {
    return {
      showDialogSucceed: false,
      showDialogFail: false,
      ServiceErrorShow: false,
      NowIndex: 1,
      conditions: null,
      views: 0,
      conditionChange: false,
      condition: null,
      view: null,
      dataDialogShow: false,
      addSign: false,
      myLineChart: null,
      myPieChart: null,
      lineData: null,
      pieDay: 0,
    };
  },
  methods: {
    conditionChangeInit() {
      this.conditionChange = !this.conditionChange;
    },
    submitData() {
      let postData = new Object();
      postData.view = this.view;
      postData.condition = this.condition;
      this.addSign = true;
      axios({
        url: "http://localhost:5000/addCondition",
        method: "post",
        data: postData,
      })
        .then((response) => {
          this.showDialogSucceed = true;
          this.addSign = false;
          return response.data;
        })
        .finally()
        .catch((response) => {
          console.log(response);
        });
    },
    lineChart() {
      var chartDom = document.getElementById("linechart");
      this.myLineChart = echarts.init(chartDom);
      this.myLineChart.clear();
      var option;
      this.lineData = new Object();
      this.lineData.peopleType = [
        "Infected People",
        "Sick People",
        "Isolated People",
      ];
      this.lineData.data = [];
      this.lineData.data.push(["type", "count", "day"]);
      const datasetWithFilters = [];
      const seriesList = [];
      let min = 0xffffff;
      let max = 0;
      for (let i = 0; i < this.condition.total_day; i++) {
        this.lineData.data.push([
          "Infected People",
          this.condition.plt_x_infectionSet[i].length,
          i,
        ]);
        if (this.condition.plt_x_infectionSet[i].length > max)
          max = this.condition.plt_x_infectionSet[i].length;
        if (this.condition.plt_x_infectionSet[i].length < min)
          min = this.condition.plt_x_infectionSet[i].length;
        this.lineData.data.push([
          "Sick People",
          this.condition.plt_x_sickSet[i].length,
          i,
        ]);
        this.lineData.data.push([
          "Isolated People",
          this.condition.plt_x_isolationSet[i].length,
          i,
        ]);
      }
      echarts.util.each(this.lineData.peopleType, function (peopleType) {
        var datasetId = "dataset_" + peopleType;
        datasetWithFilters.push({
          id: datasetId,
          fromDatasetId: "dataset_raw",
          transform: {
            type: "filter",
            config: {
              and: [
                { dimension: "day", gte: 0 },
                { dimension: "type", "=": peopleType },
              ],
            },
          },
        });
        seriesList.push({
          type: "line",
          datasetId: datasetId,
          showSymbol: false,
          name: peopleType,
          endLabel: {
            show: true,
            formatter: function (params) {
              return params.value[0] + ": " + params.value[1];
            },
          },
          labelLayout: {
            moveOverlap: "shiftY",
          },
          emphasis: {
            focus: "series",
          },
          encode: {
            x: "day",
            y: "count",
            label: ["type", "count"],
            itemName: "day",
            tooltip: ["count"],
          },
        });
      });
      option = {
        animationDuration: 10000,
        /* color:[
          this.$store.state.injectionStyle.color,
          this.$store.state.sickStyle.color,
          this.$store.state.isolationStyle.color
        ],*/
        dataset: [
          {
            id: "dataset_raw",
            source: this.lineData.data,
          },
          ...datasetWithFilters,
        ],
        title: {
          text: "Changes in the number of people over time",
          left: "center",
        },
        tooltip: {
          order: "valueDesc",
          trigger: "axis",
        },
        xAxis: {
          type: "category",
          nameLocation: "middle",
          name: "Day",
        },
        yAxis: {
          name: "Count",
        },
        grid: {
          right: 140,
        },
        series: seriesList,
      };
      this.myLineChart.setOption(option, true);
    },
    pieChart() {
      var chartDom = document.getElementById("piechart");
      this.myPieChart = echarts.init(chartDom);
      this.myPieChart.clear();
      var data = [];
      var item = new Object();
      item["value"] = this.condition.plt_x_infectionSet[this.pieDay].length - this.condition.plt_x_sickSet[this.pieDay].length
      item["name"] = "Infected People";
      data.push(item);
      item = new Object();
      item["value"] = this.condition.plt_x_sickSet[this.pieDay].length;
      item["name"] = "Sick People";
      data.push(item);
      item = new Object();
      item["value"] = this.condition.plt_x_isolationSet[this.pieDay].length;
      item["name"] = "Isolated People";
      data.push(item);
      item = new Object();
      item["value"] =
        this.condition.plt_xSet[this.pieDay].length -
        this.condition.plt_x_infectionSet[this.pieDay].length -
        this.condition.plt_x_isolationSet[this.pieDay].length;
      item["name"] = "Normal People";
      data.push(item);
      var option;
      option = {
        title: {
          text: "Distribution of various types of personnel in a day",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "bottom",
          left: "center",
        },
        series: [
          {

            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "40",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: data,
          },
        ],
      };
      option && this.myPieChart.setOption(option, true);
    },
  },
  computed: {
    conditionChangeGlobal() {
      return this.$store.state.conditionSelectSign;
    },
    conditionChangeMonitor() {
      return this.conditionChange;
    },
  },
  watch: {
    conditionChangeMonitor() {
      this.condition = this.conditions[this.NowIndex];
      this.view = this.views[this.NowIndex];
      this.lineChart();
      this.pieDay = 0;
      document.getElementById("pieday").max = this.condition.total_day - 1;
      this.pieChart();
      this.$forceUpdate();
    },
    conditionChangeGlobal() {
      this.conditions = this.$store.state.conditions;
      this.views = this.$store.state.views;
      this.condition = this.conditions[this.NowIndex];
      this.view = this.views[this.NowIndex];
      this.lineChart();
      this.pieDay = 0;
      document.getElementById("pieday").max = this.condition.total_day - 1;
      this.pieChart();
      this.$forceUpdate();
    },
  },
  mounted() {
    this.$store.state.conditionSelectSign = false;
    this.conditions = this.$store.state.conditions;
    this.views = this.$store.state.views;
    if (this.conditions.length == 1) {
      this.condition = this.conditions[0];
      this.view = this.views[0];
    } else {
      this.condition = this.conditions[this.NowIndex];
      this.view = this.views[this.NowIndex];
    }
    this.$nextTick(function () {
      this.lineChart();
      document.getElementById("pieday").max = this.condition.total_day - 1;
      this.pieChart();
    });
  },
};
</script>
<style>
</style>
