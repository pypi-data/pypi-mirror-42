(window.webpackJsonp=window.webpackJsonp||[]).push([[86],{105:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return PaperItemBehavior});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_behaviors_iron_button_state_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(27),_polymer_iron_behaviors_iron_control_state_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(25);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const PaperItemBehaviorImpl={hostAttributes:{role:"option",tabindex:"0"}},PaperItemBehavior=[_polymer_iron_behaviors_iron_button_state_js__WEBPACK_IMPORTED_MODULE_1__.a,_polymer_iron_behaviors_iron_control_state_js__WEBPACK_IMPORTED_MODULE_2__.a,PaperItemBehaviorImpl]},125:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(39),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(60),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(40),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(50);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const $_documentContainer=document.createElement("template");$_documentContainer.setAttribute("style","display: none;");$_documentContainer.innerHTML=`<dom-module id="paper-item-shared-styles">
  <template>
    <style>
      :host, .paper-item {
        display: block;
        position: relative;
        min-height: var(--paper-item-min-height, 48px);
        padding: 0px 16px;
      }

      .paper-item {
        @apply --paper-font-subhead;
        border:none;
        outline: none;
        background: white;
        width: 100%;
        text-align: left;
      }

      :host([hidden]), .paper-item[hidden] {
        display: none !important;
      }

      :host(.iron-selected), .paper-item.iron-selected {
        font-weight: var(--paper-item-selected-weight, bold);

        @apply --paper-item-selected;
      }

      :host([disabled]), .paper-item[disabled] {
        color: var(--paper-item-disabled-color, var(--disabled-text-color));

        @apply --paper-item-disabled;
      }

      :host(:focus), .paper-item:focus {
        position: relative;
        outline: 0;

        @apply --paper-item-focused;
      }

      :host(:focus):before, .paper-item:focus:before {
        @apply --layout-fit;

        background: currentColor;
        content: '';
        opacity: var(--dark-divider-opacity);
        pointer-events: none;

        @apply --paper-item-focused-before;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content)},153:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return computeStateDomain});var _compute_domain__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(156);function computeStateDomain(stateObj){return Object(_compute_domain__WEBPACK_IMPORTED_MODULE_0__.a)(stateObj.entity_id)}},154:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return domainIcon});var _const__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(104);const fixedIcons={alert:"hass:alert",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weblink:"hass:open-in-new"};function domainIcon(domain,state){if(domain in fixedIcons){return fixedIcons[domain]}switch(domain){case"alarm_control_panel":switch(state){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell";}case"binary_sensor":return state&&"off"===state?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===state?"hass:window-closed":"hass:window-open";case"lock":return state&&"unlocked"===state?"hass:lock-open":"hass:lock";case"media_player":return state&&"off"!==state&&"idle"!==state?"hass:cast-connected":"hass:cast";case"zwave":switch(state){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave";}default:console.warn("Unable to find icon for domain "+domain+" ("+state+")");return _const__WEBPACK_IMPORTED_MODULE_0__.a;}}},155:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(39),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(40),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(50),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(2);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},156:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return computeDomain});function computeDomain(entityId){return entityId.substr(0,entityId.indexOf("."))}},157:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_iron_icon_iron_icon__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(92);const ironIconClass=customElements.get("iron-icon");let loaded=!1;class HaIcon extends ironIconClass{constructor(...args){super(...args);this._iconsetName=void 0}listen(node,eventName,methodName){super.listen(node,eventName,methodName);if(!loaded&&"mdi"===this._iconsetName){loaded=!0;__webpack_require__.e(57).then(__webpack_require__.bind(null,205))}}}customElements.define("ha-icon",HaIcon)},160:function(module,__webpack_exports__,__webpack_require__){"use strict";var lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(10),_ha_icon__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(157),_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(153),_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(167);function _decorate(decorators,factory,superClass,mixins){var api=_getDecoratorsApi();if(mixins){for(var i=0;i<mixins.length;i++){api=mixins[i](api)}}var r=factory(function initialize(O){api.initializeInstanceElements(O,decorated.elements)},superClass),decorated=api.decorateClass(_coalesceClassElements(r.d.map(_createElementDescriptor)),decorators);api.initializeClassElements(r.F,decorated.elements);return api.runClassFinishers(r.F,decorated.finishers)}function _getDecoratorsApi(){_getDecoratorsApi=function(){return api};var api={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(O,elements){["method","field"].forEach(function(kind){elements.forEach(function(element){if(element.kind===kind&&"own"===element.placement){this.defineClassElement(O,element)}},this)},this)},initializeClassElements:function(F,elements){var proto=F.prototype;["method","field"].forEach(function(kind){elements.forEach(function(element){var placement=element.placement;if(element.kind===kind&&("static"===placement||"prototype"===placement)){var receiver="static"===placement?F:proto;this.defineClassElement(receiver,element)}},this)},this)},defineClassElement:function(receiver,element){var descriptor=element.descriptor;if("field"===element.kind){var initializer=element.initializer;descriptor={enumerable:descriptor.enumerable,writable:descriptor.writable,configurable:descriptor.configurable,value:void 0===initializer?void 0:initializer.call(receiver)}}Object.defineProperty(receiver,element.key,descriptor)},decorateClass:function(elements,decorators){var newElements=[],finishers=[],placements={static:[],prototype:[],own:[]};elements.forEach(function(element){this.addElementPlacement(element,placements)},this);elements.forEach(function(element){if(!_hasDecorators(element))return newElements.push(element);var elementFinishersExtras=this.decorateElement(element,placements);newElements.push(elementFinishersExtras.element);newElements.push.apply(newElements,elementFinishersExtras.extras);finishers.push.apply(finishers,elementFinishersExtras.finishers)},this);if(!decorators){return{elements:newElements,finishers:finishers}}var result=this.decorateConstructor(newElements,decorators);finishers.push.apply(finishers,result.finishers);result.finishers=finishers;return result},addElementPlacement:function(element,placements,silent){var keys=placements[element.placement];if(!silent&&-1!==keys.indexOf(element.key)){throw new TypeError("Duplicated element ("+element.key+")")}keys.push(element.key)},decorateElement:function(element,placements){for(var extras=[],finishers=[],decorators=element.decorators,i=decorators.length-1,keys;0<=i;i--){keys=placements[element.placement];keys.splice(keys.indexOf(element.key),1);var elementObject=this.fromElementDescriptor(element),elementFinisherExtras=this.toElementFinisherExtras((0,decorators[i])(elementObject)||elementObject);element=elementFinisherExtras.element;this.addElementPlacement(element,placements);if(elementFinisherExtras.finisher){finishers.push(elementFinisherExtras.finisher)}var newExtras=elementFinisherExtras.extras;if(newExtras){for(var j=0;j<newExtras.length;j++){this.addElementPlacement(newExtras[j],placements)}extras.push.apply(extras,newExtras)}}return{element:element,finishers:finishers,extras:extras}},decorateConstructor:function(elements,decorators){for(var finishers=[],i=decorators.length-1;0<=i;i--){var obj=this.fromClassDescriptor(elements),elementsAndFinisher=this.toClassDescriptor((0,decorators[i])(obj)||obj);if(elementsAndFinisher.finisher!==void 0){finishers.push(elementsAndFinisher.finisher)}if(elementsAndFinisher.elements!==void 0){elements=elementsAndFinisher.elements;for(var j=0;j<elements.length-1;j++){for(var k=j+1;k<elements.length;k++){if(elements[j].key===elements[k].key&&elements[j].placement===elements[k].placement){throw new TypeError("Duplicated element ("+elements[j].key+")")}}}}}return{elements:elements,finishers:finishers}},fromElementDescriptor:function(element){var obj={kind:element.kind,key:element.key,placement:element.placement,descriptor:element.descriptor},desc={value:"Descriptor",configurable:!0};Object.defineProperty(obj,Symbol.toStringTag,desc);if("field"===element.kind)obj.initializer=element.initializer;return obj},toElementDescriptors:function(elementObjects){if(elementObjects===void 0)return;return _toArray(elementObjects).map(function(elementObject){var element=this.toElementDescriptor(elementObject);this.disallowProperty(elementObject,"finisher","An element descriptor");this.disallowProperty(elementObject,"extras","An element descriptor");return element},this)},toElementDescriptor:function(elementObject){var kind=elementObject.kind+"";if("method"!==kind&&"field"!==kind){throw new TypeError("An element descriptor's .kind property must be either \"method\" or"+" \"field\", but a decorator created an element descriptor with"+" .kind \""+kind+"\"")}var key=_toPropertyKey(elementObject.key),placement=elementObject.placement+"";if("static"!==placement&&"prototype"!==placement&&"own"!==placement){throw new TypeError("An element descriptor's .placement property must be one of \"static\","+" \"prototype\" or \"own\", but a decorator created an element descriptor"+" with .placement \""+placement+"\"")}var descriptor=elementObject.descriptor;this.disallowProperty(elementObject,"elements","An element descriptor");var element={kind:kind,key:key,placement:placement,descriptor:Object.assign({},descriptor)};if("field"!==kind){this.disallowProperty(elementObject,"initializer","A method descriptor")}else{this.disallowProperty(descriptor,"get","The property descriptor of a field descriptor");this.disallowProperty(descriptor,"set","The property descriptor of a field descriptor");this.disallowProperty(descriptor,"value","The property descriptor of a field descriptor");element.initializer=elementObject.initializer}return element},toElementFinisherExtras:function(elementObject){var element=this.toElementDescriptor(elementObject),finisher=_optionalCallableProperty(elementObject,"finisher"),extras=this.toElementDescriptors(elementObject.extras);return{element:element,finisher:finisher,extras:extras}},fromClassDescriptor:function(elements){var obj={kind:"class",elements:elements.map(this.fromElementDescriptor,this)},desc={value:"Descriptor",configurable:!0};Object.defineProperty(obj,Symbol.toStringTag,desc);return obj},toClassDescriptor:function(obj){var kind=obj.kind+"";if("class"!==kind){throw new TypeError("A class descriptor's .kind property must be \"class\", but a decorator"+" created a class descriptor with .kind \""+kind+"\"")}this.disallowProperty(obj,"key","A class descriptor");this.disallowProperty(obj,"placement","A class descriptor");this.disallowProperty(obj,"descriptor","A class descriptor");this.disallowProperty(obj,"initializer","A class descriptor");this.disallowProperty(obj,"extras","A class descriptor");var finisher=_optionalCallableProperty(obj,"finisher"),elements=this.toElementDescriptors(obj.elements);return{elements:elements,finisher:finisher}},runClassFinishers:function(constructor,finishers){for(var i=0,newConstructor;i<finishers.length;i++){newConstructor=(0,finishers[i])(constructor);if(newConstructor!==void 0){if("function"!==typeof newConstructor){throw new TypeError("Finishers must return a constructor.")}constructor=newConstructor}}return constructor},disallowProperty:function(obj,name,objectType){if(obj[name]!==void 0){throw new TypeError(objectType+" can't have a ."+name+" property.")}}};return api}function _createElementDescriptor(def){var key=_toPropertyKey(def.key),descriptor;if("method"===def.kind){descriptor={value:def.value,writable:!0,configurable:!0,enumerable:!1}}else if("get"===def.kind){descriptor={get:def.value,configurable:!0,enumerable:!1}}else if("set"===def.kind){descriptor={set:def.value,configurable:!0,enumerable:!1}}else if("field"===def.kind){descriptor={configurable:!0,writable:!0,enumerable:!0}}var element={kind:"field"===def.kind?"field":"method",key:key,placement:def.static?"static":"field"===def.kind?"own":"prototype",descriptor:descriptor};if(def.decorators)element.decorators=def.decorators;if("field"===def.kind)element.initializer=def.value;return element}function _coalesceGetterSetter(element,other){if(element.descriptor.get!==void 0){other.descriptor.get=element.descriptor.get}else{other.descriptor.set=element.descriptor.set}}function _coalesceClassElements(elements){for(var newElements=[],isSameElement=function(other){return"method"===other.kind&&other.key===element.key&&other.placement===element.placement},i=0;i<elements.length;i++){var element=elements[i],other;if("method"===element.kind&&(other=newElements.find(isSameElement))){if(_isDataDescriptor(element.descriptor)||_isDataDescriptor(other.descriptor)){if(_hasDecorators(element)||_hasDecorators(other)){throw new ReferenceError("Duplicated methods ("+element.key+") can't be decorated.")}other.descriptor=element.descriptor}else{if(_hasDecorators(element)){if(_hasDecorators(other)){throw new ReferenceError("Decorators can't be placed on different accessors with for "+"the same property ("+element.key+").")}other.decorators=element.decorators}_coalesceGetterSetter(element,other)}}else{newElements.push(element)}}return newElements}function _hasDecorators(element){return element.decorators&&element.decorators.length}function _isDataDescriptor(desc){return desc!==void 0&&!(desc.value===void 0&&desc.writable===void 0)}function _optionalCallableProperty(obj,name){var value=obj[name];if(value!==void 0&&"function"!==typeof value){throw new TypeError("Expected '"+name+"' to be a function")}return value}function _toPropertyKey(arg){var key=_toPrimitive(arg,"string");return"symbol"===typeof key?key:key+""}function _toPrimitive(input,hint){if("object"!==typeof input||null===input)return input;var prim=input[Symbol.toPrimitive];if(prim!==void 0){var res=prim.call(input,hint||"default");if("object"!==typeof res)return res;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===hint?String:Number)(input)}function _toArray(arr){return _arrayWithHoles(arr)||_iterableToArray(arr)||_nonIterableRest()}function _nonIterableRest(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}function _iterableToArray(iter){if(Symbol.iterator in Object(iter)||"[object Arguments]"===Object.prototype.toString.call(iter))return Array.from(iter)}function _arrayWithHoles(arr){if(Array.isArray(arr))return arr}let StateBadge=_decorate(null,function(_initialize,_LitElement){class StateBadge extends _LitElement{constructor(...args){super(...args);_initialize(this)}}return{F:StateBadge,d:[{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.f)()],key:"stateObj",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.f)()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.g)("ha-icon")],key:"_icon",value:void 0},{kind:"method",key:"render",value:function render(){const stateObj=this.stateObj;if(!stateObj){return lit_element__WEBPACK_IMPORTED_MODULE_0__.e``}return lit_element__WEBPACK_IMPORTED_MODULE_0__.e`
      <ha-icon
        id="icon"
        data-domain=${Object(_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_2__.a)(stateObj)}
        data-state=${stateObj.state}
        .icon=${this.overrideIcon||Object(_common_entity_state_icon__WEBPACK_IMPORTED_MODULE_3__.a)(stateObj)}
      ></ha-icon>
    `}},{kind:"method",key:"updated",value:function updated(changedProps){if(!changedProps.has("stateObj")){return}const stateObj=this.stateObj,iconStyle={color:"",filter:""},hostStyle={backgroundImage:""};if(stateObj){if(stateObj.attributes.entity_picture){hostStyle.backgroundImage="url("+stateObj.attributes.entity_picture+")";iconStyle.display="none"}else{if(stateObj.attributes.hs_color){const hue=stateObj.attributes.hs_color[0],sat=stateObj.attributes.hs_color[1];if(10<sat){iconStyle.color=`hsl(${hue}, 100%, ${100-sat/2}%)`}}if(stateObj.attributes.brightness){const brightness=stateObj.attributes.brightness;if("number"!==typeof brightness){const errorMessage=`Type error: state-badge expected number, but type of ${stateObj.entity_id}.attributes.brightness is ${typeof brightness} (${brightness})`;console.warn(errorMessage)}iconStyle.filter=`brightness(${(brightness+245)/5}%)`}}}Object.assign(this._icon.style,iconStyle);Object.assign(this.style,hostStyle)}},{kind:"get",static:!0,key:"styles",value:function styles(){return lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      :host {
        position: relative;
        display: inline-block;
        width: 40px;
        color: var(--paper-item-icon-color, #44739e);
        border-radius: 50%;
        height: 40px;
        text-align: center;
        background-size: cover;
        line-height: 40px;
      }

      ha-icon {
        transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
      }

      /* Color the icon if light or sun is on */
      ha-icon[data-domain="light"][data-state="on"],
      ha-icon[data-domain="switch"][data-state="on"],
      ha-icon[data-domain="binary_sensor"][data-state="on"],
      ha-icon[data-domain="fan"][data-state="on"],
      ha-icon[data-domain="sun"][data-state="above_horizon"] {
        color: var(--paper-item-icon-active-color, #fdd835);
      }

      /* Color the icon if unavailable */
      ha-icon[data-state="unavailable"] {
        color: var(--state-icon-unavailable-color);
      }
    `}}]}},lit_element__WEBPACK_IMPORTED_MODULE_0__.a);customElements.define("state-badge",StateBadge)},161:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(39),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(50),_paper_item_shared_styles_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(125),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(2),_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(105);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__.a]})},163:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(60),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__),_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(132),_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2__),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(2),_paper_spinner_behavior_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(109);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const template=_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left"></div>
      <div class="circle-clipper right"></div>
    </div>
  </div>
