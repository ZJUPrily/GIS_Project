<template>
  <div id="ViewMeum" style="width:1000px;height:600px">
    <md-content class="md-scrollbar" style="width:1000px;height=500px">
      <md-card style="width:280px;height=700px;right:0px;">
        <md-card-header data-background-color="green">
          <h4 v-if="AddViewSign">Add New Condition</h4>
          <h4 v-else>{{view.name}}</h4>
        </md-card-header>

        <md-card-content v-if="ViewMeumPage==1">
          <md-field>
            <label>Infection Condition Name</label>
            <md-input v-model="view.name"></md-input>
            <span class="md-helper-text">Name of Infection Condition</span>
          </md-field>
          <p>View Set</p>
          <b>Longitude</b>
          <br />
          <input
            type="range"
            max="180"
            min="-180"
            step="0.01"
            v-model.number="view.Lon"
            @input="function(){ViewChange()}"
          />
          <span>{{view.Lon.toFixed(2)}}</span>
          <br />
          <b>Latitude</b>
          <br />
          <input
            type="range"
            max="90"
            min="-90"
            step="0.01"
            v-model.number="view.Lat"
            @input="function(){ViewChange()}"
          />
          <span>{{view.Lat.toFixed(2)}}</span>
          <br />
          <b>Altitude</b>
          <br />
          <input
            type="range"
            max="20000"
            min="0"
            step="1"
            v-model.number="view.Alt"
            @input="function(){ViewChange()}"
          />
          <span>{{view.Alt.toFixed(2)}}</span>
          <br />
          <b>Heading</b>
          <br />
          <input
            type="range"
            max="720"
            min="0"
            step="0.01"
            v-model.number="view.Heading"
            @input="function(){ViewChange()}"
          />
          <span>{{view.Heading.toFixed(2)}}</span>
          <br />
          <b>Pitch</b>
          <br />
          <input
            type="range"
            max="0"
            min="-180"
            step="0.01"
            v-model.number="view.Pitch"
            @input="function(){ViewChange()}"
          />
          <span>{{view.Pitch.toFixed(2)}}</span>
          <br />
          <b>Roll</b>
          <br />
          <input
            type="range"
            max="720"
            min="0"
            step="0.01"
            v-model.number="view.Roll"
            @input="function(){ViewChange()}"
          />
          <span>{{view.Roll.toFixed(2)}}</span>
          <br />
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage++"
            v-if="ViewMeumPageTop!=ViewMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage--"
            v-if="ViewMeumPage!=1"
          >
            <md-icon>arrow_back_ios</md-icon>
          </md-icon-button>
        </md-card-content>

        <md-card-content v-if="ViewMeumPage==2">
          <p>Condition Set</p>

          <md-field>
            <label>Sum of People</label>
            <md-input v-model="condition.sum_of_human"></md-input>
            <span class="md-helper-text">The total population of the study area</span>
          </md-field>

          <md-field>
            <label>Incubation Period</label>
            <md-input v-model="condition.incubation_period"></md-input>
            <span
              class="md-helper-text"
            >How long does it take for a patient to get sick after contracting the virus</span>
          </md-field>
          <br />
          <md-field>
            <label>Treat Willingness</label>
            <md-input v-model="condition.treat_willingness"></md-input>
            <span
              class="md-helper-text"
            >How many days does the patient go to the hospital after the onset of the disease</span>
          </md-field>
          <br />

          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage++"
            v-if="ViewMeumPageTop!=ViewMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage--"
            v-if="ViewMeumPage!=1"
          >
            <md-icon>arrow_back_ios</md-icon>
          </md-icon-button>
        </md-card-content>

        <md-card-content v-if="ViewMeumPage==3">
          <md-field>
            <label>Isolation Pos</label>
            <md-input v-model="condition.isolation_pos"></md-input>
            <span class="md-helper-text">Number of isolates that can be accommodated</span>
          </md-field>
          <br />
          <md-field>
            <label>Infection Area</label>
            <md-input v-model="condition.infection_area"></md-input>
            <span class="md-helper-text">Infection range</span>
          </md-field>

          <md-field>
            <label>Move Area Param</label>
            <md-input v-model="condition.move_area_param"></md-input>
            <span class="md-helper-text">Range of motion parameters (suppose to be 0-1)</span>
          </md-field>
          <br />

          <md-field>
            <label>First Infected Cnt</label>
            <md-input v-model="condition.first_infected_cnt"></md-input>
            <span class="md-helper-text">Number of people initially infected</span>
          </md-field>
          <br />

          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage++"
            v-if="ViewMeumPageTop!=ViewMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage--"
            v-if="ViewMeumPage!=1"
          >
            <md-icon>arrow_back_ios</md-icon>
          </md-icon-button>
        </md-card-content>

        <md-card-content v-if="ViewMeumPage==4">
          <md-field>
            <label>Total Day</label>
            <md-input v-model="condition.total_day"></md-input>
            <span class="md-helper-text">Total number of days in the process</span>
          </md-field>
          <br />
          <md-button class="md-primary" @click="function(){ConditionInit()}">Show Init Situation</md-button>
          <br />
          <md-button class="md-primary" @click="function(){ResitView()}">Reset</md-button>
          <b></b>
          <md-button v-if="AddViewSign" class="md-primary" @click="function(){SubmitView()}">Submit</md-button>

          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage++"
            v-if="ViewMeumPageTop!=ViewMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="ViewMeumPage--"
            v-if="ViewMeumPage!=1"
          >
            <md-icon>arrow_back_ios</md-icon>
          </md-icon-button>
        </md-card-content>
      </md-card>
      <div
        id="Stylemap"
        style="width:500px;height:700px;position: absolute;top: 80px;right: 5px; width:700px;height:400px"
      ></div>
    </md-content>
    <md-dialog :md-active.sync="showDialogSucceed">
      <md-dialog-title>Succeed!</md-dialog-title>
      <p md-label="General" style="margin: 10px 50px">Succeed in adding initial infection point!</p>
      <md-dialog-actions>
        <md-button class="md-primary" @click="showDialogSucceed = false">OK</md-button>
      </md-dialog-actions>
    </md-dialog>
    <md-dialog :md-active.sync="showDialogFail">
      <md-dialog-title>Fail!</md-dialog-title>
      <p md-label="General" style="margin: 10px 50px">Error! Information is not completed!</p>
      <md-dialog-actions>
        <md-button class="md-primary" @click="showDialogFail = false">OK</md-button>
      </md-dialog-actions>
    </md-dialog>
  </div>
