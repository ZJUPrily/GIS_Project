<template>
  <div class="md-layout">
    <div class="md-layout-item md-medium-size-100 md-size-66">
      <md-card>
        <md-card-header :data-background-color="dataBackgroundColor">
          <h4 class="title">Condition Sytle</h4>
          <p class="category">Set the style of the condition</p>
        </md-card-header>

        <md-card-content>
          <div class="md-layout">
            <div class="md-layout-item md-small-size-100 md-size-50">
              <div id="Stylemap" style="left:20%"></div>
            </div>
            <div class="md-layout-item md-small-size-100 md-size-50">
              <md-field>
                <label for="font">Point Type</label>
                <md-select
                  name="font"
                  id="font"
                  @input="function(){LayerStyleChange()}"
                  v-model="pointType"
                >
                  <md-option value="0">Common People</md-option>
                  <md-option value="1">Injected People</md-option>
                  <md-option value="2">Sick People</md-option>
                  <md-option value="3">Isolated People</md-option>
                </md-select>
              </md-field>
              
              
            </div>
            <div class="md-layout-item md-small-size-100 md-size-50">
              <b>Show Infected Area</b>
              <br />
              <md-switch
                v-model="pointStyle.spread"
                v-show="(pointType==1 || pointType==2) && pointStyle.spread "
                @change="LayerStyleChange()"
              >Infected on</md-switch>
              <md-switch
                v-model="pointStyle.spread"
                v-show="(pointType==1 || pointType==2) && !pointStyle.spread "
                @change="LayerStyleChange()"
              >Infected off</md-switch>
              <md-switch v-show="(pointType!=1 && pointType!=2)">Do Not Support</md-switch>
              <br />
              <b>Point Size</b>
              <br />
              <input
                type="range"
                v-model.number="pointStyle.size"
                @input="function(){LayerStyleChange()}"
                style="width :90%"
              />
              <span>{{pointStyle.size}}px</span>
              <br />
              <b>Point Transparency</b>
            <input
              type="range"
              v-model.number="pointStyle.transparency"
              @input="function(){LayerStyleChange()}"
              style="width :90%"
            />
            <span >{{pointStyle.transparency}}%</span>
              <br />
              <b>Point Color</b>
              <br />
              <colorPicker v-model="pointStyle.color" @change="LayerStyleChange()" />
              Color:{{pointStyle.color}}
              <br />
              <b>Point Outline Width</b>
              <br />
              <input
                type="range"
                style="width :90%"
                v-model.number="pointStyle.OutLineWidth"
                min="1"
                @input="function(){LayerStyleChange()}"
              />
              <span>{{pointStyle.OutLineWidth}}px</span>
              <br />
              <b>Point OutLine Transparency</b>
              <br />
              <input
                type="range"
                v-model.number="pointStyle.OutLineTransparency"
                @input="function(){LayerStyleChange()}"
                style="width :90%"
              />
              <span>{{pointStyle.OutLineTransparency}}%</span>
              <br />
              <b>Point OutLine Color</b>
              <br />
              <colorPicker v-model="pointStyle.OutLineColor" @change="LayerStyleChange()" />
              Color:{{pointStyle.OutLineColor}}
              <br />
            </div>
            <div class="md-layout-item md-small-size-100 md-size-50">
              <b>Point Icon</b>
              <br />
              <md-switch
                v-model="pointStyle.IconShow"
                v-if="pointStyle.IconShow"
                @change="LayerStyleChange()"
              >Icon Stylized on</md-switch>
              <md-switch
                v-model="pointStyle.IconShow"
                v-else
                @change="LayerStyleChange()"
              >Icon Stylized off</md-switch>
              <br />
              <b>Icon Color</b>
              <br />
              <colorPicker v-model="pointStyle.IconColor" @change="LayerStyleChange()" />
              Color:{{pointStyle.IconColor}}
              <br />
              <md-field style="top:0px">
                <label for="Property for Label">Property for Label</label>
                <md-select
                  name="Property for Label"
                  v-model="pointStyle.IconIndex"
                  @input="LayerStyleChange()"
                >
                  <md-option
                    v-for="(item, index) in icon = this.$store.state.icon"
                    v-bind:value="index"
                  >{{item.name}}</md-option>
                </md-select>
              </md-field>
              <b>Icon Width</b>
              <br />
              <input
                type="range"
                v-model.number="pointStyle.IconWidth"
                @input="function(){LayerStyleChange()}"
                style="width :90%"
              />
              <span>{{pointStyle.IconWidth}}px</span>
              <br />
              <b>Icon Height</b>
              <br />
              <input
                type="range"
                v-model.number="pointStyle.IconHeight"
                @input="function(){LayerStyleChange()}"
                style="width :90%"
              />
              <span>{{pointStyle.IconHeight}}px</span>
              <br />
              <b>Icon Rotation</b>
              <br />
              <input
                type="range"
                max="360"
                min="-360"
                v-model.number="pointStyle.IconRotation"
                @input="function(){LayerStyleChange()}"
                style="width :90%"
              />
              <span>{{pointStyle.IconRotation}}°</span>
              <br />
              <b>Icon Transparency</b>
              <br />
              <input
                type="range"
                v-model.number="pointStyle.IconTransparency"
                @input="function(){LayerStyleChange()}"
                style="width :90%"
              />
              <span>{{pointStyle.IconTransparency}}%</span>
              <br />
            </div>
          </div>
        </md-card-content>
      </md-card>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "conStyle",
  props: {
    dataBackgroundColor: {
      type: String,
      default: "green",
    },
  },
  data() {
    return {
      pointType: 0,
      pointStyle: null,
    };
  },
  methods: {
    showInitCondition() {
      let rectangle = this.viewer.camera.computeViewRectangle();
      var x =
        (Cesium.Math.toDegrees(rectangle.east) +
          Cesium.Math.toDegrees(rectangle.west)) /
        2;
      var y =
        (Cesium.Math.toDegrees(rectangle.north) +
          Cesium.Math.toDegrees(rectangle.south)) /
        2;
      this.viewer.entities.removeAll();
      let r1 = 5000;
      let r2 = 5000;
      let Alt = 10000;
      if (this.pointType == 0) {
        var entity = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(x, y),
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
      if (this.pointType == 1) {
        var entityInfection = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(x, y),
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
        let alt = Alt * 40;
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
              r1 = r1 + 5000;
              if (r1 >= alt) {
                r1 = 0;
              }
              return r1;
            }, false),
            semiMajorAxis: new Cesium.CallbackProperty(function () {
              r2 = r2 + 5000;
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
      if (this.pointType == 2) {
        var entitySick = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(x, y),
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
          let alt = Alt * 40;
          entitySick.ellipse = new Cesium.EllipseGraphics({
            semiMinorAxis: new Cesium.CallbackProperty(function () {
              r1 = r1 + 5000;
              if (r1 >= alt) {
                r1 = 0;
              }
              return r1;
            }, false),
            semiMajorAxis: new Cesium.CallbackProperty(function () {
              r2 = r2 + 5000;
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
      if (this.pointType == 3) {
        var entityIsolation = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(x, y),
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
    CesiumInit() {
      Cesium.Camera.DEFAULT_VIEW_RECTANGLE = Cesium.Rectangle.fromDegrees(
        0,
        90,
        0,
        -90
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
    },
    LayerStyleChange() {
      if (this.pointType == 0) this.pointStyle = this.$store.state.peopleStyle;
      if (this.pointType == 1)
        this.pointStyle = this.$store.state.injectionStyle;
      if (this.pointType == 2) this.pointStyle = this.$store.state.sickStyle;
      if (this.pointType == 3)
        this.pointStyle = this.$store.state.isolationStyle;
      this.StyleChange = !this.StyleChange;
      this.showInitCondition();
    },
  },
  computed: {
    StyleMeumMonitor() {
      return this.$store.state.StyleChange;
    },
    StyleChangeMonitor() {
      return this.StyleChange;
    },
  },
  watch: {
    StyleChangeMonitor: {
      handler: function (val, oldVal) {
        this.layers[this.index] = this.layer;
        this.$store.commit("UpdateLayersToStore", this.layers);
        var change = this.$store.state.CesiumChange;
        this.$store.commit("SituationChange", !change);
      },
      deep: true,
    },
  },
  created() {
    this.pointType = 0;
    if (this.pointType == 0) this.pointStyle = this.$store.state.peopleStyle;
    if (this.pointType == 1) this.pointStyle = this.$store.state.injectionStyle;
    if (this.pointType == 2) this.pointStyle = this.$store.state.sickStyle;
    if (this.pointType == 3) this.pointStyle = this.$store.state.isolationStyle;
  },
  mounted() {
    this.CesiumInit();
    if (this.pointType == 0) this.pointStyle = this.$store.state.peopleStyle;
    if (this.pointType == 1) this.pointStyle = this.$store.state.injectionStyle;
    if (this.pointType == 2) this.pointStyle = this.$store.state.sickStyle;
    if (this.pointType == 3) this.pointStyle = this.$store.state.isolationStyle;
    this.showInitCondition();
  },
};
</script>
<style>
</style>