`;template.setAttribute("strip-whitespace","");Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__.a)({_template:template,is:"paper-spinner",behaviors:[_paper_spinner_behavior_js__WEBPACK_IMPORTED_MODULE_5__.a]})},164:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(94),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(78),_polymer_paper_item_paper_icon_item__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(161),_polymer_paper_item_paper_item_body__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(155),_vaadin_vaadin_combo_box_vaadin_combo_box_light__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(186),memoize_one__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(166),_state_badge__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(160),_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(103),lit_element__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(10),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(58);function _decorate(decorators,factory,superClass,mixins){var api=_getDecoratorsApi();if(mixins){for(var i=0;i<mixins.length;i++){api=mixins[i](api)}}var r=factory(function initialize(O){api.initializeInstanceElements(O,decorated.elements)},superClass),decorated=api.decorateClass(_coalesceClassElements(r.d.map(_createElementDescriptor)),decorators);api.initializeClassElements(r.F,decorated.elements);return api.runClassFinishers(r.F,decorated.finishers)}function _getDecoratorsApi(){_getDecoratorsApi=function(){return api};var api={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(O,elements){["method","field"].forEach(function(kind){elements.forEach(function(element){if(element.kind===kind&&"own"===element.placement){this.defineClassElement(O,element)}},this)},this)},initializeClassElements:function(F,elements){var proto=F.prototype;["method","field"].forEach(function(kind){elements.forEach(function(element){var placement=element.placement;if(element.kind===kind&&("static"===placement||"prototype"===placement)){var receiver="static"===placement?F:proto;this.defineClassElement(receiver,element)}},this)},this)},defineClassElement:function(receiver,element){var descriptor=element.descriptor;if("field"===element.kind){var initializer=element.initializer;descriptor={enumerable:descriptor.enumerable,writable:descriptor.writable,configurable:descriptor.configurable,value:void 0===initializer?void 0:initializer.call(receiver)}}Object.defineProperty(receiver,element.key,descriptor)},decorateClass:function(elements,decorators){var newElements=[],finishers=[],placements={static:[],prototype:[],own:[]};elements.forEach(function(element){this.addElementPlacement(element,placements)},this);elements.forEach(function(element){if(!_hasDecorators(element))return newElements.push(element);var elementFinishersExtras=this.decorateElement(element,placements);newElements.push(elementFinishersExtras.element);newElements.push.apply(newElements,elementFinishersExtras.extras);finishers.push.apply(finishers,elementFinishersExtras.finishers)},this);if(!decorators){return{elements:newElements,finishers:finishers}}var result=this.decorateConstructor(newElements,decorators);finishers.push.apply(finishers,result.finishers);result.finishers=finishers;return result},addElementPlacement:function(element,placements,silent){var keys=placements[element.placement];if(!silent&&-1!==keys.indexOf(element.key)){throw new TypeError("Duplicated element ("+element.key+")")}keys.push(element.key)},decorateElement:function(element,placements){for(var extras=[],finishers=[],decorators=element.decorators,i=decorators.length-1,keys;0<=i;i--){keys=placements[element.placement];keys.splice(keys.indexOf(element.key),1);var elementObject=this.fromElementDescriptor(element),elementFinisherExtras=this.toElementFinisherExtras((0,decorators[i])(elementObject)||elementObject);element=elementFinisherExtras.element;this.addElementPlacement(element,placements);if(elementFinisherExtras.finisher){finishers.push(elementFinisherExtras.finisher)}var newExtras=elementFinisherExtras.extras;if(newExtras){for(var j=0;j<newExtras.length;j++){this.addElementPlacement(newExtras[j],placements)}extras.push.apply(extras,newExtras)}}return{element:element,finishers:finishers,extras:extras}},decorateConstructor:function(elements,decorators){for(var finishers=[],i=decorators.length-1;0<=i;i--){var obj=this.fromClassDescriptor(elements),elementsAndFinisher=this.toClassDescriptor((0,decorators[i])(obj)||obj);if(elementsAndFinisher.finisher!==void 0){finishers.push(elementsAndFinisher.finisher)}if(elementsAndFinisher.elements!==void 0){elements=elementsAndFinisher.elements;for(var j=0;j<elements.length-1;j++){for(var k=j+1;k<elements.length;k++){if(elements[j].key===elements[k].key&&elements[j].placement===elements[k].placement){throw new TypeError("Duplicated element ("+elements[j].key+")")}}}}}return{elements:elements,finishers:finishers}},fromElementDescriptor:function(element){var obj={kind:element.kind,key:element.key,placement:element.placement,descriptor:element.descriptor},desc={value:"Descriptor",configurable:!0};Object.defineProperty(obj,Symbol.toStringTag,desc);if("field"===element.kind)obj.initializer=element.initializer;return obj},toElementDescriptors:function(elementObjects){if(elementObjects===void 0)return;return _toArray(elementObjects).map(function(elementObject){var element=this.toElementDescriptor(elementObject);this.disallowProperty(elementObject,"finisher","An element descriptor");this.disallowProperty(elementObject,"extras","An element descriptor");return element},this)},toElementDescriptor:function(elementObject){var kind=elementObject.kind+"";if("method"!==kind&&"field"!==kind){throw new TypeError("An element descriptor's .kind property must be either \"method\" or"+" \"field\", but a decorator created an element descriptor with"+" .kind \""+kind+"\"")}var key=_toPropertyKey(elementObject.key),placement=elementObject.placement+"";if("static"!==placement&&"prototype"!==placement&&"own"!==placement){throw new TypeError("An element descriptor's .placement property must be one of \"static\","+" \"prototype\" or \"own\", but a decorator created an element descriptor"+" with .placement \""+placement+"\"")}var descriptor=elementObject.descriptor;this.disallowProperty(elementObject,"elements","An element descriptor");var element={kind:kind,key:key,placement:placement,descriptor:Object.assign({},descriptor)};if("field"!==kind){this.disallowProperty(elementObject,"initializer","A method descriptor")}else{this.disallowProperty(descriptor,"get","The property descriptor of a field descriptor");this.disallowProperty(descriptor,"set","The property descriptor of a field descriptor");this.disallowProperty(descriptor,"value","The property descriptor of a field descriptor");element.initializer=elementObject.initializer}return element},toElementFinisherExtras:function(elementObject){var element=this.toElementDescriptor(elementObject),finisher=_optionalCallableProperty(elementObject,"finisher"),extras=this.toElementDescriptors(elementObject.extras);return{element:element,finisher:finisher,extras:extras}},fromClassDescriptor:function(elements){var obj={kind:"class",elements:elements.map(this.fromElementDescriptor,this)},desc={value:"Descriptor",configurable:!0};Object.defineProperty(obj,Symbol.toStringTag,desc);return obj},toClassDescriptor:function(obj){var kind=obj.kind+"";if("class"!==kind){throw new TypeError("A class descriptor's .kind property must be \"class\", but a decorator"+" created a class descriptor with .kind \""+kind+"\"")}this.disallowProperty(obj,"key","A class descriptor");this.disallowProperty(obj,"placement","A class descriptor");this.disallowProperty(obj,"descriptor","A class descriptor");this.disallowProperty(obj,"initializer","A class descriptor");this.disallowProperty(obj,"extras","A class descriptor");var finisher=_optionalCallableProperty(obj,"finisher"),elements=this.toElementDescriptors(obj.elements);return{elements:elements,finisher:finisher}},runClassFinishers:function(constructor,finishers){for(var i=0,newConstructor;i<finishers.length;i++){newConstructor=(0,finishers[i])(constructor);if(newConstructor!==void 0){if("function"!==typeof newConstructor){throw new TypeError("Finishers must return a constructor.")}constructor=newConstructor}}return constructor},disallowProperty:function(obj,name,objectType){if(obj[name]!==void 0){throw new TypeError(objectType+" can't have a ."+name+" property.")}}};return api}function _createElementDescriptor(def){var key=_toPropertyKey(def.key),descriptor;if("method"===def.kind){descriptor={value:def.value,writable:!0,configurable:!0,enumerable:!1}}else if("get"===def.kind){descriptor={get:def.value,configurable:!0,enumerable:!1}}else if("set"===def.kind){descriptor={set:def.value,configurable:!0,enumerable:!1}}else if("field"===def.kind){descriptor={configurable:!0,writable:!0,enumerable:!0}}var element={kind:"field"===def.kind?"field":"method",key:key,placement:def.static?"static":"field"===def.kind?"own":"prototype",descriptor:descriptor};if(def.decorators)element.decorators=def.decorators;if("field"===def.kind)element.initializer=def.value;return element}function _coalesceGetterSetter(element,other){if(element.descriptor.get!==void 0){other.descriptor.get=element.descriptor.get}else{other.descriptor.set=element.descriptor.set}}function _coalesceClassElements(elements){for(var newElements=[],isSameElement=function(other){return"method"===other.kind&&other.key===element.key&&other.placement===element.placement},i=0;i<elements.length;i++){var element=elements[i],other;if("method"===element.kind&&(other=newElements.find(isSameElement))){if(_isDataDescriptor(element.descriptor)||_isDataDescriptor(other.descriptor)){if(_hasDecorators(element)||_hasDecorators(other)){throw new ReferenceError("Duplicated methods ("+element.key+") can't be decorated.")}other.descriptor=element.descriptor}else{if(_hasDecorators(element)){if(_hasDecorators(other)){throw new ReferenceError("Decorators can't be placed on different accessors with for "+"the same property ("+element.key+").")}other.decorators=element.decorators}_coalesceGetterSetter(element,other)}}else{newElements.push(element)}}return newElements}function _hasDecorators(element){return element.decorators&&element.decorators.length}function _isDataDescriptor(desc){return desc!==void 0&&!(desc.value===void 0&&desc.writable===void 0)}function _optionalCallableProperty(obj,name){var value=obj[name];if(value!==void 0&&"function"!==typeof value){throw new TypeError("Expected '"+name+"' to be a function")}return value}function _toPropertyKey(arg){var key=_toPrimitive(arg,"string");return"symbol"===typeof key?key:key+""}function _toPrimitive(input,hint){if("object"!==typeof input||null===input)return input;var prim=input[Symbol.toPrimitive];if(prim!==void 0){var res=prim.call(input,hint||"default");if("object"!==typeof res)return res;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===hint?String:Number)(input)}function _toArray(arr){return _arrayWithHoles(arr)||_iterableToArray(arr)||_nonIterableRest()}function _nonIterableRest(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}function _iterableToArray(iter){if(Symbol.iterator in Object(iter)||"[object Arguments]"===Object.prototype.toString.call(iter))return Array.from(iter)}function _arrayWithHoles(arr){if(Array.isArray(arr))return arr}function _get(target,property,receiver){if("undefined"!==typeof Reflect&&Reflect.get){_get=Reflect.get}else{_get=function _get(target,property,receiver){var base=_superPropBase(target,property);if(!base)return;var desc=Object.getOwnPropertyDescriptor(base,property);if(desc.get){return desc.get.call(receiver)}return desc.value}}return _get(target,property,receiver||target)}function _superPropBase(object,property){while(!Object.prototype.hasOwnProperty.call(object,property)){object=_getPrototypeOf(object);if(null===object)break}return object}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function _getPrototypeOf(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}const rowRenderer=(root,_owner,model)=>{if(!root.firstElementChild){root.innerHTML=`
      <style>
        paper-icon-item {
          margin: -10px;
          padding: 0;
        }
      </style>
      <paper-icon-item>
        <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>
        <paper-item-body two-line="">
          <div class='name'>[[_computeStateName(item)]]</div>
          <div secondary>[[item.entity_id]]</div>
        </paper-item-body>
      </paper-icon-item>
    `}root.querySelector("state-badge").stateObj=model.item;root.querySelector(".name").textContent=Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_7__.a)(model.item);root.querySelector("[secondary]").textContent=model.item.entity_id};let HaEntityPicker=_decorate(null,function(_initialize,_LitElement){class HaEntityPicker extends _LitElement{constructor(...args){super(...args);_initialize(this)}}return{F:HaEntityPicker,d:[{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)({type:Boolean})],key:"autofocus",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)({type:Boolean})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)()],key:"label",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)()],key:"value",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)()],key:"domainFilter",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)()],key:"entityFilter",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)({type:Boolean})],key:"_opened",value:void 0},{kind:"field",decorators:[Object(lit_element__WEBPACK_IMPORTED_MODULE_8__.f)()],key:"_hass",value:void 0},{kind:"field",key:"_getStates",value(){return Object(memoize_one__WEBPACK_IMPORTED_MODULE_5__.a)((hass,domainFilter,entityFilter)=>{let states=[];if(!hass){return[]}let entityIds=Object.keys(hass.states);if(domainFilter){entityIds=entityIds.filter(eid=>eid.substr(0,eid.indexOf("."))===domainFilter)}states=entityIds.sort().map(key=>hass.states[key]);if(entityFilter){states=states.filter(stateObj=>stateObj.entity_id===this.value||entityFilter(stateObj))}return states})}},{kind:"method",key:"updated",value:function updated(changedProps){_get(_getPrototypeOf(HaEntityPicker.prototype),"updated",this).call(this,changedProps);if(changedProps.has("hass")&&!this._opened){this._hass=this.hass}}},{kind:"method",key:"render",value:function render(){const states=this._getStates(this._hass,this.domainFilter,this.entityFilter);return lit_element__WEBPACK_IMPORTED_MODULE_8__.e`
      <vaadin-combo-box-light
        item-value-path="entity_id"
        item-label-path="entity_id"
        .items=${states}
        .value=${this._value}
        .allowCustomValue=${this.allowCustomEntity}
        .renderer=${rowRenderer}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        <paper-input
          .autofocus=${this.autofocus}
          .label=${this.label===void 0&&this._hass?this._hass.localize("ui.components.entity.entity-picker.entity"):this.label}
          .value=${this._value}
          .disabled=${this.disabled}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
        >
          ${this.value?lit_element__WEBPACK_IMPORTED_MODULE_8__.e`
                <paper-icon-button
                  slot="suffix"
                  class="clear-button"
                  icon="hass:close"
                  no-ripple
                >
                  Clear
                </paper-icon-button>
              `:""}
          ${0<states.length?lit_element__WEBPACK_IMPORTED_MODULE_8__.e`
                <paper-icon-button
                  slot="suffix"
                  class="toggle-button"
                  .icon=${this._opened?"hass:menu-up":"hass:menu-down"}
                >
                  Toggle
                </paper-icon-button>
              `:""}
        </paper-input>
      </vaadin-combo-box-light>
    `}},{kind:"get",key:"_value",value:function _value(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function _openedChanged(ev){this._opened=ev.detail.value}},{kind:"method",key:"_valueChanged",value:function _valueChanged(ev){const newValue=ev.detail.value;if(newValue!==this._value){this.value=ev.detail.value;setTimeout(()=>{Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_9__.a)(this,"value-changed",{value:this.value});Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_9__.a)(this,"change")},0)}}},{kind:"get",static:!0,key:"styles",value:function styles(){return lit_element__WEBPACK_IMPORTED_MODULE_8__.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}]}},lit_element__WEBPACK_IMPORTED_MODULE_8__.a);customElements.define("ha-entity-picker",HaEntityPicker)},166:function(module,__webpack_exports__,__webpack_require__){"use strict";var shallowEqual=function shallowEqual(newValue,oldValue){return newValue===oldValue},simpleIsEqual=function simpleIsEqual(newArgs,lastArgs){return newArgs.length===lastArgs.length&&newArgs.every(function(newArg,index){return shallowEqual(newArg,lastArgs[index])})};function index(resultFn,isEqual){if(void 0===isEqual){isEqual=simpleIsEqual}var lastThis,lastArgs=[],lastResult,calledOnce=!1,result=function result(){for(var _len=arguments.length,newArgs=Array(_len),_key=0;_key<_len;_key++){newArgs[_key]=arguments[_key]}if(calledOnce&&lastThis===this&&isEqual(newArgs,lastArgs)){return lastResult}lastResult=resultFn.apply(this,newArgs);calledOnce=!0;lastThis=this;lastArgs=newArgs;return lastResult};return result}__webpack_exports__.a=index},167:function(module,__webpack_exports__,__webpack_require__){"use strict";var common_const=__webpack_require__(104),compute_domain=__webpack_require__(156),domain_icon=__webpack_require__(154);function binarySensorIcon(state){const activated=state.state&&"off"===state.state;switch(state.attributes.device_class){case"battery":return activated?"hass:battery":"hass:battery-outline";case"cold":return activated?"hass:thermometer":"hass:snowflake";case"connectivity":return activated?"hass:server-network-off":"hass:server-network";case"door":return activated?"hass:door-closed":"hass:door-open";case"garage_door":return activated?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return activated?"hass:shield-check":"hass:alert";case"heat":return activated?"hass:thermometer":"hass:fire";case"light":return activated?"hass:brightness-5":"hass:brightness-7";case"lock":return activated?"hass:lock":"hass:lock-open";case"moisture":return activated?"hass:water-off":"hass:water";case"motion":return activated?"hass:walk":"hass:run";case"occupancy":return activated?"hass:home-outline":"hass:home";case"opening":return activated?"hass:square":"hass:square-outline";case"plug":return activated?"hass:power-plug-off":"hass:power-plug";case"presence":return activated?"hass:home-outline":"hass:home";case"sound":return activated?"hass:music-note-off":"hass:music-note";case"vibration":return activated?"hass:crop-portrait":"hass:vibrate";case"window":return activated?"hass:window-closed":"hass:window-open";default:return activated?"hass:radiobox-blank":"hass:checkbox-marked-circle";}}function coverIcon(state){const open="closed"!==state.state;switch(state.attributes.device_class){case"garage":return open?"hass:garage-open":"hass:garage";default:return Object(domain_icon.a)("cover",state.state);}}const fixedDeviceClassIcons={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge"};function sensorIcon(state){const dclass=state.attributes.device_class;if(dclass&&dclass in fixedDeviceClassIcons){return fixedDeviceClassIcons[dclass]}if("battery"===dclass){const battery=+state.state;if(isNaN(battery)){return"hass:battery-unknown"}const batteryRound=10*Math.round(battery/10);if(100<=batteryRound){return"hass:battery"}if(0>=batteryRound){return"hass:battery-alert"}return`${"hass"}:battery-${batteryRound}`}const unit=state.attributes.unit_of_measurement;if(unit===common_const.j||unit===common_const.k){return"hass:thermometer"}return Object(domain_icon.a)("sensor")}function inputDateTimeIcon(state){if(!state.attributes.has_date){return"hass:clock"}if(!state.attributes.has_time){return"hass:calendar"}return Object(domain_icon.a)("input_datetime")}__webpack_require__.d(__webpack_exports__,"a",function(){return stateIcon});const domainIcons={binary_sensor:binarySensorIcon,cover:coverIcon,sensor:sensorIcon,input_datetime:inputDateTimeIcon};function stateIcon(state){if(!state){return common_const.a}if(state.attributes.icon){return state.attributes.icon}const domain=Object(compute_domain.a)(state.entity_id);if(domain in domainIcons){return domainIcons[domain](state)}return Object(domain_icon.a)(domain,state.state)}},176:function(module,__webpack_exports__,__webpack_require__){"use strict";var _Mathabs=Math.abs,_Mathround=Math.round,fecha={},token=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,twoDigits="\\d\\d?",threeDigits="\\d{3}",fourDigits="\\d{4}",word="[^\\s]+",literal=/\[([^]*?)\]/gm,noop=function(){};function regexEscape(str){return str.replace(/[|\\{()[^$+*?.-]/g,"\\$&")}function shorten(arr,sLen){for(var newArr=[],i=0,len=arr.length;i<len;i++){newArr.push(arr[i].substr(0,sLen))}return newArr}function monthUpdate(arrName){return function(d,v,i18n){var index=i18n[arrName].indexOf(v.charAt(0).toUpperCase()+v.substr(1).toLowerCase());if(~index){d.month=index}}}function pad(val,len){val=val+"";len=len||2;while(val.length<len){val="0"+val}return val}var dayNames=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],monthNames=["January","February","March","April","May","June","July","August","September","October","November","December"],monthNamesShort=shorten(monthNames,3),dayNamesShort=shorten(dayNames,3);fecha.i18n={dayNamesShort:dayNamesShort,dayNames:dayNames,monthNamesShort:monthNamesShort,monthNames:monthNames,amPm:["am","pm"],DoFn:function DoFn(D){return D+["th","st","nd","rd"][3<D%10?0:(10!==D-D%10)*D%10]}};var formatFlags={D:function(dateObj){return dateObj.getDate()},DD:function(dateObj){return pad(dateObj.getDate())},Do:function(dateObj,i18n){return i18n.DoFn(dateObj.getDate())},d:function(dateObj){return dateObj.getDay()},dd:function(dateObj){return pad(dateObj.getDay())},ddd:function(dateObj,i18n){return i18n.dayNamesShort[dateObj.getDay()]},dddd:function(dateObj,i18n){return i18n.dayNames[dateObj.getDay()]},M:function(dateObj){return dateObj.getMonth()+1},MM:function(dateObj){return pad(dateObj.getMonth()+1)},MMM:function(dateObj,i18n){return i18n.monthNamesShort[dateObj.getMonth()]},MMMM:function(dateObj,i18n){return i18n.monthNames[dateObj.getMonth()]},YY:function(dateObj){return pad(dateObj.getFullYear()+"",4).substr(2)},YYYY:function(dateObj){return pad(dateObj.getFullYear(),4)},h:function(dateObj){return dateObj.getHours()%12||12},hh:function(dateObj){return pad(dateObj.getHours()%12||12)},H:function(dateObj){return dateObj.getHours()},HH:function(dateObj){return pad(dateObj.getHours())},m:function(dateObj){return dateObj.getMinutes()},mm:function(dateObj){return pad(dateObj.getMinutes())},s:function(dateObj){return dateObj.getSeconds()},ss:function(dateObj){return pad(dateObj.getSeconds())},S:function(dateObj){return _Mathround(dateObj.getMilliseconds()/100)},SS:function(dateObj){return pad(_Mathround(dateObj.getMilliseconds()/10),2)},SSS:function(dateObj){return pad(dateObj.getMilliseconds(),3)},a:function(dateObj,i18n){return 12>dateObj.getHours()?i18n.amPm[0]:i18n.amPm[1]},A:function(dateObj,i18n){return 12>dateObj.getHours()?i18n.amPm[0].toUpperCase():i18n.amPm[1].toUpperCase()},ZZ:function(dateObj){var o=dateObj.getTimezoneOffset();return(0<o?"-":"+")+pad(100*Math.floor(_Mathabs(o)/60)+_Mathabs(o)%60,4)}},parseFlags={D:[twoDigits,function(d,v){d.day=v}],Do:[twoDigits+word,function(d,v){d.day=parseInt(v,10)}],M:[twoDigits,function(d,v){d.month=v-1}],YY:[twoDigits,function(d,v){var da=new Date,cent=+(""+da.getFullYear()).substr(0,2);d.year=""+(68<v?cent-1:cent)+v}],h:[twoDigits,function(d,v){d.hour=v}],m:[twoDigits,function(d,v){d.minute=v}],s:[twoDigits,function(d,v){d.second=v}],YYYY:[fourDigits,function(d,v){d.year=v}],S:["\\d",function(d,v){d.millisecond=100*v}],SS:["\\d{2}",function(d,v){d.millisecond=10*v}],SSS:[threeDigits,function(d,v){d.millisecond=v}],d:[twoDigits,noop],ddd:[word,noop],MMM:[word,monthUpdate("monthNamesShort")],MMMM:[word,monthUpdate("monthNames")],a:[word,function(d,v,i18n){var val=v.toLowerCase();if(val===i18n.amPm[0]){d.isPm=!1}else if(val===i18n.amPm[1]){d.isPm=!0}}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(d,v){var parts=(v+"").match(/([+-]|\d\d)/gi),minutes;if(parts){minutes=+(60*parts[1])+parseInt(parts[2],10);d.timezoneOffset="+"===parts[0]?minutes:-minutes}}]};parseFlags.dd=parseFlags.d;parseFlags.dddd=parseFlags.ddd;parseFlags.DD=parseFlags.D;parseFlags.mm=parseFlags.m;parseFlags.hh=parseFlags.H=parseFlags.HH=parseFlags.h;parseFlags.MM=parseFlags.M;parseFlags.ss=parseFlags.s;parseFlags.A=parseFlags.a;fecha.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"};fecha.format=function(dateObj,mask,i18nSettings){var i18n=i18nSettings||fecha.i18n;if("number"===typeof dateObj){dateObj=new Date(dateObj)}if("[object Date]"!==Object.prototype.toString.call(dateObj)||isNaN(dateObj.getTime())){throw new Error("Invalid Date in fecha.format")}mask=fecha.masks[mask]||mask||fecha.masks["default"];var literals=[];mask=mask.replace(literal,function($0,$1){literals.push($1);return"??"});mask=mask.replace(token,function($0){return $0 in formatFlags?formatFlags[$0](dateObj,i18n):$0.slice(1,$0.length-1)});return mask.replace(/\?\?/g,function(){return literals.shift()})};fecha.parse=function(dateStr,format,i18nSettings){var i18n=i18nSettings||fecha.i18n;if("string"!==typeof format){throw new Error("Invalid format in fecha.parse")}format=fecha.masks[format]||format;if(1e3<dateStr.length){return null}var dateInfo={},parseInfo=[],newFormat=regexEscape(format).replace(token,function($0){if(parseFlags[$0]){var info=parseFlags[$0];parseInfo.push(info[1]);return"("+info[0]+")"}return $0}),matches=dateStr.match(new RegExp(newFormat,"i"));if(!matches){return null}for(var i=1;i<matches.length;i++){parseInfo[i-1](dateInfo,matches[i],i18n)}var today=new Date;if(!0===dateInfo.isPm&&null!=dateInfo.hour&&12!==+dateInfo.hour){dateInfo.hour=+dateInfo.hour+12}else if(!1===dateInfo.isPm&&12===+dateInfo.hour){dateInfo.hour=0}var date;if(null!=dateInfo.timezoneOffset){dateInfo.minute=+(dateInfo.minute||0)-+dateInfo.timezoneOffset;date=new Date(Date.UTC(dateInfo.year||today.getFullYear(),dateInfo.month||0,dateInfo.day||1,dateInfo.hour||0,dateInfo.minute||0,dateInfo.second||0,dateInfo.millisecond||0))}else{date=new Date(dateInfo.year||today.getFullYear(),dateInfo.month||0,dateInfo.day||1,dateInfo.hour||0,dateInfo.minute||0,dateInfo.second||0,dateInfo.millisecond||0)}return date};__webpack_exports__.a=fecha},193:function(module,__webpack_exports__,__webpack_require__){"use strict";var fecha__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(176);function toLocaleTimeStringSupportsOptions(){try{new Date().toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}__webpack_exports__.a=toLocaleTimeStringSupportsOptions()?(dateObj,locales)=>dateObj.toLocaleTimeString(locales,{hour:"numeric",minute:"2-digit"}):dateObj=>fecha__WEBPACK_IMPORTED_MODULE_0__.a.format(dateObj,"shortTime")},212:function(module,__webpack_exports__,__webpack_require__){"use strict";var fecha__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(176);function toLocaleDateStringSupportsOptions(){try{new Date().toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}__webpack_exports__.a=toLocaleDateStringSupportsOptions()?(dateObj,locales)=>dateObj.toLocaleDateString(locales,{year:"numeric",month:"long",day:"numeric"}):dateObj=>fecha__WEBPACK_IMPORTED_MODULE_0__.a.format(dateObj,"mediumDate")},304:function(module,__webpack_exports__,__webpack_require__){"use strict";var _Mathmin=Math.min,_Mathfloor=Math.floor,_Mathabs2=Math.abs,sizing=__webpack_require__(192),spacing=__webpack_require__(183),menu_overlay=__webpack_require__(263),html_tag=__webpack_require__(2);const $_documentContainer=html_tag.a`<dom-module id="lumo-date-picker-overlay" theme-for="vaadin-date-picker-overlay">
  <template>
    <style include="lumo-menu-overlay">
      [part="overlay"] {
        /*
        Width:
            date cell widths
          + month calendar side padding
          + year scroller width
        */
        width:
          calc(
              var(--lumo-size-m) * 7
            + var(--lumo-space-xs) * 2
            + 57px
          );
        height: 100%;
        max-height: calc(var(--lumo-size-m) * 14);
        overflow: hidden;
        -webkit-tap-highlight-color: transparent;
      }

      [part="content"] {
        padding: 0;
        height: 100%;
        overflow: hidden;
        -webkit-mask-image: none;
        mask-image: none;
      }

      @media (max-width: 420px), (max-height: 420px) {
        [part="overlay"] {
          width: 100vw;
          height: 70vh;
          max-height: 70vh;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content);var color=__webpack_require__(197),style=__webpack_require__(188),typography=__webpack_require__(203);const vaadin_button_styles_$_documentContainer=document.createElement("template");vaadin_button_styles_$_documentContainer.innerHTML=`<dom-module id="lumo-button" theme-for="vaadin-button">
  <template>
    <style>
      :host {
        /* Sizing */
        --lumo-button-size: var(--lumo-size-m);
        min-width: calc(var(--lumo-button-size) * 2);
        height: var(--lumo-button-size);
        padding: 0 calc(var(--lumo-button-size) / 3 + var(--lumo-border-radius) / 2);
        margin: var(--lumo-space-xs) 0;
        box-sizing: border-box;
        /* Style */
        font-family: var(--lumo-font-family);
        font-size: var(--lumo-font-size-m);
        font-weight: 500;
        color: var(--lumo-primary-text-color);
        background-color: var(--lumo-contrast-5pct);
        border-radius: var(--lumo-border-radius);
        cursor: default;
        -webkit-tap-highlight-color: transparent;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      /* Set only for the internal parts so we don’t affect the host vertical alignment */
      [part="label"],
      [part="prefix"],
      [part="suffix"] {
        line-height: var(--lumo-line-height-xs);
      }

      [part="label"] {
        padding: calc(var(--lumo-button-size) / 6) 0;
      }

      :host([theme~="small"]) {
        font-size: var(--lumo-font-size-s);
        --lumo-button-size: var(--lumo-size-s);
      }

      :host([theme~="large"]) {
        font-size: var(--lumo-font-size-l);
        --lumo-button-size: var(--lumo-size-l);
      }

      /* This needs to be the last selector for it to take priority */
      :host([disabled][disabled]) {
        pointer-events: none;
        color: var(--lumo-disabled-text-color);
        background-color: var(--lumo-contrast-5pct);
      }

      /* For interaction states */
      :host::before,
      :host::after {
        content: "";
        /* We rely on the host always being relative */
        position: absolute;
        z-index: 1;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: currentColor;
        border-radius: inherit;
        opacity: 0;
        transition: opacity 0.2s;
        pointer-events: none;
      }

      /* Hover */

      :host(:hover)::before {
        opacity: 0.05;
      }

      /* Disable hover for touch devices */
      @media (pointer: coarse) {
        :host(:not([active]):hover)::before {
          opacity: 0;
        }
      }

      /* Active */

      :host::after {
        transition: opacity 1.4s, transform 0.1s;
        filter: blur(8px);
      }

      :host([active])::before {
        opacity: 0.1;
        transition-duration: 0s;
      }

      :host([active])::after {
        opacity: 0.1;
        transition-duration: 0s, 0s;
        transform: scale(0);
      }

      /* Keyboard focus */

      :host([focus-ring]) {
        box-shadow: 0 0 0 2px var(--lumo-primary-color-50pct);
      }

      /* Types (primary, tertiary, tertiary-inline */

      :host([theme~="tertiary"]),
      :host([theme~="tertiary-inline"]) {
        background-color: transparent !important;
        transition: opacity 0.2s;
        min-width: 0;
      }

      :host([theme~="tertiary"])::before,
      :host([theme~="tertiary-inline"])::before {
        display: none;
      }

      :host([theme~="tertiary"]) {
        padding: 0 calc(var(--lumo-button-size) / 6);
      }

      @media (hover: hover) {
        :host([theme*="tertiary"]:not([active]):hover) {
          opacity: 0.8;
        }
      }

      :host([theme~="tertiary"][active]),
      :host([theme~="tertiary-inline"][active]) {
        opacity: 0.5;
        transition-duration: 0s;
      }

      :host([theme~="tertiary-inline"]) {
        margin: 0;
        height: auto;
        padding: 0;
        line-height: inherit;
        font-size: inherit;
      }

      :host([theme~="tertiary-inline"]) [part="label"] {
        padding: 0;
        line-height: inherit;
      }

      :host([theme~="primary"]) {
        background-color: var(--lumo-primary-color);
        color: var(--lumo-primary-contrast-color);
        font-weight: 600;
        min-width: calc(var(--lumo-button-size) * 2.5);
      }

      :host([theme~="primary"]:hover)::before {
        opacity: 0.1;
      }

      :host([theme~="primary"][active])::before {
        background-color: var(--lumo-shade-20pct);
      }

      @media (pointer: coarse) {
        :host([theme~="primary"][active])::before {
          background-color: var(--lumo-shade-60pct);
        }

        :host([theme~="primary"]:not([active]):hover)::before {
          opacity: 0;
        }
      }

      :host([theme~="primary"][active])::after {
        opacity: 0.2;
      }

      /* Colors (success, error, contrast) */

      :host([theme~="success"]) {
        color: var(--lumo-success-text-color);
      }

      :host([theme~="success"][theme~="primary"]) {
        background-color: var(--lumo-success-color);
        color: var(--lumo-success-contrast-color);
      }

      :host([theme~="error"]) {
        color: var(--lumo-error-text-color);
      }

      :host([theme~="error"][theme~="primary"]) {
        background-color: var(--lumo-error-color);
        color: var(--lumo-error-contrast-color);
      }

      :host([theme~="contrast"]) {
        color: var(--lumo-contrast);
      }

      :host([theme~="contrast"][theme~="primary"]) {
        background-color: var(--lumo-contrast);
        color: var(--lumo-base-color);
      }

      /* Icons */

      [part] ::slotted(iron-icon) {
        display: inline-block;
        width: var(--lumo-icon-size-m);
        height: var(--lumo-icon-size-m);
      }

      /* Vaadin icons are based on a 16x16 grid (unlike Lumo and Material icons with 24x24), so they look too big by default */
      [part] ::slotted(iron-icon[icon^="vaadin:"]) {
        padding: 0.25em;
        box-sizing: border-box !important;
      }

      [part="prefix"] {
        margin-left: -0.25em;
        margin-right: 0.25em;
      }

      [part="suffix"] {
        margin-left: 0.25em;
        margin-right: -0.25em;
      }

      /* Icon-only */

      :host([theme~="icon"]) {
        min-width: var(--lumo-button-size);
        padding-left: calc(var(--lumo-button-size) / 4);
        padding-right: calc(var(--lumo-button-size) / 4);
      }

      :host([theme~="icon"]) [part="prefix"],
      :host([theme~="icon"]) [part="suffix"] {
        margin-left: 0;
        margin-right: 0;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_button_styles_$_documentContainer.content);var polymer_element=__webpack_require__(13),gesture_event_listeners=__webpack_require__(45),vaadin_themable_mixin=__webpack_require__(182);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const TabIndexMixin=superClass=>class VaadinTabIndexMixin extends superClass{static get properties(){var properties={tabindex:{type:Number,value:0,reflectToAttribute:!0,observer:"_tabindexChanged"}};if(window.ShadyDOM){properties.tabIndex=properties.tabindex}return properties}},ControlStateMixin=superClass=>class VaadinControlStateMixin extends TabIndexMixin(superClass){static get properties(){return{autofocus:{type:Boolean},_previousTabIndex:{type:Number},disabled:{type:Boolean,observer:"_disabledChanged",reflectToAttribute:!0},_isShiftTabbing:{type:Boolean}}}ready(){this.addEventListener("focusin",e=>{if(e.composedPath()[0]===this){this._focus(e)}else if(-1!==e.composedPath().indexOf(this.focusElement)&&!this.disabled){this._setFocused(!0)}});this.addEventListener("focusout",e=>this._setFocused(!1));super.ready();const ensureEventComposed=e=>{if(!e.composed){e.target.dispatchEvent(new CustomEvent(e.type,{bubbles:!0,composed:!0,cancelable:!1}))}};this.shadowRoot.addEventListener("focusin",ensureEventComposed);this.shadowRoot.addEventListener("focusout",ensureEventComposed);this.addEventListener("keydown",e=>{if(!e.defaultPrevented&&e.shiftKey&&9===e.keyCode){this._isShiftTabbing=!0;HTMLElement.prototype.focus.apply(this);this._setFocused(!1);setTimeout(()=>this._isShiftTabbing=!1,0)}});if(this.autofocus&&!this.focused&&!this.disabled){window.requestAnimationFrame(()=>{this._focus();this._setFocused(!0);this.setAttribute("focus-ring","")})}this._boundKeydownListener=this._bodyKeydownListener.bind(this);this._boundKeyupListener=this._bodyKeyupListener.bind(this)}connectedCallback(){super.connectedCallback();document.body.addEventListener("keydown",this._boundKeydownListener,!0);document.body.addEventListener("keyup",this._boundKeyupListener,!0)}disconnectedCallback(){super.disconnectedCallback();document.body.removeEventListener("keydown",this._boundKeydownListener,!0);document.body.removeEventListener("keyup",this._boundKeyupListener,!0);if(this.hasAttribute("focused")){this._setFocused(!1)}}_setFocused(focused){if(focused){this.setAttribute("focused","")}else{this.removeAttribute("focused")}if(focused&&this._tabPressed){this.setAttribute("focus-ring","")}else{this.removeAttribute("focus-ring")}}_bodyKeydownListener(e){this._tabPressed=9===e.keyCode}_bodyKeyupListener(){this._tabPressed=!1}get focusElement(){window.console.warn(`Please implement the 'focusElement' property in <${this.localName}>`);return this}_focus(e){if(this._isShiftTabbing){return}this.focusElement.focus();this._setFocused(!0)}focus(){if(this.disabled){return}this.focusElement.focus();this._setFocused(!0)}blur(){this.focusElement.blur();this._setFocused(!1)}_disabledChanged(disabled){this.focusElement.disabled=disabled;if(disabled){this.blur();this._previousTabIndex=this.tabindex;this.tabindex=-1;this.setAttribute("aria-disabled","true")}else{if("undefined"!==typeof this._previousTabIndex){this.tabindex=this._previousTabIndex}this.removeAttribute("aria-disabled")}}_tabindexChanged(tabindex){if(tabindex!==void 0){this.focusElement.tabIndex=tabindex}if(this.disabled&&this.tabindex){if(-1!==this.tabindex){this._previousTabIndex=this.tabindex}this.tabindex=tabindex=void 0}if(window.ShadyDOM){this.setProperties({tabIndex:tabindex,tabindex:tabindex})}}};var utils_async=__webpack_require__(8),debounce=__webpack_require__(17),flush=__webpack_require__(19);const DEV_MODE_CODE_REGEXP=/\/\*\*\s+vaadin-dev-mode:start([\s\S]*)vaadin-dev-mode:end\s+\*\*\//i;function isMinified(){function test(){return!0}return uncommentAndRun(test)}function isDevelopmentMode(){try{return isForcedDevelopmentMode()||isLocalhost()&&!isMinified()&&!isFlowProductionMode()}catch(e){return!1}}function isForcedDevelopmentMode(){return localStorage.getItem("vaadin.developmentmode.force")}function isLocalhost(){return 0<=["localhost","127.0.0.1"].indexOf(window.location.hostname)}function isFlowProductionMode(){if(window.Vaadin&&window.Vaadin.Flow&&window.Vaadin.Flow.clients){const productionModeApps=Object.keys(window.Vaadin.Flow.clients).map(key=>window.Vaadin.Flow.clients[key]).filter(client=>client.productionMode);if(0<productionModeApps.length){return!0}}return!1}function uncommentAndRun(callback,args){if("function"!==typeof callback){return}const match=DEV_MODE_CODE_REGEXP.exec(callback.toString());if(match){try{callback=new Function(match[1])}catch(e){console.log("vaadin-development-mode-detector: uncommentAndRun() failed",e)}}return callback(args)}window.Vaadin=window.Vaadin||{};const runIfDevelopmentMode=function(callback,args){if(window.Vaadin.developmentMode){return uncommentAndRun(callback,args)}};if(window.Vaadin.developmentMode===void 0){window.Vaadin.developmentMode=isDevelopmentMode()}function maybeGatherAndSendStats(){}const usageStatistics=function(){if("function"===typeof runIfDevelopmentMode){return runIfDevelopmentMode(maybeGatherAndSendStats)}};if(!window.Vaadin){window.Vaadin={}}window.Vaadin.registrations=window.Vaadin.registrations||[];window.Vaadin.developmentModeCallback=window.Vaadin.developmentModeCallback||{};window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]=function(){if(usageStatistics){usageStatistics()}};let statsJob;const ElementMixin=superClass=>class VaadinElementMixin extends superClass{static _finalizeClass(){super._finalizeClass();if(this.is){window.Vaadin.registrations.push(this);if(window.Vaadin.developmentModeCallback){statsJob=debounce.a.debounce(statsJob,utils_async.b,()=>{window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]()});Object(flush.a)(statsJob)}}}ready(){super.ready();if(null===document.doctype){console.warn("Vaadin components require the \"standards mode\" declaration. Please add <!DOCTYPE html> to the HTML document.")}}};var gestures=__webpack_require__(28);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_button_ButtonElement extends ElementMixin(ControlStateMixin(Object(vaadin_themable_mixin.a)(Object(gesture_event_listeners.a)(polymer_element.a)))){static get template(){return html_tag.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        outline: none;
        white-space: nowrap;
      }

      :host([hidden]) {
        display: none !important;
      }

      /* Ensure the button is always aligned on the baseline */
      .vaadin-button-container::before {
        content: "\\2003";
        display: inline-block;
        width: 0;
      }

      .vaadin-button-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        height: 100%;
        min-height: inherit;
        text-shadow: inherit;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      [part="prefix"],
      [part="suffix"] {
        flex: none;
      }

      [part="label"] {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      #button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: inherit;
      }
    </style>
    <div class="vaadin-button-container">
      <div part="prefix">
        <slot name="prefix"></slot>
      </div>
      <div part="label">
        <slot></slot>
      </div>
      <div part="suffix">
        <slot name="suffix"></slot>
      </div>
    </div>
    <button id="button" type="button"></button>
`}static get is(){return"vaadin-button"}static get version(){return"2.1.0"}ready(){super.ready();this.setAttribute("role","button");this.$.button.setAttribute("role","presentation");this._addActiveListeners()}disconnectedCallback(){super.disconnectedCallback();if(this.hasAttribute("active")){this.removeAttribute("active")}}_addActiveListeners(){Object(gestures.b)(this,"down",()=>!this.disabled&&this.setAttribute("active",""));Object(gestures.b)(this,"up",()=>this.removeAttribute("active"));this.addEventListener("keydown",e=>!this.disabled&&0<=[13,32].indexOf(e.keyCode)&&this.setAttribute("active",""));this.addEventListener("keyup",()=>this.removeAttribute("active"));this.addEventListener("blur",()=>this.removeAttribute("active"))}get focusElement(){return this.$.button}}customElements.define(vaadin_button_ButtonElement.is,vaadin_button_ButtonElement);const vaadin_date_picker_overlay_content_styles_$_documentContainer=html_tag.a`<dom-module id="lumo-date-picker-overlay-content" theme-for="vaadin-date-picker-overlay-content">
  <template>
    <style>
      :host {
        position: relative;
        background-color: transparent;
        /* Background for the year scroller, placed here as we are using a mask image on the actual years part */
        background-image: linear-gradient(var(--lumo-shade-5pct), var(--lumo-shade-5pct));
        background-size: 57px 100%;
        background-position: top right;
        background-repeat: no-repeat;
        cursor: default;
      }

      /* Month scroller */

      [part="months"] {
        /* Month calendar height:
              header height + margin-bottom
            + weekdays height + margin-bottom
            + date cell heights
            + small margin between month calendars
        */
        --vaadin-infinite-scroller-item-height:
          calc(
              var(--lumo-font-size-l) + var(--lumo-space-m)
            + var(--lumo-font-size-xs) + var(--lumo-space-s)
            + var(--lumo-size-m) * 6
            + var(--lumo-space-s)
          );
        --vaadin-infinite-scroller-buffer-offset: 20%;
        -webkit-mask-image: linear-gradient(transparent, #000 10%, #000 85%, transparent);
        mask-image: linear-gradient(transparent, #000 10%, #000 85%, transparent);
        position: relative;
        margin-right: 57px;
      }

      /* Year scroller */

      [part="years"] {
        /* TODO get rid of fixed magic number */
        --vaadin-infinite-scroller-buffer-width: 97px;
        width: 57px;
        height: auto;
        top: 0;
        bottom: 0;
        font-size: var(--lumo-font-size-s);
        box-shadow: inset 2px 0 4px 0 var(--lumo-shade-5pct);
        -webkit-mask-image: linear-gradient(transparent, #000 35%, #000 65%, transparent);
        mask-image: linear-gradient(transparent, #000 35%, #000 65%, transparent);
      }

      [part="year-number"],
      [part="year-separator"] {
        opacity: 0.5;
        transition: 0.2s opacity;
      }

      [part="years"]:hover [part="year-number"],
      [part="years"]:hover [part="year-separator"] {
        opacity: 1;
      }

      /* TODO unsupported selector */
      #scrollers {
        position: static;
        display: block;
      }

      /* TODO unsupported selector, should fix this in vaadin-date-picker that it adapts to the
       * width of the year scroller */
      #scrollers[desktop] [part="months"] {
        right: auto;
      }

      /* Year scroller position indicator */
      [part="years"]::before {
        border: none;
        width: 1em;
        height: 1em;
        background-color: var(--lumo-base-color);
        background-image: linear-gradient(var(--lumo-tint-5pct), var(--lumo-tint-5pct));
        transform: translate(-75%, -50%) rotate(45deg);
        border-top-right-radius: calc(var(--lumo-border-radius) / 2);
        box-shadow: 2px -2px 6px 0 var(--lumo-shade-5pct);
        z-index: 1;
      }

      [part="year-number"],
      [part="year-separator"] {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 50%;
        transform: translateY(-50%);
      }

      [part="years"] [part="year-separator"]::after {
        color: var(--lumo-disabled-text-color);
        content: "•";
      }

      /* Current year */

      [part="years"] [part="year-number"][current] {
        color: var(--lumo-primary-text-color);
      }

      /* Toolbar (footer) */

      [part="toolbar"] {
        padding: var(--lumo-space-s);
        box-shadow: 0 -1px 0 0 var(--lumo-contrast-10pct);
        border-bottom-left-radius: var(--lumo-border-radius);
        margin-right: 57px;
      }

      @supports (mask-image: linear-gradient(#000, #000)) or (-webkit-mask-image: linear-gradient(#000, #000)) {
        [part="toolbar"] {
          box-shadow: none;
        }
      }

      /* Today and Cancel buttons */

      /* TODO: Would be great if I could apply the "tertiary" theme from here instead of copying those styles */
      [part="toolbar"] [part\$="button"] {
        background-color: transparent;
        margin: 0;
        min-width: 0;
        padding: 0 0.75em;
      }

      /* Narrow viewport mode (fullscreen) */

      :host([fullscreen]) [part="toolbar"] {
        order: -1;
        background-color: var(--lumo-base-color);
      }

      :host([fullscreen]) [part="overlay-header"] {
        order: -2;
        height: var(--lumo-size-m);
        padding: var(--lumo-space-s);
        position: absolute;
        left: 0;
        right: 0;
        justify-content: center;
      }

      :host([fullscreen]) [part="toggle-button"],
      :host([fullscreen]) [part="clear-button"],
      [part="overlay-header"] [part="label"] {
        display: none;
      }

      /* Very narrow screen (year scroller initially hidden) */

      [part="years-toggle-button"] {
        position: relative;
        right: auto;
        display: flex;
        align-items: center;
        height: var(--lumo-size-s);
        padding: 0 0.5em;
        border-radius: var(--lumo-border-radius);
        z-index: 3;
        color: var(--lumo-primary-text-color);
        font-weight: 500;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      :host([years-visible]) [part="years-toggle-button"] {
        background-color: var(--lumo-primary-color);
        color: var(--lumo-primary-contrast-color);
      }

      [part="years-toggle-button"]::before {
        content: none;
      }

      /* TODO magic number (same as used for iron-media-query in vaadin-date-picker-overlay-content) */
      @media screen and (max-width: 374px) {
        :host {
          background-image: none;
        }

        [part="years"] {
          background-color: var(--lumo-shade-5pct);
        }

        [part="toolbar"],
        [part="months"] {
          margin-right: 0;
        }

        /* TODO make date-picker adapt to the width of the years part */
        [part="years"] {
          --vaadin-infinite-scroller-buffer-width: 90px;
          width: 50px;
        }

        :host([years-visible]) [part="months"] {
          padding-left: 50px;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_date_picker_overlay_content_styles_$_documentContainer.content);const vaadin_month_calendar_styles_$_documentContainer=html_tag.a`<dom-module id="lumo-month-calendar" theme-for="vaadin-month-calendar">
  <template>
    <style>
      :host {
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        -webkit-tap-highlight-color: transparent;
        user-select: none;
        font-size: var(--lumo-font-size-m);
        color: var(--lumo-body-text-color);
        text-align: center;
        padding: 0 var(--lumo-space-xs);
      }

      /* Month header */

      [part="month-header"] {
        color: var(--lumo-header-text-color);
        font-size: var(--lumo-font-size-l);
        line-height: 1;
        font-weight: 500;
        margin-bottom: var(--lumo-space-m);
      }

      /* Week days and numbers */

      [part="weekdays"],
      [part="weekday"],
      [part="week-numbers"] {
        font-size: var(--lumo-font-size-xs);
        line-height: 1;
        color: var(--lumo-tertiary-text-color);
      }

      [part="weekdays"] {
        margin-bottom: var(--lumo-space-s);
      }

      /* TODO should have part="week-number" for the cell in weekdays-container */
      [part="weekday"]:empty,
      [part="week-numbers"] {
        width: var(--lumo-size-xs);
      }

      /* Date and week number cells */

      [part="date"],
      [part="week-number"] {
        box-sizing: border-box;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: var(--lumo-size-m);
        position: relative;
      }

      [part="date"] {
        transition: color 0.1s;
      }

      /* Today date */

      [part="date"][today] {
        color: var(--lumo-primary-text-color);
      }

      /* Focused date */

      [part="date"]::before {
        content: "";
        position: absolute;
        z-index: -1;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        min-width: 2em;
        min-height: 2em;
        width: 80%;
        height: 80%;
        max-height: 100%;
        max-width: 100%;
        border-radius: var(--lumo-border-radius);
      }

      [part="date"][focused]::before {
        box-shadow: 0 0 0 2px var(--lumo-primary-color-50pct);
      }

      :host(:not([focused])) [part="date"][focused]::before {
        animation: vaadin-date-picker-month-calendar-focus-date 1.4s infinite;
      }

      @keyframes vaadin-date-picker-month-calendar-focus-date {
        50% {
          box-shadow: 0 0 0 2px transparent;
        }
      }

      /* TODO should not rely on the role attribute */
      [part="date"][role="button"]:not([disabled]):not([selected]):hover::before {
        background-color: var(--lumo-primary-color-10pct);
      }

      [part="date"][selected] {
        color: var(--lumo-primary-contrast-color);
      }

      [part="date"][selected]::before {
        background-color: var(--lumo-primary-color);
      }

      [part="date"][disabled] {
        color: var(--lumo-disabled-text-color);
      }

      @media (pointer: coarse) {
        [part="date"]:hover:not([selected])::before,
        [part="date"][focused]:not([selected])::before {
          display: none;
        }

        [part="date"][role="button"]:not([disabled]):active::before {
          display: block;
        }

        [part="date"][selected]::before {
          box-shadow: none;
        }
      }

      /* Disabled */

      :host([disabled]) * {
        color: var(--lumo-disabled-text-color) !important;
      }
    </style>
  </template>
