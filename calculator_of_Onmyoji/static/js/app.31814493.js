(function(t){function e(e){for(var i,s,r=e[0],c=e[1],o=e[2],h=0,m=[];h<r.length;h++)s=r[h],u[s]&&m.push(u[s][0]),u[s]=0;for(i in c)Object.prototype.hasOwnProperty.call(c,i)&&(t[i]=c[i]);l&&l(e);while(m.length)m.shift()();return n.push.apply(n,o||[]),a()}function a(){for(var t,e=0;e<n.length;e++){for(var a=n[e],i=!0,r=1;r<a.length;r++){var c=a[r];0!==u[c]&&(i=!1)}i&&(n.splice(e--,1),t=s(s.s=a[0]))}return t}var i={},u={app:0},n=[];function s(e){if(i[e])return i[e].exports;var a=i[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,s),a.l=!0,a.exports}s.m=t,s.c=i,s.d=function(t,e,a){s.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},s.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.t=function(t,e){if(1&e&&(t=s(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(s.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)s.d(a,i,function(e){return t[e]}.bind(null,i));return a},s.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return s.d(e,"a",e),e},s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},s.p="/static/";var r=window["webpackJsonp"]=window["webpackJsonp"]||[],c=r.push.bind(r);r.push=e,r=r.slice();for(var o=0;o<r.length;o++)e(r[o]);var l=c;n.push([0,"chunk-vendors"]),a()})({0:function(t,e,a){t.exports=a("cd49")},1642:function(t,e,a){"use strict";var i=a("900f"),u=a.n(i);u.a},"5c48":function(t,e,a){},6721:function(t,e,a){},"7c55":function(t,e,a){"use strict";var i=a("5c48"),u=a.n(i);u.a},"900f":function(t,e,a){},b8cc:function(t,e,a){"use strict";var i=a("6721"),u=a.n(i);u.a},cd49:function(t,e,a){"use strict";a.r(e);a("cadf"),a("551c"),a("097d");var i=a("2b0e"),u=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"app"}},[a("Calculator")],1)},n=[],s=a("d225"),r=a("308d"),c=a("6bb5"),o=a("4e2b"),l=a("9ab4"),h=a("60a3"),m=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"calculator"},[t._m(0),a("section",{staticClass:"main"},[a("Form",{staticClass:"filter-options-form"},[a("div",{staticClass:"yuhun-package-input"},[a("Popover",{ref:"presetYuhunSet",attrs:{placement:"right",trigger:"hover"}},[a("RadioGroup",{staticClass:"preset",attrs:{size:"mini"},on:{change:t.onSelectPresetYuhun},model:{value:t.presetYuhunPackageList,callback:function(e){t.presetYuhunPackageList=e},expression:"presetYuhunPackageList"}},t._l(this.presetYuhunPackages,function(e){return a("RadioButton",{key:e.name,attrs:{label:e.value}},[t._v("\n                      "+t._s(e.name)+"\n                    ")])}),1)],1),a("p",{staticClass:"title"},[t._v("\n                  御魂套装组合\n                  "),a("Tag",{directives:[{name:"popover",rawName:"v-popover:presetYuhunSet",arg:"presetYuhunSet"}],attrs:{title:"常用"}},[t._v("+")])],1),a("Select",{staticClass:"yuhun",attrs:{placeholder:"选择御魂套装"},model:{value:t.yuhunPackage,callback:function(e){t.yuhunPackage=e},expression:"yuhunPackage"}},t._l(t.yuhunOptions,function(e){return a("OptionGroup",{key:e.name,attrs:{label:e.name}},t._l(e.list,function(t){return a("Option",{key:t,attrs:{label:t,value:t}})}),1)}),1),a("Button",{attrs:{type:"primary",disabled:t.disableAddYuhunPackageButton},on:{click:t.addYuhunPackageLimit}},[t._v("添加")]),a("div",{staticClass:"select-yuhun-list"},t._l(this.yuhunPackageList,function(e,i){return a("Tag",{key:i,attrs:{closable:""},on:{close:function(a){t.removeYuhunPackageLimit(e)}}},[t._v(t._s(e))])}),1)],1),a("FormItem",[a("Checkbox",{attrs:{label:"限定使用套装"},model:{value:t.usePackage,callback:function(e){t.usePackage=e},expression:"usePackage"}}),a("Checkbox",{attrs:{label:"限定使用输出御魂"},model:{value:t.useAttack,callback:function(e){t.useAttack=e},expression:"useAttack"}}),a("Popover",{ref:"presetAttribute",attrs:{placement:"right",trigger:"hover"}},[a("RadioGroup",{staticClass:"preset",attrs:{size:"mini"},on:{change:t.onSelectPresetAttribute},model:{value:t.presetAttribute,callback:function(e){t.presetAttribute=e},expression:"presetAttribute"}},t._l(this.presetAttributes,function(e){return a("RadioButton",{key:e.value,attrs:{label:e.value}},[t._v("\n                      "+t._s(e.value)+"\n                    ")])}),1)],1)],1),a("FormItem",{staticClass:"multi-checkbox"},[a("p",{staticClass:"title"},[t._v("二号位属性"),a("Tag",{directives:[{name:"popover",rawName:"v-popover:presetAttribute",arg:"presetAttribute"}],attrs:{title:"常用"}},[t._v("+")])],1),a("CheckboxGroup",{attrs:{size:"mini"},model:{value:t.secondAttributeList,callback:function(e){t.secondAttributeList=e},expression:"secondAttributeList"}},[a("CheckboxButton",{attrs:{label:"攻击加成"}}),a("CheckboxButton",{attrs:{label:"生命加成"}}),a("CheckboxButton",{attrs:{label:"防御加成"}}),a("CheckboxButton",{attrs:{label:"速度"}})],1)],1),a("FormItem",{staticClass:"multi-checkbox"},[a("p",{staticClass:"title"},[t._v("四号位属性")]),a("CheckboxGroup",{attrs:{size:"mini"},model:{value:t.fourthAttributeList,callback:function(e){t.fourthAttributeList=e},expression:"fourthAttributeList"}},[a("CheckboxButton",{attrs:{label:"攻击加成"}}),a("CheckboxButton",{attrs:{label:"生命加成"}}),a("CheckboxButton",{attrs:{label:"防御加成"}}),a("CheckboxButton",{attrs:{label:"效果命中"}}),a("CheckboxButton",{attrs:{label:"效果抵抗"}})],1)],1),a("FormItem",{staticClass:"multi-checkbox"},[a("p",{staticClass:"title"},[t._v("六号位属性")]),a("CheckboxGroup",{attrs:{size:"mini"},model:{value:t.sixthAttributeList,callback:function(e){t.sixthAttributeList=e},expression:"sixthAttributeList"}},[a("CheckboxButton",{attrs:{label:"攻击加成"}}),a("CheckboxButton",{attrs:{label:"生命加成"}}),a("CheckboxButton",{attrs:{label:"防御加成"}}),a("CheckboxButton",{attrs:{label:"暴击"}}),a("CheckboxButton",{attrs:{label:"暴击伤害"}})],1)],1),a("FormItem",{attrs:{label:""}},[a("p",{staticClass:"title"},[t._v("忽略指定关键字御魂")]),a("Input",{attrs:{placeholder:"御魂列表(以,分隔)"},model:{value:t.ignoreSerial,callback:function(e){t.ignoreSerial=e},expression:"ignoreSerial"}})],1)],1),a("Form",{staticClass:"expect-options-form"},[a("FormItem",{staticClass:"input-item",attrs:{label:"伤害期望"}},[a("Input",{attrs:{placeholder:"格式: 式神基础攻击,式神基础爆伤,期望伤害值"},model:{value:t.damageExpect,callback:function(e){t.damageExpect=e},expression:"damageExpect"}}),a("label",[t._v("攻击加成: ")]),a("Select",{model:{value:t.attackBuff,callback:function(e){t.attackBuff=e},expression:"attackBuff"}},t._l(t.attackBuffs,function(t){return a("Option",{key:t.name,attrs:{label:t.name,value:t.value}})}),1)],1),a("FormItem",{staticClass:"input-item",attrs:{label:"治疗期望"}},[a("Input",{attrs:{placeholder:"格式: 式神基础生命,式神基础爆伤,期望治疗值"},model:{value:t.healthExpect,callback:function(e){t.healthExpect=e},expression:"healthExpect"}})],1),a("FormItem",{staticClass:"input-item",attrs:{label:"有效副属性"}},[a("Autocomplete",{attrs:{placeholder:"属性列表(以,分隔)  例如: 暴击,暴击伤害","popper-class":"esp-autocomplete","fetch-suggestions":t.queryEffectiveAttributes},scopedSlots:t._u([{key:"default",fn:function(e){var i=e.item;return[a("span",[t._v(t._s(i.name))]),a("span",[t._v("<"+t._s(i.value)+">")])]}}]),model:{value:t.effectiveAttributes,callback:function(e){t.effectiveAttributes=e},expression:"effectiveAttributes"}}),a("Autocomplete",{attrs:{placeholder:"各位置加成次数(以,分隔)  例如: 3,3,3,3,3,0","fetch-suggestions":t.queryEffectiveAttributesBonusCount},model:{value:t.effectiveAttributesBonusCount,callback:function(e){t.effectiveAttributesBonusCount=e},expression:"effectiveAttributesBonusCount"}})],1),a("FormItem",[a("p",{staticClass:"title"},[t._v("目标属性限制")]),a("label",[t._v("属性:")]),a("Select",{model:{value:t.targetAttribute,callback:function(e){t.targetAttribute=e},expression:"targetAttribute"}},t._l(t.attributes,function(t){return a("Option",{key:t,attrs:{label:t,value:t}})}),1),a("br"),a("div",{directives:[{name:"show",rawName:"v-show",value:""!==t.targetAttribute,expression:"targetAttribute !== ''"}]},[a("label",[t._v("下限:")]),a("InputNumber",{attrs:{min:0,max:999,size:"small","controls-position":"right"},model:{value:t.lowerValue,callback:function(e){t.lowerValue=e},expression:"lowerValue"}}),a("label",[t._v("上限:")]),a("InputNumber",{attrs:{min:0,max:999,size:"small","controls-position":"right"},model:{value:t.upperValue,callback:function(e){t.upperValue=e},expression:"upperValue"}})],1)],1),a("FormItem",{staticClass:"attribute-results"},t._l(this.targetAttributeList,function(e){return a("Tag",{key:e.split(" ")[0],attrs:{closable:""},on:{close:function(a){t.removeTargetAttribute(e)}}},[t._v(t._s(e))])}),1)],1),a("Form",{staticClass:"control"},[a("FormItem",{attrs:{label:"输入文件"}},[a("br"),t.filename?a("p",[t._v(t._s(t.filename))]):a("p",[t._v("尚未选择御魂数据文件")]),a("Button",{attrs:{type:"primary"},on:{click:t.selectFile}},[t._v("选择文件")])],1),a("FormItem",[100===t.calculateProgress?a("Button",{attrs:{type:"primary",disabled:!t.serverOnline},on:{click:t.run}},[t._v("开始计算")]):a("Button",{attrs:{type:"primary",loading:""}},[t._v("计算中... "+t._s(t.calculateProgress)+"%")])],1),a("CustomScheme",{attrs:{currentScheme:t.currentScheme},on:{selectScheme:t.handleSelectScheme}})],1)],1)])},p=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("header",{staticClass:"header"},[a("p",[t._v("《阴阳师》御魂计算器")])])}],f=(a("06f1"),a("450d"),a("6ac9")),b=a.n(f),v=(a("3db2"),a("58b8")),g=a.n(v),d=(a("a7cc"),a("df33")),k=a.n(d),A=(a("cbb5"),a("8bbc")),y=a.n(A),L=(a("9d4c"),a("e450")),x=a.n(L),S=(a("10cb"),a("f3ad")),C=a.n(S),P=(a("fe07"),a("6ac5")),_=a.n(P),O=(a("3c52"),a("0d7b")),B=a.n(O),E=(a("b5d8"),a("f494")),j=a.n(E),w=(a("c526"),a("1599")),I=a.n(w),V=(a("560b"),a("dcdc")),F=a.n(V),N=(a("d4df"),a("7fc1")),Y=a.n(N),T=(a("016f"),a("486c")),$=a.n(T),G=(a("6611"),a("e772")),z=a.n(G),R=(a("1f1a"),a("4e4b")),M=a.n(R),q=(a("ae26"),a("845f")),J=a.n(q),D=(a("1951"),a("eedf")),U=a.n(D),H=(a("eca7"),a("3787")),K=a.n(H),Q=(a("425f"),a("4105")),W=a.n(Q),X=(a("46a1"),a("e5f2")),Z=a.n(X),tt=a("768b"),et=(a("0fb7"),a("f529")),at=a.n(et),it=(a("7f7f"),a("28a5"),a("20d6"),a("b0b4")),ut=a("bc3a"),nt=a.n(ut),st=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"custom-scheme"},[a("FormItem",[a("Button",{attrs:{type:"primary"},on:{click:t.saveScheme}},[t._v("保存当前方案")])],1),a("FormItem",[a("Button",{attrs:{type:"primary"},on:{click:t.selectCustomScheme}},[t._v("选择自定义方案")])],1),a("FormItem",[a("Button",{attrs:{type:"primary"},on:{click:t.selectPresetScheme}},[t._v("选择预设方案")])],1)],1)},rt=[],ct=a("5d73"),ot=a.n(ct),lt=(a("7514"),a("5176")),ht=a.n(lt),mt=(a("9e1f"),a("6ed5")),pt=a.n(mt),ft=a("f499"),bt=a.n(ft),vt=[{name:"吃星暴伤针女大天狗",yuhunPackageList:["针女,4"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3135.6,150,0",healthExpect:"",targetAttributeList:["暴击 90 - 95","速度 0 - 18"]},{name:"超星暴伤针女大天狗",yuhunPackageList:["针女,4"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3135.6,150,0",healthExpect:"",targetAttributeList:["暴击 90 - 95","速度 18 - 999"]},{name:"超星荒骷髅茨木",yuhunPackageList:["破势,4","荒骷髅,2"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3216,150,17120",healthExpect:"",targetAttributeList:["暴击 90 - 95","速度 16 - 999"]},{name:"超星普通茨木",yuhunPackageList:["破势,4"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3216,150,20510",healthExpect:"",targetAttributeList:["暴击 90 - 95","速度 16 - 999"]},{name:"吃星荒骷髅茨木",yuhunPackageList:["破势,4","荒骷髅,2"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3216,150,13170",healthExpect:"",targetAttributeList:["暴击 90 - 95","速度 0 - 16"]},{name:"吃星普通茨木",yuhunPackageList:["破势,4"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3216,150,15780",healthExpect:"",targetAttributeList:["暴击 90 - 95","速度 0 - 16"]},{name:"暴伤玉藻前",yuhunPackageList:["破势,4"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害"],ignoreSerial:"",damageExpect:"3350,160,0",healthExpect:"",targetAttributeList:["暴击 88 - 95"]},{name:"正堆+反堆暴伤针女",yuhunPackageList:["针女,4"],usePackage:!0,useAttack:!0,secondAttributeList:["攻击加成"],fourthAttributeList:["攻击加成"],sixthAttributeList:["暴击伤害","暴击"],ignoreSerial:"",damageExpect:"",healthExpect:"",targetAttributeList:["暴击 90 - 95","暴击伤害 80 - 999"]},{name:"散件蜃气楼生生暴书翁",yuhunPackageList:["蜃气楼,2"],usePackage:!1,useAttack:!1,secondAttributeList:["生命加成"],fourthAttributeList:["生命加成"],sixthAttributeList:["暴击"],ignoreSerial:"",damageExpect:"",healthExpect:"11393,150,0",targetAttributeList:["暴击 92 - 95"]}],gt=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("Select",{model:{value:t.selectedPresetSchemeName,callback:function(e){t.selectedPresetSchemeName=e},expression:"selectedPresetSchemeName"}},t._l(t.schemeList,function(t){return a("Option",{key:t.name,attrs:{label:t.name,value:t.name}})}),1)},dt=[],kt=function(t){function e(){var t;return Object(s["a"])(this,e),t=Object(r["a"])(this,Object(c["a"])(e).apply(this,arguments)),t.selectedPresetSchemeName="",t}return Object(o["a"])(e,t),Object(it["a"])(e,[{key:"onSelectSchemeChange",value:function(){this.$emit("SelectSchemeChange",this.selectedPresetSchemeName)}}]),e}(h["c"]);l["a"]([Object(h["b"])({default:[]})],kt.prototype,"schemeList",void 0),l["a"]([Object(h["d"])("selectedPresetSchemeName")],kt.prototype,"onSelectSchemeChange",null),kt=l["a"]([Object(h["a"])({components:{Select:M.a,Option:z.a}})],kt);var At=kt,yt=At,Lt=a("2877"),xt=Object(Lt["a"])(yt,gt,dt,!1,null,null,null);xt.options.__file="SchemeSelect.vue";var St=xt.exports,Ct="customSchemeList",Pt=window.localStorage.getItem(Ct)||"[]",_t=function(t){function e(){var t;return Object(s["a"])(this,e),t=Object(r["a"])(this,Object(c["a"])(e).apply(this,arguments)),t.schemeList=JSON.parse(Pt),t.selectedCustomSchemeName="",t.selectedPresetSchemeName="",t}return Object(o["a"])(e,t),Object(it["a"])(e,[{key:"saveStorage",value:function(){window.localStorage.setItem(Ct,bt()(this.schemeList))}},{key:"saveScheme",value:function(){var t=this;pt.a.prompt("","请输入自定义方案名称").then(function(e){var a=e.value,i=ht()({name:a},t.currentScheme);t.schemeList.push(i),t.saveStorage(),at.a.success("保存自定义方案「".concat(i.name,"」成功"))})}},{key:"selectCustomScheme",value:function(){var t=this,e=this.$createElement;pt()({title:"自定义方案列表",message:e("SchemeSelect",{key:"CustomSchemeSelct",props:{schemeList:this.schemeList},on:{SelectSchemeChange:function(e){t.selectedCustomSchemeName=e}}}),showCancelButton:!0,confirmButtonText:"选择",cancelButtonText:"删除",cancelButtonClass:"delete",distinguishCancelAndClose:!0}).then(function(){var e=t.schemeList.find(function(e){return e.name===t.selectedCustomSchemeName});e&&(t.$emit("selectScheme",e),at.a.success("应用自定义方案「".concat(e.name,"」成功")))}).catch(function(e){if("close"!==e){var a=t.schemeList.findIndex(function(e){return e.name===t.selectedCustomSchemeName});-1!==a&&(at.a.success("删除自定义方案「".concat(t.schemeList[a].name,"」成功")),t.schemeList.splice(a,1),t.saveStorage(),t.selectedCustomSchemeName="")}})}},{key:"selectPresetScheme",value:function(){var t=this,e=this.$createElement;pt()({title:"预设方案列表",message:e("SchemeSelect",{key:"PresetSchemeSelct",props:{schemeList:vt},on:{SelectSchemeChange:function(e){t.selectedCustomSchemeName=e}}}),confirmButtonText:"选择",distinguishCancelAndClose:!0}).then(function(){var e=!0,a=!1,i=void 0;try{for(var u,n=ot()(vt);!(e=(u=n.next()).done);e=!0){var s=u.value;if(s.name===t.selectedCustomSchemeName){t.$emit("selectScheme",s),at.a.success("应用预设方案「".concat(t.selectedCustomSchemeName,"」成功"));break}}}catch(r){a=!0,i=r}finally{try{e||null==n.return||n.return()}finally{if(a)throw i}}})}}]),e}(h["c"]);l["a"]([Object(h["b"])({default:{}})],_t.prototype,"currentScheme",void 0),_t=l["a"]([Object(h["a"])({components:{FormItem:K.a,Button:U.a,Select:M.a,Option:z.a,Dialog:k.a,SchemeSelect:St}})],_t);var Ot=_t,Bt=Ot,Et=(a("1642"),Object(Lt["a"])(Bt,st,rt,!1,null,null,null));Et.options.__file="CustomScheme.vue";var jt=Et.exports,wt="//localhost:2019",It={validateStatus:function(t){return t>=200&&t<=500}},Vt=function(t){function e(){var t;return Object(s["a"])(this,e),t=Object(r["a"])(this,Object(c["a"])(e).apply(this,arguments)),t.serverOnline=!0,t.yuhunPackage="",t.yuhunPackageList=[],t.presetYuhunPackageList=[],t.usePackage=!0,t.useAttack=!1,t.secondAttributeList=[],t.fourthAttributeList=[],t.sixthAttributeList=[],t.presetAttribute="",t.ignoreSerial="",t.damageExpect="",t.attackBuff="",t.healthExpect="",t.effectiveAttributes="",t.effectiveAttributesBonusCount="",t.targetAttribute="",t.lowerValue=0,t.upperValue=999,t.targetAttributeList=[],t.filename="",t.calculateProgress=100,t}return Object(o["a"])(e,t),Object(it["a"])(e,[{key:"addYuhunPackageLimit",value:function(){this.disableAddYuhunPackageButton||this.yuhunPackageList.push(this.yuhunPackage)}},{key:"removeYuhunPackageLimit",value:function(t){var e=this.yuhunPackageList.findIndex(function(e){return e===t});this.yuhunPackageList.splice(e,1)}},{key:"addTargetAttribute",value:function(){var t=this,e="".concat(this.targetAttribute," ").concat(this.lowerValue||0," - ").concat(this.upperValue||0),a=this.targetAttributeList.findIndex(function(e){return e.split(" ")[0]===t.targetAttribute});-1===a?this.targetAttributeList.push(e):this.targetAttributeList.splice(a,1,e)}},{key:"removeTargetAttribute",value:function(t){var e=this.targetAttributeList.findIndex(function(e){return e===t});-1!==e&&this.targetAttributeList.splice(e,1)}},{key:"ontargetAttributeChange",value:function(t){t&&(this.lowerValue=0,this.upperValue=0,this.addTargetAttribute())}},{key:"onLowerValueChange",value:function(t,e){0===e&&(this.upperValue=t+10),this.upperValue<t&&(this.upperValue=t),this.addTargetAttribute()}},{key:"onUpperValueChange",value:function(t){this.lowerValue>t&&(this.lowerValue=t),this.addTargetAttribute()}},{key:"selectFile",value:function(){var t=this,e=document.createElement("input");e.style.display="none",e.setAttribute("type","file"),e.setAttribute("accept",".json,.xls"),e.onclick=function(){e.value="",document.body.onfocus=function(){setTimeout(function(){e.value.length,document.body.onfocus=null},500)}},e.onchange=function(e){var a=e.target.files[0];a&&(t.filename=a.name)},e.click()}},{key:"verifyInputValue",value:function(){return this.damageExpect&&!/^[0-9]+,[0-9]+,[0-9]+(?:,[0-9]+)?$/.test(this.damageExpect)?(at.a.warning('"伤害期望" 格式错误'),!1):this.healthExpect&&!/^[0-9]+,[0-9]+,[0-9]+(?:,[0-9]+)?$/.test(this.healthExpect)?(at.a.warning('"治疗期望" 格式错误'),!1):this.effectiveAttributes&&!/^(攻击加成|生命加成|防御加成|速度|效果命中|效果抵抗|暴击|暴击伤害)(,(攻击加成|生命加成|防御加成|速度|效果命中|效果抵抗|暴击|暴击伤害))*$/.test(this.effectiveAttributes)?(at.a.warning('"有效副属性 => 属性列表" 格式错误'),!1):!(this.effectiveAttributesBonusCount&&!/^[0-9]+,[0-9]+,[0-9]+,[0-9]+,[0-9]+,[0-9]+$/.test(this.effectiveAttributesBonusCount))||(at.a.warning('"有效副属性 => 各位置加成次数" 格式错误'),!1)}},{key:"run",value:function(){this.filename?this.verifyInputValue()&&(nt.a.post(wt+"/calculate",{src_filename:this.filename,mitama_suit:this.yuhunPackageList.join("."),prop_limit:this.targetAttributeList.map(function(t){var e=t.split(/ |-/),a=Object(tt["a"])(e,2),i=a[0],u=a[1];return i+","+u}).join("."),upper_prop_limit:this.targetAttributeList.map(function(t){var e=t.split(/ |-/),a=Object(tt["a"])(e,5),i=a[0],u=a[4];return i+","+u}).join("."),sec_prop_value:this.getPropValue(this.secondAttributeList),fth_prop_value:this.getPropValue(this.fourthAttributeList),sth_prop_value:this.getPropValue(this.sixthAttributeList),ignore_serial:this.ignoreSerial,all_suit:this.usePackage,damage_limit:this.damageExpect||"0,0,0",health_limit:this.healthExpect||"0,0,0",attack_only:this.useAttack,effective_secondary_prop:this.effectiveAttributes||"",effective_secondary_prop_num:this.effectiveAttributesBonusCount||"",attack_buff:this.attackBuff||0},It).then(function(t){switch(t.status){case 500:at()({type:"error",message:"计算失败, 服务端错误: ".concat(t.data.reason),duration:5e3});break;case 200:at.a.success("计算完毕, 组合数量:".concat(t.data.result_num));break;default:at.a.error("计算失败, 服务端返回状态码:".concat(t.status));break}}).catch(function(t){at.a.error("计算失败")}),setTimeout(this.getCalculateStatus.bind(this),500)):at.a.warning("请先选择御魂数据文件")}},{key:"mounted",value:function(){var t=this;nt.a.get(wt+"/status").catch(function(){Z.a.error({title:"提示",message:"未检测到服务端, 请先启动服务端后再试",duration:0}),t.serverOnline=!1})}},{key:"handleSelectScheme",value:function(t){this.yuhunPackageList=t.yuhunPackageList,this.usePackage=t.usePackage,this.useAttack=t.useAttack,this.secondAttributeList=t.secondAttributeList,this.fourthAttributeList=t.fourthAttributeList,this.sixthAttributeList=t.sixthAttributeList,this.ignoreSerial=t.ignoreSerial,this.damageExpect=t.damageExpect,this.healthExpect=t.healthExpect,this.targetAttributeList=t.targetAttributeList,this.targetAttribute="",this.attackBuff=""}},{key:"getCalculateStatus",value:function(){var t=this;nt.a.get(wt+"/status").then(function(e){var a=e.data.progress;void 0!==a&&(t.calculateProgress=Math.floor(100*a),1!==a&&setTimeout(t.getCalculateStatus.bind(t),100))}).catch(function(){console.warn("获取计算进度失败")})}},{key:"getPropValue",value:function(t){return t.map(function(t){switch(t){case"速度":return"速度,57";case"暴击伤害":return"暴击伤害,89";default:return t+",55"}}).join(".")}},{key:"queryEffectiveAttributes",value:function(t,e){var a=this.effectiveAttributesChoices;return t&&(a=a.filter(function(e){return 0===e.name.toLowerCase().indexOf(t.toLowerCase())||0===e.value.toLowerCase().indexOf(t.toLowerCase())})),e(a)}},{key:"queryEffectiveAttributesBonusCount",value:function(t,e){var a=this.effectiveAttributesBonusCountChoices;return t&&(a=a.filter(function(e){return-1!==e.value.indexOf(t.toLowerCase())})),e(a)}},{key:"onSelectPresetAttribute",value:function(t){var e={"生":["生命加成"],"攻":["攻击加成"],"暴":["暴击","暴击伤害"],"命":["效果命中"],"抗":["效果抵抗"],"速":["速度"]};if(3===t.length){var a=t.split("").map(function(t){return e[t]});this.secondAttributeList=a[0],this.fourthAttributeList=a[1],this.sixthAttributeList=a[2]}}},{key:"onSelectPresetYuhun",value:function(t){this.yuhunPackageList=this.presetYuhunPackageList.slice()}},{key:"yuhunOptions",get:function(){return[{name:"散件",list:["攻击加成,2","暴击,2","生命加成,2","效果命中,2","效果抵抗,2"]},{name:"首领御魂",list:["荒骷髅,2","土蜘蛛,2","地震鲶,2","蜃气楼,2","胧车,2"]},{name:"暴击",list:["针女,4","破势,4","网切,4","三味,4","伤魂鸟,4","镇魂兽,4"]},{name:"攻击加成",list:["蝠翼,4","鸣屋,4","心眼,4","狰,4","轮入道,4","狂骨,4","阴摩罗,4"]},{name:"生命加成",list:["树妖,4","地藏像,4","薙魂,4","镜姬,4","钟灵,4","涅槃之火,4","被服,4"]},{name:"防御加成",list:["珍珠,4","魅妖,4","雪幽魂,4","招财猫,4","反枕,4","日女巳时,4","木魅,4"]},{name:"效果命中",list:["蚌精,4","火灵,4"]},{name:"效果抵抗",list:["骰子鬼,4","返魂香,4","幽谷响,4","魍魉之匣,4"]}]}},{key:"attributes",get:function(){return["暴击","暴击伤害","效果命中","效果抵抗","速度","攻击加成","生命加成","防御加成"]}},{key:"attackBuffs",get:function(){return[{name:"无buff",value:0},{name:"1级兔子舞",value:10},{name:"满级兔子舞",value:20},{name:"满级兄弟之绊",value:25},{name:"黑晴明+1级兔子舞",value:30},{name:"黑晴明+满级兔子舞",value:40},{name:"黑晴明+满级兄弟之绊",value:45}]}},{key:"presetAttributes",get:function(){return[{name:"攻攻暴",value:"攻攻暴"},{name:"速攻暴",value:"速攻暴"},{name:"生生暴",value:"生生暴"},{name:"速生暴",value:"速生暴"},{name:"速命生",value:"速命生"},{name:"速抗生",value:"速抗生"}]}},{key:"presetYuhunPackages",get:function(){return[{name:"破荒",value:["破势,4","荒骷髅,2"]},{name:"心荒",value:["心眼,4","荒骷髅,2"]},{name:"狂荒",value:["狂骨,4","荒骷髅,2"]},{name:"针荒",value:["针女,4","荒骷髅,2"]},{name:"散件生命",value:["生命加成,2","生命加成,2","生命加成,2"]}]}},{key:"effectiveAttributesChoices",get:function(){return[{name:"输出",value:"暴击,暴击伤害,攻击加成,速度"},{name:"奶盾",value:"暴击,暴击伤害,生命加成,速度"},{name:"命中",value:"效果命中,速度"},{name:"抵抗",value:"效果抵抗,速度"},{name:"双堆",value:"速度,效果命中,效果抵抗"}]}},{key:"effectiveAttributesBonusCountChoices",get:function(){return[{name:"1",value:"1,1,1,1,1,0"},{name:"2",value:"3,3,3,3,3,1"},{name:"3",value:"3,2,3,2,3,0"},{name:"4",value:"5,3,5,3,5,1"}]}},{key:"disableAddYuhunPackageButton",get:function(){if(!this.yuhunPackage)return!0;var t=0;if(this.yuhunPackage){var e=this.yuhunPackage.split(","),a=Object(tt["a"])(e,2),i=a[1];t=+i}return t+this.selectedYuhunPackageCount>6}},{key:"selectedYuhunPackageCount",get:function(){return this.yuhunPackageList.map(function(t){var e=t.split(","),a=Object(tt["a"])(e,2),i=a[1];return+i}).reduce(function(t,e){return t+e},0)}},{key:"currentScheme",get:function(){return{yuhunPackageList:this.yuhunPackageList,usePackage:this.usePackage,useAttack:this.useAttack,secondAttributeList:this.secondAttributeList,fourthAttributeList:this.fourthAttributeList,sixthAttributeList:this.sixthAttributeList,ignoreSerial:this.ignoreSerial,damageExpect:this.damageExpect,healthExpect:this.healthExpect,targetAttributeList:this.targetAttributeList}}}]),e}(h["c"]);l["a"]([Object(h["d"])("yuhunPackage")],Vt.prototype,"addYuhunPackageLimit",null),l["a"]([Object(h["d"])("targetAttribute")],Vt.prototype,"ontargetAttributeChange",null),l["a"]([Object(h["d"])("lowerValue")],Vt.prototype,"onLowerValueChange",null),l["a"]([Object(h["d"])("upperValue")],Vt.prototype,"onUpperValueChange",null),Vt=l["a"]([Object(h["a"])({components:{Form:W.a,FormItem:K.a,Button:U.a,ButtonGroup:J.a,Select:M.a,Option:z.a,OptionGroup:$.a,CheckboxGroup:Y.a,Checkbox:F.a,CheckboxButton:I.a,Radio:j.a,RadioButton:B.a,RadioGroup:_.a,Input:C.a,InputNumber:x.a,Tag:y.a,Dialog:k.a,CustomScheme:jt,Autocomplete:g.a,Popover:b.a}})],Vt);var Ft=Vt,Nt=Ft,Yt=(a("b8cc"),Object(Lt["a"])(Nt,m,p,!1,null,null,null));Yt.options.__file="Calculator.vue";var Tt=Yt.exports,$t=function(t){function e(){return Object(s["a"])(this,e),Object(r["a"])(this,Object(c["a"])(e).apply(this,arguments))}return Object(o["a"])(e,t),e}(h["c"]);$t=l["a"]([Object(h["a"])({components:{Calculator:Tt}})],$t);var Gt=$t,zt=Gt,Rt=(a("7c55"),Object(Lt["a"])(zt,u,n,!1,null,null,null));Rt.options.__file="App.vue";var Mt=Rt.exports;i["default"].config.productionTip=!1,new i["default"]({render:function(t){return t(Mt)}}).$mount("#app")}});
//# sourceMappingURL=app.31814493.js.map