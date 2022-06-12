<template>
  <div id="StyleMeum" style="width:1000px;height:600px">
    <md-content class="md-scrollbar" style="width:1000px;height=500px">
      <md-card style="width:280px;height=700px;right:0px;">
        <md-card-header data-background-color="green">
          <h4 class="title" v-model="layer">{{ layer.name + " Style" }}</h4>
          <p class="category">{{ layer.service }}-{{layer.type}}-{{layer.format}}</p>
        </md-card-header>

        <md-card-content v-if="StyleMeumPage==1">
          <div v-if="TransparencyShow">
            Transparency
            <br />
            <input
              type="range"
              v-model.number="layer.transparency"
              @input="function(){LayerStyleChange()}"
              v-if="TransparencyPermitSign"
            />

            <input
              type="range"
              v-model.number="layer.transparency"
              @input="function(){LayerStyleChange()}"
              v-else
              disabled
            />
            <span v-if="TransparencyPermitSign">{{layer.transparency}}%</span>
            <span v-else>Forbidden</span>
          </div>

          <div v-if="PointPermitSign">
            Point Stylized
            <br />
            <b>Point Color</b>
            <br />
            <colorPicker v-model="layer.color" @change="LayerStyleChange()" />
            Color:{{layer.color}}
            <br />
            <b>Point Size</b>
            <br />
            <input type="range" v-model.number="layer.size" @input="function(){LayerStyleChange()}" />
            <span>{{layer.size}}px</span>
            <br />
            <b>Label</b>
            <br />
            <md-switch
              v-model="layer.LabelShow"
              v-if="layer.LabelShow"
              @change="LayerStyleChange()"
            >Label Shown</md-switch>
            <md-switch v-model="layer.LabelShow" v-else @change="LayerStyleChange()">Label Hidden</md-switch>
            <div class="md-layout-item">
              <md-field style="top:0px">
                <label for="Property for Label">Property for Label</label>
                <md-select
                  name="Property for Label"
                  v-model="layer.LabelProperty"
                  @input="LayerStyleChange()"
                >
                  <md-option
                    v-for="(item, index) in layer.propertyNames"
                    v-bind:value="index"
                  >{{item}}</md-option>
                </md-select>
              </md-field>
            </div>
          </div>

          <div v-else-if="GLTFPermitSign">
            GLTF Stylized
            <br />
            <b>GLTF Color</b>
            <br />
            <colorPicker v-model="layer.color" @change="LayerStyleChange()" />
            Color:{{layer.color}}
            <br />

            <b>Color transparency</b>
            <br />
            <input
              type="range"
              v-model.number="layer.transparency"
              @input="function(){LayerStyleChange()}"
            />
            <span>{{layer.transparency}}%</span>
            <br />
            <b>Scale</b>
            <br />
            <input
              type="range"
              v-model.number="layer.size"
              min="0"
              max="5"
              step="0.01"
              @input="function(){LayerStyleChange()}"
            />
            <span>{{layer.size}}</span>
            <br />
            <span>Position</span>
            <br />
            <b>Latitude</b>
            <br />
            <input
              type="range"
              v-model.number="layer.EntityLat"
              min="-90"
              max="90"
              step="0.01"
              @input="function(){LayerStyleChange()}"
            />
            <span>{{layer.EntityLat}}</span>
            <br />
            <b>Longitude</b>
            <br />
            <input
              type="range"
              v-model.number="layer.EntityLon"
              min="-180"
              max="180"
              step="0.01"
              @input="function(){LayerStyleChange()}"
            />
            <span>{{layer.EntityLon}}</span>
            <br />
            <b>Altitude</b>
            <br />
            <input
              type="range"
              v-model.number="layer.EntityAl"
              min="0"
              max="1000000"
              step="1000"
              @input="function(){LayerStyleChange()}"
            />
            <span>{{layer.EntityAl}}</span>
            <br />
          </div>

          <div v-else-if="ModelTilePermitSign">
            <b>Heigher Color</b>
            <br />
            <colorPicker v-model="layer.ModelColorSet[0]" @change="LayerStyleChange()" />
            Color:{{layer.ModelColorSet[0]}}
            <br />
            <b>Lower Color</b>
            <br />
            <colorPicker v-model="layer.ModelColorSet[1]" @change="LayerStyleChange()" />
            Color:{{layer.ModelColorSet[1]}}
            <br />
            <md-field md-clearable>
              <label>Height of Spilt Color</label>
              <md-input
                v-model="layer.ModelSplitHeightSet[0]"
                type="text"
                @input="function(){LayerStyleChange()}"
              ></md-input>
            </md-field>
          </div>

          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="StyleMeumPage++"
            v-if="StyleMeumPageTop!=StyleMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="StyleMeumPage--"
            v-if="StyleMeumPage!=1"
          >
            <md-icon>arrow_back_ios</md-icon>
          </md-icon-button>
        </md-card-content>

        <md-card-content v-if="StyleMeumPage==2">
          <div v-if="PointPermitSign">
            <b>Point Outline Width</b>
            <br />
            <input type="range" v-model.number="layer.OutLineWidth" min="1" @input="function(){LayerStyleChange()}" / >
            <span>{{layer.OutLineWidth}}px</span>
            <br />
            <div>
              <b>Point OutLine Transparency</b>
              <br />
              <input
                type="range"
                v-model.number="layer.OutLineTransparency"
                @input="function(){LayerStyleChange()}"
              />
              <span>{{layer.OutLineTransparency}}%</span>
              <br />
              <b>Point OutLine Color</b>
              <br />
              <colorPicker v-model="layer.OutLineColor" @change="LayerStyleChange()" />
              Color:{{layer.OutLineColor}}
              <br />
            </div>
          </div>

          <div v-else-if="GLTFPermitSign">
            <b>GLTF Outline Width</b>
            <br />
            <input
              type="range"
              v-model.number="layer.OutLineWidth"
              min="1"
              @input="function(){LayerStyleChange()}"
            />

            <span>{{layer.OutLineWidth}}px</span>
            <br />

            <b>GLTF OutLine Transparency</b>
            <br />
            <input
              type="range"
              v-model.number="layer.OutLineTransparency"
              @input="function(){LayerStyleChange()}"
            />
            <span>{{layer.OutLineTransparency}}%</span>
            <br />
            <b>GLTF OutLine Color</b>
            <br />
            <colorPicker v-model="layer.OutLineColor" @change="LayerStyleChange()" />
            Color:{{layer.OutLineColor}}
            <br />
          </div>

          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="StyleMeumPage++"
            v-if="StyleMeumPageTop!=StyleMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="StyleMeumPage--"
            v-if="StyleMeumPage!=1"
          >
            <md-icon>arrow_back_ios</md-icon>
          </md-icon-button>
        </md-card-content>

        <md-card-content v-if="StyleMeumPage==3">
          <div v-if="PointPermitSign">
            <div>
              <b>Point Icon</b>
              <br />
              <md-switch
                v-model="layer.IconShow"
                v-if="layer.IconShow"
                @change="LayerStyleChange()"
              >Icon Stylized on</md-switch>
              <md-switch
                v-model="layer.IconShow"
                v-else
                @change="LayerStyleChange()"
              >Icon Stylized off</md-switch>
              <br />
              <b>Icon Color</b>
              <br />
              <colorPicker v-model="layer.IconColor" @change="LayerStyleChange()" />
              Color:{{layer.IconColor}}
              <br />
              <md-field style="top:0px">
                <label for="Property for Label">Property for Label</label>
                <md-select
                  name="Property for Label"
                  v-model="layer.IconIndex"
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
                v-model.number="layer.IconWidth"
                @input="function(){LayerStyleChange()}"
              />
              <span>{{layer.IconWidth}}px</span>
              <br />
              <b>Icon Height</b>
              <br />
              <input
                type="range"
                v-model.number="layer.IconHeight"
                @input="function(){LayerStyleChange()}"
              />
              <span>{{layer.IconHeight}}px</span>
              <br />
              <b>Icon Rotation</b>
              <br />
              <input
                type="range"
                max="360"
                min="-360"
                v-model.number="layer.IconRotation"
                @input="function(){LayerStyleChange()}"
              />
              <span>{{layer.IconRotation}}°</span>
              <br />
              <b>Icon Transparency</b>
              <br />
              <input
                type="range"
                v-model.number="layer.IconTransparency"
                @input="function(){LayerStyleChange()}"
              />
              <span>{{layer.IconTransparency}}%</span>
              <br />
            </div>
          </div>

          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="StyleMeumPage++"
            v-if="StyleMeumPageTop!=StyleMeumPage"
          >
            <md-icon>arrow_forward_ios</md-icon>
          </md-icon-button>
          <md-icon-button
            class="md-button-toggle"
            style="float:right"
            v-on:click="StyleMeumPage--"
            v-if="StyleMeumPage!=1"
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
  </div>