</dom-module><custom-style>
  <style>
    @keyframes vaadin-date-picker-month-calendar-focus-date {
      50% {
        box-shadow: 0 0 0 2px transparent;
      }
    }
  </style>
</custom-style>`;document.head.appendChild(vaadin_month_calendar_styles_$_documentContainer.content);var font_icons=__webpack_require__(231);const field_button_$_documentContainer=document.createElement("template");field_button_$_documentContainer.innerHTML=`<dom-module id="lumo-field-button">
  <template>
    <style>
      [part\$="button"] {
        flex: none;
        width: 1em;
        height: 1em;
        line-height: 1;
        font-size: var(--lumo-icon-size-m);
        text-align: center;
        color: var(--lumo-contrast-60pct);
        transition: 0.2s color;
        cursor: default;
      }

      :host(:not([readonly])) [part\$="button"]:hover {
        color: var(--lumo-contrast-90pct);
      }

      :host([disabled]) [part\$="button"],
      :host([readonly]) [part\$="button"] {
        color: var(--lumo-contrast-20pct);
      }

      [part\$="button"]::before {
        font-family: "lumo-icons";
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(field_button_$_documentContainer.content);const vaadin_text_field_styles_$_documentContainer=document.createElement("template");vaadin_text_field_styles_$_documentContainer.innerHTML=`<dom-module id="lumo-text-field" theme-for="vaadin-text-field">
  <template>
    <style>
      :host {
        --lumo-text-field-size: var(--lumo-size-m);
        color: var(--lumo-body-text-color);
        font-size: var(--lumo-font-size-m);
        font-family: var(--lumo-font-family);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        -webkit-tap-highlight-color: transparent;
        padding: var(--lumo-space-xs) 0;
      }

      :host::before {
        height: var(--lumo-text-field-size);
        box-sizing: border-box;
        display: inline-flex;
        align-items: center;
      }

      [part="label"] {
        align-self: flex-start;
        color: var(--lumo-secondary-text-color);
        font-weight: 500;
        font-size: var(--lumo-font-size-s);
        margin-left: calc(var(--lumo-border-radius) / 4);
        transition: color 0.2s;
        line-height: 1;
        padding-bottom: 0.5em;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        position: relative;
        max-width: 100%;
        box-sizing: border-box;
      }

      :host([has-label])::before {
        /* Label height + margin */
        margin-top: calc(var(--lumo-font-size-s) * 1.5);
      }

      :host([has-label]) {
        padding-top: var(--lumo-space-m);
      }

      :host([focused]:not([readonly])) [part="label"] {
        color: var(--lumo-primary-text-color);
      }

      :host([required]) [part="label"] {
        padding-right: 1em;
      }

      /* Used for required and invalid indicators */
      [part="label"]::after {
        content: var(--lumo-required-field-indicator, "•");
        transition: opacity 0.2s;
        opacity: 0;
        color: var(--lumo-primary-text-color);
        position: absolute;
        right: 0;
        width: 1em;
        text-align: center;
      }

      [part="value"],
      [part="input-field"] ::slotted([part="value"]) {
        cursor: inherit;
        min-height: var(--lumo-text-field-size);
        padding: 0 0.25em;
        --_lumo-text-field-overflow-mask-image: linear-gradient(to left, transparent, #000 1.25em);
        -webkit-mask-image: var(--_lumo-text-field-overflow-mask-image);
      }

      [part="value"]:focus {
        -webkit-mask-image: none;
        mask-image: none;
      }

      /*
        TODO: CSS custom property in \`mask-image\` causes crash in Edge
        see https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/15415089/
      */
      @-moz-document url-prefix() {
        [part="value"],
        [part="input-field"] ::slotted([part="value"]) {
          mask-image: var(--_lumo-text-field-overflow-mask-image);
        }
      }

      [part="value"]::-webkit-input-placeholder {
        color: inherit;
        transition: opacity 0.175s 0.05s;
        opacity: 0.5;
      }

      [part="value"]:-ms-input-placeholder {
        color: inherit;
        opacity: 0.5;
      }

      [part="value"]::-moz-placeholder {
        color: inherit;
        transition: opacity 0.175s 0.05s;
        opacity: 0.5;
      }

      [part="value"]::placeholder {
        color: inherit;
        transition: opacity 0.175s 0.1s;
        opacity: 0.5;
      }

      [part="input-field"] {
        border-radius: var(--lumo-border-radius);
        background-color: var(--lumo-contrast-10pct);
        padding: 0 calc(0.375em + var(--lumo-border-radius) / 4 - 1px);
        font-weight: 500;
        line-height: 1;
        position: relative;
        cursor: text;
        box-sizing: border-box;
      }

      /* Used for hover and activation effects */
      [part="input-field"]::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        border-radius: inherit;
        pointer-events: none;
        background-color: var(--lumo-contrast-50pct);
        opacity: 0;
        transition: transform 0.15s, opacity 0.2s;
        transform-origin: 100% 0;
      }

      /* Hover */

      :host(:hover:not([readonly]):not([focused])) [part="label"] {
        color: var(--lumo-body-text-color);
      }

      :host(:hover:not([readonly]):not([focused])) [part="input-field"]::after {
        opacity: 0.1;
      }

      /* Touch device adjustment */
      @media (pointer: coarse) {
        :host(:hover:not([readonly]):not([focused])) [part="label"] {
          color: var(--lumo-secondary-text-color);
        }

        :host(:hover:not([readonly]):not([focused])) [part="input-field"]::after {
          opacity: 0;
        }

        :host(:active:not([readonly]):not([focused])) [part="input-field"]::after {
          opacity: 0.2;
        }
      }

      /* Trigger when not focusing using the keyboard */
      :host([focused]:not([focus-ring]):not([readonly])) [part="input-field"]::after {
        transform: scaleX(0);
        transition-duration: 0.15s, 1s;
      }

      /* Focus-ring */

      :host([focus-ring]) [part="input-field"] {
        box-shadow: 0 0 0 2px var(--lumo-primary-color-50pct);
      }

      /* Read-only and disabled */
      :host([readonly]) [part="value"]::-webkit-input-placeholder,
      :host([disabled]) [part="value"]::-webkit-input-placeholder {
        opacity: 0;
      }

      :host([readonly]) [part="value"]:-ms-input-placeholder,
      :host([disabled]) [part="value"]:-ms-input-placeholder {
        opacity: 0;
      }

      :host([readonly]) [part="value"]::-moz-placeholder,
      :host([disabled]) [part="value"]::-moz-placeholder {
        opacity: 0;
      }

      :host([readonly]) [part="value"]::placeholder,
      :host([disabled]) [part="value"]::placeholder {
        opacity: 0;
      }

      /* Read-only */

      :host([readonly]) [part="input-field"] {
        color: var(--lumo-secondary-text-color);
        background-color: transparent;
        cursor: default;
      }

      :host([readonly]) [part="input-field"]::after {
        background-color: transparent;
        opacity: 1;
        border: 1px dashed var(--lumo-contrast-30pct);
      }

      /* Disabled style */

      :host([disabled]) {
        pointer-events: none;
      }

      :host([disabled]) [part="input-field"] {
        background-color: var(--lumo-contrast-5pct);
      }

      :host([disabled]) [part="label"],
      :host([disabled]) [part="value"],
      :host([disabled]) [part="input-field"] ::slotted(*) {
        color: var(--lumo-disabled-text-color);
        -webkit-text-fill-color: var(--lumo-disabled-text-color);
      }

      /* Required field style */

      :host([required]:not([has-value])) [part="label"]::after {
        opacity: 1;
      }

      /* Invalid style */

      :host([invalid]) [part="label"]::after {
        color: var(--lumo-error-text-color);
      }

      :host([invalid]) [part="input-field"] {
        background-color: var(--lumo-error-color-10pct);
      }

      :host([invalid]) [part="input-field"]::after {
        background-color: var(--lumo-error-color-50pct);
      }

      :host([invalid][focus-ring]) [part="input-field"] {
        box-shadow: 0 0 0 2px var(--lumo-error-color-50pct);
      }

      /* Error message */

      [part="error-message"] {
        margin-left: calc(var(--lumo-border-radius) / 4);
        font-size: var(--lumo-font-size-xs);
        line-height: var(--lumo-line-height-xs);
        color: var(--lumo-error-text-color);
        will-change: max-height;
        transition: 0.4s max-height;
        max-height: 5em;
      }

      /* Margin that doesn’t reserve space when there’s no error message */
      [part="error-message"]:not(:empty)::before,
      [part="error-message"]:not(:empty)::after {
        content: "";
        display: block;
        height: 0.4em;
      }

      :host(:not([invalid])) [part="error-message"] {
        max-height: 0;
        overflow: hidden;
      }

      /* Small theme */

      :host([theme~="small"]) {
        font-size: var(--lumo-font-size-s);
        --lumo-text-field-size: var(--lumo-size-s);
      }

      :host([theme~="small"][has-label]) [part="label"] {
        font-size: var(--lumo-font-size-xs);
      }

      :host([theme~="small"][has-label]) [part="error-message"] {
        font-size: var(--lumo-font-size-xxs);
      }

      /* Text align */

      :host([theme~="align-center"]) [part="value"] {
        text-align: center;
        --_lumo-text-field-overflow-mask-image: none;
      }

      :host([theme~="align-right"]) [part="value"] {
        text-align: right;
        --_lumo-text-field-overflow-mask-image: none;
      }

      @-moz-document url-prefix() {
        /* Firefox is smart enough to align overflowing text to right */
        :host([theme~="align-right"]) [part="value"] {
          --_lumo-text-field-overflow-mask-image: linear-gradient(to right, transparent 0.25em, #000 1.5em);
        }
      }

      /* Slotted content */

      [part="input-field"] ::slotted(:not([part]):not(iron-icon)) {
        color: var(--lumo-secondary-text-color);
        font-weight: 400;
      }

      /* Slotted icons */

      [part="input-field"] ::slotted(iron-icon) {
        color: var(--lumo-contrast-60pct);
        width: var(--lumo-icon-size-m);
        height: var(--lumo-icon-size-m);
      }

      /* Vaadin icons are based on a 16x16 grid (unlike Lumo and Material icons with 24x24), so they look too big by default */
      [part="input-field"] ::slotted(iron-icon[icon^="vaadin:"]) {
        padding: 0.25em;
        box-sizing: border-box !important;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_text_field_styles_$_documentContainer.content);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const vaadin_text_field_mixin_$_documentContainer=document.createElement("template");vaadin_text_field_mixin_$_documentContainer.innerHTML=`<dom-module id="vaadin-text-field-shared-styles">
  <template>
    <style>
      :host {
        display: inline-flex;
        outline: none;
      }

      :host::before {
        content: "\\2003";
        width: 0;
        display: inline-block;
        /* Size and position this element on the same vertical position as the input-field element
           to make vertical align for the host element work as expected */
      }

      :host([hidden]) {
        display: none !important;
      }

      .vaadin-text-field-container,
      .vaadin-text-area-container {
        display: flex;
        flex-direction: column;
        min-width: 100%;
        max-width: 100%;
        width: var(--vaadin-text-field-default-width, 12em);
      }

      [part="label"]:empty {
        display: none;
      }

      [part="input-field"] {
        display: flex;
        align-items: center;
        flex: auto;
      }

      /* Reset the native input styles */
      [part="value"] {
        -webkit-appearance: none;
        -moz-appearance: none;
        outline: none;
        margin: 0;
        padding: 0;
        border: 0;
        border-radius: 0;
        min-width: 0;
        font: inherit;
        font-size: 1em;
        line-height: normal;
        color: inherit;
        background-color: transparent;
        /* Disable default invalid style in Firefox */
        box-shadow: none;
      }

      [part="input-field"] ::slotted(*) {
        flex: none;
      }

      /* Slotted by vaadin-dropdown-menu-text-field */
      [part="value"],
      [part="input-field"] ::slotted([part="value"]) {
        flex: auto;
        white-space: nowrap;
        overflow: hidden;
        width: 100%;
        height: 100%;
      }

      [part="value"]::-ms-clear {
        display: none;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_text_field_mixin_$_documentContainer.content);const TextFieldMixin=subclass=>class VaadinTextFieldMixin extends ControlStateMixin(subclass){static get properties(){return{autocomplete:{type:String},autocorrect:{type:String},autocapitalize:{type:String},errorMessage:{type:String,value:""},label:{type:String,value:"",observer:"_labelChanged"},maxlength:{type:Number},minlength:{type:Number},name:{type:String},placeholder:{type:String},readonly:{type:Boolean,reflectToAttribute:!0},required:{type:Boolean,reflectToAttribute:!0},value:{type:String,value:"",observer:"_valueChanged",notify:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},preventInvalidInput:{type:Boolean},_labelId:{type:String},_errorId:{type:String}}}get focusElement(){return this.root.querySelector("[part=value]")}_onInput(e){if(this.preventInvalidInput){const input=this.focusElement;if(0<input.value.length&&!this.checkValidity()){input.value=this.value||""}}}_onChange(e){const changeEvent=new CustomEvent("change",{detail:{sourceEvent:e},bubbles:e.bubbles,cancelable:e.cancelable});this.dispatchEvent(changeEvent)}_valueChanged(newVal,oldVal){if(""===newVal&&oldVal===void 0){return}if(this.invalid){this.validate()}if(""!==newVal&&null!=newVal){this.setAttribute("has-value","")}else{this.removeAttribute("has-value")}}_labelChanged(label){if(""!==label&&null!=label){this.setAttribute("has-label","")}else{this.removeAttribute("has-label")}}checkValidity(){if(this.required||this.pattern||this.maxlength||this.minlength){return this.focusElement.checkValidity()}else{return!this.invalid}}ready(){super.ready();if(!(window.ShadyCSS&&window.ShadyCSS.nativeCss)){this.updateStyles()}var uniqueId=TextFieldMixin._uniqueId=1+TextFieldMixin._uniqueId||0;this._errorId=`${this.constructor.is}-error-${uniqueId}`;this._labelId=`${this.constructor.is}-label-${uniqueId}`;if(navigator.userAgent.match(/Trident/)){this._addIEListeners()}}validate(){return!(this.invalid=!this.checkValidity())}_addIEListeners(){const prevent=e=>{e.stopImmediatePropagation();this.focusElement.removeEventListener("input",prevent)},shouldPreventInput=()=>this.placeholder&&this.focusElement.addEventListener("input",prevent);this.focusElement.addEventListener("focusin",shouldPreventInput);this.focusElement.addEventListener("focusout",shouldPreventInput);this._createPropertyObserver("placeholder",shouldPreventInput)}_getActiveErrorId(invalid,errorMessage,errorId){return errorMessage&&invalid?errorId:void 0}_getActiveLabelId(label,labelId){return label?labelId:void 0}_getErrorMessageAriaHidden(invalid,errorMessage,errorId){return(!this._getActiveErrorId(invalid,errorMessage,errorId)).toString()}attributeChangedCallback(prop,oldVal,newVal){super.attributeChangedCallback(prop,oldVal,newVal);if(!(window.ShadyCSS&&window.ShadyCSS.nativeCss)&&/^(focused|focus-ring|invalid|disabled|placeholder|has-value)$/.test(prop)){this.updateStyles()}const isSafari=/^((?!chrome|android).)*safari/i.test(navigator.userAgent);if(isSafari&&this.root){const WEBKIT_PROPERTY="-webkit-backface-visibility";this.root.querySelectorAll("*").forEach(el=>{el.style[WEBKIT_PROPERTY]="visible";el.style[WEBKIT_PROPERTY]=""})}}};/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_text_field_TextFieldElement extends ElementMixin(TextFieldMixin(Object(vaadin_themable_mixin.a)(polymer_element.a))){static get template(){return html_tag.a`
    <style include="vaadin-text-field-shared-styles">
      /* polymer-cli linter breaks with empty line */
    </style>

    <div class="vaadin-text-field-container">

      <label part="label" on-click="focus" id="[[_labelId]]">[[label]]</label>

      <div part="input-field">

        <slot name="prefix"></slot>

        <input part="value" autocomplete\$="[[autocomplete]]" autocorrect\$="[[autocorrect]]" autocapitalize\$="[[autocapitalize]]" autofocus\$="[[autofocus]]" disabled\$="[[disabled]]" list="[[list]]" maxlength\$="[[maxlength]]" minlength\$="[[minlength]]" pattern="[[pattern]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" aria-readonly\$="[[readonly]]" required\$="[[required]]" aria-required\$="[[required]]" value="{{value::input}}" title="[[title]]" on-blur="validate" on-input="_onInput" on-change="_onChange" aria-describedby\$="[[_getActiveErrorId(invalid, errorMessage, _errorId)]]" aria-labelledby\$="[[_getActiveLabelId(label, _labelId)]]" aria-invalid\$="[[invalid]]">

        <slot name="suffix"></slot>

      </div>

      <div part="error-message" id="[[_errorId]]" aria-live="assertive" aria-hidden\$="[[_getErrorMessageAriaHidden(invalid, errorMessage, _errorId)]]">[[errorMessage]]</div>

    </div>
`}static get is(){return"vaadin-text-field"}static get version(){return"2.1.2"}static get properties(){return{list:{type:String},pattern:{type:String},title:{type:String}}}}customElements.define(vaadin_text_field_TextFieldElement.is,vaadin_text_field_TextFieldElement);const vaadin_date_picker_styles_$_documentContainer=html_tag.a`<dom-module id="lumo-date-picker" theme-for="vaadin-date-picker">
  <template>
    <style include="lumo-field-button">
      :host {
        outline: none;
      }

      [part="toggle-button"]::before {
        content: var(--lumo-icons-calendar);
      }

      [part="clear-button"]::before {
        content: var(--lumo-icons-cross);
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_date_picker_styles_$_documentContainer.content);var iron_media_query=__webpack_require__(110),vaadin_theme_property_mixin=__webpack_require__(232),vaadin_overlay=__webpack_require__(238);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_date_picker_overlay_DatePickerOverlayElement extends vaadin_overlay.a{static get is(){return"vaadin-date-picker-overlay"}}customElements.define(vaadin_date_picker_overlay_DatePickerOverlayElement.is,vaadin_date_picker_overlay_DatePickerOverlayElement);var iron_a11y_keys_behavior=__webpack_require__(20),iron_a11y_announcer=__webpack_require__(79),dom_repeat=__webpack_require__(67);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const DatePickerHelper=class VaadinDatePickerHelper{static _getISOWeekNumber(date){var dayOfWeek=date.getDay();if(0===dayOfWeek){dayOfWeek=7}var nearestThursdayDiff=4-dayOfWeek,nearestThursday=new Date(date.getTime()+1e3*(3600*(24*nearestThursdayDiff))),firstOfJanuary=new Date(0,0);firstOfJanuary.setFullYear(nearestThursday.getFullYear());var timeDiff=nearestThursday.getTime()-firstOfJanuary.getTime(),daysSinceFirstOfJanuary=Math.round(timeDiff/(1e3*(3600*24)));return _Mathfloor(daysSinceFirstOfJanuary/7+1)}static _dateEquals(date1,date2){return date1 instanceof Date&&date2 instanceof Date&&date1.getFullYear()===date2.getFullYear()&&date1.getMonth()===date2.getMonth()&&date1.getDate()===date2.getDate()}static _dateAllowed(date,min,max){return(!min||date>=min)&&(!max||date<=max)}static _getClosestDate(date,dates){return dates.filter(date=>date!==void 0).reduce((closestDate,candidate)=>{if(!candidate){return closestDate}if(!closestDate){return candidate}var candidateDiff=_Mathabs2(date.getTime()-candidate.getTime()),closestDateDiff=_Mathabs2(closestDate.getTime()-date.getTime());return candidateDiff<closestDateDiff?candidate:closestDate})}static _extractDateParts(date){return{day:date.getDate(),month:date.getMonth(),year:date.getFullYear()}}};/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_month_calendar_MonthCalendarElement extends Object(vaadin_themable_mixin.a)(Object(gesture_event_listeners.a)(polymer_element.a)){static get template(){return html_tag.a`
    <style>
      :host {
        display: block;
      }

      [part="weekdays"],
      #days {
        display: flex;
        flex-wrap: wrap;
        flex-grow: 1;
      }

      #days-container,
      #weekdays-container {
        display: flex;
      }

      [part="week-numbers"] {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex-shrink: 0;
      }

      [part="week-numbers"][hidden],
      [part="weekday"][hidden] {
        display: none;
      }

      [part="weekday"],
      [part="date"] {
        /* Would use calc(100% / 7) but it doesn't work nice on IE */
        width: 14.285714286%;
      }

      [part="weekday"]:empty,
      [part="week-numbers"] {
        width: 12.5%;
        flex-shrink: 0;
      }
    </style>

    <div part="month-header" role="heading">[[_getTitle(month, i18n.monthNames)]]</div>
    <div id="monthGrid" on-tap="_handleTap" on-touchend="_preventDefault" on-touchstart="_onMonthGridTouchStart">
      <div id="weekdays-container">
        <div hidden="[[!_showWeekSeparator(showWeekNumbers, i18n.firstDayOfWeek)]]" part="weekday"></div>
        <div part="weekdays">
          <template is="dom-repeat" items="[[_getWeekDayNames(i18n.weekdays, i18n.weekdaysShort, showWeekNumbers, i18n.firstDayOfWeek)]]">
            <div part="weekday" role="heading" aria-label\$="[[item.weekDay]]">[[item.weekDayShort]]</div>
          </template>
        </div>
      </div>
      <div id="days-container">
        <div part="week-numbers" hidden="[[!_showWeekSeparator(showWeekNumbers, i18n.firstDayOfWeek)]]">
          <template is="dom-repeat" items="[[_getWeekNumbers(_days)]]">
            <div part="week-number" role="heading" aria-label\$="[[i18n.week]] [[item]]">[[item]]</div>
          </template>
        </div>
        <div id="days">
          <template is="dom-repeat" items="[[_days]]">
            <div part="date" today\$="[[_isToday(item)]]" selected\$="[[_dateEquals(item, selectedDate)]]" focused\$="[[_dateEquals(item, focusedDate)]]" date="[[item]]" disabled\$="[[!_dateAllowed(item, minDate, maxDate)]]" role\$="[[_getRole(item)]]" aria-label\$="[[_getAriaLabel(item)]]" aria-disabled\$="[[_getAriaDisabled(item, minDate, maxDate)]]">[[_getDate(item)]]</div>
          </template>
        </div>
      </div>
    </div>
