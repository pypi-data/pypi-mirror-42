(window.webpackJsonp=window.webpackJsonp||[]).push([[21],{113:function(module,__webpack_exports__,__webpack_require__){"use strict";var polymer_legacy=__webpack_require__(3),iron_form_element_behavior=__webpack_require__(52),iron_validatable_behavior=__webpack_require__(53);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const IronCheckedElementBehaviorImpl={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(_value){return this.disabled||!this.required||this.checked},_requiredChanged:function(){if(this.required){this.setAttribute("aria-required","true")}else{this.removeAttribute("aria-required")}},_checkedChanged:function(){this.active=this.checked;this.fire("iron-change")},_valueChanged:function(){if(this.value===void 0||null===this.value){this.value="on"}}},IronCheckedElementBehavior=[iron_form_element_behavior.a,iron_validatable_behavior.a,IronCheckedElementBehaviorImpl];var paper_inky_focus_behavior=__webpack_require__(51),paper_ripple_behavior=__webpack_require__(62);__webpack_require__.d(__webpack_exports__,"a",function(){return PaperCheckedElementBehavior});/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const PaperCheckedElementBehaviorImpl={_checkedChanged:function(){IronCheckedElementBehaviorImpl._checkedChanged.call(this);if(this.hasRipple()){if(this.checked){this._ripple.setAttribute("checked","")}else{this._ripple.removeAttribute("checked")}}},_buttonStateChanged:function(){paper_ripple_behavior.a._buttonStateChanged.call(this);if(this.disabled){return}if(this.isAttached){this.checked=this.active}}},PaperCheckedElementBehavior=[paper_inky_focus_behavior.a,IronCheckedElementBehavior,PaperCheckedElementBehaviorImpl]},145:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_slider_paper_slider__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(143);const PaperSliderClass=customElements.get("paper-slider");class HaPaperSlider extends PaperSliderClass{static get template(){const tpl=document.createElement("template");tpl.innerHTML=PaperSliderClass.template.innerHTML;const styleEl=document.createElement("style");styleEl.innerHTML=`
      .pin > .slider-knob > .slider-knob-inner {
        font-size:  var(--ha-paper-slider-pin-font-size, 10px);
        line-height: normal;
      }

      .pin > .slider-knob > .slider-knob-inner::before {
        top: unset;
        margin-left: unset;

        bottom: calc(15px + var(--calculated-paper-slider-height)/2);
        left: 50%;
        width: 2.2em;
        height: 2.2em;

        -webkit-transform-origin: left bottom;
        transform-origin: left bottom;
        -webkit-transform: rotate(-45deg) scale(0) translate(0);
        transform: rotate(-45deg) scale(0) translate(0);
      }

      .pin.expand > .slider-knob > .slider-knob-inner::before {
        -webkit-transform: rotate(-45deg) scale(1) translate(7px, -7px);
        transform: rotate(-45deg) scale(1) translate(7px, -7px);
      }

      .pin > .slider-knob > .slider-knob-inner::after {
        top: unset;
        font-size: unset;

        bottom: calc(15px + var(--calculated-paper-slider-height)/2);
        left: 50%;
        margin-left: -1.1em;
        width: 2.2em;
        height: 2.1em;

        -webkit-transform-origin: center bottom;
        transform-origin: center bottom;
        -webkit-transform: scale(0) translate(0);
        transform: scale(0) translate(0);
      }

      .pin.expand > .slider-knob > .slider-knob-inner::after {
        -webkit-transform: scale(1) translate(0, -10px);
        transform: scale(1) translate(0, -10px);
      }
    `;tpl.content.appendChild(styleEl);return tpl}}customElements.define("ha-paper-slider",HaPaperSlider)},147:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_checkbox_paper_checkbox__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(140),_polymer_paper_dropdown_menu_paper_dropdown_menu__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(132),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(96),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(81),_polymer_paper_item_paper_item__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(129),_polymer_paper_listbox_paper_listbox__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(131),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(2),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(18),_ha_paper_slider__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(145),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(60);class HaForm extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_7__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_6__.a`
      <style>
        .error {
          color: red;
        }
        paper-checkbox {
          display: inline-block;
          padding: 22px 0;
        }
      </style>
      <template is="dom-if" if="[[_isArray(schema)]]" restamp="">
        <template is="dom-if" if="[[error.base]]">
          <div class="error">[[computeError(error.base, schema)]]</div>
        </template>

        <template is="dom-repeat" items="[[schema]]">
          <ha-form
            data="[[_getValue(data, item)]]"
            schema="[[item]]"
            error="[[_getValue(error, item)]]"
            on-data-changed="_valueChanged"
            compute-label="[[computeLabel]]"
            compute-error="[[computeError]]"
          ></ha-form>
        </template>
      </template>
      <template is="dom-if" if="[[!_isArray(schema)]]" restamp="">
        <template is="dom-if" if="[[error]]">
          <div class="error">[[computeError(error, schema)]]</div>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "string")]]'
          restamp=""
        >
          <template
            is="dom-if"
            if='[[_includes(schema.name, "password")]]'
            restamp=""
          >
            <paper-input
              type="[[_passwordFieldType(unmaskedPassword)]]"
              label="[[computeLabel(schema)]]"
              value="{{data}}"
              required="[[schema.required]]"
              auto-validate="[[schema.required]]"
              error-message="Required"
            >
              <paper-icon-button
                toggles
                active="{{unmaskedPassword}}"
                slot="suffix"
                icon="[[_passwordFieldIcon(unmaskedPassword)]]"
                id="iconButton"
                title="Click to toggle between masked and clear password"
              >
              </paper-icon-button>
            </paper-input>
          </template>
          <template
            is="dom-if"
            if='[[!_includes(schema.name, "password")]]'
            restamp=""
          >
            <paper-input
              label="[[computeLabel(schema)]]"
              value="{{data}}"
              required="[[schema.required]]"
              auto-validate="[[schema.required]]"
              error-message="Required"
            ></paper-input>
          </template>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "integer")]]'
          restamp=""
        >
          <template is="dom-if" if="[[_isRange(schema)]]" restamp="">
            <div>
              [[computeLabel(schema)]]
              <ha-paper-slider
                pin=""
                value="{{data}}"
                min="[[schema.valueMin]]"
                max="[[schema.valueMax]]"
              ></ha-paper-slider>
            </div>
          </template>
          <template is="dom-if" if="[[!_isRange(schema)]]" restamp="">
            <paper-input
              label="[[computeLabel(schema)]]"
              value="{{data}}"
              type="number"
              required="[[schema.required]]"
              auto-validate="[[schema.required]]"
              error-message="Required"
            ></paper-input>
          </template>
        </template>

        <template is="dom-if" if='[[_equals(schema.type, "float")]]' restamp="">
          <!-- TODO -->
          <paper-input
            label="[[computeLabel(schema)]]"
            value="{{data}}"
            required="[[schema.required]]"
            auto-validate="[[schema.required]]"
            error-message="Required"
          ></paper-input>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "boolean")]]'
          restamp=""
        >
          <div>
            <paper-checkbox checked="{{data}}"
              >[[computeLabel(schema)]]</paper-checkbox
            >
          </div>
        </template>

        <template
          is="dom-if"
          if='[[_equals(schema.type, "select")]]'
          restamp=""
        >
          <paper-dropdown-menu label="[[computeLabel(schema)]]">
            <paper-listbox
              slot="dropdown-content"
              attr-for-selected="item-name"
              selected="{{data}}"
            >
              <template is="dom-repeat" items="[[schema.options]]">
                <paper-item item-name$="[[_optionValue(item)]]"
                  >[[_optionLabel(item)]]</paper-item
                >
              </template>
            </paper-listbox>
          </paper-dropdown-menu>
        </template>
      </template>
    `}static get properties(){return{data:{type:Object,notify:!0},schema:Object,error:Object,computeLabel:{type:Function,value:()=>schema=>schema&&schema.name},computeError:{type:Function,value:()=>(error,schema)=>error}}}_isArray(val){return Array.isArray(val)}_isRange(schema){return"valueMin"in schema&&"valueMax"in schema}_equals(a,b){return a===b}_includes(a,b){return 0<=a.indexOf(b)}_getValue(obj,item){if(obj){return obj[item.name]}return null}_valueChanged(ev){let value=ev.detail.value;if("integer"===ev.model.item.type){value=+ev.detail.value}this.set(["data",ev.model.item.name],value)}_passwordFieldType(unmaskedPassword){return unmaskedPassword?"text":"password"}_passwordFieldIcon(unmaskedPassword){return unmaskedPassword?"hass:eye-off":"hass:eye"}_optionValue(item){return Array.isArray(item)?item[0]:item}_optionLabel(item){return Array.isArray(item)?item[1]:item}}customElements.define("ha-form",HaForm)},174:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(61),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__),_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(139),_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2__),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(2),_paper_spinner_behavior_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(115);/**
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
`;template.setAttribute("strip-whitespace","");Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__.a)({_template:template,is:"paper-spinner",behaviors:[_paper_spinner_behavior_js__WEBPACK_IMPORTED_MODULE_5__.a]})},176:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"b",function(){return PaperDialogBehaviorImpl});__webpack_require__.d(__webpack_exports__,"a",function(){return PaperDialogBehavior});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(75),_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(0);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const PaperDialogBehaviorImpl={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.__readied=!0},_modalChanged:function(modal,readied){if(!readied){return}if(modal){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.noCancelOnOutsideClick=!0;this.noCancelOnEscKey=!0;this.withBackdrop=!0}else{this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick;this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey;this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop}},_updateClosingReasonConfirmed:function(confirmed){this.closingReason=this.closingReason||{};this.closingReason.confirmed=confirmed},_onDialogClick:function(event){for(var path=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(event).path,i=0,l=path.indexOf(this),target;i<l;i++){target=path[i];if(target.hasAttribute&&(target.hasAttribute("dialog-dismiss")||target.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(target.hasAttribute("dialog-confirm"));this.close();event.stopPropagation();break}}}},PaperDialogBehavior=[_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__.a,PaperDialogBehaviorImpl]},181:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(40),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(41),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(50),_polymer_paper_styles_shadow_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(98);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const $_documentContainer=document.createElement("template");$_documentContainer.setAttribute("style","display: none;");$_documentContainer.innerHTML=`<dom-module id="paper-dialog-shared-styles">
  <template>
    <style>
      :host {
        display: block;
        margin: 24px 40px;

        background: var(--paper-dialog-background-color, var(--primary-background-color));
        color: var(--paper-dialog-color, var(--primary-text-color));

        @apply --paper-font-body1;
        @apply --shadow-elevation-16dp;
        @apply --paper-dialog;
      }

      :host > ::slotted(*) {
        margin-top: 20px;
        padding: 0 24px;
      }

      :host > ::slotted(.no-padding) {
        padding: 0;
      }

      
      :host > ::slotted(*:first-child) {
        margin-top: 24px;
      }

      :host > ::slotted(*:last-child) {
        margin-bottom: 24px;
      }

      /* In 1.x, this selector was \`:host > ::content h2\`. In 2.x <slot> allows
      to select direct children only, which increases the weight of this
      selector, so we have to re-define first-child/last-child margins below. */
      :host > ::slotted(h2) {
        position: relative;
        margin: 0;

        @apply --paper-font-title;
        @apply --paper-dialog-title;
      }

      /* Apply mixin again, in case it sets margin-top. */
      :host > ::slotted(h2:first-child) {
        margin-top: 24px;
        @apply --paper-dialog-title;
      }

      /* Apply mixin again, in case it sets margin-bottom. */
      :host > ::slotted(h2:last-child) {
        margin-bottom: 24px;
        @apply --paper-dialog-title;
      }

      :host > ::slotted(.paper-dialog-buttons),
      :host > ::slotted(.buttons) {
        position: relative;
        padding: 8px 8px 8px 24px;
        margin: 0;

        color: var(--paper-dialog-button-color, var(--primary-color));

        @apply --layout-horizontal;
        @apply --layout-end-justified;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content)},184:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_paper_dialog_behavior_paper_dialog_shared_styles_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(181),_polymer_neon_animation_neon_animation_runner_behavior_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(111),_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(176),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(2);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__.a,_polymer_neon_animation_neon_animation_runner_behavior_js__WEBPACK_IMPORTED_MODULE_2__.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation();this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation();this.playAnimation("exit")},_onNeonAnimationFinish:function(){if(this.opened){this._finishRenderOpened()}else{this._finishRenderClosed()}}})},191:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(40),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(41),_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(176),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(2);/**
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
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget();this.classList.add("no-padding")},attached:function(){this._ensureTarget();requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",0<this.scrollTarget.scrollTop);this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight);this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement;if(this.dialogElement&&this.dialogElement.behaviors&&0<=this.dialogElement.behaviors.indexOf(_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__.b)){this.dialogElement.sizingTarget=this.scrollTarget;this.scrollTarget.classList.remove("fit")}else if(this.dialogElement){this.scrollTarget.classList.add("fit")}}})},223:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(18),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(60);let loaded=null;const svgWhiteList=["svg","path"];class HaMarkdown extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_1__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{content:{type:String,observer:"_render"},allowSvg:{type:Boolean,value:!1}}}connectedCallback(){super.connectedCallback();this._scriptLoaded=0;this._renderScheduled=!1;this._resize=()=>this.fire("iron-resize");if(!loaded){loaded=Promise.all([__webpack_require__.e(118),__webpack_require__.e(56)]).then(__webpack_require__.bind(null,277))}loaded.then(({marked,filterXSS})=>{this.marked=marked;this.filterXSS=filterXSS;this._scriptLoaded=1},()=>{this._scriptLoaded=2}).then(()=>this._render())}_render(){if(0===this._scriptLoaded||this._renderScheduled)return;this._renderScheduled=!0;Promise.resolve().then(()=>{this._renderScheduled=!1;if(1===this._scriptLoaded){this.innerHTML=this.filterXSS(this.marked(this.content,{gfm:!0,tables:!0,breaks:!0}),{onIgnoreTag:this.allowSvg?(tag,html)=>0<=svgWhiteList.indexOf(tag)?html:null:null});this._resize();const walker=document.createTreeWalker(this,1,null,!1);while(walker.nextNode()){const node=walker.currentNode;if("A"===node.tagName&&node.host!==document.location.host){node.target="_blank"}else if("IMG"===node.tagName){node.addEventListener("load",this._resize)}}}else if(2===this._scriptLoaded){this.innerText=this.content}})}}customElements.define("ha-markdown",HaMarkdown)},770:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _material_mwc_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(74),_polymer_paper_dialog_scrollable_paper_dialog_scrollable__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(191),_polymer_paper_dialog_paper_dialog__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(184),_polymer_paper_tooltip_paper_tooltip__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(244),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(174),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(2),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(18),_components_ha_form__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(147),_components_ha_markdown__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(223),_resources_ha_style__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(101),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(60),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(107);let instance=0;class HaConfigFlow extends Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_11__.a)(Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_6__.a)){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_5__.a`
      <style include="ha-style-dialog">
        .error {
          color: red;
        }
        paper-dialog {
          max-width: 500px;
        }
        ha-markdown {
          word-break: break-word;
        }
        ha-markdown a {
          color: var(--primary-color);
        }
        ha-markdown img:first-child:last-child {
          display: block;
          margin: 0 auto;
        }
        .init-spinner {
          padding: 10px 100px 34px;
          text-align: center;
        }
        .submit-spinner {
          margin-right: 16px;
        }
      </style>
      <paper-dialog
        id="dialog"
        with-backdrop=""
        opened="{{_opened}}"
        on-opened-changed="_openedChanged"
      >
        <h2>
          <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
            Aborted
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
            Success!
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
            [[_computeStepTitle(localize, _step)]]
          </template>
        </h2>
        <paper-dialog-scrollable>
          <template is="dom-if" if="[[_errorMsg]]">
            <div class="error">[[_errorMsg]]</div>
          </template>
          <template is="dom-if" if="[[!_step]]">
            <div class="init-spinner">
              <paper-spinner active></paper-spinner>
            </div>
          </template>
          <template is="dom-if" if="[[_step]]">
            <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
              <p>Created config for [[_step.title]]</p>
            </template>

            <template
              is="dom-if"
              if="[[_computeStepDescription(localize, _step)]]"
            >
              <ha-markdown
                content="[[_computeStepDescription(localize, _step)]]"
                allow-svg
              ></ha-markdown>
            </template>

            <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
              <ha-form
                data="{{_stepData}}"
                on-data-changed="_increaseCounter"
                schema="[[_step.data_schema]]"
                error="[[_step.errors]]"
                compute-label="[[_computeLabelCallback(localize, _step)]]"
                compute-error="[[_computeErrorCallback(localize, _step)]]"
              ></ha-form>
            </template>
          </template>
        </paper-dialog-scrollable>
        <div class="buttons">
          <template is="dom-if" if="[[_equals(_step.type, 'abort')]]">
            <mwc-button on-click="_flowDone">Close</mwc-button>
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'create_entry')]]">
            <mwc-button on-click="_flowDone">Close</mwc-button>
          </template>
          <template is="dom-if" if="[[_equals(_step.type, 'form')]]">
            <template is="dom-if" if="[[_loading]]">
              <div class="submit-spinner">
                <paper-spinner active></paper-spinner>
              </div>
            </template>
            <template is="dom-if" if="[[!_loading]]">
              <div>
                <mwc-button on-click="_submitStep" disabled="[[!_canSubmit]]"
                  >Submit</mwc-button
                >
                <template is="dom-if" if="[[!_canSubmit]]">
                  <paper-tooltip position="left">
                    Not all required fields are filled in.
                  </paper-tooltip>
                </template>
              </div>
            </template>
          </template>
        </div>
      </paper-dialog>
    `}static get properties(){return{_hass:Object,_dialogClosedCallback:Function,_instance:Number,_loading:{type:Boolean,value:!1},_errorMsg:String,_canSubmit:{type:Boolean,computed:"_computeCanSubmit(_step, _stepData, _counter)"},_counter:{type:Number,value:0},_opened:{type:Boolean,value:!1},_step:{type:Object,value:null},_stepData:{type:Object,value:null}}}ready(){super.ready();this.addEventListener("keypress",ev=>{if(13===ev.keyCode){this._submitStep()}})}showDialog({hass,continueFlowId,newFlowForHandler,dialogClosedCallback}){this.hass=hass;this._instance=instance++;this._dialogClosedCallback=dialogClosedCallback;this._createdFromHandler=!!newFlowForHandler;this._loading=!0;this._opened=!0;const fetchStep=continueFlowId?this.hass.callApi("get",`config/config_entries/flow/${continueFlowId}`):this.hass.callApi("post","config/config_entries/flow",{handler:newFlowForHandler}),curInstance=this._instance;fetchStep.then(step=>{if(curInstance!==this._instance)return;this._processStep(step);this._loading=!1;setTimeout(()=>this.$.dialog.center(),0)})}_submitStep(){this._loading=!0;this._errorMsg=null;const curInstance=this._instance,data={};Object.keys(this._stepData).forEach(key=>{const value=this._stepData[key],isEmpty=[void 0,""].includes(value);if(!isEmpty){data[key]=value}});this.hass.callApi("post",`config/config_entries/flow/${this._step.flow_id}`,data).then(step=>{if(curInstance!==this._instance)return;this._processStep(step);this._loading=!1},err=>{this._errorMsg=err&&err.body&&err.body.message||"Unknown error occurred";this._loading=!1})}_processStep(step){if(!step.errors)step.errors={};this._step=step;if("form"===step.type&&0===Object.keys(step.errors).length){const data={};step.data_schema.forEach(field=>{if("default"in field){data[field.name]=field.default}});this._stepData=data}}_flowDone(){this._opened=!1;const flowFinished=this._step&&["success","abort"].includes(this._step.type);if(this._step&&!flowFinished&&this._createdFromHandler){this.hass.callApi("delete",`config/config_entries/flow/${this._step.flow_id}`)}this._dialogClosedCallback({flowFinished});this._errorMsg=null;this._step=null;this._stepData={};this._dialogClosedCallback=null}_equals(a,b){return a===b}_openedChanged(ev){if(this._step&&!ev.detail.value){this._flowDone()}}_computeStepTitle(localize,step){return localize(`component.${step.handler}.config.step.${step.step_id}.title`)}_computeStepDescription(localize,step){const args=[];if("form"===step.type){args.push(`component.${step.handler}.config.step.${step.step_id}.description`)}else if("abort"===step.type){args.push(`component.${step.handler}.config.abort.${step.reason}`)}else if("create_entry"===step.type){args.push(`component.${step.handler}.config.create_entry.${step.description||"default"}`)}const placeholders=step.description_placeholders||{};Object.keys(placeholders).forEach(key=>{args.push(key);args.push(placeholders[key])});return localize(...args)}_computeLabelCallback(localize,step){return schema=>localize(`component.${step.handler}.config.step.${step.step_id}.data.${schema.name}`)}_computeErrorCallback(localize,step){return error=>localize(`component.${step.handler}.config.error.${error}`)}_computeCanSubmit(step,stepData){return null!==step&&"form"===step.type&&null!==stepData&&step.data_schema.every(field=>field.optional||!["",void 0].includes(stepData[field.name]))}_increaseCounter(){this._counter+=1}}customElements.define("ha-config-flow",HaConfigFlow)}}]);
//# sourceMappingURL=cf4aabac79abf7d9b229.chunk.js.map