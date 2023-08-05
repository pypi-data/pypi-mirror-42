(window.webpackJsonp=window.webpackJsonp||[]).push([[71],{179:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(18),_resources_ha_style__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(68);class HaConfigSection extends _polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a{static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <style include="iron-flex ha-style">
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        .header {
          @apply --paper-font-display1;
          opacity: var(--dark-primary-opacity);
        }

        .together {
          margin-top: 32px;
        }

        .intro {
          @apply --paper-font-subhead;
          width: 100%;
          max-width: 400px;
          margin-right: 40px;
          opacity: var(--dark-primary-opacity);
        }

        .panel {
          margin-top: -24px;
        }

        .panel ::slotted(*) {
          margin-top: 24px;
          display: block;
        }

        .narrow.content {
          max-width: 640px;
        }
        .narrow .together {
          margin-top: 20px;
        }
        .narrow .header {
          @apply --paper-font-headline;
        }
        .narrow .intro {
          font-size: 14px;
          padding-bottom: 20px;
          margin-right: 0;
          max-width: 500px;
        }
      </style>
      <div class$="[[computeContentClasses(isWide)]]">
        <div class="header"><slot name="header"></slot></div>
        <div class$="[[computeClasses(isWide)]]">
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(isWide){var classes="content ";return isWide?classes:classes+"narrow"}computeClasses(isWide){var classes="together layout ";return classes+(isWide?"horizontal":"vertical narrow")}}customElements.define("ha-config-section",HaConfigSection)},239:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_exports__.a=(a,b)=>{if(a<b){return-1}if(a>b){return 1}return 0}},721:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(6),paper_item=__webpack_require__(128),paper_item_body=__webpack_require__(164),paper_card=__webpack_require__(160),paper_fab=__webpack_require__(221);const fetchPersons=hass=>hass.callWS({type:"person/list"}),createPerson=(hass,values)=>hass.callWS(Object.assign({type:"person/create"},values)),updatePerson=(hass,personId,updates)=>hass.callWS(Object.assign({type:"person/update",person_id:personId},updates)),deletePerson=(hass,personId)=>hass.callWS({type:"person/delete",person_id:personId});var hass_subpage=__webpack_require__(140),hass_loading_screen=__webpack_require__(145),compare=__webpack_require__(239),ha_config_section=__webpack_require__(179),fire_event=__webpack_require__(58);const loadPersonDetailDialog=()=>Promise.all([__webpack_require__.e(0),__webpack_require__.e(1),__webpack_require__.e(2),__webpack_require__.e(3),__webpack_require__.e(93)]).then(__webpack_require__.bind(null,780)),showPersonDetailDialog=(element,systemLogDetailParams)=>{Object(fire_event.a)(element,"show-dialog",{dialogTag:"dialog-person-detail",dialogImport:loadPersonDetailDialog,dialogParams:systemLogDetailParams})};class ha_config_person_HaConfigPerson extends lit_element.a{constructor(...args){super(...args);this.hass=void 0;this.isWide=void 0;this._storageItems=void 0;this._configItems=void 0}static get properties(){return{hass:{},isWide:{},_storageItems:{},_configItems:{}}}render(){if(!this.hass||this._storageItems===void 0||this._configItems===void 0){return lit_element.e`
        <hass-loading-screen></hass-loading-screen>
      `}return lit_element.e`
      <hass-subpage header="Persons">
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header">Persons</span>
          <span slot="introduction">
            Here you can define each person of interest in Home Assistant.
            ${0<this._configItems.length?lit_element.e`
                  <p>
                    Note: people configured via configuration.yaml cannot be
                    edited via the UI.
                  </p>
                `:""}
          </span>
          <paper-card class="storage">
            ${this._storageItems.map(entry=>{return lit_element.e`
                <paper-item @click=${this._openEditEntry} .entry=${entry}>
                  <paper-item-body>
                    ${entry.name}
                  </paper-item-body>
                </paper-item>
              `})}
            ${0===this._storageItems.length?lit_element.e`
                  <div class="empty">
                    Looks like you have no people yet!
                    <mwc-button @click=${this._createPerson}>
                      CREATE PERSON</mwc-button
                    >
                  </div>
                `:lit_element.e``}
          </paper-card>
          ${0<this._configItems.length?lit_element.e`
                <paper-card heading="Configuration.yaml people">
                  ${this._configItems.map(entry=>{return lit_element.e`
                      <paper-item>
                        <paper-item-body>
                          ${entry.name}
                        </paper-item-body>
                      </paper-item>
                    `})}
                </paper-card>
              `:""}
        </ha-config-section>
      </hass-subpage>

      <paper-fab
        ?is-wide=${this.isWide}
        icon="hass:plus"
        title="Create Area"
        @click=${this._createPerson}
      ></paper-fab>
    `}firstUpdated(changedProps){super.firstUpdated(changedProps);this._fetchData();loadPersonDetailDialog()}async _fetchData(){const personData=await fetchPersons(this.hass);this._storageItems=personData.storage.sort((ent1,ent2)=>Object(compare.a)(ent1.name,ent2.name));this._configItems=personData.config.sort((ent1,ent2)=>Object(compare.a)(ent1.name,ent2.name))}_createPerson(){this._openDialog()}_openEditEntry(ev){const entry=ev.currentTarget.entry;this._openDialog(entry)}_openDialog(entry){showPersonDetailDialog(this,{entry,createEntry:async values=>{const created=await createPerson(this.hass,values);this._storageItems=this._storageItems.concat(created).sort((ent1,ent2)=>Object(compare.a)(ent1.name,ent2.name))},updateEntry:async values=>{const updated=await updatePerson(this.hass,entry.id,values);this._storageItems=this._storageItems.map(ent=>ent===entry?updated:ent)},removeEntry:async()=>{if(!confirm(`Are you sure you want to delete this area?

All devices in this area will become unassigned.`)){return!1}try{await deletePerson(this.hass,entry.id);this._storageItems=this._storageItems.filter(ent=>ent!==entry);return!0}catch(err){return!1}}})}static get styles(){return lit_element.c`
      a {
        color: var(--primary-color);
      }
      paper-card {
        display: block;
        max-width: 600px;
        margin: 16px auto;
      }
      .empty {
        text-align: center;
      }
      paper-item {
        padding-top: 4px;
        padding-bottom: 4px;
      }
      paper-card.storage paper-item {
        cursor: pointer;
      }
      paper-fab {
        position: fixed;
        bottom: 16px;
        right: 16px;
        z-index: 1;
      }

      paper-fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
    `}}customElements.define("ha-config-person",ha_config_person_HaConfigPerson)}}]);
//# sourceMappingURL=ab058f70562321af0a99.chunk.js.map