</template>

<script>
import axios from "axios";
import * as Cesium from "cesium/Source/Cesium";
import "cesium/Source/Widgets/widgets.css";
export default {
  name: "style-meum",
  data() {
    return {
      layer: null,
      layers: [],
      layernames: [],
      index: 1,
      StyleChange: false,
      ServiceList: [],
      TransparencyPermitSign: true,
      PointPermitSign: true,
      StyleMeumPage: 1,
      StyleMeumPageTop: 1,
      viewer: null,
      DataSource: null,
      GLTFPermitSign: true,
      TransparencyShow: true,
      ModelTilePermitSign: true,
      highlightedEntity: null,
    };
  },
  StyleChange: false,
  computed: {
    StyleMeumMonitor() {
      return this.$store.state.StyleChange;
    },
    StyleChangeMonitor() {
      return this.StyleChange;
    },
  },
  watch: {
    StyleMeumMonitor: {
      handler: function (val, oldVal) {
        this.$forceUpdate();
      },
    },
    StyleChangeMonitor: {
      handler: function (val, oldVal) {
        this.layers[this.index] = this.layer;
        this.$store.commit("UpdateLayersToStore", this.layers);
        var change = this.$store.state.CesiumChange;
        this.$store.commit("SituationChange", !change);
        this.StyleLayerShow();
      },
      deep: true,
    },
  },
  methods: {
    BreakStyleBar() {
      this.$store.commit("StyleBarChangeSubmit", true);
    },
    update() {
      this.layers = this.$store.state.layers;
      this.index = this.$store.state.NowLayerIndex;
      this.layer = this.layers[this.index];
    },
    LayerStyleChange() {
      this.StyleChange = !this.StyleChange;
    },
    TransparencyPermit() {
      if (this.layer.service == "WFS" || this.layer.type == "GLTF")
        this.TransparencyPermitSign = false;
    },
    Permit() {
      if (this.layer.format != "point") this.PointPermitSign = false;
      if (this.layer.type != "GLTF") this.GLTFPermitSign = false;
      if (this.layer.type != "3DTile") this.ModelTilePermitSign = false;
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
    },
    StyleLayerShow() {
      var dafultLayer = this.viewer.imageryLayers.get(0);
      this.viewer.imageryLayers.removeAll(false);
      this.viewer.dataSources.removeAll(false);
      this.viewer.entities.removeAll(false);
      this.viewer.imageryLayers.add(dafultLayer);
      if (this.layer.service == "WMS") {
        var provider = new Cesium.WebMapServiceImageryProvider({
          url: this.layer.url,
          layers: this.layer.layer,
          parameters: {
            service: this.layer.service,
            format: this.layer.format,
          },
        });
        var NowLayer = this.viewer.imageryLayers.addImageryProvider(provider);
        this.viewer.flyTo(NowLayer);
        this.DataSource = NowLayer;
        NowLayer.alpha = 1 - this.layer.transparency / 100;
      } else if (this.layer.service == "WMTS") {
        var provider = new Cesium.WebMapTileServiceImageryProvider({
          url: this.layer.url,
          layer: this.layer.layer,
          format: this.layer.format,
          style: "",
          tileMatrixSetID: "EPSG:900913",
        });
        var NowLayer = this.viewer.imageryLayers.addImageryProvider(provider);
        this.DataSource = NowLayer;
        this.viewer.flyTo(this.DataSource);
        NowLayer.alpha = 1 - this.layer.transparency / 100;
      } else if (this.layer.service == "TMS") {
        var provider = new Cesium.UrlTemplateImageryProvider({
          url: this.layer.url,
        });
        this.DataSource = provider;
        var NowLayer = this.viewer.imageryLayers.addImageryProvider(provider);
        this.viewer.flyTo(NowLayer);
        this.DataSource = NowLayer;
        NowLayer.alpha = 1 - this.layer.transparency / 100;
      } else if (this.layer.service == "WFS") {
        let data = this.layer.url;
        var that = this;
        Cesium.GeoJsonDataSource.load(data).then(function (NowLayer) {
          that.viewer.dataSources.add(NowLayer);
          that.DataSource = NowLayer;
          that.viewer.flyTo(NowLayer);
        });
      } else if (this.layer.service == "OpenStreetMap") {
        var tdtLayer = new Cesium.UrlTemplateImageryProvider({
          url: this.layer.url,
          subdomains: ["a", "b", "c", "d"],
        });
        var NowLayer = this.viewer.imageryLayers.addImageryProvider(tdtLayer);
        this.viewer.flyTo(NowLayer);
        this.DataSource = NowLayer;
        NowLayer.alpha = 1 - this.layer.transparency / 100;
      } else if (this.layer.service == "ArcGIS") {
        var tdtLayer = new Cesium.ArcGisMapServerImageryProvider({
          url: this.layer.url,
          subdomains: ["a", "b", "c", "d"],
        });
        var NowLayer = this.viewer.imageryLayers.addImageryProvider(tdtLayer);
        this.DataSource = NowLayer;
        this.viewer.flyTo(NowLayer);
        NowLayer.alpha = 1 - this.layer.transparency / 100;
      } else if (this.layer.service == "LOCAL") {
        let data = this.layer.url;
        if (this.layer.type == "GeoJson") {
          var that = this;
          Cesium.GeoJsonDataSource.load("data/" + data).then(function (
            NowLayer
          ) {
            that.viewer.dataSources.add(NowLayer);
            that.DataSource = NowLayer;
            that.viewer.flyTo(NowLayer);
            var entities = NowLayer.entities.values;
            console.log(entities.length);
            for (let i = 0; i < entities.length; i++) {
              var entity = entities[i];
              if (that.layer.format == "point") {
                if (that.layer.IconShow) {
                  entity.billboard = new Cesium.BillboardGraphics({
                    image: that.$store.state.icon[that.layer.IconIndex].path,
                    height: that.layer.IconHeight,
                    width: that.layer.IconWidth,
                    rotation: Cesium.Math.toRadians(that.layer.IconRotation),
                    color: Cesium.Color.fromAlpha(
                      Cesium.Color.fromCssColorString(that.layer.IconColor),
                      1 - that.layer.IconTransparency / 100
                    ),
                  });
                } else entity.billboard = undefined;
                entity.point = new Cesium.PointGraphics({
                  color: Cesium.Color.fromAlpha(
                    Cesium.Color.fromCssColorString(that.layer.color),
                    1 - that.layer.transparency / 100
                  ),
                  pixelSize: that.layer.size,
                  outlineColor: Cesium.Color.fromAlpha(
                    Cesium.Color.fromCssColorString(that.layer.OutLineColor),
                    1 - that.layer.OutLineTransparency / 100
                  ),
                  OutLineWidth: that.layer.OutLineWidth,
                });
                that.layer.propertyNames = entity.properties.propertyNames;
                that.SubmitLayer();
                var propertyName =
                  entity.properties.propertyNames[that.layer.LabelProperty];
                var propertyValue = entity.properties[propertyName]._value;
                console.log(propertyValue);
                entity.label = new Cesium.LabelGraphics({
                  show: that.layer.LabelShow,
                  text: String(propertyValue),
                });
              }
            }
          });
        } else if (this.layer.type == "GLTF") {
          var position = Cesium.Cartesian3.fromDegrees(
            this.layer.EntityLon,
            this.layer.EntityLat,
            this.layer.EntityAl,
            this.viewer.scene.globe.ellipsoid
          );
          var heading = Cesium.Math.toRadians(this.layer.EntityHeading);
          var pitch = this.layer.EntityPitch;
          var roll = this.layer.EntityRoll;
          var hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
          var orientation = Cesium.Transforms.headingPitchRollQuaternion(
            position,
            hpr
          );

          var entity = this.viewer.entities.add({
            position: position,
            orientation: orientation,
            model: {
              uri: "data/" + this.layer.url,
              minimumPixelSize: 128,
              maximumScale: 20000,
              silhouetteColor: Cesium.Color.fromAlpha(
                Cesium.Color.fromCssColorString(this.layer.OutLineColor),
                1 - this.layer.OutLineTransparency / 100
              ),
              silhouetteSize: this.layer.OutLineWidth,
              color: Cesium.Color.fromAlpha(
                Cesium.Color.fromCssColorString(this.layer.color),
                1 - this.layer.transparency / 100
              ),
              scale: this.layer.size,
            },
          });
          this.viewer.flyTo(entity);
        } else if (this.layer.type == "3DTile") {
          this.viewer.scene.primitives.removeAll(false);
          var tilesetModel = new Cesium.Cesium3DTileset({
            url: "data/" + this.layer.url,
          });
          this.viewer.scene.primitives.add(tilesetModel);
          this.viewer.flyTo(tilesetModel);
          tilesetModel.style = new Cesium.Cesium3DTileStyle({
            color: {
              conditions: [
                [
                  "${Height} >= " + String(this.layer.ModelSplitHeightSet[0]),
                  'color("' +
                    this.layer.ModelColorSet[0] +
                    '",' +
                    String(1.0 - this.layer.transparency / 100) +
                    " )",
                ],
                [
                  "true",
                  'color("' +
                    this.layer.ModelColorSet[1] +
                    '",' +
                    String(1.0 - this.layer.transparency / 100) +
                    " )",
                ],
              ],
            },
          });
        } else if (this.layer.type == "TopoJson") {
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
            that.viewer.flyTo(NowLayer);
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
    },
    SubmitLayer() {
      this.$store.commit("UpdateLayersToStore", this.layers);
    },
  },
  created() {
    this.update();
    this.TransparencyPermit();
    this.Permit();
    this.StyleChange = false;
  },
  mounted() {
    this.update();
    this.ServiceList = this.$store.state.ServiceList;
    this.$store.commit("StyleBarChangeSubmit", true);
    if (this.layer.format == "point") this.StyleMeumPageTop = 3;
    if (this.layer.type == "GLTF") this.StyleMeumPageTop = 2;
    this.CesiumInit();
    this.StyleLayerShow();
  },
};
</script>

<style scoped>
</style>