<template>
  <div class="content">
    <md-dialog :md-active.sync="showDialogSucceed">
          <md-dialog-title>Succeed!</md-dialog-title>
          <p md-label="General" style="margin: 10px 50px">Succeed in adding from database!</p>
          <md-dialog-actions>
            <md-button class="md-primary" @click="showDialogSucceed = false">OK</md-button>
          </md-dialog-actions>
        </md-dialog>
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">Condition Database</h4>
            <p class="category">Add Condition from Database</p>
          </md-card-header>
          <md-card-content v-show="getSign">
            <md-icon
              class="md-primary md-size-1x"
              style ="left:20%"
            >wifi</md-icon>
            <span
              class="md-subheading"
            >Waiting...</span>
            <md-progress-bar md-mode="indeterminate"></md-progress-bar>
            
          </md-card-content>
          <md-card-content v-show="addSign">
            <md-progress-spinner
              :md-diameter="100"
              :md-stroke="10"
              md-mode="indeterminate"
              style="left:25%"
            ></md-progress-spinner>
            <br/>
            <span
              class="md-subheading"
            >Waiting for Condition Querying...</span>
            <md-icon
              class="md-primary md-size-2x"
              style =" position:absolute;top:45%;left:37%"
            >query_stats</md-icon>
          </md-card-content>
          <md-card-content v-show="!getSign && !addSign">
            <md-table v-model="databaseConditions" md-fixed-header table-header-color="green">
              <md-table-row slot="md-table-row" slot-scope="{ item,index }">
                <md-table-cell md-label="Condition">{{ item[0] }}</md-table-cell>
                <md-table-cell md-label="Human Count">{{ item[1] }}</md-table-cell>
                <md-table-cell md-label="First Infected">{{ item[2] }}</md-table-cell>
                <md-table-cell md-label="Total Day">{{ item[3] }}</md-table-cell>
                <md-table-cell>
                  <md-button class="md-primary md-size-20" @click="function(){addData(index)}">ADD</md-button>
                </md-table-cell>
              </md-table-row>
            </md-table>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "database",
  data() {
    return {
      databaseConditions: null,
      newView: null,
      newCondition: null,
      showDialogSucceed: false,
      getSign:false,
      addSign:false,
    };
  },
  computed: {},
  watch: {},
  methods: {
    addData(index) {
      var postData = new Object();
      postData.name = this.databaseConditions[index][0];
      this.addSign=true;
      axios({
        url: "http://localhost:5000/getCondition",
        method: "post",
        data: postData,
      })
        .then((response) => {
          this.newView = response.data.view;
          this.newCondition = response.data.condition;
          this.newCondition.haveComp = true;
          this.addSign =false;
          this.$store.state.views.push(this.newView);
          this.$store.state.conditions.push(this.newCondition);
          this.$store.state.conditionSelectSign = !this.$store.state.conditionSelectSign
          this.showDialogSucceed = true;
          return response.data;
        })
        .finally()
        .catch((response) => {
          console.log(response);
        });
    },
  },
  created() {},
  mounted() {
    var postData = null;
    this.getSign =true;
    axios({
      url: "http://localhost:5000/getAllCondition",
      method: "post",
      data: postData,
    })
      .then((response) => {
        this.databaseConditions = response.data;
        this.getSign=false;
        return response.data;
      })
      .finally()
      .catch((response) => {
        console.log(response);
      });
  },
};
</script>

<style scoped>
</style>