`}static get is(){return"vaadin-month-calendar"}static get properties(){return{month:{type:Date,value:new Date},selectedDate:{type:Date,notify:!0},focusedDate:Date,showWeekNumbers:{type:Boolean,value:!1},i18n:{type:Object},ignoreTaps:Boolean,_notTapping:Boolean,minDate:{type:Date,value:null},maxDate:{type:Date,value:null},_days:{type:Array,computed:"_getDays(month, i18n.firstDayOfWeek, minDate, maxDate)"},disabled:{type:Boolean,reflectToAttribute:!0,computed:"_isDisabled(month, minDate, maxDate)"}}}static get observers(){return["_showWeekNumbersChanged(showWeekNumbers, i18n.firstDayOfWeek)"]}_dateEquals(date1,date2){return DatePickerHelper._dateEquals(date1,date2)}_dateAllowed(date,min,max){return DatePickerHelper._dateAllowed(date,min,max)}_isDisabled(month,minDate,maxDate){var firstDate=new Date(0,0);firstDate.setFullYear(month.getFullYear());firstDate.setMonth(month.getMonth());firstDate.setDate(1);var lastDate=new Date(0,0);lastDate.setFullYear(month.getFullYear());lastDate.setMonth(month.getMonth()+1);lastDate.setDate(-1);if(minDate&&maxDate&&minDate.getMonth()===maxDate.getMonth()&&minDate.getMonth()===month.getMonth()&&0<=maxDate.getDate()-minDate.getDate()){return!1}return!this._dateAllowed(firstDate,minDate,maxDate)&&!this._dateAllowed(lastDate,minDate,maxDate)}_getTitle(month,monthNames){if(month===void 0||monthNames===void 0){return}return this.i18n.formatTitle(monthNames[month.getMonth()],month.getFullYear())}_onMonthGridTouchStart(){this._notTapping=!1;setTimeout(()=>this._notTapping=!0,300)}_dateAdd(date,delta){date.setDate(date.getDate()+delta)}_applyFirstDayOfWeek(weekDayNames,firstDayOfWeek){if(weekDayNames===void 0||firstDayOfWeek===void 0){return}return weekDayNames.slice(firstDayOfWeek).concat(weekDayNames.slice(0,firstDayOfWeek))}_getWeekDayNames(weekDayNames,weekDayNamesShort,showWeekNumbers,firstDayOfWeek){if(weekDayNames===void 0||weekDayNamesShort===void 0||showWeekNumbers===void 0||firstDayOfWeek===void 0){return}weekDayNames=this._applyFirstDayOfWeek(weekDayNames,firstDayOfWeek);weekDayNamesShort=this._applyFirstDayOfWeek(weekDayNamesShort,firstDayOfWeek);weekDayNames=weekDayNames.map((day,index)=>{return{weekDay:day,weekDayShort:weekDayNamesShort[index]}});return weekDayNames}_getDate(date){return date?date.getDate():""}_showWeekNumbersChanged(showWeekNumbers,firstDayOfWeek){if(showWeekNumbers&&1===firstDayOfWeek){this.setAttribute("week-numbers","")}else{this.removeAttribute("week-numbers")}}_showWeekSeparator(showWeekNumbers,firstDayOfWeek){return showWeekNumbers&&1===firstDayOfWeek}_isToday(date){return this._dateEquals(new Date,date)}_getDays(month,firstDayOfWeek){if(month===void 0||firstDayOfWeek===void 0){return}var date=new Date(0,0);date.setFullYear(month.getFullYear());date.setMonth(month.getMonth());date.setDate(1);while(date.getDay()!==firstDayOfWeek){this._dateAdd(date,-1)}var days=[],startMonth=date.getMonth(),targetMonth=month.getMonth();while(date.getMonth()===targetMonth||date.getMonth()===startMonth){days.push(date.getMonth()===targetMonth?new Date(date.getTime()):null);this._dateAdd(date,1)}return days}_getWeekNumber(date,days){if(date===void 0||days===void 0){return}if(!date){date=days.reduce((acc,d)=>{return!acc&&d?d:acc})}return DatePickerHelper._getISOWeekNumber(date)}_getWeekNumbers(dates){return dates.map(date=>this._getWeekNumber(date,dates)).filter((week,index,arr)=>arr.indexOf(week)===index)}_handleTap(e){if(!this.ignoreTaps&&!this._notTapping&&e.target.date&&!e.target.hasAttribute("disabled")){this.selectedDate=e.target.date;this.dispatchEvent(new CustomEvent("date-tap",{bubbles:!0,composed:!0}))}}_preventDefault(e){e.preventDefault()}_getRole(date){return date?"button":"presentation"}_getAriaLabel(date){if(!date){return""}var ariaLabel=this._getDate(date)+" "+this.i18n.monthNames[date.getMonth()]+" "+date.getFullYear()+", "+this.i18n.weekdays[date.getDay()];if(this._isToday(date)){ariaLabel+=", "+this.i18n.today}return ariaLabel}_getAriaDisabled(date,min,max){if(date===void 0||min===void 0||max===void 0){return}return this._dateAllowed(date,min,max)?"false":"true"}}customElements.define(vaadin_month_calendar_MonthCalendarElement.is,vaadin_month_calendar_MonthCalendarElement);var templatize=__webpack_require__(26),render_status=__webpack_require__(54);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_infinite_scroller_InfiniteScrollerElement extends polymer_element.a{static get template(){return html_tag.a`
    <style>
      :host {
        display: block;
        overflow: hidden;
        height: 500px;
      }

      #scroller {
        position: relative;
        height: 100%;
        overflow: auto;
        outline: none;
        margin-right: -40px;
        -webkit-overflow-scrolling: touch;
        -ms-overflow-style: none;
        overflow-x: hidden;
      }

      #scroller.notouchscroll {
        -webkit-overflow-scrolling: auto;
      }

      #scroller::-webkit-scrollbar {
        display: none;
      }

      .buffer {
        position: absolute;
        width: var(--vaadin-infinite-scroller-buffer-width, 100%);
        box-sizing: border-box;
        padding-right: 40px;
        top: var(--vaadin-infinite-scroller-buffer-offset, 0);
        animation: fadein 0.2s;
      }

      @keyframes fadein {
        from { opacity: 0; }
        to { opacity: 1; }
      }
    </style>

    <div id="scroller" on-scroll="_scroll">
      <div class="buffer"></div>
      <div class="buffer"></div>
      <div id="fullHeight"></div>
    </div>