</template>

<script>
import axios from "axios";
import * as Cesium from "cesium/Source/Cesium";
import "cesium/Source/Widgets/widgets.css";
export default {
  name: "view-meum",
  data() {
    return {
      layer: null,
      layers: [],
      layernames: [],
      index: 1,
      viewer: null,
      AddViewSign: false,
      view: null,
      viewIndex: 0,
      views: [],
      showDialogSucceed: false,
      showDialogFail: false,
      ViewMeumPage: 1,
      ViewMeumPageTop: 4,
      conditions: [],
      condition: null,
      loadSign: true,
    };
  },
  StyleChange: false,
  computed: {},
  watch: {},
  methods: {
    update() {
      this.layers = this.$store.state.layers;
      this.index = this.$store.state.NowLayerIndex;
      this.layer = this.layers[this.index];
    },
    CesiumInit() {
      Cesium.Camera.DEFAULT_VIEW_RECTANGLE = Cesium.Rectangle.fromDegrees(
        90,
        -20,
        130,
        50
      ); //home定位到中国范围
      Cesium.Ion.defaultAccessToken =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NTRkMzQ0Zi0yYTExLTQyMjMtYjJkMS0yNmZkYTA1MTgwMjgiLCJpZCI6ODY3NzIsImlhdCI6MTY0ODAxODI2MX0.B6IPcv0jQqjLqH8w40gPyZHkW5uK7tKGlwnPgDxhw8o";
      this.viewer = new Cesium.Viewer("Stylemap", {
        TerrainProvider: null,
        selectionIndicator: false,
        animation: false, //是否显示动画控件
        baseLayerPicker: false, //是否显示图层选择控件
        geocoder: false, //是否显示地名查找控件
        timeline: false, //是否显示时间线控件
        sceneModePicker: false, //是否显示投影方式控件
        navigationHelpButton: false, //是否显示帮助信息控件
        infoBox: false, //是否显示点击要素之后显示的信息
        fullscreenButton: false,
        homeButton: false, //隐藏home按钮
      });
      // 去除logo
      this.viewer.cesiumWidget.creditContainer.style.display = "none";
      this.viewer.scene.skyBox.show = false;
      this.viewer.scene.backgroundColor = new Cesium.Color(1, 1, 1, 0.0);
      var change = this.$store.state.CesiumChange;
      this.$store.commit("SituationChange", !change);
      this.viewer.camera.setView({
        destination: new Cesium.Cartesian3.fromDegrees(
          this.view.Lon,
          this.view.Lat,
          this.view.Alt * 1000
        ),
        orientation: {
          heading: Cesium.Math.toRadians(this.view.Heading),
          pitch: Cesium.Math.toRadians(this.view.Pitch),
          roll: Cesium.Math.toRadians(this.view.Roll),
        },
      });
      this.viewer.scene.camera.percentageChanged = 1; //设置相机变化的识别精度，默认值为0.5
      //设置相机变化的监听事件
      let removeChanged = this.viewer.camera.changed.addEventListener(() => {
        this.view.Heading = Cesium.Math.toDegrees(
          this.viewer.scene.camera.heading
        );
        this.view.Pitch = Cesium.Math.toDegrees(this.viewer.scene.camera.pitch);
        this.view.Roll = Cesium.Math.toDegrees(this.viewer.scene.camera.roll);
        var cartographic =
          this.viewer.scene.globe.ellipsoid.cartesianToCartographic(
            this.viewer.scene.camera.position
          );
        this.view.Lat = Number(Cesium.Math.toDegrees(cartographic.latitude));
        this.view.Lon = Number(Cesium.Math.toDegrees(cartographic.longitude));
        this.view.Alt = Number(cartographic.height / 1000);
      });
    },
    SubmitLayer() {
      this.$store.commit("UpdateLayersToStore", this.layers);
    },
    ViewChange() {
      this.viewer.camera.setView({
        destination: new Cesium.Cartesian3.fromDegrees(
          this.view.Lon,
          this.view.Lat,
          this.view.Alt * 1000
        ),
        orientation: {
          heading: Cesium.Math.toRadians(this.view.Heading),
          pitch: Cesium.Math.toRadians(this.view.Pitch),
          roll: Cesium.Math.toRadians(this.view.Roll),
        },
      });
    },
    ResitView() {
      this.view.name = "";
      this.view.Lat = 15;
      this.view.Lon = 110;
      this.view.Alt = 20000;
      this.view.Roll = 0;
      this.view.Pitch = -90;
      this.view.Heading = 0;
      this.view.layer = undefined;
      this.ViewChange();
      this.condition.sum_of_human = 2000;
      this.condition.incubation_period = 40;
      this.condition.treat_willingness = 40;
      this.condition.isolation_pos = 400;
      this.condition.infection_area = 0.02;
      this.condition.move_area_param = 0.3;
      this.condition.first_infected_cnt = 20;
      this.condition.total_day = 1000;
      this.viewer.entities.removeAll();
    },
    SubmitView() {
      if (!this.view.name) {
        this.showDialogFail = true;
        return;
      }
      var newView = new Object();
      newView.name = this.view.name;
      newView.Lat = this.view.Lat;
      newView.Lon = this.view.Lon;
      newView.Alt = this.view.Alt;
      newView.Roll = this.view.Roll;
      newView.Pitch = this.view.Pitch;
      newView.Heading = this.view.Heading;
      newView.layer = this.view.layer;
      this.$store.commit("AddView", newView);
      var newCondition = new Object();
      newCondition.sum_of_human = this.condition.sum_of_human;
      newCondition.incubation_period = this.condition.incubation_period;
      newCondition.treat_willingness = this.condition.treat_willingness;
      newCondition.isolation_pos = this.condition.isolation_pos;
      newCondition.infection_area = this.condition.infection_area;
      newCondition.move_area_param = this.condition.move_area_param;
      newCondition.first_infected_cnt = this.condition.first_infected_cnt;
      newCondition.total_day = this.condition.total_day;
      newCondition.haveComp = this.condition.haveComp;
      newCondition.x1 = this.condition.x1;
      newCondition.y1 = this.condition.y1;
      newCondition.x2 = this.condition.x2;
      newCondition.y2 = this.condition.y2;
      newCondition.plt_xSet = this.condition.plt_xSet;
      newCondition.plt_ySet = this.condition.plt_ySet;
      newCondition.plt_x_infectionSet = this.condition.plt_x_infectionSet;
      newCondition.plt_y_infectionSet = this.condition.plt_y_infectionSet;
      newCondition.plt_x_sickSet = this.condition.plt_x_sickSet;
      newCondition.plt_y_sickSet = this.condition.plt_y_sickSet;
      newCondition.plt_x_isolationSet = this.condition.plt_x_isolationSet;
      newCondition.plt_y_isolationSet = this.condition.plt_y_isolationSet;
      newCondition.infected_index_history =
        this.condition.infected_index_history;
      newCondition.west = this.condition.west;
      newCondition.east = this.condition.east;
      newCondition.north = this.condition.north;
      newCondition.south = this.condition.south;
      newCondition.day = this.condition.day;
      newCondition.isolation_set = this.condition.isolation_set
      newCondition.infected_index_set = this.condition.infected_index_set
      this.showDialogSucceed = true;
      this.$store.commit("AddCondition", newCondition);
      this.showDialogSucceed = true;
      this.ResitView();
    },
    ConditionInit() {
      //获取当前视角经纬度坐标
      this.loadSign = false;
      let rectangle = this.viewer.camera.computeViewRectangle();
      this.condition.west = Cesium.Math.toDegrees(rectangle.west);
      this.condition.east = Cesium.Math.toDegrees(rectangle.east);
      this.condition.north = Cesium.Math.toDegrees(rectangle.north);
      this.condition.south = Cesium.Math.toDegrees(rectangle.south);
      this.condition.day = 0;
      this.condition.x1 = [];
      this.condition.x2 = [];
      this.condition.y1 = [];
      this.condition.y2 = [];
      this.condition.plt_xSet = [];
      this.condition.plt_ySet = [];
      this.condition.plt_x_infectionSet = [];
      this.condition.plt_y_infectionSet = [];
      this.condition.plt_x_sickSet = [];
      this.condition.plt_y_sickSet = [];
      this.condition.plt_x_isolationSet = [];
      this.condition.plt_y_isolationSet = [];
      this.condition.infected_index_history = [];
      let postData = this.condition;
      axios({
        url: "http://localhost:5000/injection",
        method: "post",
        data: postData,
      })
        .then((response) => {
          this.condition = response.data;
          this.showInitCondition();
          return response.data;
        })
        .finally()
        .catch((response) => {
          console.log(response);
        });
    },
    showInitCondition() {
      this.viewer.entities.removeAll();
      let r1 = 50;
      let r2 = 50;
      for (let i = 0; i < this.condition.plt_xSet[0].length; i++) {
        var entity = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_xSet[0][i],
            this.condition.plt_ySet[0][i]
          ),
        });

        if (this.$store.state.peopleStyle.IconShow) {
          entity.billboard = new Cesium.BillboardGraphics({
            image:
              this.$store.state.icon[this.$store.state.peopleStyle.IconIndex]
                .path,
            height: this.$store.state.peopleStyle.IconHeight,
            width: this.$store.state.peopleStyle.IconWidth,
            rotation: Cesium.Math.toRadians(
              this.$store.state.peopleStyle.IconRotation
            ),
            color: Cesium.Color.fromAlpha(
              Cesium.Color.fromCssColorString(
                this.$store.state.peopleStyle.IconColor
              ),
              1 - this.$store.state.peopleStyle.IconTransparency / 100
            ),
          });
        } else entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
          color: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.peopleStyle.color
            ),
            1 - this.$store.state.peopleStyle.transparency / 100
          ),
          pixelSize: this.$store.state.peopleStyle.size,
          outlineColor: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.peopleStyle.OutLineColor
            ),
            1 - this.$store.state.peopleStyle.OutLineTransparency / 100
          ),
          OutLineWidth: this.$store.state.peopleStyle.OutLineWidth,
        });
      }
      for (let i = 0; i < this.condition.plt_x_infectionSet[0].length; i++) {
        var entityInfection = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_x_infectionSet[0][i],
            this.condition.plt_y_infectionSet[0][i]
          ),
        });
        if (this.$store.state.injectionStyle.IconShow) {
          entityInfection.billboard = new Cesium.BillboardGraphics({
            image:
              this.$store.state.icon[this.$store.state.injectionStyle.IconIndex]
                .path,
            height: this.$store.state.injectionStyle.IconHeight,
            width: this.$store.state.injectionStyle.IconWidth,
            rotation: Cesium.Math.toRadians(
              this.$store.state.injectionStyle.IconRotation
            ),
            color: Cesium.Color.fromAlpha(
              Cesium.Color.fromCssColorString(
                this.$store.state.injectionStyle.IconColor
              ),
              1 - this.$store.state.injectionStyle.IconTransparency / 100
            ),
          });
        } else entityInfection.billboard = undefined;
        let alt = this.view.Alt * 40;
        entityInfection.point = new Cesium.PointGraphics({
          color: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.injectionStyle.color
            ),
            1 - this.$store.state.injectionStyle.transparency / 100
          ),
          pixelSize: this.$store.state.injectionStyle.size,
          outlineColor: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.injectionStyle.OutLineColor
            ),
            1 - this.$store.state.injectionStyle.OutLineTransparency / 100
          ),
          OutLineWidth: this.$store.state.injectionStyle.OutLineWidth,
        });
        if (this.$store.state.injectionStyle.spread) {
          entityInfection.ellipse = new Cesium.EllipseGraphics({
            semiMinorAxis: new Cesium.CallbackProperty(function () {
              r1 = r1 + 5;
              if (r1 >= alt) {
                r1 = 0;
              }
              return r1;
            }, false),
            semiMajorAxis: new Cesium.CallbackProperty(function () {
              r2 = r2 + 5;
              if (r2 >= alt) {
                r2 = 0;
              }
              return r2;
            }, false),
            height: 10,
            material: new Cesium.ImageMaterialProperty({
              repeat: new Cesium.Cartesian2(1.0, 1.0),
              transparent: true,
              color: Cesium.Color.fromAlpha(
                Cesium.Color.fromCssColorString(
                  this.$store.state.injectionStyle.color
                ),
                0.1
              ),
            }),
          });
        }
      }
      for (let i = 0; i < this.condition.plt_x_sickSet[0].length; i++) {
        var entitySick = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_x_sickSet[0][i],
            this.condition.plt_y_sickSet[0][i]
          ),
        });
        if (this.$store.state.sickStyle.IconShow) {
          entitySick.billboard = new Cesium.BillboardGraphics({
            image:
              this.$store.state.icon[this.$store.state.sickStyle.IconIndex]
                .path,
            height: this.$store.state.sickStyle.IconHeight,
            width: this.$store.state.sickStyle.IconWidth,
            rotation: Cesium.Math.toRadians(
              this.$store.state.sickStyle.IconRotation
            ),
            color: Cesium.Color.fromAlpha(
              Cesium.Color.fromCssColorString(
                this.$store.state.sickStyle.IconColor
              ),
              1 - this.$store.state.sickStyle.IconTransparency / 100
            ),
          });
        } else entitySick.billboard = undefined;
        entitySick.point = new Cesium.PointGraphics({
          color: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(this.$store.state.sickStyle.color),
            1 - this.$store.state.sickStyle.transparency / 100
          ),
          pixelSize: this.$store.state.sickStyle.size,
          outlineColor: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.sickStyle.OutLineColor
            ),
            1 - this.$store.state.sickStyle.OutLineTransparency / 100
          ),
          OutLineWidth: this.$store.state.sickStyle.OutLineWidth,
        });
        if (this.$store.state.sickStyle.spread) {
          let alt = this.view.Alt * 40;
          entitySick.ellipse = new Cesium.EllipseGraphics({
            semiMinorAxis: new Cesium.CallbackProperty(function () {
              r1 = r1 + 5;
              if (r1 >= alt) {
                r1 = 0;
              }
              return r1;
            }, false),
            semiMajorAxis: new Cesium.CallbackProperty(function () {
              r2 = r2 + 5;
              if (r2 >= alt) {
                r2 = 0;
              }
              return r2;
            }, false),
            height: 10,
            material: new Cesium.ImageMaterialProperty({
              repeat: new Cesium.Cartesian2(1.0, 1.0),
              transparent: true,
              color: Cesium.Color.fromAlpha(
                Cesium.Color.fromCssColorString(
                  this.$store.state.sickStyle.color
                ),
                0.1
              ),
            }),
          });
        }
      }
      for (let i = 0; i < this.condition.plt_x_isolationSet[0].length; i++) {
        var entityIsolation = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_x_isolationSet[0][i],
            this.condition.plt_y_isolationSet[0][i]
          ),
        });
        if (this.$store.state.isolationStyle.IconShow) {
          entityIsolation.billboard = new Cesium.BillboardGraphics({
            image:
              this.$store.state.icon[this.$store.state.isolationStyle.IconIndex]
                .path,
            height: this.$store.state.isolationStyle.IconHeight,
            width: this.$store.state.isolationStyle.IconWidth,
            rotation: Cesium.Math.toRadians(
              this.$store.state.isolationStyle.IconRotation
            ),
            color: Cesium.Color.fromAlpha(
              Cesium.Color.fromCssColorString(
                this.$store.state.isolationStyle.IconColor
              ),
              1 - this.$store.state.isolationStyle.IconTransparency / 100
            ),
          });
        } else entityIsolation.billboard = undefined;
        entityIsolation.point = new Cesium.PointGraphics({
          color: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.isolationStyle.color
            ),
            1 - this.$store.state.isolationStyle.transparency / 100
          ),
          pixelSize: this.$store.state.isolationStyle.size,
          outlineColor: Cesium.Color.fromAlpha(
            Cesium.Color.fromCssColorString(
              this.$store.state.isolationStyle.OutLineColor
            ),
            1 - this.$store.state.isolationStyle.OutLineTransparency / 100
          ),
          OutLineWidth: this.$store.state.isolationStyle.OutLineWidth,
        });
      }
    },
  },
  created() {
    this.AddViewSign = this.$store.state.AddViewSign;
    this.views = this.$store.state.views;
    this.conditions = this.$store.state.conditions;
    if (this.AddViewSign) this.viewIndex = 0;
    else this.viewIndex = this.$store.state.NowViewIndex;
    this.view = this.views[this.viewIndex];
    this.condition = this.conditions[this.viewIndex];
  },
  mounted() {
    this.AddViewSign = this.$store.state.AddViewSign;
    this.$store.commit("AddViewSignSubmit", false);
    this.views = this.$store.state.views;
    this.conditions = this.$store.state.conditions;
    if (this.AddViewSign) this.viewIndex = 0;
    this.view = this.views[this.viewIndex];
    this.condition = this.conditions[this.viewIndex];
    this.update();
    console.log(1);
    this.CesiumInit();
  },
};
</script>

<style scoped>
</style>