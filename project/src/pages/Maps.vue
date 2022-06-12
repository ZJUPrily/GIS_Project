<template>
  <div>
    <div id="map" style="margin-buttom : 0"></div>
    <div id="control" v-show="conditionControl" style="position: fixed;top :570px;width:100%">
      <md-button
        class="md-primary md-fab md-mini md-icon-button"
        style="position:absolute;top: 0%;left :5%"
        v-show="onPlay"
        @click="function(){stopPlay()}"
      >
        <md-icon>pause</md-icon>
      </md-button>
      <md-button
        class="md-primary md-fab md-mini md-icon-button"
        style="position:absolute;top: 0%;left :5%"
        v-show="offPlay"
        @click="function(){beginPlay()}"
      >
        <md-icon>play_arrow</md-icon>
      </md-button>
      <input
        type="range"
        v-model.number="nowDay"
        class="md-raised md-primary"
        style="width: 60%;position:absolute;top: 20px;left :10%"
        id="dayRange"
        ref="range"
        min="0"
        v-show="afterComp"
      />
      <span
        class="md-body-2"
        style="position:absolute;top: 19px;left :71%"
        v-show="afterComp"
      >{{"Day " + nowDay}}</span>
      <md-button
        class="md-raised md-primary"
        v-show="beforeComp"
        style="width: 40%;left: 20%;"
        @click="function(){simulation()}"
      >
        <md-icon>coronavirus</md-icon>Start Simulation! ! !
      </md-button>
      <md-progress-spinner
        md-mode="indeterminate"
        :md-diameter="45"
        v-show="inComp"
        style="left: 30%;"
      ></md-progress-spinner>
      <span
        v-show="inComp"
        class="md-headline"
        style="top: 20%;left: 37%;position:absolute"
      >{{"Processing: "+progressPresent+"%"}}</span>
      <md-icon
        style="top: 20%;left: 30.8%;position:absolute"
        class="md-primary"
        v-show="inComp"
      >coronavirus</md-icon>
      <md-progress-bar
        md-mode="buffer"
        :md-value="progressPresent"
        :md-buffer="0"
        v-show="inComp"
        style="width: 60%;left: 10%;"
      ></md-progress-bar>
    </div>
    <md-dialog :md-active.sync="showDialogSucceed">
      <md-dialog-title>Succeed!</md-dialog-title>
      <p md-label="General" style="margin: 10px 50px">Succeed in Simulation!</p>
      <md-dialog-actions>
        <md-button class="md-primary" @click="showDialogSucceed = false">OK</md-button>
      </md-dialog-actions>
    </md-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