`}static get is(){return"vaadin-infinite-scroller"}static get properties(){return{bufferSize:{type:Number,value:20},_initialScroll:{value:5e5},_initialIndex:{value:0},_buffers:Array,_preventScrollEvent:Boolean,_mayHaveMomentum:Boolean,_initialized:Boolean,active:{type:Boolean,observer:"_activated"}}}ready(){super.ready();this._buffers=Array.prototype.slice.call(this.root.querySelectorAll(".buffer"));this.$.fullHeight.style.height=2*this._initialScroll+"px";var tpl=this.querySelector("template");this._TemplateClass=Object(templatize.b)(tpl,this,{forwardHostProp:function(prop,value){if("index"!==prop){this._buffers.forEach(buffer=>{[].forEach.call(buffer.children,insertionPoint=>{insertionPoint._itemWrapper.instance[prop]=value})})}}});var isFirefox=-1<navigator.userAgent.toLowerCase().indexOf("firefox");if(isFirefox){this.$.scroller.tabIndex=-1}}_activated(active){if(active&&!this._initialized){this._createPool();this._initialized=!0}}_finishInit(){if(!this._initDone){this._buffers.forEach(buffer=>{[].forEach.call(buffer.children,insertionPoint=>this._ensureStampedInstance(insertionPoint._itemWrapper))},this);if(!this._buffers[0].translateY){this._reset()}this._initDone=!0}}_translateBuffer(up){var index=up?1:0;this._buffers[index].translateY=this._buffers[index?0:1].translateY+this._bufferHeight*(index?-1:1);this._buffers[index].style.transform="translate3d(0, "+this._buffers[index].translateY+"px, 0)";this._buffers[index].updated=!1;this._buffers.reverse()}_scroll(){if(this._scrollDisabled){return}var scrollTop=this.$.scroller.scrollTop;if(scrollTop<this._bufferHeight||scrollTop>2*this._initialScroll-this._bufferHeight){this._initialIndex=~~this.position;this._reset()}var bufferOffset=this.root.querySelector(".buffer").offsetTop,upperThresholdReached=scrollTop>this._buffers[1].translateY+this.itemHeight+bufferOffset,lowerThresholdReached=scrollTop<this._buffers[0].translateY+this.itemHeight+bufferOffset;if(upperThresholdReached||lowerThresholdReached){this._translateBuffer(lowerThresholdReached);this._updateClones()}if(!this._preventScrollEvent){this.dispatchEvent(new CustomEvent("custom-scroll",{bubbles:!1,composed:!0}));this._mayHaveMomentum=!0}this._preventScrollEvent=!1;this._debouncerScrollFinish=debounce.a.debounce(this._debouncerScrollFinish,utils_async.d.after(200),()=>{var scrollerRect=this.$.scroller.getBoundingClientRect();if(!this._isVisible(this._buffers[0],scrollerRect)&&!this._isVisible(this._buffers[1],scrollerRect)){this.position=this.position}})}set position(index){this._preventScrollEvent=!0;if(index>this._firstIndex&&index<this._firstIndex+2*this.bufferSize){this.$.scroller.scrollTop=this.itemHeight*(index-this._firstIndex)+this._buffers[0].translateY}else{this._initialIndex=~~index;this._reset();this._scrollDisabled=!0;this.$.scroller.scrollTop+=index%1*this.itemHeight;this._scrollDisabled=!1}if(this._mayHaveMomentum){this.$.scroller.classList.add("notouchscroll");this._mayHaveMomentum=!1;setTimeout(()=>{this.$.scroller.classList.remove("notouchscroll")},10)}}get position(){return(this.$.scroller.scrollTop-this._buffers[0].translateY)/this.itemHeight+this._firstIndex}get itemHeight(){if(!this._itemHeightVal){const itemHeight=window.ShadyCSS?window.ShadyCSS.getComputedStyleValue(this,"--vaadin-infinite-scroller-item-height"):getComputedStyle(this).getPropertyValue("--vaadin-infinite-scroller-item-height"),tmpStyleProp="background-position";this.$.fullHeight.style.setProperty(tmpStyleProp,itemHeight);const itemHeightPx=getComputedStyle(this.$.fullHeight).getPropertyValue(tmpStyleProp);this.$.fullHeight.style.removeProperty(tmpStyleProp);this._itemHeightVal=parseFloat(itemHeightPx)}return this._itemHeightVal}get _bufferHeight(){return this.itemHeight*this.bufferSize}_reset(){this._scrollDisabled=!0;this.$.scroller.scrollTop=this._initialScroll;this._buffers[0].translateY=this._initialScroll-this._bufferHeight;this._buffers[1].translateY=this._initialScroll;this._buffers.forEach(buffer=>{buffer.style.transform="translate3d(0, "+buffer.translateY+"px, 0)"});this._buffers[0].updated=this._buffers[1].updated=!1;this._updateClones(!0);this._debouncerUpdateClones=debounce.a.debounce(this._debouncerUpdateClones,utils_async.d.after(200),()=>{this._buffers[0].updated=this._buffers[1].updated=!1;this._updateClones()});this._scrollDisabled=!1}_createPool(){var container=this.getBoundingClientRect();this._buffers.forEach(buffer=>{for(var i=0;i<this.bufferSize;i++){const itemWrapper=document.createElement("div");itemWrapper.style.height=this.itemHeight+"px";itemWrapper.instance={};const contentId=vaadin_infinite_scroller_InfiniteScrollerElement._contentIndex=vaadin_infinite_scroller_InfiniteScrollerElement._contentIndex+1||0,slotName="vaadin-infinite-scroller-item-content-"+contentId,insertionPoint=document.createElement("slot");insertionPoint.setAttribute("name",slotName);insertionPoint._itemWrapper=itemWrapper;buffer.appendChild(insertionPoint);itemWrapper.setAttribute("slot",slotName);this.appendChild(itemWrapper);Object(flush.b)();setTimeout(()=>{if(this._isVisible(itemWrapper,container)){this._ensureStampedInstance(itemWrapper)}},1)}},this);setTimeout(()=>{Object(render_status.a)(this,this._finishInit.bind(this))},1)}_ensureStampedInstance(itemWrapper){if(itemWrapper.firstElementChild){return}var tmpInstance=itemWrapper.instance;itemWrapper.instance=new this._TemplateClass({});itemWrapper.appendChild(itemWrapper.instance.root);Object.keys(tmpInstance).forEach(prop=>{itemWrapper.instance.set(prop,tmpInstance[prop])})}_updateClones(viewPortOnly){this._firstIndex=~~((this._buffers[0].translateY-this._initialScroll)/this.itemHeight)+this._initialIndex;var scrollerRect=viewPortOnly?this.$.scroller.getBoundingClientRect():void 0;this._buffers.forEach((buffer,bufferIndex)=>{if(!buffer.updated){var firstIndex=this._firstIndex+this.bufferSize*bufferIndex;[].forEach.call(buffer.children,(insertionPoint,index)=>{const itemWrapper=insertionPoint._itemWrapper;if(!viewPortOnly||this._isVisible(itemWrapper,scrollerRect)){itemWrapper.instance.index=firstIndex+index}});buffer.updated=!0}},this)}_isVisible(element,container){var rect=element.getBoundingClientRect();return rect.bottom>container.top&&rect.top<container.bottom}}customElements.define(vaadin_infinite_scroller_InfiniteScrollerElement.is,vaadin_infinite_scroller_InfiniteScrollerElement);var custom_style=__webpack_require__(83);const src_vaadin_date_picker_styles_$_documentContainer=document.createElement("template");src_vaadin_date_picker_styles_$_documentContainer.innerHTML=`<custom-style>
  <style>
    @font-face {
      font-family: 'vaadin-date-picker-icons';
      src: url(data:application/font-woff;charset=utf-8;base64,d09GRgABAAAAAAYoAAsAAAAABdwAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAABPUy8yAAABCAAAAGAAAABgDxIFqWNtYXAAAAFoAAAAVAAAAFQXVtKKZ2FzcAAAAbwAAAAIAAAACAAAABBnbHlmAAABxAAAAUAAAAFAAtWm1WhlYWQAAAMEAAAANgAAADYNRs5taGhlYQAAAzwAAAAkAAAAJAdCA8lobXR4AAADYAAAACAAAAAgFW4CxGxvY2EAAAOAAAAAEgAAABIBEgDCbWF4cAAAA5QAAAAgAAAAIAAMACNuYW1lAAADtAAAAlIAAAJSbLEfa3Bvc3QAAAYIAAAAIAAAACAAAwAAAAMDfAGQAAUAAAKZAswAAACPApkCzAAAAesAMwEJAAAAAAAAAAAAAAAAAAAAARAAAAAAAAAAAAAAAAAAAAAAQAAA6QMDwP/AAEADwABAAAAAAQAAAAAAAAAAAAAAIAAAAAAAAwAAAAMAAAAcAAEAAwAAABwAAwABAAAAHAAEADgAAAAKAAgAAgACAAEAIOkD//3//wAAAAAAIOkA//3//wAB/+MXBAADAAEAAAAAAAAAAAAAAAEAAf//AA8AAQAAAAAAAAAAAAIAADc5AQAAAAABAAAAAAAAAAAAAgAANzkBAAAAAAEAAAAAAAAAAAACAAA3OQEAAAAAAQFvAKsCqwKrAAUAAAEHFwcXAQGrPMPDPAEAAqs8xMQ8AQAAAQDVAIADKwLVAAsAAAEnBycHFwcXNxc3JwMrPO/vPO/vPO/vPO8CmTzu7jzu7zzv7zzvAAMAgAArA4ADgAADABwAIAAAASMVMwMVITUjFSMiBhURFBYzITI2NRE0JisBNSMTIREhAtXV1Sr+qlUrIzIyIwJWIzIyIytVgP2qAlYBq9YCq1VVVTIk/asjMjIjAlUkMlX9AAHVAAAAAQAAAAADbgNuABMAAAEUDgIjIi4CNTQ+AjMyHgIDbkV3oFtboHdFRXegW1ugd0UBt1ugd0VFd6BbW6B3RUV3oAAAAAABAAAAAQAAvCcusV8PPPUACwQAAAAAANVURPgAAAAA1VRE+AAAAAADgAOAAAAACAACAAAAAAAAAAEAAAPA/8AAAAQAAAAAAAOAAAEAAAAAAAAAAAAAAAAAAAAIBAAAAAAAAAAAAAAAAgAAAAQAAW8EAADVBAAAgANuAAAAAAAAAAoAFAAeADAASgB+AKAAAAABAAAACAAhAAMAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAADgCuAAEAAAAAAAEAGAAAAAEAAAAAAAIABwD5AAEAAAAAAAMAGABpAAEAAAAAAAQAGAEOAAEAAAAAAAUACwBIAAEAAAAAAAYAGACxAAEAAAAAAAoAGgFWAAMAAQQJAAEAMAAYAAMAAQQJAAIADgEAAAMAAQQJAAMAMACBAAMAAQQJAAQAMAEmAAMAAQQJAAUAFgBTAAMAAQQJAAYAMADJAAMAAQQJAAoANAFwdmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzVmVyc2lvbiAxLjAAVgBlAHIAcwBpAG8AbgAgADEALgAwdmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzdmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzUmVndWxhcgBSAGUAZwB1AGwAYQBydmFhZGluLWRhdGUtcGlja2VyLWljb25zAHYAYQBhAGQAaQBuAC0AZABhAHQAZQAtAHAAaQBjAGsAZQByAC0AaQBjAG8AbgBzRm9udCBnZW5lcmF0ZWQgYnkgSWNvTW9vbi4ARgBvAG4AdAAgAGcAZQBuAGUAcgBhAHQAZQBkACAAYgB5ACAASQBjAG8ATQBvAG8AbgAuAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==) format('woff');
      font-weight: normal;
      font-style: normal;
    }
  </style>
</custom-style><dom-module id="vaadin-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">
  <template>
    <style>
      :host {
        align-items: flex-start;
        justify-content: flex-start;
      }

      :host([bottom-aligned]) {
        justify-content: flex-end;
      }

      :host([right-aligned]) {
        align-items: flex-end;
      }

      [part="overlay"] {
        display: flex;
        flex: auto;
      }

      [part~="content"] {
        flex: auto;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(src_vaadin_date_picker_styles_$_documentContainer.content);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_date_picker_overlay_content_DatePickerOverlayContentElement extends Object(vaadin_themable_mixin.a)(Object(vaadin_theme_property_mixin.a)(Object(gesture_event_listeners.a)(polymer_element.a))){static get template(){return html_tag.a`
    <style>
      :host {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        outline: none;
        background: #fff;
      }

      [part="overlay-header"] {
        display: flex;
        flex-shrink: 0;
        flex-wrap: nowrap;
        align-items: center;
      }

      :host(:not([fullscreen])) [part="overlay-header"] {
        display: none;
      }

      [part="label"] {
        flex-grow: 1;
      }

      [part="clear-button"],
      [part="toggle-button"],
      [part="years-toggle-button"]::before {
        font-family: 'vaadin-date-picker-icons';
      }

      [part="clear-button"]:not([showclear]) {
        display: none;
      }

      [part="clear-button"]::before {
        content: "\\e901";
      }

      [part="toggle-button"]::before {
        content: "\\e902";
      }

      [part="years-toggle-button"] {
        display: flex;
      }

      [part="years-toggle-button"][desktop] {
        display: none;
      }

      [part="years-toggle-button"]::before {
        content: "\\e900";
      }

      :host(:not([years-visible])) [part="years-toggle-button"]::before {
        transform: rotate(180deg);
      }

      #scrollers {
        display: flex;
        height: 100%;
        width: 100%;
        position: relative;
        overflow: hidden;
      }

      [part="months"],
      [part="years"] {
        height: 100%;
      }

      [part="months"] {
        --vaadin-infinite-scroller-item-height: 270px;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
      }

      #scrollers[desktop] [part="months"] {
        right: 50px;
        transform: none !important;
      }

      [part="years"] {
        --vaadin-infinite-scroller-item-height: 80px;
        width: 50px;
        position: absolute;
        right: 0;
        transform: translateX(100%);
        -webkit-tap-highlight-color: transparent;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        /* Center the year scroller position. */
        --vaadin-infinite-scroller-buffer-offset: 50%;
      }

      #scrollers[desktop] [part="years"] {
        position: absolute;
        transform: none !important;
      }

      [part="years"]::before {
        content: '';
        display: block;
        background: transparent;
        width: 0;
        height: 0;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        border-width: 6px;
        border-style: solid;
        border-color: transparent;
        border-left-color: #000;
      }

      :host(.animate) [part="months"],
      :host(.animate) [part="years"] {
        transition: all 200ms;
      }

      [part="toolbar"] {
        display: flex;
        justify-content: space-between;
        z-index: 2;
        flex-shrink: 0;
      }

      [part~="overlay-header"]:not([desktop]) {
        padding-bottom: 40px;
      }

      [part~="years-toggle-button"] {
        position: absolute;
        top: auto;
        right: 8px;
        bottom: 0;
        z-index: 1;
        padding: 8px;
      }

      #announcer {
        display: inline-block;
        position: fixed;
        clip: rect(0, 0, 0, 0);
        clip-path: inset(100%);
      }
    </style>

    <div id="announcer" role="alert" aria-live="polite">
      [[i18n.calendar]]
    </div>

    <div part="overlay-header" on-touchend="_preventDefault" desktop\$="[[_desktopMode]]" aria-hidden="true">
      <div part="label">[[_formatDisplayed(selectedDate, i18n.formatDate, label)]]</div>
      <div part="clear-button" on-tap="_clear" showclear\$="[[_showClear(selectedDate)]]"></div>
      <div part="toggle-button" on-tap="_cancel"></div>

      <div part="years-toggle-button" desktop\$="[[_desktopMode]]" on-tap="_toggleYearScroller" aria-hidden="true">
        [[_yearAfterXMonths(_visibleMonthIndex)]]
      </div>
    </div>

    <div id="scrollers" desktop\$="[[_desktopMode]]" on-track="_track">
      <vaadin-infinite-scroller id="monthScroller" on-custom-scroll="_onMonthScroll" on-touchstart="_onMonthScrollTouchStart" buffer-size="3" active="[[initialPosition]]" part="months">
        <template>
          <vaadin-month-calendar i18n="[[i18n]]" month="[[_dateAfterXMonths(index)]]" selected-date="{{selectedDate}}" focused-date="[[focusedDate]]" ignore-taps="[[_ignoreTaps]]" show-week-numbers="[[showWeekNumbers]]" min-date="[[minDate]]" max-date="[[maxDate]]" focused\$="[[_focused]]" part="month" theme\$="[[theme]]">
          </vaadin-month-calendar>
        </template>
      </vaadin-infinite-scroller>
      <vaadin-infinite-scroller id="yearScroller" on-tap="_onYearTap" on-custom-scroll="_onYearScroll" on-touchstart="_onYearScrollTouchStart" buffer-size="12" active="[[initialPosition]]" part="years">
        <template>
          <div part="year-number" role="button" current\$="[[_isCurrentYear(index)]]" selected\$="[[_isSelectedYear(index, selectedDate)]]">
            [[_yearAfterXYears(index)]]
          </div>
          <div part="year-separator" aria-hidden="true"></div>
        </template>
      </vaadin-infinite-scroller>
    </div>

    <div on-touchend="_preventDefault" role="toolbar" part="toolbar">
      <vaadin-button id="todayButton" part="today-button" disabled="[[!_isTodayAllowed(minDate, maxDate)]]" on-tap="_onTodayTap">
        [[i18n.today]]
      </vaadin-button>
      <vaadin-button id="cancelButton" part="cancel-button" on-tap="_cancel">
        [[i18n.cancel]]
      </vaadin-button>
    </div>

    <iron-media-query query="(min-width: 375px)" query-matches="{{_desktopMode}}"></iron-media-query>
`}static get is(){return"vaadin-date-picker-overlay-content"}static get properties(){return{selectedDate:{type:Date,notify:!0},focusedDate:{type:Date,notify:!0,observer:"_focusedDateChanged"},_focusedMonthDate:Number,initialPosition:{type:Date,observer:"_initialPositionChanged"},_originDate:{value:new Date},_visibleMonthIndex:Number,_desktopMode:Boolean,_translateX:{observer:"_translateXChanged"},_yearScrollerWidth:{value:50},i18n:{type:Object},showWeekNumbers:{type:Boolean},_ignoreTaps:Boolean,_notTapping:Boolean,minDate:Date,maxDate:Date,_focused:Boolean,label:String}}ready(){super.ready();this.setAttribute("tabindex",0);this.addEventListener("keydown",this._onKeydown.bind(this));Object(gestures.b)(this,"tap",this._stopPropagation);this.addEventListener("focus",this._onOverlayFocus.bind(this));this.addEventListener("blur",this._onOverlayBlur.bind(this))}connectedCallback(){super.connectedCallback();this._closeYearScroller();this._toggleAnimateClass(!0);Object(gestures.f)(this.$.scrollers,"pan-y");iron_a11y_announcer.a.requestAvailability()}announceFocusedDate(){var focusedDate=this._currentlyFocusedDate(),announce=[];if(DatePickerHelper._dateEquals(focusedDate,new Date)){announce.push(this.i18n.today)}announce=announce.concat([this.i18n.weekdays[focusedDate.getDay()],focusedDate.getDate(),this.i18n.monthNames[focusedDate.getMonth()],focusedDate.getFullYear()]);if(this.showWeekNumbers&&1===this.i18n.firstDayOfWeek){announce.push(this.i18n.week);announce.push(DatePickerHelper._getISOWeekNumber(focusedDate))}this.dispatchEvent(new CustomEvent("iron-announce",{bubbles:!0,composed:!0,detail:{text:announce.join(" ")}}));return}focusCancel(){this.$.cancelButton.focus()}scrollToDate(date,animate){this._scrollToPosition(this._differenceInMonths(date,this._originDate),animate)}_focusedDateChanged(focusedDate){this.revealDate(focusedDate)}_isCurrentYear(yearsFromNow){return 0===yearsFromNow}_isSelectedYear(yearsFromNow,selectedDate){if(selectedDate){return selectedDate.getFullYear()===this._originDate.getFullYear()+yearsFromNow}}revealDate(date){if(date){var diff=this._differenceInMonths(date,this._originDate),scrolledAboveViewport=this.$.monthScroller.position>diff,visibleItems=this.$.monthScroller.clientHeight/this.$.monthScroller.itemHeight,scrolledBelowViewport=this.$.monthScroller.position+visibleItems-1<diff;if(scrolledAboveViewport){this._scrollToPosition(diff,!0)}else if(scrolledBelowViewport){this._scrollToPosition(diff-visibleItems+1,!0)}}}_onOverlayFocus(){this._focused=!0}_onOverlayBlur(){this._focused=!1}_initialPositionChanged(initialPosition){this.scrollToDate(initialPosition)}_repositionYearScroller(){this._visibleMonthIndex=_Mathfloor(this.$.monthScroller.position);this.$.yearScroller.position=(this.$.monthScroller.position+this._originDate.getMonth())/12}_repositionMonthScroller(){this.$.monthScroller.position=12*this.$.yearScroller.position-this._originDate.getMonth();this._visibleMonthIndex=_Mathfloor(this.$.monthScroller.position)}_onMonthScroll(){this._repositionYearScroller();this._doIgnoreTaps()}_onYearScroll(){this._repositionMonthScroller();this._doIgnoreTaps()}_onYearScrollTouchStart(){this._notTapping=!1;setTimeout(()=>this._notTapping=!0,300);this._repositionMonthScroller()}_onMonthScrollTouchStart(){this._repositionYearScroller()}_doIgnoreTaps(){this._ignoreTaps=!0;this._debouncer=debounce.a.debounce(this._debouncer,utils_async.d.after(300),()=>this._ignoreTaps=!1)}_formatDisplayed(date,formatDate,label){if(date){return formatDate(DatePickerHelper._extractDateParts(date))}else{return label}}_onTodayTap(){var today=new Date;if(this.$.monthScroller.position===this._differenceInMonths(today,this._originDate)){this.selectedDate=today;this._close()}else{this._scrollToCurrentMonth()}}_scrollToCurrentMonth(){if(this.focusedDate){this.focusedDate=new Date}this.scrollToDate(new Date,!0)}_showClear(selectedDate){return!!selectedDate}_onYearTap(e){if(!this._ignoreTaps&&!this._notTapping){var scrollDelta=e.detail.y-(this.$.yearScroller.getBoundingClientRect().top+this.$.yearScroller.clientHeight/2),yearDelta=scrollDelta/this.$.yearScroller.itemHeight;this._scrollToPosition(this.$.monthScroller.position+12*yearDelta,!0)}}_scrollToPosition(targetPosition,animate){if(this._targetPosition!==void 0){this._targetPosition=targetPosition;return}if(!animate){this.$.monthScroller.position=targetPosition;this._targetPosition=void 0;this._repositionYearScroller();return}this._targetPosition=targetPosition;var easingFunction=(t,b,c,d)=>{t/=d/2;if(1>t){return c/2*t*t+b}t--;return-c/2*(t*(t-2)-1)+b},duration=animate?300:0,start=0,initialPosition=this.$.monthScroller.position,smoothScroll=timestamp=>{start=start||timestamp;var currentTime=timestamp-start;if(currentTime<duration){var currentPos=easingFunction(currentTime,initialPosition,this._targetPosition-initialPosition,duration);this.$.monthScroller.position=currentPos;window.requestAnimationFrame(smoothScroll)}else{this.dispatchEvent(new CustomEvent("scroll-animation-finished",{bubbles:!0,composed:!0,detail:{position:this._targetPosition,oldPosition:initialPosition}}));this.$.monthScroller.position=this._targetPosition;this._targetPosition=void 0}setTimeout(this._repositionYearScroller.bind(this),1)};window.requestAnimationFrame(smoothScroll)}_limit(value,range){return _Mathmin(range.max,Math.max(range.min,value))}_handleTrack(e){if(10>_Mathabs2(e.detail.dx)||10<_Mathabs2(e.detail.ddy)){return}if(_Mathabs2(e.detail.ddx)>this._yearScrollerWidth/3){this._toggleAnimateClass(!0)}var newTranslateX=this._translateX+e.detail.ddx;this._translateX=this._limit(newTranslateX,{min:0,max:this._yearScrollerWidth})}_track(e){if(this._desktopMode){return}switch(e.detail.state){case"start":this._toggleAnimateClass(!1);break;case"track":this._handleTrack(e);break;case"end":this._toggleAnimateClass(!0);if(this._translateX>=this._yearScrollerWidth/2){this._closeYearScroller()}else{this._openYearScroller()}break;}}_toggleAnimateClass(enable){if(enable){this.classList.add("animate")}else{this.classList.remove("animate")}}_toggleYearScroller(){this._isYearScrollerVisible()?this._closeYearScroller():this._openYearScroller()}_openYearScroller(){this._translateX=0;this.setAttribute("years-visible","")}_closeYearScroller(){this.removeAttribute("years-visible");this._translateX=this._yearScrollerWidth}_isYearScrollerVisible(){return this._translateX<this._yearScrollerWidth/2}_translateXChanged(x){if(!this._desktopMode){this.$.monthScroller.style.transform="translateX("+(x-this._yearScrollerWidth)+"px)";this.$.yearScroller.style.transform="translateX("+x+"px)"}}_yearAfterXYears(index){var result=new Date(this._originDate);result.setFullYear(parseInt(index)+this._originDate.getFullYear());return result.getFullYear()}_yearAfterXMonths(months){return this._dateAfterXMonths(months).getFullYear()}_dateAfterXMonths(months){var result=new Date(this._originDate);result.setDate(1);result.setMonth(parseInt(months)+this._originDate.getMonth());return result}_differenceInMonths(date1,date2){var months=12*(date1.getFullYear()-date2.getFullYear());return months-date2.getMonth()+date1.getMonth()}_differenceInYears(date1,date2){return this._differenceInMonths(date1,date2)/12}_clear(){this.selectedDate=""}_close(){const overlayContent=this.getRootNode().host,overlay=overlayContent?overlayContent.getRootNode().host:null;if(overlay){overlay.opened=!1}this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}_cancel(){this.focusedDate=this.selectedDate;this._close()}_preventDefault(e){e.preventDefault()}_eventKey(e){for(var keys=["down","up","right","left","enter","space","home","end","pageup","pagedown","tab","esc"],i=0,k;i<keys.length;i++){k=keys[i];if(iron_a11y_keys_behavior.a.keyboardEventMatchesKeys(e,k)){return k}}}_onKeydown(e){var focus=this._currentlyFocusedDate();const isToday=0<=e.composedPath().indexOf(this.$.todayButton),isCancel=0<=e.composedPath().indexOf(this.$.cancelButton),isScroller=!isToday&&!isCancel;var eventKey=this._eventKey(e);if("tab"===eventKey){e.stopPropagation();const isFullscreen=this.hasAttribute("fullscreen"),isShift=e.shiftKey;if(isFullscreen){e.preventDefault()}else if(isShift&&isScroller||!isShift&&isCancel){e.preventDefault();this.dispatchEvent(new CustomEvent("focus-input",{bubbles:!0,composed:!0}))}else if(isShift&&isToday){this._focused=!0;setTimeout(()=>this.revealDate(this.focusedDate),1)}else{this._focused=!1}}else if(eventKey){e.preventDefault();e.stopPropagation();switch(eventKey){case"down":this._moveFocusByDays(7);this.focus();break;case"up":this._moveFocusByDays(-7);this.focus();break;case"right":if(isScroller){this._moveFocusByDays(1)}break;case"left":if(isScroller){this._moveFocusByDays(-1)}break;case"enter":if(isScroller||isCancel){this._close()}else if(isToday){this._onTodayTap()}break;case"space":if(isCancel){this._close()}else if(isToday){this._onTodayTap()}else{var focusedDate=this.focusedDate;if(DatePickerHelper._dateEquals(focusedDate,this.selectedDate)){this.selectedDate="";this.focusedDate=focusedDate}else{this.selectedDate=focusedDate}}break;case"home":this._moveFocusInsideMonth(focus,"minDate");break;case"end":this._moveFocusInsideMonth(focus,"maxDate");break;case"pagedown":this._moveFocusByMonths(e.shiftKey?12:1);break;case"pageup":this._moveFocusByMonths(e.shiftKey?-12:-1);break;case"esc":this._cancel();break;}}}_currentlyFocusedDate(){return this.focusedDate||this.selectedDate||this.initialPosition||new Date}_focusDate(dateToFocus){this.focusedDate=dateToFocus;this._focusedMonthDate=dateToFocus.getDate()}_focusClosestDate(focus){this._focusDate(DatePickerHelper._getClosestDate(focus,[this.minDate,this.maxDate]))}_moveFocusByDays(days){var focus=this._currentlyFocusedDate(),dateToFocus=new Date(0,0);dateToFocus.setFullYear(focus.getFullYear());dateToFocus.setMonth(focus.getMonth());dateToFocus.setDate(focus.getDate()+days);if(this._dateAllowed(dateToFocus,this.minDate,this.maxDate)){this._focusDate(dateToFocus)}else{if(this._dateAllowed(focus,this.minDate,this.maxDate)){if(0<days){this._focusDate(this.maxDate)}else{this._focusDate(this.minDate)}}else{this._focusClosestDate(focus)}}}_moveFocusByMonths(months){var focus=this._currentlyFocusedDate(),dateToFocus=new Date(0,0);dateToFocus.setFullYear(focus.getFullYear());dateToFocus.setMonth(focus.getMonth()+months);var targetMonth=dateToFocus.getMonth();dateToFocus.setDate(this._focusedMonthDate||(this._focusedMonthDate=focus.getDate()));if(dateToFocus.getMonth()!==targetMonth){dateToFocus.setDate(0)}if(this._dateAllowed(dateToFocus,this.minDate,this.maxDate)){this.focusedDate=dateToFocus}else{if(this._dateAllowed(focus,this.minDate,this.maxDate)){if(0<months){this._focusDate(this.maxDate)}else{this._focusDate(this.minDate)}}else{this._focusClosestDate(focus)}}}_moveFocusInsideMonth(focusedDate,property){var dateToFocus=new Date(0,0);dateToFocus.setFullYear(focusedDate.getFullYear());if("minDate"===property){dateToFocus.setMonth(focusedDate.getMonth());dateToFocus.setDate(1)}else{dateToFocus.setMonth(focusedDate.getMonth()+1);dateToFocus.setDate(0)}if(this._dateAllowed(dateToFocus,this.minDate,this.maxDate)){this._focusDate(dateToFocus)}else{if(this._dateAllowed(focusedDate,this.minDate,this.maxDate)){this._focusDate(this[property])}else{this._focusClosestDate(focusedDate)}}}_dateAllowed(date,min,max){return(!min||date>=min)&&(!max||date<=max)}_isTodayAllowed(min,max){var today=new Date,todayMidnight=new Date(0,0);todayMidnight.setFullYear(today.getFullYear());todayMidnight.setMonth(today.getMonth());todayMidnight.setDate(today.getDate());return this._dateAllowed(todayMidnight,min,max)}_stopPropagation(e){e.stopPropagation()}}customElements.define(vaadin_date_picker_overlay_content_DatePickerOverlayContentElement.is,vaadin_date_picker_overlay_content_DatePickerOverlayContentElement);var iron_resizable_behavior=__webpack_require__(81),legacy_class=__webpack_require__(62);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const DatePickerMixin=subclass=>class VaadinDatePickerMixin extends Object(legacy_class.b)([iron_resizable_behavior.a],subclass){static get properties(){return{_selectedDate:{type:Date},_focusedDate:Date,value:{type:String,observer:"_valueChanged",notify:!0,value:""},required:{type:Boolean,value:!1},name:{type:String},initialPosition:String,label:String,opened:{type:Boolean,reflectToAttribute:!0,notify:!0,observer:"_openedChanged"},showWeekNumbers:{type:Boolean},_fullscreen:{value:!1,observer:"_fullscreenChanged"},_fullscreenMediaQuery:{value:"(max-width: 420px), (max-height: 420px)"},_touchPrevented:Array,i18n:{type:Object,value:()=>{return{monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],weekdays:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],weekdaysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],firstDayOfWeek:0,week:"Week",calendar:"Calendar",clear:"Clear",today:"Today",cancel:"Cancel",formatDate:d=>{const yearStr=(d.year+"").replace(/\d+/,y=>"0000".substr(y.length)+y);return[d.month+1,d.day,yearStr].join("/")},parseDate:text=>{const parts=text.split("/"),today=new Date;let date,month=today.getMonth(),year=today.getFullYear();if(3===parts.length){year=parseInt(parts[2]);if(3>parts[2].length&&0<=year){year+=50>year?2e3:1900}month=parseInt(parts[0])-1;date=parseInt(parts[1])}else if(2===parts.length){month=parseInt(parts[0])-1;date=parseInt(parts[1])}else if(1===parts.length){date=parseInt(parts[0])}if(date!==void 0){return{day:date,month,year}}},formatTitle:(monthName,fullYear)=>{return monthName+" "+fullYear}}}},min:{type:String,observer:"_minChanged"},max:{type:String,observer:"_maxChanged"},_minDate:{type:Date,value:""},_maxDate:{type:Date,value:""},_noInput:{type:Boolean,computed:"_isNoInput(_fullscreen, _ios, i18n, i18n.*)"},_ios:{type:Boolean,value:navigator.userAgent.match(/iP(?:hone|ad;(?: U;)? CPU) OS (\d+)/)},_webkitOverflowScroll:{type:Boolean,value:""===document.createElement("div").style.webkitOverflowScrolling},_ignoreAnnounce:{value:!0},_focusOverlayOnOpen:Boolean}}static get observers(){return["_updateHasValue(value)","_validateInput(_selectedDate, _minDate, _maxDate)","_selectedDateChanged(_selectedDate, i18n.formatDate)","_focusedDateChanged(_focusedDate, i18n.formatDate)","_announceFocusedDate(_focusedDate, opened, _ignoreAnnounce)"]}ready(){super.ready();this._boundOnScroll=this._onScroll.bind(this);this._boundFocus=this._focus.bind(this);this._boundUpdateAlignmentAndPosition=this._updateAlignmentAndPosition.bind(this);Object(gestures.b)(this,"tap",this.open);this.addEventListener("touchend",this._preventDefault.bind(this));this.addEventListener("keydown",this._onKeydown.bind(this));this._overlayContent.addEventListener("close",this._close.bind(this));this._overlayContent.addEventListener("focus-input",this._focusAndSelect.bind(this));this.addEventListener("input",this._onUserInput.bind(this));this.addEventListener("focus",e=>this._noInput&&e.target.blur())}connectedCallback(){super.connectedCallback();this.$.overlay.addEventListener("vaadin-overlay-escape-press",this._boundFocus)}disconnectedCallback(){super.disconnectedCallback();this.$.overlay.removeEventListener("vaadin-overlay-escape-press",this._boundFocus);this.opened=!1}open(){if(!this.disabled&&!this.readonly){this.$.overlay.opened=!0}}_close(e){if(e){e.stopPropagation()}this._focus();this.close()}close(){this.$.overlay.close()}get _inputElement(){return this._input()}get _nativeInput(){if(this._inputElement){return this._inputElement.focusElement?this._inputElement.focusElement:this._inputElement.inputElement?this._inputElement.inputElement:window.unwrap?window.unwrap(this._inputElement):this._inputElement}}_parseDate(str){var parts=/^([-+]\d{1}|\d{2,4}|[-+]\d{6})-(\d{1,2})-(\d{1,2})$/.exec(str);if(!parts){return}var date=new Date(0,0);date.setFullYear(parseInt(parts[1],10));date.setMonth(parseInt(parts[2],10)-1);date.setDate(parseInt(parts[3],10));return date}_isNoInput(fullscreen,ios,i18n){return!this._inputElement||fullscreen||ios||!i18n.parseDate}_formatISO(date){if(!(date instanceof Date)){return""}const pad=(num,fmt="00")=>(fmt+num).substr((fmt+num).length-fmt.length);let yearSign="",yearFmt="0000",yearAbs=date.getFullYear();if(0>yearAbs){yearAbs=-yearAbs;yearSign="-";yearFmt="000000"}else if(1e4<=date.getFullYear()){yearSign="+";yearFmt="000000"}const year=yearSign+pad(yearAbs,yearFmt),month=pad(date.getMonth()+1),day=pad(date.getDate());return[year,month,day].join("-")}_openedChanged(opened){if(!opened){return}this._updateAlignmentAndPosition()}_selectedDateChanged(selectedDate,formatDate){if(selectedDate===void 0||formatDate===void 0){return}if(this.__userInputOccurred){this.__dispatchChange=!0}const inputValue=selectedDate&&formatDate(DatePickerHelper._extractDateParts(selectedDate)),value=this._formatISO(selectedDate);if(value!==this.value){this.validate(inputValue);this.value=value}this.__userInputOccurred=!1;this.__dispatchChange=!1;this._focusedDate=selectedDate;this._inputValue=selectedDate?inputValue:""}_focusedDateChanged(focusedDate,formatDate){if(focusedDate===void 0||formatDate===void 0){return}this.__userInputOccurred=!0;if(!this._ignoreFocusedDateChange&&!this._noInput){this._inputValue=focusedDate?formatDate(DatePickerHelper._extractDateParts(focusedDate)):""}}_updateHasValue(value){if(value){this.setAttribute("has-value","")}else{this.removeAttribute("has-value")}}_handleDateChange(property,value,oldValue){if(!value){this[property]="";return}var date=this._parseDate(value);if(!date){this.value=oldValue;return}if(!DatePickerHelper._dateEquals(this[property],date)){this[property]=date}}_valueChanged(value,oldValue){if(this.__dispatchChange){this.dispatchEvent(new CustomEvent("change",{bubbles:!0}))}this._handleDateChange("_selectedDate",value,oldValue)}_minChanged(value,oldValue){this._handleDateChange("_minDate",value,oldValue)}_maxChanged(value,oldValue){this._handleDateChange("_maxDate",value,oldValue)}_updateAlignmentAndPosition(){if(!this._fullscreen){const inputRect=this._inputElement.getBoundingClientRect(),bottomAlign=inputRect.top>window.innerHeight/2,rightAlign=inputRect.left+this.clientWidth/2>window.innerWidth/2;if(rightAlign){const viewportWidth=_Mathmin(window.innerWidth,document.documentElement.clientWidth);this.$.overlay.setAttribute("right-aligned","");this.$.overlay.style.removeProperty("left");this.$.overlay.style.right=viewportWidth-inputRect.right+"px"}else{this.$.overlay.removeAttribute("right-aligned");this.$.overlay.style.removeProperty("right");this.$.overlay.style.left=inputRect.left+"px"}if(bottomAlign){const viewportHeight=_Mathmin(window.innerHeight,document.documentElement.clientHeight);this.$.overlay.setAttribute("bottom-aligned","");this.$.overlay.style.removeProperty("top");this.$.overlay.style.bottom=viewportHeight-inputRect.top+"px"}else{this.$.overlay.removeAttribute("bottom-aligned");this.$.overlay.style.removeProperty("bottom");this.$.overlay.style.top=inputRect.bottom+"px"}}this._overlayContent._repositionYearScroller()}_fullscreenChanged(){if(this.$.overlay.opened){this._updateAlignmentAndPosition()}}_onOverlayOpened(){this._openedWithFocusRing=this.hasAttribute("focus-ring")||this.focusElement&&this.focusElement.hasAttribute("focus-ring");var parsedInitialPosition=this._parseDate(this.initialPosition),initialPosition=this._selectedDate||this._overlayContent.initialPosition||parsedInitialPosition||new Date;if(parsedInitialPosition||DatePickerHelper._dateAllowed(initialPosition,this._minDate,this._maxDate)){this._overlayContent.initialPosition=initialPosition}else{this._overlayContent.initialPosition=DatePickerHelper._getClosestDate(initialPosition,[this._minDate,this._maxDate])}this._overlayContent.scrollToDate(this._overlayContent.focusedDate||this._overlayContent.initialPosition);this._ignoreFocusedDateChange=!0;this._overlayContent.focusedDate=this._overlayContent.focusedDate||this._overlayContent.initialPosition;this._ignoreFocusedDateChange=!1;window.addEventListener("scroll",this._boundOnScroll,!0);this.addEventListener("iron-resize",this._boundUpdateAlignmentAndPosition);if(this._webkitOverflowScroll){this._touchPrevented=this._preventWebkitOverflowScrollingTouch(this.parentElement)}if(this._focusOverlayOnOpen){this._overlayContent.focus();this._focusOverlayOnOpen=!1}else{this._focus()}if(this._noInput&&this.focusElement){this.focusElement.blur()}this.updateStyles();this._ignoreAnnounce=!1}_preventWebkitOverflowScrollingTouch(element){var result=[];while(element){if("touch"===window.getComputedStyle(element).webkitOverflowScrolling){var oldInlineValue=element.style.webkitOverflowScrolling;element.style.webkitOverflowScrolling="auto";result.push({element:element,oldInlineValue:oldInlineValue})}element=element.parentElement}return result}_onOverlayClosed(){this._ignoreAnnounce=!0;window.removeEventListener("scroll",this._boundOnScroll,!0);this.removeEventListener("iron-resize",this._boundUpdateAlignmentAndPosition);if(this._touchPrevented){this._touchPrevented.forEach(prevented=>prevented.element.style.webkitOverflowScrolling=prevented.oldInlineValue);this._touchPrevented=[]}this.updateStyles();this._ignoreFocusedDateChange=!0;if(this.i18n.parseDate){var inputValue=this._inputValue||"";const dateObject=this.i18n.parseDate(inputValue),parsedDate=dateObject&&this._parseDate(`${dateObject.year}-${dateObject.month+1}-${dateObject.day}`);if(this._isValidDate(parsedDate)){this._selectedDate=parsedDate}else{this._selectedDate=null;this._inputValue=inputValue}}else if(this._focusedDate){this._selectedDate=this._focusedDate}this._ignoreFocusedDateChange=!1;if(this._nativeInput&&this._nativeInput.selectionStart){this._nativeInput.selectionStart=this._nativeInput.selectionEnd}this.validate()}validate(value){this.invalid=!1;value=value!==void 0?value:this._inputValue;return!(this.invalid=!this.checkValidity(value))}checkValidity(value){var inputValid=!value||this._selectedDate&&value===this.i18n.formatDate(DatePickerHelper._extractDateParts(this._selectedDate)),minMaxValid=!this._selectedDate||DatePickerHelper._dateAllowed(this._selectedDate,this._minDate,this._maxDate),inputValidity=!0;if(this._inputElement){if(this._inputElement.checkValidity){inputValidity=this._inputElement.checkValidity(value)}else if(this._inputElement.validate){inputValidity=this._inputElement.validate(value)}}return inputValid&&minMaxValid&&inputValidity}_onScroll(e){if(e.target===window||!this._overlayContent.contains(e.target)){this._updateAlignmentAndPosition()}}_focus(){if(this._noInput){this._overlayContent.focus()}else{this._inputElement.focus()}}_focusAndSelect(){this._focus();this._setSelectionRange(0,this._inputValue.length)}_setSelectionRange(a,b){if(this._nativeInput&&this._nativeInput.setSelectionRange){this._nativeInput.setSelectionRange(a,b)}}_preventDefault(e){e.preventDefault()}_eventKey(e){for(var keys=["down","up","enter","esc","tab"],i=0,k;i<keys.length;i++){k=keys[i];if(iron_a11y_keys_behavior.a.keyboardEventMatchesKeys(e,k)){return k}}}_isValidDate(d){return d&&!isNaN(d.getTime())}_onKeydown(e){if(this._noInput){var allowedKeys=[9];if(-1===allowedKeys.indexOf(e.keyCode)){e.preventDefault()}}switch(this._eventKey(e)){case"down":case"up":e.preventDefault();if(this.opened){this._overlayContent.focus();this._overlayContent._onKeydown(e)}else{this._focusOverlayOnOpen=!0;this.open()}break;case"enter":if(this._overlayContent.focusedDate){this._selectedDate=this._overlayContent.focusedDate}this.close();break;case"esc":this._focusedDate=this._selectedDate;this._close();break;case"tab":if(this.opened){e.preventDefault();this._setSelectionRange(0,0);if(e.shiftKey){this._overlayContent.focusCancel()}else{this._overlayContent.focus();this._overlayContent.revealDate(this._focusedDate)}}break;}}_validateInput(date,min,max){if(date&&(min||max)){this.invalid=!DatePickerHelper._dateAllowed(date,min,max)}}_onUserInput(e){if(!this.opened){this.open()}this._userInputValueChanged()}_userInputValueChanged(value){if(this.opened&&this._inputValue){const dateObject=this.i18n.parseDate&&this.i18n.parseDate(this._inputValue),parsedDate=dateObject&&this._parseDate(`${dateObject.year}-${dateObject.month+1}-${dateObject.day}`);if(this._isValidDate(parsedDate)){this._ignoreFocusedDateChange=!0;if(!DatePickerHelper._dateEquals(parsedDate,this._focusedDate)){this._focusedDate=parsedDate}this._ignoreFocusedDateChange=!1}}}_announceFocusedDate(_focusedDate,opened,_ignoreAnnounce){if(opened&&!_ignoreAnnounce){this._overlayContent.announceFocusedDate()}}get _overlayContent(){return this.$.overlay.content.querySelector("#overlay-content")}};/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_date_picker_DatePickerElement extends ElementMixin(ControlStateMixin(Object(vaadin_themable_mixin.a)(Object(vaadin_theme_property_mixin.a)(DatePickerMixin(Object(gesture_event_listeners.a)(polymer_element.a)))))){static get template(){return html_tag.a`
    <style>
      :host {
        display: inline-block;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host([opened]) {
        pointer-events: auto;
      }

      [part="text-field"] {
        width: 100%;
        min-width: 0;
      }

      [part="clear-button"],
      [part="toggle-button"] {
        font-family: 'vaadin-date-picker-icons';
      }

      [part="clear-button"]::before {
        content: "\\e901";
      }

      [part="toggle-button"]::before {
        content: "\\e902";
      }

      :host([disabled]) [part="clear-button"],
      :host([readonly]) [part="clear-button"],
      :host(:not([has-value])) [part="clear-button"] {
        display: none;
      }
    </style>


    <vaadin-text-field id="input" role="application" autocomplete="off" on-focus="_focus" value="{{_userInputValue}}" invalid="[[invalid]]" label="[[label]]" name="[[name]]" placeholder="[[placeholder]]" required="[[required]]" disabled="[[disabled]]" readonly="[[readonly]]" error-message="[[errorMessage]]" aria-label\$="[[label]]" part="text-field" theme\$="[[theme]]">
      <slot name="prefix" slot="prefix"></slot>
      <div part="clear-button" slot="suffix" on-touchend="_clearTouchend" on-click="_clear" role="button" aria-label\$="[[i18n.clear]]"></div>
      <div part="toggle-button" slot="suffix" on-tap="_toggle" role="button" aria-label\$="[[i18n.calendar]]" aria-expanded\$="[[_getAriaExpanded(opened)]]"></div>
    </vaadin-text-field>

    <vaadin-date-picker-overlay id="overlay" opened="{{opened}}" fullscreen\$="[[_fullscreen]]" theme\$="[[theme]]" on-vaadin-overlay-open="_onOverlayOpened" on-vaadin-overlay-close="_onOverlayClosed">
      <template>
        <vaadin-date-picker-overlay-content id="overlay-content" i18n="[[i18n]]" fullscreen\$="[[_fullscreen]]" label="[[label]]" selected-date="{{_selectedDate}}" slot="dropdown-content" focused-date="{{_focusedDate}}" show-week-numbers="[[showWeekNumbers]]" min-date="[[_minDate]]" max-date="[[_maxDate]]" role="dialog" on-date-tap="_close" part="overlay-content" theme\$="[[theme]]">
        </vaadin-date-picker-overlay-content>
      </template>
    </vaadin-date-picker-overlay>

    <iron-media-query query="[[_fullscreenMediaQuery]]" query-matches="{{_fullscreen}}">
    </iron-media-query>
`}static get is(){return"vaadin-date-picker"}static get version(){return"3.3.1"}static get properties(){return{disabled:{type:Boolean,value:!1,reflectToAttribute:!0},errorMessage:String,placeholder:String,readonly:{type:Boolean,value:!1,reflectToAttribute:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},_userInputValue:String}}static get observers(){return["_userInputValueChanged(_userInputValue)"]}ready(){super.ready();Object(render_status.a)(this,()=>this._inputElement.validate=()=>{});this._overlayContent.addEventListener("focus",()=>this.focusElement._setFocused(!0));this.$.overlay.addEventListener("vaadin-overlay-close",this._onVaadinOverlayClose.bind(this))}_onVaadinOverlayClose(e){if(this._openedWithFocusRing&&this.hasAttribute("focused")){this.focusElement.setAttribute("focus-ring","")}else if(!this.hasAttribute("focused")){this.focusElement.blur()}if(e.detail.sourceEvent&&-1!==e.detail.sourceEvent.composedPath().indexOf(this)){e.preventDefault()}}_clear(){this.__dispatchChange=!0;this.value="";this.validate();this.focus();Object(gestures.d)("tap");this.__dispatchChange=!1}_clearTouchend(e){this._clear();e.preventDefault();Object(gestures.d)("tap")}_toggle(e){e.stopPropagation();this[this.$.overlay.opened?"close":"open"]()}_input(){return this.$.input}set _inputValue(value){this._inputElement.value=value}get _inputValue(){return this._inputElement.value}_getAriaExpanded(opened){return(!!opened).toString()}get focusElement(){return this._input()||this}}customElements.define(vaadin_date_picker_DatePickerElement.is,vaadin_date_picker_DatePickerElement)},338:function(module,exports){const documentContainer=document.createElement("template");documentContainer.setAttribute("style","display: none;");documentContainer.innerHTML=`<dom-module id="ha-date-picker-vaadin-date-picker-styles" theme-for="vaadin-date-picker">
  <template>
    <style>
      :host([required]) [part~="clear-button"] {
        display: none;
      }

      [part~="toggle-button"] {
        color: var(--secondary-text-color);
        font-size: var(--paper-font-subhead_-_font-size);
        margin-right: 5px;
      }

      :host([opened]) [part~="toggle-button"] {
        color: var(--primary-color);
      }
    </style>
  </template>
</dom-module><dom-module id="ha-date-picker-text-field-styles" theme-for="vaadin-text-field">
  <template>
    <style>
      :host {
        padding: 8px 0;
      }

      [part~="label"] {
        color: var(--paper-input-container-color, var(--secondary-text-color));
        font-family: var(--paper-font-caption_-_font-family);
        font-size: var(--paper-font-caption_-_font-size);
        font-weight: var(--paper-font-caption_-_font-weight);
        letter-spacing: var(--paper-font-caption_-_letter-spacing);
        line-height: var(--paper-font-caption_-_line-height);
      }
      :host([focused]) [part~="label"] {
          color: var(--paper-input-container-focus-color, var(--primary-color));
      }

      [part~="input-field"] {
        padding-bottom: 1px;
        border-bottom: 1px solid var(--paper-input-container-color, var(--secondary-text-color));
        line-height: var(--paper-font-subhead_-_line-height);
      }

      :host([focused]) [part~="input-field"] {
        padding-bottom: 0;
        border-bottom: 2px solid var(--paper-input-container-focus-color, var(--primary-color));
      }
      [part~="value"]:focus {
        outline: none;
      }

      [part~="value"] {
        font-size: var(--paper-font-subhead_-_font-size);
        font-family: inherit;
        color: inherit;
        border: none;
        background: transparent;
      }
    </style>
  </template>
</dom-module><dom-module id="ha-date-picker-button-styles" theme-for="vaadin-button">
  <template>
    <style>
      :host([part~="today-button"]) [part~="button"]::before {
        content: "⦿";
        color: var(--primary-color);
      }

      [part~="button"] {
        font-family: inherit;
        font-size: var(--paper-font-subhead_-_font-size);
        border: none;
        background: transparent;
        cursor: pointer;
        min-height: var(--paper-item-min-height, 48px);
        padding: 0px 16px;
        color: inherit;
      }

      [part~="button"]:focus {
        outline: none;
      }
    </style>
  </template>
</dom-module><dom-module id="ha-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">
  <template>
    <style include="vaadin-date-picker-overlay-default-theme">
      :host {
        background-color: var(--paper-card-background-color, var(--primary-background-color));
      }

      [part~="toolbar"] {
        padding: 0.3em;
        background-color: var(--secondary-background-color);
      }

      [part="years"] {
        background-color: var(--paper-grey-200);
      }

    </style>
  </template>
</dom-module><dom-module id="ha-date-picker-month-styles" theme-for="vaadin-month-calendar">
  <template>
    <style include="vaadin-month-calendar-default-theme">
      :host([focused]) [part="date"][focused],
      [part="date"][selected] {
        background-color: var(--paper-grey-200);
      }
      [part="date"][today] {
        color: var(--primary-color);
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(documentContainer.content)},777:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var app_header_layout=__webpack_require__(178),app_header=__webpack_require__(172),app_toolbar=__webpack_require__(127),paper_icon_button=__webpack_require__(94),paper_input=__webpack_require__(78),paper_spinner=__webpack_require__(163),html_tag=__webpack_require__(2),polymer_element=__webpack_require__(13),vaadin_date_picker=__webpack_require__(304),ha_menu_button=__webpack_require__(131),ha_entity_picker=__webpack_require__(164),ha_date_picker_style=__webpack_require__(338),ha_style=__webpack_require__(97);const DATA_CACHE={},ALL_ENTITIES="*";class ha_logbook_data_HaLogbookData extends polymer_element.a{static get properties(){return{hass:{type:Object,observer:"hassChanged"},filterDate:{type:String,observer:"filterDataChanged"},filterPeriod:{type:Number,observer:"filterDataChanged"},filterEntity:{type:String,observer:"filterDataChanged"},isLoading:{type:Boolean,value:!0,readOnly:!0,notify:!0},entries:{type:Object,value:null,readOnly:!0,notify:!0}}}hassChanged(newHass,oldHass){if(!oldHass&&this.filterDate){this.updateData()}}filterDataChanged(newValue,oldValue){if(oldValue!==void 0){this.updateData()}}updateData(){if(!this.hass)return;this._setIsLoading(!0);this.getDate(this.filterDate,this.filterPeriod,this.filterEntity).then(logbookEntries=>{this._setEntries(logbookEntries);this._setIsLoading(!1)})}getDate(date,period,entityId){if(!entityId)entityId=ALL_ENTITIES;if(!DATA_CACHE[period])DATA_CACHE[period]=[];if(!DATA_CACHE[period][date])DATA_CACHE[period][date]=[];if(DATA_CACHE[period][date][entityId]){return DATA_CACHE[period][date][entityId]}if(entityId!==ALL_ENTITIES&&DATA_CACHE[period][date][ALL_ENTITIES]){return DATA_CACHE[period][date][ALL_ENTITIES].then(function(entities){return entities.filter(function(entity){return entity.entity_id===entityId})})}DATA_CACHE[period][date][entityId]=this._getFromServer(date,period,entityId);return DATA_CACHE[period][date][entityId]}_getFromServer(date,period,entityId){let url="logbook/"+date+"?period="+period;if(entityId!==ALL_ENTITIES){url+="&entity="+entityId}return this.hass.callApi("GET",url).then(function(logbookEntries){logbookEntries.reverse();return logbookEntries},function(){return null})}refreshLogbook(){DATA_CACHE[this.filterPeriod][this.filterDate]=[];this.updateData()}}customElements.define("ha-logbook-data",ha_logbook_data_HaLogbookData);var iron_flex_layout_classes=__webpack_require__(123),iron_icon=__webpack_require__(92),format_time=__webpack_require__(193),format_date=__webpack_require__(212),events_mixin=__webpack_require__(59),domain_icon=__webpack_require__(154),compute_rtl=__webpack_require__(82);class ha_logbook_HaLogbook extends Object(events_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
      <style include="iron-flex"></style>
      <style>
        :host {
          display: block;
        }

        :host([rtl]) {
          direction: ltr;
        }

        .entry {
          @apply --paper-font-body1;
          line-height: 2em;
        }

        .time {
          width: 55px;
          font-size: 0.8em;
          color: var(--secondary-text-color);
        }

        :host([rtl]) .date {
          direction: rtl;
        }

        iron-icon {
          margin: 0 8px 0 16px;
          color: var(--primary-text-color);
        }

        .message {
          color: var(--primary-text-color);
        }

        a {
          color: var(--primary-color);
        }
      </style>

      <template is="dom-if" if="[[!entries.length]]">
        No logbook entries found.
      </template>

      <template is="dom-repeat" items="[[entries]]">
        <template is="dom-if" if="{{_needHeader(entries.*, index)}}">
          <h4 class="date">[[_formatDate(item.when)]]</h4>
        </template>

        <div class="horizontal layout entry">
          <div class="time">[[_formatTime(item.when)]]</div>
          <iron-icon icon="[[_computeIcon(item.domain)]]"></iron-icon>
          <div class="message" flex="">
            <template is="dom-if" if="[[!item.entity_id]]">
              <span class="name">[[item.name]]</span>
            </template>
            <template is="dom-if" if="[[item.entity_id]]">
              <a href="#" on-click="entityClicked" class="name"
                >[[item.name]]</a
              >
            </template>
            <span> </span> <span>[[item.message]]</span>
          </div>
        </div>
      </template>
    `}static get properties(){return{hass:{type:Object},entries:{type:Array,value:[]},rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}_formatTime(date){return Object(format_time.a)(new Date(date),this.hass.language)}_formatDate(date){return Object(format_date.a)(new Date(date),this.hass.language)}_needHeader(change,index){if(!index)return!0;const current=this.get("when",change.base[index]),previous=this.get("when",change.base[index-1]);return current&&previous&&new Date(current).toDateString()!==new Date(previous).toDateString()}_computeIcon(domain){return Object(domain_icon.a)(domain)}_computeRTL(hass){return Object(compute_rtl.a)(hass)}entityClicked(ev){ev.preventDefault();this.fire("hass-more-info",{entityId:ev.model.item.entity_id})}}customElements.define("ha-logbook",ha_logbook_HaLogbook);var localize_mixin=__webpack_require__(102);class ha_panel_logbook_HaPanelLogbook extends Object(localize_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
      <style include="ha-style">
        .content {
          padding: 0 16px 16px;
        }

        paper-spinner {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        .wrap {
          margin-bottom: 24px;
        }

        vaadin-date-picker {
          --vaadin-date-picker-clear-icon: {
            display: none;
          }
          max-width: 200px;
          margin-right: 16px;
        }

        paper-dropdown-menu {
          max-width: 100px;
          margin-right: 16px;
          --paper-input-container-label-floating: {
            padding-bottom: 10px;
          }
        }

        :host([rtl]) paper-dropdown-menu {
          text-align: right;
        }

        paper-item {
          cursor: pointer;
        }

        ha-entity-picker {
          display: inline-block;
          width: 100%;
          max-width: 400px;
        }

        [hidden] {
          display: none !important;
        }
      </style>

      <ha-logbook-data
        hass="[[hass]]"
        is-loading="{{isLoading}}"
        entries="{{entries}}"
        filter-date="[[_computeFilterDate(_currentDate)]]"
        filter-period="[[_computeFilterDays(_periodIndex)]]"
        filter-entity="[[entityId]]"
      ></ha-logbook-data>

      <app-header-layout has-scrolling-region>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button
              narrow="[[narrow]]"
              show-menu="[[showMenu]]"
            ></ha-menu-button>
            <div main-title>[[localize('panel.logbook')]]</div>
            <paper-icon-button
              icon="hass:refresh"
              on-click="refreshLogbook"
              hidden$="[[isLoading]]"
            ></paper-icon-button>
          </app-toolbar>
        </app-header>

        <div class="content">
          <paper-spinner
            active="[[isLoading]]"
            hidden$="[[!isLoading]]"
            alt="[[localize('ui.common.loading')]]"
          ></paper-spinner>

          <div class="flex layout horizontal wrap">
            <vaadin-date-picker
              id="picker"
              value="{{_currentDate}}"
              label="[[localize('ui.panel.logbook.showing_entries')]]"
              disabled="[[isLoading]]"
              required
            ></vaadin-date-picker>

            <paper-dropdown-menu
              label-float
              label="[[localize('ui.panel.logbook.period')]]"
              disabled="[[isLoading]]"
            >
              <paper-listbox
                slot="dropdown-content"
                selected="{{_periodIndex}}"
              >
                <paper-item
                  >[[localize('ui.duration.day', 'count', 1)]]</paper-item
                >
                <paper-item
                  >[[localize('ui.duration.day', 'count', 3)]]</paper-item
                >
                <paper-item
                  >[[localize('ui.duration.week', 'count', 1)]]</paper-item
                >
              </paper-listbox>
            </paper-dropdown-menu>

            <ha-entity-picker
              hass="[[hass]]"
              value="{{_entityId}}"
              label="[[localize('ui.components.entity.entity-picker.entity')]]"
              disabled="[[isLoading]]"
              on-change="_entityPicked"
            ></ha-entity-picker>
          </div>

          <ha-logbook
            hass="[[hass]]"
            entries="[[entries]]"
            hidden$="[[isLoading]]"
          ></ha-logbook>
        </div>
      </app-header-layout>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean,value:!1},showMenu:{type:Boolean,value:!1},_currentDate:{type:String,value:function(){const value=new Date,today=new Date(Date.UTC(value.getFullYear(),value.getMonth(),value.getDate()));return today.toISOString().split("T")[0]}},_periodIndex:{type:Number,value:0},_entityId:{type:String,value:""},entityId:{type:String,value:"",readOnly:!0},isLoading:{type:Boolean},entries:{type:Array},datePicker:{type:Object},rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}connectedCallback(){super.connectedCallback();this.$.picker.set("i18n.parseDate",null);this.$.picker.set("i18n.formatDate",date=>Object(format_date.a)(new Date(date.year,date.month,date.day),this.hass.language))}_computeFilterDate(_currentDate){if(!_currentDate)return;var parts=_currentDate.split("-");parts[1]=parseInt(parts[1])-1;return new Date(parts[0],parts[1],parts[2]).toISOString()}_computeFilterDays(periodIndex){switch(periodIndex){case 1:return 3;case 2:return 7;default:return 1;}}_entityPicked(ev){this._setEntityId(ev.target.value)}refreshLogbook(){this.shadowRoot.querySelector("ha-logbook-data").refreshLogbook()}_computeRTL(hass){return Object(compute_rtl.a)(hass)}}customElements.define("ha-panel-logbook",ha_panel_logbook_HaPanelLogbook)},78:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_input_iron_input_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(98),_paper_input_char_counter_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(99),_paper_input_container_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(100),_paper_input_error_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(101),_polymer_iron_form_element_behavior_iron_form_element_behavior_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(52),_polymer_polymer_lib_elements_dom_module_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(33),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(2),_paper_input_behavior_js__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(80);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_7__.a)({is:"paper-input",_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_8__.a`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate\$="[[autoValidate]]" disabled\$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden\$="[[!label]]" aria-hidden="true" for\$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id\$="[[_inputId]]" maxlength\$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby\$="[[_ariaLabelledBy]]" aria-describedby\$="[[_ariaDescribedBy]]" disabled\$="[[disabled]]" title\$="[[title]]" type\$="[[type]]" pattern\$="[[pattern]]" required\$="[[required]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]" min\$="[[min]]" max\$="[[max]]" step\$="[[step]]" name\$="[[name]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" list\$="[[list]]" size\$="[[size]]" autocapitalize\$="[[autocapitalize]]" autocorrect\$="[[autocorrect]]" on-change="_onChange" tabindex\$="[[tabIndex]]" autosave\$="[[autosave]]" results\$="[[results]]" accept\$="[[accept]]" multiple\$="[[multiple]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[_paper_input_behavior_js__WEBPACK_IMPORTED_MODULE_9__.a,_polymer_iron_form_element_behavior_iron_form_element_behavior_js__WEBPACK_IMPORTED_MODULE_5__.a],properties:{value:{type:String}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){if(!this.$.nativeInput){this.$.nativeInput=this.$$("input")}if(this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)){this.alwaysFloatLabel=!0}if(!!this.inputElement.bindValue){this.$.container._handleValueAndAutoValidate(this.inputElement)}}})},79:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return IronA11yAnnouncer});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(2);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const IronA11yAnnouncer=Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_1__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_2__.a`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live\$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},_text:{type:String,value:""}},created:function(){if(!IronA11yAnnouncer.instance){IronA11yAnnouncer.instance=this}document.body.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(text){this._text="";this.async(function(){this._text=text},100)},_onIronAnnounce:function(event){if(event.detail&&event.detail.text){this.announce(event.detail.text)}}});IronA11yAnnouncer.instance=null;IronA11yAnnouncer.requestAvailability=function(){if(!IronA11yAnnouncer.instance){IronA11yAnnouncer.instance=document.createElement("iron-a11y-announcer")}document.body.appendChild(IronA11yAnnouncer.instance)}},98:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_a11y_announcer_iron_a11y_announcer_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(79),_polymer_iron_validatable_behavior_iron_validatable_behavior_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(53),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(0),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(2);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[_polymer_iron_validatable_behavior_iron_validatable_behavior_js__WEBPACK_IMPORTED_MODULE_2__.a],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){_polymer_iron_a11y_announcer_iron_a11y_announcer_js__WEBPACK_IMPORTED_MODULE_1__.a.requestAvailability();this._previousValidInput="";this._patternAlreadyChecked=!1},attached:function(){this._observer=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_4__.b)(this).observeNodes(function(info){this._initSlottedInput()}.bind(this))},detached:function(){if(this._observer){Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_4__.b)(this).unobserveNodes(this._observer);this._observer=null}},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0];if(this.inputElement&&this.inputElement.value){this.bindValue=this.inputElement.value}this.fire("iron-input-ready")},get _patternRegExp(){var pattern;if(this.allowedPattern){pattern=new RegExp(this.allowedPattern)}else{switch(this.inputElement.type){case"number":pattern=/[0-9.,e-]/;break;}}return pattern},_bindValueChanged:function(bindValue,inputElement){if(!inputElement){return}if(bindValue===void 0){inputElement.value=null}else if(bindValue!==inputElement.value){this.inputElement.value=bindValue}if(this.autoValidate){this.validate()}this.fire("bind-value-changed",{value:bindValue})},_onInput:function(){if(this.allowedPattern&&!this._patternAlreadyChecked){var valid=this._checkPatternValidity();if(!valid){this._announceInvalidCharacter("Invalid string of characters not entered.");this.inputElement.value=this._previousValidInput}}this.bindValue=this._previousValidInput=this.inputElement.value;this._patternAlreadyChecked=!1},_isPrintable:function(event){var anyNonPrintable=8==event.keyCode||9==event.keyCode||13==event.keyCode||27==event.keyCode,mozNonPrintable=19==event.keyCode||20==event.keyCode||45==event.keyCode||46==event.keyCode||144==event.keyCode||145==event.keyCode||32<event.keyCode&&41>event.keyCode||111<event.keyCode&&124>event.keyCode;return!anyNonPrintable&&!(0==event.charCode&&mozNonPrintable)},_onKeypress:function(event){if(!this.allowedPattern&&"number"!==this.inputElement.type){return}var regexp=this._patternRegExp;if(!regexp){return}if(event.metaKey||event.ctrlKey||event.altKey){return}this._patternAlreadyChecked=!0;var thisChar=String.fromCharCode(event.charCode);if(this._isPrintable(event)&&!regexp.test(thisChar)){event.preventDefault();this._announceInvalidCharacter("Invalid character "+thisChar+" not entered.")}},_checkPatternValidity:function(){var regexp=this._patternRegExp;if(!regexp){return!0}for(var i=0;i<this.inputElement.value.length;i++){if(!regexp.test(this.inputElement.value[i])){return!1}}return!0},validate:function(){if(!this.inputElement){this.invalid=!1;return!0}var valid=this.inputElement.checkValidity();if(valid){if(this.required&&""===this.bindValue){valid=!1}else if(this.hasValidator()){valid=_polymer_iron_validatable_behavior_iron_validatable_behavior_js__WEBPACK_IMPORTED_MODULE_2__.a.validate.call(this,this.bindValue)}}this.invalid=!valid;this.fire("iron-input-validate");return valid},_announceInvalidCharacter:function(message){this.fire("iron-announce",{text:message})},_computeValue:function(bindValue){return bindValue}})}}]);
//# sourceMappingURL=ec51e753b770c78cab4d.chunk.js.map