import * as Cesium from "cesium/Source/Cesium";
import "cesium/Source/Widgets/widgets.css";
export default {
  name: "Cesium",
  computed: {
    CesiumMonitor() {
      return this.$store.state.CesiumChange;
    },
    ViewMonitor() {
      return this.$store.state.ViewChange;
    },
    dayMonitor() {
      return this.nowDay;
    },
  },
  watch: {
    ViewMonitor() {
      this.view = this.$store.state.views[this.$store.state.NowViewIndex];
      this.conditionInit();
    },
    CesiumMonitor() {
      this.viewer.imageryLayers.removeAll(false);
      this.viewer.dataSources.removeAll(false);
      this.viewer.entities.removeAll(false);
      var dtLayer = new Cesium.ArcGisMapServerImageryProvider({
        url: "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
        subdomains: ["a", "b", "c", "d"],
      });
      this.viewer.imageryLayers.addImageryProvider(dtLayer);
      this.GetLayers();
      var LayerGroup = [];
      for (let index = this.layers.length - 1; index >= 0; index--) {
        if (this.layers[index].show == true) {
          if (this.layers[index].service == "WMS") {
            var provider = new Cesium.WebMapServiceImageryProvider({
              url: this.layers[index].url,
              layers: this.layers[index].layer,
              parameters: {
                service: this.layers[index].service,
                format: this.layers[index].format,
              },
            });
            LayerGroup.push(provider);
            var NowLayer =
              this.viewer.imageryLayers.addImageryProvider(provider);
            NowLayer.alpha = 1 - this.layers[index].transparency / 100;
          } else if (this.layers[index].service == "WMTS") {
            var provider = new Cesium.WebMapTileServiceImageryProvider({
              url: this.layers[index].url,
              layer: this.layers[index].layer,
              format: this.layers[index].format,
              style: "",
              tileMatrixSetID: "EPSG:900913",
            });
            LayerGroup.push(provider);
            var NowLayer =
              this.viewer.imageryLayers.addImageryProvider(provider);
            NowLayer.alpha = 1 - this.layers[index].transparency / 100;
          } else if (this.layers[index].service == "TMS") {
            var provider = new Cesium.UrlTemplateImageryProvider({
              url: this.layers[index].url,
            });
            LayerGroup.push(provider);
            var NowLayer =
              this.viewer.imageryLayers.addImageryProvider(provider);
            NowLayer.alpha = 1 - this.layers[index].transparency / 100;
          } else if (this.layers[index].service == "WFS") {
            let data = this.layers[index].url;
            var that = this;
            Cesium.GeoJsonDataSource.load(data).then(function (NowLayer) {
              that.viewer.dataSources.add(NowLayer);
            });
          } else if (this.layers[index].service == "OpenStreetMap") {
            var tdtLayer = new Cesium.UrlTemplateImageryProvider({
              url: this.layers[index].url,
              subdomains: ["a", "b", "c", "d"],
            });
            var NowLayer =
              this.viewer.imageryLayers.addImageryProvider(tdtLayer);
            NowLayer.alpha = 1 - this.layers[index].transparency / 100;
          } else if (this.layers[index].service == "ArcGIS") {
            var tdtLayer = new Cesium.ArcGisMapServerImageryProvider({
              url: this.layers[index].url,
              subdomains: ["a", "b", "c", "d"],
            });
            var NowLayer =
              this.viewer.imageryLayers.addImageryProvider(tdtLayer);
            NowLayer.alpha = 1 - this.layers[index].transparency / 100;
          } else if (this.layers[index].service == "LOCAL") {
            let data = this.layers[index].url;
            if (this.layers[index].type == "GeoJson") {
              var that = this;
              Cesium.GeoJsonDataSource.load("data/" + data).then(function (
                NowLayer
              ) {
                that.viewer.dataSources.add(NowLayer);
                var entities = NowLayer.entities.values;
                for (let i = 0; i < entities.length; i++) {
                  var entity = entities[i];
                  if (that.layers[index].format == "point") {
                    if (that.layers[index].IconShow) {
                      entity.billboard = new Cesium.BillboardGraphics({
                        image:
                          that.$store.state.icon[that.layers[index].IconIndex]
                            .path,
                        height: that.layers[index].IconHeight,
                        width: that.layers[index].IconWidth,
                        rotation: Cesium.Math.toRadians(
                          that.layers[index].IconRotation
                        ),
                        color: Cesium.Color.fromAlpha(
                          Cesium.Color.fromCssColorString(
                            that.layers[index].IconColor
                          ),
                          1 - that.layers[index].IconTransparency / 100
                        ),
                      });
                    } else entity.billboard = undefined;
                    that.layers[index].propertyNames =
                      entity.properties.propertyNames;
                    that.SubmitLayer();
                    var propertyName =
                      entity.properties.propertyNames[
                        that.layers[index].LabelProperty
                      ];
                    var propertyValue = entity.properties[propertyName]._value;
                    entity.label = new Cesium.LabelGraphics({
                      show: that.layers[index].LabelShow,
                      text: String(propertyValue),
                    });
                    entity.point = new Cesium.PointGraphics({
                      color: Cesium.Color.fromAlpha(
                        Cesium.Color.fromCssColorString(
                          that.layers[index].color
                        ),
                        1 - that.layers[index].transparency / 100
                      ),
                      pixelSize: that.layers[index].size,
                      outlineColor: Cesium.Color.fromAlpha(
                        Cesium.Color.fromCssColorString(
                          that.layers[index].OutLineColor
                        ),
                        1 - that.layers[index].OutLineTransparency / 100
                      ),
                      outlineWidth: that.layers[index].OutLineWidth,
                    });
                  }
                }
              });
            } else if (this.layers[index].type == "GLTF") {
              var position = Cesium.Cartesian3.fromDegrees(
                this.layers[index].EntityLon,
                this.layers[index].EntityLat,
                this.layers[index].EntityAl,
                this.viewer.scene.globe.ellipsoid
              );
              var heading = Cesium.Math.toRadians(
                this.layers[index].EntityHeading
              );
              var pitch = this.layers[index].EntityPitch;
              var roll = this.layers[index].EntityRoll;
              var hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
              var orientation = Cesium.Transforms.headingPitchRollQuaternion(
                position,
                hpr
              );

              var entity = this.viewer.entities.add({
                position: position,
                orientation: orientation,
                model: {
                  uri: "data/" + this.layers[index].url,
                  minimumPixelSize: 128,
                  maximumScale: 20000,
                  silhouetteColor: Cesium.Color.fromAlpha(
                    Cesium.Color.fromCssColorString(
                      this.layers[index].OutLineColor
                    ),
                    1 - this.layers[index].OutLineTransparency / 100
                  ),
                  silhouetteSize: this.layers[index].OutLineWidth,
                  color: Cesium.Color.fromAlpha(
                    Cesium.Color.fromCssColorString(this.layers[index].color),
                    1 - this.layers[index].transparency / 100
                  ),
                  scale: this.layers[index].size,
                },
              });
            } else if (this.layers[index].type == "3DTile") {
              this.viewer.scene.primitives.removeAll(false);
              var tilesetModel = new Cesium.Cesium3DTileset({
                url: "data/" + this.layers[index].url,
              });
              this.viewer.scene.primitives.add(tilesetModel);
              tilesetModel.style = new Cesium.Cesium3DTileStyle({
                color: {
                  conditions: [
                    [
                      "${Height} >= " +
                        String(this.layers[index].ModelSplitHeightSet[0]),
                      'color("' +
                        this.layers[index].ModelColorSet[0] +
                        '",' +
                        String(1.0 - this.layers[index].transparency / 100) +
                        " )",
                    ],
                    [
                      "true",
                      'color("' +
                        this.layers[index].ModelColorSet[1] +
                        '",' +
                        String(1.0 - this.layers[index].transparency / 100) +
                        " )",
                    ],
                  ],
                },
              });
            } else if (this.layers[index].type == "TopoJson") {
              var highlightedEntity;
              var highlightColor = Cesium.Color.GREEN.withAlpha(0.6);
              var normalColor = Cesium.Color.YELLOW.withAlpha(0.6);

              //一种属性，如果实体当前被鼠标悬停，则返回高亮显示颜色，否则返回默认颜色.
              function createCallback(entity) {
                var colorProperty = new Cesium.CallbackProperty(function (
                  time,
                  result
                ) {
                  if (highlightedEntity === entity) {
                    return Cesium.Color.clone(highlightColor, result);
                  }
                  return Cesium.Color.clone(normalColor, result);
                },
                false);
                return new Cesium.ColorMaterialProperty(colorProperty);
              }
              var that = this;
              Cesium.GeoJsonDataSource.load("data/" + data).then(function (
                NowLayer
              ) {
                that.viewer.dataSources.add(NowLayer);
                var entities = NowLayer.entities.values;
                for (let i = 0; i < entities.length; i++) {
                  var entity = entities[i];
                  entity.polygon.material = createCallback(entity);
                }
              });

              var scene = this.viewer.scene;
              var handler = this.viewer.screenSpaceEventHandler;
              handler.setInputAction(function (movement) {
                var pickedObject = scene.pick(movement.endPosition);
                if (
                  Cesium.defined(pickedObject) &&
                  pickedObject.id instanceof Cesium.Entity
                ) {
                  highlightedEntity = pickedObject.id;
                } else {
                  highlightedEntity = undefined;
                }
              }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
            }
          }
        }
      }
    },
    dayMonitor() {
      if (this.offPlay) this.showCondition(this.nowDay);
    },
  },
  data() {
    return {
      layers: [],
      viewer: null,
      view: null,
      condition: null,
      conditionControl: false,
      beforeComp: false,
      inComp: false,
      afterComp: false,
      progressPresent: 0,
      utc: new Cesium.JulianDate.fromDate(new Date("2021/07/04 04:00:00")),
      onPlay: false,
      offPlay: false,
      nowDay: 0,
      showDialogSucceed: false,
      handler: null,
    };
  },
  methods: {
    SubmitLayer() {
      this.$store.commit("UpdateLayersToStore", this.layers);
    },
    GetLayers() {
      this.layers = this.$store.state.layers;
    },
    addGeoJson(index) {
      let { data } = axios.get(this.layers[index].url);
      this.viewer.dataSources.add(Cesium.GeoJsonDataSource.load(data));
    },
    getChinaPostion() {
      return Cartesian3.fromDegrees(116.435314, 40.960521, 10000000.0);
    },
    flytochina() {
      this.viewer.camera.flyTo({
        destination: this.getChinaPostion(),
        duration: 8,
      });
    },
    conditionInit() {
      this.nowDay = 0;
      this.offPlay = false;
      this.onPlay = false;
      this.beforeComp = false;
      this.inComp = false;
      this.afterComp = false;
      this.$store.state.conditionSelectSign = true;
      this.condition =
        this.$store.state.conditions[this.$store.state.NowViewIndex];
      this.conditionControl = true;
      this.showCondition(0);
      if (this.condition.haveComp) {
        this.afterComp = true;
        this.offPlay = true;
        this.nowDay = 0;
      } else this.beforeComp = true;
      this.$refs.range.max = this.condition.total_day - 1;
    },
    showCondition(day) {
      if (day == 0) {
        this.viewer.camera.flyTo({
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
      }
      if (this.beforeComp == true) {
        let rectangle = this.viewer.camera.computeViewRectangle();
        this.condition.west = Cesium.Math.toDegrees(rectangle.west);
        this.condition.east = Cesium.Math.toDegrees(rectangle.east);
        this.condition.north = Cesium.Math.toDegrees(rectangle.north);
        this.condition.south = Cesium.Math.toDegrees(rectangle.south);
      }
      let oldEntities = [];
      this.viewer.entities.values.forEach((c) => {
        oldEntities.push(this.viewer.entities.getById(c.id));
      });
      let r1 = 50;
      let r2 = 50;
      console.log(this.$store.state.conditions);
      console.log(this.$store.state.NowViewIndex);
      for (let i = 0; i < this.condition.plt_xSet[day].length; i++) {
        var entity = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_xSet[day][i],
            this.condition.plt_ySet[day][i]
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
      for (let i = 0; i < this.condition.plt_x_infectionSet[day].length; i++) {
        var entityInfection = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_x_infectionSet[day][i],
            this.condition.plt_y_infectionSet[day][i]
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
      for (let i = 0; i < this.condition.plt_x_sickSet[day].length; i++) {
        var entitySick = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_x_sickSet[day][i],
            this.condition.plt_y_sickSet[day][i]
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
      for (let i = 0; i < this.condition.plt_x_isolationSet[day].length; i++) {
        var entityIsolation = this.viewer.entities.add({
          name: "conidition",
          position: new Cesium.Cartesian3.fromDegrees(
            this.condition.plt_x_isolationSet[day][i],
            this.condition.plt_y_isolationSet[day][i]
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
      oldEntities.forEach((c) => {
        this.viewer.entities.remove(this.viewer.entities.getById(c.id));
      });
    },
    computing(day) {
      if (day >= this.condition.total_day) {
        this.condition.haveComp = this.$store.state.conditions[
          this.$store.state.NowViewIndex
        ].haveComp = true;
        this.$store.state.conditions[this.$store.state.NowViewIndex] =
          this.condition;
        this.inComp = false;
        this.afterComp = true;
        this.offPlay = true;
        this.onPlay = false;
        this.showDialogSucceed = true;
        // 鼠标移入自定义弹出框

        this.showCondition(0);
        return;
      } else {
        this.condition.day = day;
        let postData = this.condition;
        axios({
          url: "http://localhost:5000/injection",
          method: "post",
          data: postData,
        })
          .then((response) => {
            this.condition = response.data;
            this.progressPresent = (
              (day * 100) /
              this.condition.total_day
            ).toFixed(0);
            this.viewer.clockViewModel.currentTime = this.utc =
              Cesium.JulianDate.addHours(this.utc, 2, new Cesium.JulianDate());
            this.showCondition(day);
            return this.computing(day + 1);
          })
          .finally()
          .catch((response) => {
            console.log(response);
          });
      }
      return;
    },
    simulation() {
      this.beforeComp = false;
      this.inComp = true;
      this.computing(1);
    },
    beginPlay() {
      this.onPlay = true;
      this.offPlay = false;
      for (let i = this.nowDay; i < this.condition.total_day; i++) {
        setTimeout((_) => {
          if (this.onPlay) {
            this.showCondition(i);
            this.nowDay = i;
            this.viewer.clockViewModel.currentTime = this.utc =
              Cesium.JulianDate.addHours(this.utc, 2, new Cesium.JulianDate());
            if (i == this.condition.total_day - 1) {
              this.onPlay = false;
              this.offPlay = true;
            }
          }
        }, 3000);
      }
    },
    stopPlay() {
      this.onPlay = false;
      this.offPlay = true;
    },
  },
  mounted() {
    this.$store.state.conditionSelectSign = false;
    Cesium.Camera.DEFAULT_VIEW_RECTANGLE = Cesium.Rectangle.fromDegrees(
      90,
      -20,
      130,
      50
    ); //home定位到中国范围
    Cesium.Ion.defaultAccessToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NTRkMzQ0Zi0yYTExLTQyMjMtYjJkMS0yNmZkYTA1MTgwMjgiLCJpZCI6ODY3NzIsImlhdCI6MTY0ODAxODI2MX0.B6IPcv0jQqjLqH8w40gPyZHkW5uK7tKGlwnPgDxhw8o";
    this.viewer = new Cesium.Viewer("map", {
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
    this.viewer.scene.globe.enableLighting = true; //开启场景光照
    var terrain = Cesium.createWorldTerrain({
        requestWaterMask: true,        // 开启水光效果
        requestVertexNormals: true     // 开启地形光照
    });
    this.viewer.terrainProvider = terrain;
    var change = this.$store.state.CesiumChange;
    this.$store.commit("SituationChange", !change);
  },
};
</script>

<style scoped>
.md-fab {
  width: 40%;
  left: 30%;
}
</style>
