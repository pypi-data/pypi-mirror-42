(window.webpackJsonp=window.webpackJsonp||[]).push([[7],{1715:function(e,t,r){"use strict";r.r(t);var a=r(2),n=r(930),i=r(1722),o=r(1708),l=r(1670),s=r(1254),c=r.n(s),m=r(44);const p=c()(l.a),d=e=>{return{"=":">",">":"<","<":"="}[e]},h=m.c.div`
  width: calc(100vw - 150px);
`,u=e=>{const{filterState:t,filterName:r,updateFunction:l,onChange:s}=e,c=t[r]||"=",m=a.createElement(n.a,{content:`Switch to ${d(c)}`},a.createElement(i.a,{minimal:!0,onClick:()=>{l({[r]:d(c)})}},c));return a.createElement(o.a,{large:!0,placeholder:"number",rightElement:m,small:!1,type:"text",onChange:e=>{s(e.currentTarget.value)}})},y=(e,t,r)=>({onChange:n})=>a.createElement(u,{onChange:n,filterState:e,filterName:t,updateFunction:r}),g=(e="=")=>(t,r)=>{const a=Number(t.value);return"="===e?r[t.id]===a:"<"===e?r[t.id]<a:">"===e?r[t.id]>a:r[t.id]},b={integer:y,number:y,string:()=>({onChange:e})=>a.createElement(o.a,{large:!0,placeholder:"string",type:"text",onChange:t=>{e(t.currentTarget.value)}})},f={integer:g,number:g,string:()=>(e,t)=>-1!==t[e.id].toLowerCase().indexOf(e.value.toLowerCase())};class x extends a.PureComponent{constructor(e){super(e),this.state={filters:{},showFilters:!1}}render(){const{data:{data:e,schema:t},height:r}=this.props,{filters:n,showFilters:o}=this.state,l=t.fields.map(e=>"string"===e.type||"number"===e.type||"integer"===e.type?{Header:e.name,accessor:e.name,fixed:-1!==t.primaryKey.indexOf(e.name)&&"left",filterMethod:(t,r)=>{if("string"===e.type||"number"===e.type||"integer"===e.type)return f[e.type](n[e.name])(t,r)},Filter:b[e.type](n,e.name,e=>{this.setState({filters:Object.assign({},n,e)})})}:{Header:e.name,accessor:e.name,fixed:-1!==t.primaryKey.indexOf(e.name)&&"left"});return a.createElement(h,null,a.createElement(i.a,{icon:"filter",onClick:()=>this.setState({showFilters:!o})},o?"Hide":"Show"," Filters"),a.createElement(p,{data:e,columns:l,style:{height:`${r}px`},className:"-striped -highlight",filterable:o}))}}x.defaultProps={metadata:{},height:500};var E=x,k=r(362),v=r(227),w=r(1709);const C=Object(m.c)(w.a)`
  .button-text {
    margin: 0 10px 10px 0;
    -webkit-appearance: none;
    padding: 5px 15px;
    background: white;
    border: 1px solid #bbb;
    color: #555;
    border-radius: 3px;
    cursor: pointer;
  }
  .button-text.selected {
    border-color: #1d8bf1;
    color: #1d8bf1;
  }
  .button-text {
    margin-right: -1px;
    border-radius: 0;
  }
  .button-text:first-child {
    border-top-left-radius: 3px;
    border-bottom-left-radius: 3px;
  }
  .button-text:last-child {
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
  }
  .button-text.selected {
    background: white;
    color: #1d8bf1;
    z-index: 1;
    position: relative;
  }
`;var T=r(1350);const M=m.c.div`
  & {
    margin: 30px 0;
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 5px;
    position: relative;
  }
  .close {
    position: absolute;
    top: 15px;
    right: 15px;
    cursor: pointer;
    opacity: 0.5;
    font-size: 40px;
    line-height: 22px;
  }
  .close:hover {
    opacity: 1;
  }
  .grid-wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 20px;
  }
  h3 {
    margin: 0 0 20px;
  }
  .box {
    cursor: pointer;
    width: 30px;
    height: 30px;
    border-radius: 5px;
    display: inline-block;
    margin: 0 20px 20px 0;
  }
  textarea {
    height: 184px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 20px;
    padding: 5px;
    font-size: 14px;
    border-color: #ccc;
  }
`,O=m.c.div`
   {
    width: 225px;
  }
`,S=m.c.div`
   {
    margin-top: 30px;
  }
`,j=m.c.button`
  & {
    margin: 0 20px 10px 0;
    -webkit-appearance: none;
    padding: 5px 15px;
    background: white;
    border: 1px solid #bbb;
    border-radius: 3px;
    cursor: pointer;
    text-transform: uppercase;
    font-size: 14px;
    color: #555;
  }
  &:hover {
    border-color: #888;
    color: #222;
  }
`;class A extends a.PureComponent{constructor(e){super(e),this.openClose=(()=>{this.setState({open:!this.state.open,colors:this.props.colors.join(",\n")})}),this.handleChange=((e,t)=>{this.setState({selectedColor:e,selectedPosition:t})}),this.pickerChange=(e=>{const{colors:t}=this.props;t[this.state.selectedPosition]=e.hex,this.props.updateColor(t),this.setState({selectedColor:e.hex,colors:t.join(",\n")})}),this.colorsFromTextarea=(()=>{const e=this.state.colors.replace(/\"/g,"").replace(/ /g,"").replace(/\[/g,"").replace(/\]/g,"").replace(/\r?\n|\r/g,"").split(",");this.props.updateColor(e)}),this.updateTextArea=(e=>{this.setState({colors:e.target.value})}),this.state={open:!1,selectedColor:e.colors[0],selectedPosition:0,colors:e.colors.join(",\n")}}render(){if(!this.state.open)return a.createElement("div",{style:{display:"inline-block"}},a.createElement(j,{onClick:this.openClose},"Adjust Palette"));const{colors:e}=this.props;return a.createElement(M,null,a.createElement("div",{className:"close",role:"button",tabIndex:0,onClick:this.openClose,onKeyPress:e=>{13===e.keyCode&&this.openClose()}},"×"),a.createElement("div",{className:"grid-wrapper"},a.createElement("div",null,a.createElement("h3",null,"Select Color"),e.map((e,t)=>a.createElement("div",{key:`color-${t}`,className:"box",style:{background:e},role:"button",tabIndex:0,onKeyPress:r=>{13===r.keyCode&&this.handleChange(e,t)},onClick:()=>this.handleChange(e,t)}))),a.createElement("div",null,a.createElement("h3",null,"Adjust Color"),a.createElement(O,null,a.createElement(T.ChromePicker,{color:this.state.selectedColor,onChangeComplete:this.pickerChange}))),a.createElement("div",null,a.createElement("h3",null,"Paste New Colors"),a.createElement("textarea",{value:this.state.colors,onChange:this.updateTextArea}),a.createElement(j,{onClick:this.colorsFromTextarea},"Update Colors"))),a.createElement(S,null,a.createElement("a",{href:`http://projects.susielu.com/viz-palette?colors=[${e.map(e=>`"${e}"`).join(",")}]&backgroundColor="white"&fontColor="black"`},"Evaluate This Palette with VIZ PALETTE")))}}A.defaultProps={metadata:{},height:500};var $=A;const P=m.c.span`
  & {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 5px;
    border-radius: 20px;
    margin-bottom: -5px;
  }
`,D=m.c.span`
  & {
    display: inline-block;
    min-width: 80px;
    margin: 5px;
  }
`,F=m.c.div`
  & {
    margin-top: 20px;
  }
`;var z=({values:e,colorHash:t,valueHash:r,colors:n=[],setColor:i})=>{return a.createElement(F,null,(e.length>18?[...e.filter((e,t)=>t<18),"Other"]:e).map((e,n)=>t[e]&&a.createElement(D,{key:`legend-item-${n}`},a.createElement(P,{style:{background:t[e]}}),a.createElement("span",{className:"html-legend-item"},e),r[e]&&r[e]>1&&`(${r[e]})`||"")),i&&a.createElement($,{colors:n,updateColor:e=>{i(e)}}))};var L=m.c.div.attrs(e=>({style:{transform:`translate(\n      ${e.x<100?"0px":"calc(-50% + 7px)"},\n      ${e.y<100?"10px":"calc(-100% - 10px)"}\n    )`}}))`
  color: black;
  padding: 10px;
  z-index: 999999;
  min-width: 120px;
  background: white;
  border: 1px solid #888;
  border-radius: 5px;
  position: relative;

  & p {
    font-size: 14px;
  }

  & h3 {
    margin: 0 0 10px;
  }

  &:before {
    ${e=>e.x<100?null:e.y<100?'\n      border-left: inherit;\n      border-top: inherit;\n      top: -8px;\n      left: calc(50% - 15px);\n      background: inherit;\n      content: "";\n      padding: 0px;\n      transform: rotate(45deg);\n      width: 15px;\n      height: 15px;\n      position: absolute;\n      z-index: 99;\n    ':'\n    border-right: inherit;\n    border-bottom: inherit;\n    bottom: -8px;\n    left: calc(50% - 15px);\n    background: inherit;\n    content: "";\n    padding: 0px;\n    transform: rotate(45deg);\n    width: 15px;\n    height: 15px;\n    position: absolute;\n    z-index: 99;\n  '}
  }
`,H=r(1442),N=r.n(H);function B(e){let t="0.[00]a";return 0===e?"0":(e>1e14||e<1e-5?t="0.[000]e+0":e<1&&(t="0.[0000]a"),N()(e).format(t))}const Z=m.c.p`
  margin: 20px 0 5px;
`,R=m.c.g`
  & text {
    text-anchor: end;
  }

  & :first-child {
    fill: white;
    stroke: white;
    opacity: 0.75;
    stroke-width: 2;
  }
`,G=[40,380];class V extends a.Component{constructor(e){super(e),this.brushing=((e,t)=>{const r=this.state.columnExtent;r[t]=e,this.setState({columnExtent:r})});const{options:t,data:r,schema:a}=this.props,{primaryKey:n}=t,i=function(e,t,r,a){const n={},i={};t.forEach(t=>{const r=[Math.min(...e.map(e=>e[t.name])),Math.max(...e.map(e=>e[t.name]))],a=Object(v.a)().domain(r).range([0,1]);n[t.name]=a;const o=Object(v.a)().domain(r).range([380,0]);i[t.name]=o});const o=[];return e.forEach(e=>{t.forEach(t=>{const i={metric:t.name,rawvalue:e[t.name],pctvalue:n[t.name](e[t.name])};r.forEach(t=>{"string"===t.type&&(i[t.name]=e[t.name])}),a.forEach(t=>{i[t]=e[t]}),o.push(i)})}),{dataPieces:o,scales:i}}(r,t.metrics,a.fields,n);this.state={filterMode:!0,data:i.dataPieces,dataScales:i.scales,columnExtent:t.metrics.reduce((e,t)=>(e[t.name]=[-1/0,1/0],e),{})}}shouldComponentUpdate(){return!0}render(){const{options:e,data:t}=this.props,{primaryKey:r,metrics:n,chart:i,colors:o,setColor:l}=e,{dim1:s}=i,{columnExtent:c,filterMode:m}=this.state,p=new Map;Object.keys(c).forEach(e=>{const t=c[e].sort((e,t)=>e-t);this.state.data.filter(r=>r.metric===e&&(r.pctvalue<t[0]||r.pctvalue>t[1])).forEach(e=>{p.set(r.map(t=>e[t]).join(","),!0)})});const d={},h=t.filter(e=>!p.get(r.map(t=>e[t]).join(","))),u=h.map(e=>r.map(t=>e[t]).join(" - ")),y={Other:"grey"};if(s&&"none"!==s){const{uniqueValues:e,valueHash:r}=h.reduce((e,t)=>{const r=t[s];return e.valueHash[r]=e.valueHash[r]&&e.valueHash[r]+1||1,e.uniqueValues=!e.uniqueValues.find(e=>e===r)&&[...e.uniqueValues,r]||e.uniqueValues,e},{uniqueValues:[],valueHash:{}});t.reduce((e,t)=>-1===e.indexOf(t[s])?[...e,t[s]]:e,[]).forEach((e,t)=>{y[e]=o[t%o.length]}),d.afterElements=e.length<=18?a.createElement(z,{values:e,colorHash:y,valueHash:r,setColor:l}):a.createElement(Z,null,u.length," items")}return m||(d.annotations=n.map(e=>({label:"",metric:e.name,type:"enclose-rect",color:"green",disable:["connector"],coordinates:[{metric:e.name,pctvalue:c[e.name][0]},{metric:e.name,pctvalue:c[e.name][1]}]})).filter(e=>0!==e.coordinates[0].pctvalue||1!==e.coordinates[1].pctvalue)),a.createElement("div",null,a.createElement(C,null,a.createElement("button",{className:`button-text ${m?"selected":""}`,onClick:()=>this.setState({filterMode:!0})},"Filter"),a.createElement("button",{className:`button-text ${m?"":"selected"}`,onClick:()=>this.setState({filterMode:!1})},"Explore")),a.createElement(k.ResponsiveOrdinalFrame,Object.assign({data:this.state.data,oAccessor:"metric",rAccessor:"pctvalue",type:{type:"point",r:2},connectorType:e=>r.map(t=>e[t]).join(","),style:e=>({fill:p.get(r.map(t=>e[t]).join(","))?"lightgray":y[e[s]],opacity:p.get(r.map(t=>e[t]).join(","))?.15:.99}),connectorStyle:e=>({stroke:p.get(r.map(t=>e.source[t]).join(","))?"gray":y[e.source[s]],strokeWidth:p.get(r.map(t=>e.source[t]).join(","))?1:1.5,strokeOpacity:p.get(r.map(t=>e.source[t]).join(","))?.1:1}),responsiveWidth:!0,margin:{top:20,left:20,right:20,bottom:100},oPadding:40,pixelColumnWidth:80,interaction:m?{columnsBrush:!0,during:this.brushing,extent:Object.keys(this.state.columnExtent)}:null,pieceHoverAnnotation:!m,tooltipContent:e=>{const t=p.get(r.map(t=>e[t]).join(","))?"grey":y[e[s]];return a.createElement(L,{x:e.x,y:e.y},a.createElement("h3",null,r.map(t=>e[t]).join(", ")),e[s]&&a.createElement("h3",{style:{color:t}},s,": ",e[s]),a.createElement("p",null,e.metric,": ",e.rawvalue))},canvasPieces:!0,canvasConnectors:!0,oLabel:e=>a.createElement("g",null,a.createElement("text",{transform:"rotate(45)"},e),a.createElement("g",{transform:"translate(-20,-395)"},a.createElement(k.Axis,{scale:this.state.dataScales[e],size:G,orient:"left",ticks:5,tickFormat:e=>a.createElement(R,null,a.createElement("text",null,B(e)),a.createElement("text",null,B(e)))})))},d)))}}V.defaultProps={metadata:{},height:500};var K=V;function W(e,t){return"function"==typeof t?t(e):e[t]}const I=(e,t,r,a)=>{const n={};let i=[];return a.forEach(r=>{const a=W(r,e);n[a]||(n[a]={array:[],value:0,label:a},i.push(n[a])),n[a].array.push(r),n[a].value+=W(r,t)}),i=i.sort((e,t)=>t.value===e.value?e.label<t.label?-1:(e.label,t.label,1):t.value-e.value),"none"!==r&&i.forEach(e=>{e.array=e.array.sort((e,t)=>W(t,r)-W(e,r))}),i.reduce((e,t)=>[...e,...t.array],[])};var X=r(131),Y=r(59);const U=(e,t)=>t=e.parent?U(e.parent,[e.key,...t]):["root",...t],q=(e,t)=>{if(0===t.depth)return"white";if(1===t.depth)return e[t.key];let r=t;for(let e=t.depth;e>1;e--)r=r.parent;return Object(Y.interpolateLab)("white",e[r.key])(Math.max(0,t.depth/6))};var J=r(86);const Q=Object(v.a)().domain([5,30]).range([8,16]).clamp(!0),_={force:e=>t=>({fill:e[t.source.id],stroke:e[t.source.id],strokeOpacity:.25}),sankey:e=>t=>({fill:e[t.source.id],stroke:e[t.source.id],strokeOpacity:.25}),matrix:e=>t=>({fill:e[t.source.id],stroke:"none"}),arc:e=>t=>({fill:"none",stroke:e[t.source.id],strokeWidth:t.weight||1,strokeOpacity:.75})},ee={force:e=>t=>({fill:e[t.id],stroke:e[t.id],strokeOpacity:.5}),sankey:e=>t=>({fill:e[t.id],stroke:e[t.id],strokeOpacity:.5}),matrix:e=>e=>({fill:"none",stroke:"#666",strokeOpacity:1}),arc:e=>t=>({fill:e[t.id],stroke:e[t.id],strokeOpacity:.5})},te=[{type:"frame-hover"},{type:"highlight",style:{stroke:"red",strokeOpacity:.5,strokeWidth:5,fill:"none"}}],re={force:te,sankey:te,matrix:[{type:"frame-hover"},{type:"highlight",style:{fill:"red",fillOpacity:.5}}],arc:te},ae={none:!1,static:!0,scaled:e=>!e.nodeSize||e.nodeSize<5?null:a.createElement("text",{textAnchor:"middle",y:Q(e.nodeSize)/2,fontSize:`${Q(e.nodeSize)}px`},e.id)},ne=Object(v.a)().domain([8,25]).range([14,8]).clamp(!0),ie=m.c.div`
  font-size: 14px;
  text-transform: uppercase;
  margin: 5px;
  font-weight: 900;
`,oe=m.c.div`
  fontsize: 12px;
  texttransform: uppercase;
  margin: 5px;
`,le={heatmap:k.heatmapping,hexbin:k.hexbinning},se=Object(v.b)().domain([.01,.2,.4,.6,.8]).range(["none","#FBEEEC","#f3c8c2","#e39787","#ce6751","#b3331d"]);const ce=(e,t,r,n="scatterplot")=>{const i=r.height-150||500,{chart:o,primaryKey:l,colors:s,setColor:c,dimensions:m}=r,{dim1:p,dim2:d,dim3:h,metric1:u,metric2:y,metric3:g}=o,b=e.filter(e=>e[u]&&e[y]&&(!g||"none"===g||e[g]));let f=()=>5;const x={Other:"grey"},E={};let k;if(d&&"none"!==d){const e=[...b].sort((e,t)=>t[u]-e[u]).filter((e,t)=>t<3),t=[...b].sort((e,t)=>t[y]-e[y]).filter(t=>-1===e.indexOf(t)).filter((e,t)=>t<3);k=function(e,t,r){const a=[],n={};return[...e,...t].forEach(e=>{const t=n[e[r]];if(t){const a=t.coordinates&&[...t.coordinates,e]||[e,t];Object.keys(n[e[r]]).forEach(t=>{delete n[e[r]][t]}),n[e[r]].id=e[r],n[e[r]].label=e[r],n[e[r]].type="react-annotation",n[e[r]].coordinates=a}else n[e[r]]=Object.assign({type:"react-annotation",label:e[r],id:e[r],coordinates:[]},e),a.push(n[e[r]])}),a}(e,t,d)}if(k=void 0,g&&"none"!==g){const e=Math.min(...b.map(e=>e[g])),t=Math.max(...b.map(e=>e[g]));f=Object(v.a)().domain([e,t]).range([2,20])}const w=I(u,"none"!==g&&g||y,"none",e);if(("scatterplot"===n||"contour"===n)&&p&&"none"!==p){const e=w.reduce((e,t)=>!e.find(e=>e===t[p].toString())&&[...e,t[p].toString()]||e,[]);e.forEach((e,t)=>{x[e]=t>18?"grey":s[t%s.length]}),E.afterElements=a.createElement(z,{valueHash:{},values:e,colorHash:x,setColor:c,colors:s})}let C=[];if("heatmap"===n||"hexbin"===n||"contour"===n&&"none"===h){if(C=[{coordinates:b}],"contour"!==n){const e=le[n]({areaType:{type:n,bins:10},data:{coordinates:b.map(e=>Object.assign({},e,{x:e[u],y:e[y]}))},size:[i,i]});C=e;const t=[.2,.4,.6,.8,1].map(t=>Math.floor(e.binMax*t)).reduce((e,t)=>0===t||-1!==e.indexOf(t)?e:[...e,t],[]),r=[0,...t],o=[];r.forEach((e,t)=>{const a=r[t+1];a&&o.push(`${e+1} - ${a}`)});const l=["#FBEEEC","#f3c8c2","#e39787","#ce6751","#b3331d"],m={};o.forEach((e,t)=>{m[e]=l[t]}),se.domain([.01,...t]).range(["none",...l.filter((e,r)=>r<t.length)]),E.afterElements=a.createElement(z,{valueHash:{},values:o,colorHash:m,colors:s,setColor:c})}}else if("contour"===n){const e={};C=[],b.forEach(t=>{e[t[p]]||(e[t[p]]={label:t[p],color:x[t[p]],coordinates:[]},C.push(e[t[p]])),e[t[p]].coordinates.push(t)})}const T=("scatterplot"===n||"contour"===n)&&e.length>999;return Object.assign({xAccessor:"hexbin"===n||"heatmap"===n?"x":u,yAccessor:"hexbin"===n||"heatmap"===n?"y":y,axes:[{orient:"left",ticks:6,label:y,tickFormat:B,baseline:"scatterplot"===n,tickSize:"heatmap"===n?0:void 0},{orient:"bottom",ticks:6,label:u,tickFormat:B,footer:"heatmap"===n,baseline:"scatterplot"===n,tickSize:"heatmap"===n?0:void 0}],points:("scatterplot"===n||"contour"===n)&&e,canvasPoints:T,areas:"scatterplot"!==n&&C,areaType:{type:n,bins:10,thresholds:"none"===h?6:3},areaStyle:e=>({fill:"contour"===n?"none":se((e.binItems||e.data.binItems).length),stroke:"contour"!==n?void 0:"none"===h?"#BBB":e.parentArea.color,strokeWidth:"contour"===n?2:1}),pointStyle:e=>({r:T?2:"contour"===n?3:f(e[g]),fill:x[e[p]]||"black",fillOpacity:.75,stroke:T?"none":"contour"===n?"white":"black",strokeWidth:"contour"===n?.5:1,strokeOpacity:.9}),hoverAnnotation:!0,responsiveWidth:!1,size:[i+225,i+80],margin:{left:75,bottom:50,right:150,top:30},annotations:"scatterplot"===n&&k||void 0,annotationSettings:{layout:{type:"marginalia",orient:"right",marginOffset:30}},tooltipContent:("hexbin"===n||"heatmap"===n)&&(e=>0===e.binItems.length?null:a.createElement(L,{x:e.x,y:e.y},a.createElement(ie,null,"ID, ",u,", ",y),e.binItems.map((e,t)=>{const r=m.map(t=>e[t.name].toString&&e[t.name].toString()||e[t.name]).join(",");return a.createElement(oe,{key:r+t},r,", ",e[u],", ",e[y])})))||(e=>a.createElement(L,{x:e.x,y:e.y},a.createElement("h3",null,l.map(t=>e[t]).join(", ")),m.map(t=>a.createElement("p",{key:`tooltip-dim-${t.name}`},t.name,":"," ",e[t.name].toString&&e[t.name].toString()||e[t.name])),a.createElement("p",null,u,": ",e[u]),a.createElement("p",null,y,": ",e[y]),g&&"none"!==g&&a.createElement("p",null,g,": ",e[g])))},E)},me={line:{Frame:k.ResponsiveXYFrame,controls:"switch between linetype",chartGenerator:(e,t,r)=>{let n;const{chart:i,selectedMetrics:o,lineType:l,metrics:s,primaryKey:c,colors:m}=r,{timeseriesSort:p}=i,d=t.fields.find(e=>e&&e.name===p),h="array-order"===p?"integer":d&&d.type?d.type:null,u=e=>"datetime"===h?e.toLocaleString().split(",")[0]:B(e),y="datetime"===h?Object(v.c)():Object(v.a)();return n=s.map((t,r)=>{const a="array-order"===p?e:e.sort((e,t)=>e[p]-t[p]);return{color:m[r%m.length],label:t.name,type:t.type,coordinates:a.map((e,a)=>({value:e[t.name],x:"array-order"===p?a:e[p],label:t.name,color:m[r%m.length],originalData:e}))}}).filter(e=>0===o.length||o.some(t=>t===e.label)),{lineType:{type:l,interpolator:J.curveMonotoneX},lines:n,xScaleType:y,renderKey:(e,t)=>e.coordinates?`line-${e.label}`:`linepoint=${e.label}-${t}`,lineStyle:e=>({fill:"line"===l?"none":e.color,stroke:e.color,fillOpacity:.75}),pointStyle:e=>({fill:e.color,fillOpacity:.75}),axes:[{orient:"left",tickFormat:B},{orient:"bottom",ticks:5,tickFormat:e=>{const t=u(e),r=t.length>4?"45":"0",n=t.length>4?"start":"middle";return a.createElement("text",{transform:`rotate(${r})`,textAnchor:n},t)}}],hoverAnnotation:!0,xAccessor:"x",yAccessor:"value",showLinePoints:"line"===l,margin:{top:20,right:200,bottom:"datetime"===h?80:40,left:50},legend:{title:"Legend",position:"right",width:200,legendGroups:[{label:"",styleFn:e=>({fill:e.color}),items:n}]},tooltipContent:e=>a.createElement(L,{x:e.x,y:e.y},a.createElement("p",null,e.parentLine&&e.parentLine.label),a.createElement("p",null,e.value&&e.value.toLocaleString()||e.value),a.createElement("p",null,p,": ",u(e.x)),c.map((t,r)=>a.createElement("p",{key:`key-${r}`},t,":"," ",e.originalData[t].toString&&e.originalData[t].toString()||e.originalData[t])))}}},scatter:{Frame:k.ResponsiveXYFrame,controls:"switch between modes",chartGenerator:ce},hexbin:{Frame:k.ResponsiveXYFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>ce(e,t,r,r.areaType)},bar:{Frame:k.ResponsiveOrdinalFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const{selectedDimensions:n,chart:i,colors:o,setColor:l}=r,{dim1:s,metric1:c,metric3:m}=i,p=0===n.length?s:e=>n.map(t=>e[t]).join(","),d=c,h={},u={Other:"grey"},y=I(p,"none"!==m&&m||d,s,e);m&&"none"!==m&&(h.dynamicColumnWidth=m);const g=y.reduce((e,t)=>e.find(e=>e===t[s].toString())?e:[...e,t[s].toString()],[]);s&&"none"!==s&&(g.forEach((e,t)=>{u[e]=t>18?"grey":o[t%o.length]}),h.afterElements=a.createElement(z,{valueHash:{},values:g,colorHash:u,setColor:l,colors:o}),n.length>0&&n.join(",")!==s&&(h.pieceHoverAnnotation=!0,h.tooltipContent=(e=>a.createElement(L,{x:e.x,y:e.y},s&&"none"!==s&&a.createElement("p",null,e[s]),a.createElement("p",null,"function"==typeof p?p(e):e[p]),a.createElement("p",null,d,": ",e[d]),m&&"none"!==m&&a.createElement("p",null,m,": ",e[m])))));const b=n.length>0&&!(1===n.length&&s===n[0])&&y.map(e=>e[s]).reduce((e,t)=>-1===e.indexOf(t)?[...e,t]:e,[]).length||0;return Object.assign({type:b>4?"clusterbar":"bar",data:y,oAccessor:p,rAccessor:d,style:e=>({fill:u[e[s]]||o[0],stroke:u[e[s]]||o[0]}),oPadding:g.length>30?1:5,oLabel:!(g.length>30)&&(e=>a.createElement("text",{transform:"rotate(90)"},e)),hoverAnnotation:!0,margin:{top:10,right:10,bottom:100,left:70},axis:{orient:"left",label:d,tickFormat:B},tooltipContent:e=>a.createElement(L,{x:e.column.xyData[0].xy.x,y:e.column.xyData[0].xy.y},a.createElement("p",null,"function"==typeof p?p(e.pieces[0]):e.pieces[0][p]),a.createElement("p",null,d,":"," ",e.pieces.map(e=>e[d]).reduce((e,t)=>e+t,0)),m&&"none"!==m&&a.createElement("p",null,m,":"," ",e.pieces.map(e=>e[m]).reduce((e,t)=>e+t,0))),baseMarkProps:{forceUpdate:!0}},h)}},summary:{Frame:k.ResponsiveOrdinalFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const n={},i={},{chart:o,summaryType:l,primaryKey:s,colors:c,setColor:m}=r,{dim1:p,metric1:d}=o,h=p,u=d,y=e.reduce((e,t)=>!e.find(e=>e===t[p].toString())&&[...e,t[p].toString()]||e,[]);return p&&"none"!==p&&(y.forEach((e,t)=>{i[e]=c[t%c.length]}),n.afterElements=a.createElement(z,{valueHash:{},values:y,colorHash:i,setColor:m,colors:c})),Object.assign({summaryType:{type:l,bins:16,amplitude:20},type:"violin"===l&&"swarm",projection:"horizontal",data:e,oAccessor:h,rAccessor:u,summaryStyle:e=>({fill:i[e[p]]||c[0],fillOpacity:.8,stroke:i[e[p]]||c[0]}),style:e=>({fill:i[e[p]]||c[0],stroke:"white"}),oPadding:5,oLabel:!(y.length>30)&&(e=>a.createElement("text",{textAnchor:"end",fontSize:`${e&&ne(e.length)||12}px`},e)),margin:{top:25,right:10,bottom:50,left:100},axis:{orient:"left",label:u,tickFormat:B},baseMarkProps:{forceUpdate:!0},pieceHoverAnnotation:"violin"===l,tooltipContent:e=>a.createElement(L,{x:e.x,y:e.y},a.createElement("h3",null,s.map(t=>e[t]).join(", ")),a.createElement("p",null,p,": ",e[p]),a.createElement("p",null,u,": ",e[u]))},n)}},network:{Frame:k.ResponsiveNetworkFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const{networkType:n="force",chart:i,colors:o}=r,{dim1:l,dim2:s,metric1:c,networkLabel:m}=i;if(!l||"none"===l||!s||"none"===s)return{};const p={},d=[];e.forEach(e=>{p[`${e[l]}-${e[s]}`]||(p[`${e[l]}-${e[s]}`]={source:e[l],target:e[s],value:0,weight:0},d.push(p[`${e[l]}-${e[s]}`])),p[`${e[l]}-${e[s]}`].value+=e[c]||1,p[`${e[l]}-${e[s]}`].weight+=1});const h={};return e.forEach(e=>{h[e[l]]||(h[e[l]]=o[Object.keys(h).length%o.length]),h[e[s]]||(h[e[s]]=o[Object.keys(h).length%o.length])}),d.forEach(e=>{e.weight=Math.min(10,e.weight)}),{edges:d,edgeType:"force"===n&&"halfarrow",edgeStyle:_[n](h),nodeStyle:ee[n](h),nodeSizeAccessor:e=>e.degree,networkType:{type:n,iterations:1e3},hoverAnnotation:re[n],tooltipContent:e=>a.createElement(L,{x:e.x,y:e.y},a.createElement("h3",null,e.id),a.createElement("p",null,"Links: ",e.degree),e.value&&a.createElement("p",null,"Value: ",e.value)),nodeLabels:"matrix"!==n&&ae[m],margin:{left:100,right:100,top:10,bottom:10}}}},hierarchy:{Frame:k.ResponsiveNetworkFrame,controls:"switch between modes",chartGenerator:(e,t,r)=>{const{hierarchyType:n="dendrogram",chart:i,selectedDimensions:o,primaryKey:l,colors:s}=r,{metric1:c}=i,m="sunburst"===n?"partition":n;if(0===o.length)return{};const p=Object(X.nest)();o.forEach(e=>{p.key(t=>t[e])});const d={},h=[];return e.forEach(e=>{d[e[o[0]]]||(d[e[o[0]]]=s[Object.keys(d).length]),h.push(Object.assign({},e,{sanitizedR:e.r,r:void 0}))}),{edges:{values:p.entries(h)},edgeStyle:()=>({fill:"lightgray",stroke:"gray"}),nodeStyle:e=>({fill:q(d,e),stroke:1===e.depth?"white":"black",strokeOpacity:.1*e.depth+.2}),networkType:{type:m,projection:"sunburst"===n&&"radial",hierarchySum:e=>e[c],hierarchyChildren:e=>e.values,padding:"treemap"===m?3:0},edgeRenderKey:(e,t)=>t,baseMarkProps:{forceUpdate:!0},margin:{left:100,right:100,top:10,bottom:10},hoverAnnotation:[{type:"frame-hover"},{type:"highlight",style:{stroke:"red",strokeOpacity:.5,strokeWidth:5,fill:"none"}}],tooltipContent:e=>a.createElement(L,{x:e.x,y:e.y},((e,t,r)=>{const n=e.parent?U(e.parent,e.key&&[e.key]||[]).join("->"):"",i=[];return e.parent?e.key?(i.push(a.createElement("h2",{key:"hierarchy-title"},e.key)),i.push(a.createElement("p",{key:"path-string"},n)),i.push(a.createElement("p",{key:"hierarchy-value"},"Total Value: ",e.value)),i.push(a.createElement("p",{key:"hierarchy-children"},"Children: ",e.children.length))):(i.push(a.createElement("p",{key:"leaf-label"},n,"->",t.map(t=>e[t]).join(", "))),i.push(a.createElement("p",{key:"hierarchy-value"},r,": ",e[r]))):i.push(a.createElement("h2",{key:"hierarchy-title"},"Root")),i})(e,l,c))}}},parallel:{Frame:K,controls:"switch between modes",chartGenerator:(e,t,r)=>({data:e,schema:t,options:r})}};var pe=r(207);const de="Line and stacked area charts for time series data where each row is a point and columns are data to be plotted.",he="Bar charts to compare individual and aggregate amounts.",ue="Scatterplot for comparing correlation between x and y values.",ye="A table of data.",ge="Force-directed, adjacency matrix, arc diagram and sankey network visualization suitable for data that is an edge list where one dimension represents source and another dimension represents target.",be="Distribution plots such as boxplots and violin plots to compare.",fe="Shows aggregate distribution of larger datasets across x and y metrics using hexbin, heatmap or contour plots.",xe="Parallel coordinates for comparing and filtering across different values in the dataset.",Ee="Nest data by categorical values using treemap, dendrogram, sunburst or partition.",ke={metric1:{default:"Plot this metric",scatter:"Plot this metric along the X axis",hexbin:"Plot this metric along the X axis"},metric2:{default:"Plot this metric along the Y axis"},metric3:{default:"Size the width of bars (Marimekko style) based on this metric",scatter:"Size the radius of points based on this metric"},dim1:{default:"Color items by this dimension",summary:"Group items into this category",network:"Use this dimension to determine the source node"},dim2:{default:"Label prominent datapoints using this dimension",network:"Use this dimension to determine the target node"},dim3:{default:"Split contours into separate groups based on this dimension"},networkType:"Represent network as a force-directed network (good for social networks) or as a sankey diagram (good for flow networks)",hierarchyType:"Represent your hierarchy as a tree (good for taxonomies) or a treemap (good for volumes) or partition (also good for volume where category volume is important)",timeseriesSort:"Sort line chart time series by its array position or by a specific metric or time",lineType:"Represent your data using a line chart, stacked area chart or ranked area chart",areaType:"Represent as a heatmap, hexbin or contour plot",lineDimensions:"Only plot the selected dimensions (or all if none are selected)"},ve=m.c.path`
  & {
    fill: var(--theme-app-bg);
    stroke: var(--theme-app-fg);
  }
`,we=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Summary Diagram"),a.createElement(ve,{d:"M 9.2300893,12.746467 15.329337,12.746467 M 0.73981357,15.376296 6.8390612,15.376296 M 3.9346579,0.6634694 3.9346579,15.376296 M 0.73981357,0.6634694 6.8390612,0.6634694 M 12.424932,1.5163867 12.424932,12.817543 M 9.2300893,1.5163867 15.329337,1.5163867 M 9.3149176,3.8522966 15.454941,3.8522966 15.454941,10.067428 9.3149176,10.067428 Z M 0.63101533,5.4042547 6.771038,5.4042547 6.771038,13.040916 0.63101533,13.040916 Z"})),Ce=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Dendrogram"),a.createElement(ve,{d:"M 5.3462352,16.86934 5.3462352,11.568531 M 5.0378073,11.186463 10.665375,16.453304 M 5.5794816,11.049276 -0.04808655,16.316116 M 10.903757,11.840357 10.903757,6.5395482 M 10.722225,5.9958343 16.349791,11.262675 M 10.758529,6.1997119 5.1309613,11.466552 M 5.3851096,6.1997401 5.3851096,0.06818774 M 5.3488028,0.96685111 10.976372,6.2336914 M 5.3851095,0.89889187 -0.24245868,6.1657322"})),Te=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Network"),a.createElement(ve,{d:"M 12.272948,3.9756652 9.2580839,6.8311579 M 3.7415227,3.9107679 6.435657,6.5066704 M 3.9981069,12.087859 6.6280954,9.6866496 M 12.208802,12.217654 9.0656456,9.556855 M 0.58721146,13.461599 A 2.0038971,2.0273734 0 0 0 2.591109,15.488973 2.0038971,2.0273734 0 0 0 4.5950056,13.461599 2.0038971,2.0273734 0 0 0 2.591109,11.434226 2.0038971,2.0273734 0 0 0 0.58721146,13.461599 Z M 11.483612,2.5370283 A 2.0038971,2.0273734 0 0 0 13.487509,4.5644013 2.0038971,2.0273734 0 0 0 15.491407,2.5370283 2.0038971,2.0273734 0 0 0 13.487509,0.50965432 2.0038971,2.0273734 0 0 0 11.483612,2.5370283 Z M 15.491407,13.461599 A 2.0038971,2.0273734 0 0 1 13.487509,15.488973 2.0038971,2.0273734 0 0 1 11.483612,13.461599 2.0038971,2.0273734 0 0 1 13.487509,11.434226 2.0038971,2.0273734 0 0 1 15.491407,13.461599 Z M 9.9298938,8.1089002 A 2.0038971,2.0273734 0 0 1 7.9259965,10.136275 2.0038971,2.0273734 0 0 1 5.9220989,8.1089002 2.0038971,2.0273734 0 0 1 7.9259965,6.0815273 2.0038971,2.0273734 0 0 1 9.9298938,8.1089002 Z M 4.5950056,2.5370283 A 2.0038971,2.0273734 0 0 1 2.591109,4.5644013 2.0038971,2.0273734 0 0 1 0.58721146,2.5370283 2.0038971,2.0273734 0 0 1 2.591109,0.50965432 2.0038971,2.0273734 0 0 1 4.5950056,2.5370283 Z"})),Me=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Scatterplot"),a.createElement(ve,{d:"M 6.2333524,7.1483631 A 2.1883047,2.1883047 0 0 1 4.0450478,9.3366678 2.1883047,2.1883047 0 0 1 1.8567431,7.1483631 2.1883047,2.1883047 0 0 1 4.0450478,4.9600585 2.1883047,2.1883047 0 0 1 6.2333524,7.1483631 Z M 12.201456,4.0316868 A 2.1883047,2.1883047 0 0 1 10.013151,6.2199914 2.1883047,2.1883047 0 0 1 7.8248465,4.0316868 2.1883047,2.1883047 0 0 1 10.013151,1.8433821 2.1883047,2.1883047 0 0 1 12.201456,4.0316868 Z M 14.787634,11.45866 A 2.1883047,2.1883047 0 0 1 12.599329,13.646965 2.1883047,2.1883047 0 0 1 10.411024,11.45866 2.1883047,2.1883047 0 0 1 12.599329,9.2703555 2.1883047,2.1883047 0 0 1 14.787634,11.45866 Z M 0.06631226,-0.01336003 0.06631226,16.100519 16.113879,16.100519"})),Oe=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Line Chart"),a.createElement(ve,{d:"M 1.98856,5.3983376 3.9789255,1.5485605 6.8981275,9.2481137 10.215403,6.6815963 15.257662,12.071285 M 0.46261318,0.00862976 0.46261318,15.600225 16.518227,15.600225"})),Se=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Hexbin"),a.createElement(ve,{d:"M 7.6646201,7.248835 10.200286,8.7365914 12.71271,7.2956277 12.71271,4.2993354 10.200286,2.8583717 7.6481891,4.3220885 Z M 2.5260861,7.248835 5.0617524,8.7365914 7.5741798,7.2956277 7.5741798,4.2993354 5.0617524,2.8583717 2.509655,4.3220885 Z M 10.151008,11.430063 12.686686,12.917818 15.199098,11.476854 15.199098,8.4805611 12.686686,7.0395985 10.134577,8.5033165 Z M 5.0124743,11.430063 7.5481406,12.917818 10.060567,11.476854 10.060567,8.4805611 7.5481406,7.0395985 4.9960421,8.5033165 Z M 0.59322509,-0.02976587 0.59322509,16.053058 16.562547,16.008864"})),je=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Bar Chart"),a.createElement(ve,{d:"M 11.58591,8.3025699 15.255735,8.3025699 15.255735,15.691481 11.58591,15.691481 Z M 6.2401471,3.973457 9.9358173,3.973457 9.9358173,15.626376 6.2401471,15.626376 Z M 0.533269,0.53717705 4.6376139,0.53717705 4.6376139,15.583893 0.533269,15.583893 Z"})),Ae=e=>a.createElement(pe.h,{width:16,height:16,viewBox:"0 0 16 16",outerProps:e},a.createElement("title",null,"Parallel Coordinates"),a.createElement(ve,{d:"M 2.7232684,11.593098 8.8105743,9.8309837 14.417303,4.2242547 M 12.356336,0.72968704 15.29192,0.72968704 15.29192,8.4261754 12.356336,8.4261754 Z M 6.8447585,6.4156084 10.103282,6.4156084 10.103282,12.352066 6.8447585,12.352066 Z M 0.51572132,6.0114684 3.9294777,6.0114684 3.9294777,16.25395 0.51572132,16.25395 Z"})),$e="\nwidth: 32px;\nheight: 32px;\ncursor: pointer;\ncolor: var(--theme-app-fg);\n",Pe=m.c.button`
  ${$e}
  border: 1px solid var(--theme-app-fg);
  background-color: var(--theme-app-bg);
`,De=m.c.button`
  ${$e}

  border: 1px outset #666;
  background-color: #aaa;
`;class Fe extends a.PureComponent{render(){const{message:e,onClick:t,children:r,selected:n}=this.props,{title:i=e}=this.props,o=n?De:Pe;return a.createElement(o,{onClick:t,key:e,title:i},r)}}const ze=m.c.div`
  display: flex;
  flex-flow: column nowrap;
  z-index: 1;
  padding: 5px;
`,Le=({dimensions:e,setGrid:t,setView:r,currentView:n})=>a.createElement(ze,{className:"dx-button-bar"},a.createElement(Fe,{title:ye,onClick:t,message:"Data Table",selected:!1},a.createElement(pe.d,null)),e.length>0&&a.createElement(Fe,{title:he,onClick:()=>r("bar"),selected:"bar"===n,message:"Bar Graph"},a.createElement(je,null)),a.createElement(Fe,{title:be,onClick:()=>r("summary"),selected:"summary"===n,message:"Summary"},a.createElement(we,null)),a.createElement(Fe,{title:ue,onClick:()=>r("scatter"),selected:"scatter"===n,message:"Scatter Plot"},a.createElement(Me,null)),a.createElement(Fe,{title:fe,onClick:()=>r("hexbin"),selected:"hexbin"===n,message:"Area Plot"},a.createElement(Se,null)),e.length>1&&a.createElement(Fe,{title:ge,onClick:()=>r("network"),selected:"network"===n,message:"Network"},a.createElement(Te,null)),e.length>0&&a.createElement(Fe,{title:Ee,onClick:()=>r("hierarchy"),selected:"hierarchy"===n,message:"Hierarchy"},a.createElement(Ce,null)),e.length>0&&a.createElement(Fe,{title:xe,onClick:()=>r("parallel"),selected:"parallel"===n,message:"Parallel Coordinates"},a.createElement(Ae,null)),a.createElement(Fe,{title:de,onClick:()=>r("line"),selected:"line"===n,message:"Line Graph"},a.createElement(Oe,null))),He=["#DA752E","#E5C209","#1441A0","#B86117","#4D430C","#1DB390","#B3331D","#088EB2","#417505","#E479A8","#F9F39E","#5782DC","#EBA97B","#A2AB60","#B291CF","#8DD2C2","#E6A19F","#3DC7E0","#98CE5B"];var Ne=r(1443),Be=r(929),Ze=r(1717);const Re=a.createElement(Ne.a,{disabled:!0,text:"No results."}),Ge=a.createElement("marker",{id:"arrow",refX:"3",refY:"3",markerWidth:"6",markerHeight:"6",orient:"auto-start-reverse"},a.createElement("path",{fill:"#5c7080",d:"M 0 0 L 6 3 L 0 6 z"})),Ve={width:"16px",height:"16px",className:"bp3-icon"},Ke=a.createElement("svg",Object.assign({},Ve),a.createElement("defs",null,Ge),a.createElement("polyline",{points:"3,3 3,13 12,13",fill:"none",stroke:"#5c7080",markerEnd:"url(#arrow)"})),We={Y:a.createElement("svg",Object.assign({},Ve),a.createElement("defs",null,Ge),a.createElement("polyline",{points:"3,3 3,13 12,13",fill:"none",stroke:"#5c7080",markerStart:"url(#arrow)"})),X:Ke,Size:a.createElement("svg",Object.assign({},Ve),a.createElement("circle",{cx:3,cy:13,r:2,fill:"none",stroke:"#5c7080"}),a.createElement("circle",{cx:6,cy:9,r:3,fill:"none",stroke:"#5c7080"}),a.createElement("circle",{cx:9,cy:5,r:4,fill:"none",stroke:"#5c7080"})),Color:a.createElement("svg",Object.assign({},Ve),a.createElement("circle",{cx:3,cy:11,r:3,fill:"rgb(179, 51, 29)"}),a.createElement("circle",{cx:13,cy:11,r:3,fill:"rgb(87, 130, 220)"}),a.createElement("circle",{cx:8,cy:5,r:3,fill:"rgb(229, 194, 9)"}))},Ie=(e,{handleClick:t,modifiers:r})=>{if(!r.matchesPredicate)return null;const n=`${e.label}`;return a.createElement(Ne.a,{active:r.active,disabled:r.disabled,key:n,onClick:t,text:n})},Xe=(e,t)=>`${t.label.toLowerCase()}`.indexOf(e.toLowerCase())>=0,Ye=e=>"X"===e||"Y"===e||"Size"===e||"Color"===e?We[e]:e,Ue=m.b`
  h2 {
    text-transform: capitalize;
    margin-bottom: 10px;
  }
  select {
    height: 30px;
  }

  .selected {
    background-color: #d8e1e8 !important;
    background-image: none !important;
  }
`,qe=m.c.div`
  margin-right: 30px;
  ${Ue}
`,Je=m.c.div`
  display: flex;
  justify-content: left;
  margin-bottom: 30px;
  ${Ue}
`,Qe=(e,t,r,n,o,l="Help me help you help yourself")=>{const s=n?e:["none",...e];let c;return c=s.length>1?a.createElement(Ze.a,{items:s.map(e=>({value:e,label:e})),query:o,noResults:Re,onItemSelect:(e,r)=>{t(e.value)},itemRenderer:Ie,itemPredicate:Xe,resetOnClose:!0},a.createElement(i.a,{icon:Ye(r),text:o,rightIcon:"double-caret-vertical"})):a.createElement("p",{style:{margin:0}},s[0]),a.createElement(qe,{title:l},a.createElement("div",null,a.createElement(Be.a,null,r)),c)},_e=[{type:"line",label:"Line Chart"},{type:"stackedarea",label:"Stacked Area Chart"},{type:"stackedpercent",label:"Stacked Area Chart (Percent)"},{type:"bumparea",label:"Ranked Area Chart"}],et=[{type:"hexbin",label:"Hexbin"},{type:"heatmap",label:"Heatmap"},{type:"contour",label:"Contour Plot"}];var tt=({view:e,chart:t,metrics:r,dimensions:n,updateChart:o,selectedDimensions:l,selectedMetrics:s,hierarchyType:c,summaryType:m,networkType:p,setLineType:d,updateMetrics:h,updateDimensions:u,lineType:y,areaType:g,setAreaType:b,data:f})=>{const x=r.map(e=>e.name),E=n.map(e=>e.name),k=e=>r=>o({chart:Object.assign({},t,{[e]:r})}),v=(e,t)=>{if(Object.keys(ke).find(e=>e===t)){const r=t,a=void 0!==ke[r]?ke[r]:null;return null==a?"":"string"==typeof a?a:null!=a[e]?a[e]:a.default}return""};return a.createElement(a.Fragment,null,a.createElement(Je,null,("summary"===e||"scatter"===e||"hexbin"===e||"bar"===e||"network"===e||"hierarchy"===e)&&Qe(x,k("metric1"),"scatter"===e||"hexbin"===e?"X":"Metric",!0,t.metric1,v(e,"metric1")),("scatter"===e||"hexbin"===e)&&Qe(x,k("metric2"),"Y",!0,t.metric2,v(e,"metric2")),("scatter"===e&&f.length<1e3||"bar"===e)&&Qe(x,k("metric3"),"bar"===e?"Width":"Size",!1,t.metric3,v(e,"metric3")),("summary"===e||"scatter"===e||"hexbin"===e&&"contour"===g||"bar"===e||"parallel"===e)&&Qe(E,k("dim1"),"summary"===e?"Category":"Color",!0,t.dim1,v(e,"dim1")),"scatter"===e&&Qe(E,k("dim2"),"Labels",!1,t.dim2,v(e,"dim2")),"hexbin"===e&&"contour"===g&&Qe(["by color"],k("dim3"),"Multiclass",!1,t.dim3,v(e,"dim3")),"network"===e&&Qe(E,k("dim1"),"SOURCE",!0,t.dim1,v(e,"dim1")),"network"===e&&Qe(E,k("dim2"),"TARGET",!0,t.dim2,v(e,"dim2")),"network"===e&&Qe(["matrix","arc","force","sankey"],e=>o({networkType:e}),"Type",!0,p,ke.networkType),"network"===e&&Qe(["static","scaled"],k("networkLabel"),"Show Labels",!1,t.networkLabel,ke.networkLabel),"hierarchy"===e&&Qe(["dendrogram","treemap","partition","sunburst"],e=>o({hierarchyType:e}),"Type",!0,c,ke.hierarchyType),"summary"===e&&Qe(["violin","boxplot","joy","heatmap","histogram"],e=>o({summaryType:e}),"Type",!0,m,ke.summaryType),"line"===e&&Qe(["array-order",...x],k("timeseriesSort"),"Sort by",!0,t.timeseriesSort,ke.timeseriesSort),"line"===e&&a.createElement("div",{title:ke.lineType,style:{display:"inline-block"}},a.createElement("div",null,a.createElement(Be.a,null,"Chart Type")),a.createElement(C,{vertical:!0},_e.map(e=>a.createElement(i.a,{key:e.type,className:`button-text ${y===e.type&&"selected"}`,active:y===e.type,onClick:()=>d(e.type)},e.label)))),"hexbin"===e&&a.createElement("div",{className:"control-wrapper",title:ke.areaType},a.createElement("div",null,a.createElement(Be.a,null,"Chart Type")),a.createElement(C,{vertical:!0},et.map(e=>{const t=e.type;return"contour"===t||"hexbin"===t||"heatmap"===t?a.createElement(i.a,{className:`button-text ${g===t&&"selected"}`,key:t,onClick:()=>b(t),active:g===t},e.label):a.createElement("div",null)}))),"hierarchy"===e&&a.createElement("div",{className:"control-wrapper",title:ke.nestingDimensions},a.createElement("div",null,a.createElement(Be.a,null,"Nesting")),0===l.length?"Select categories to nest":`root, ${l.join(", ")}`),("bar"===e||"hierarchy"===e)&&a.createElement("div",{className:"control-wrapper",title:ke.barDimensions},a.createElement("div",null,a.createElement(Be.a,null,"Categories")),a.createElement(C,{vertical:!0},n.map(e=>a.createElement(i.a,{key:`dimensions-select-${e.name}`,className:`button-text ${-1!==l.indexOf(e.name)&&"selected"}`,onClick:()=>u(e.name),active:-1!==l.indexOf(e.name)},e.name)))),"line"===e&&a.createElement("div",{className:"control-wrapper",title:ke.lineDimensions},a.createElement("div",null,a.createElement(Be.a,null,"Metrics")),a.createElement(C,{vertical:!0},r.map(e=>a.createElement(i.a,{key:`metrics-select-${e.name}`,className:`button-text ${-1!==s.indexOf(e.name)&&"selected"}`,onClick:()=>h(e.name),active:-1!==s.indexOf(e.name)},e.name))))))};const rt="application/vnd.dataresource+json",at=({view:e,lineType:t,areaType:r,selectedDimensions:a,selectedMetrics:n,pieceType:i,summaryType:o,networkType:l,hierarchyType:s,chart:c})=>`${e}-${t}-${r}-${a.join(",")}-${n.join(",")}-${i}-${o}-${l}-${s}-${JSON.stringify(c)}`,nt=[500,300],it=m.c.div`
  & {
    font-family: Source Sans Pro, Helvetica Neue, Helvetica, Arial, sans-serif;
  }
`,ot=m.c.div`
  & {
    backgroundcolor: #cce;
    padding: 10px;
    paddingleft: 20px;
  }
`,lt=({metadata:e})=>{const t=e&&e.sampled?a.createElement("span",null,a.createElement("b",null,"NOTE:")," This data is sampled"):null;return a.createElement(it,null,t?a.createElement(ot,null,t):null)},st=m.c.div`
  display: flex;
  flex-flow: row nowrap;
  width: 100%;
`,ct=m.c.div`
  flex: 1;
`,mt=m.c.div`
  width: "calc(100vw - 200px)";
  .html-legend-item {
    color: var(--theme-app-fg);
  }

  .tick > path {
    stroke: lightgray;
  }

  .axis-labels,
  .ordinal-labels {
    fill: var(--theme-app-fg);
    font-size: 14px;
  }

  path.connector,
  path.connector-end {
    stroke: var(--theme-app-fg);
  }

  path.connector-end {
    fill: var(--theme-app-fg);
  }

  text.annotation-note-label,
  text.legend-title,
  .legend-item text {
    fill: var(--theme-app-fg);
    stroke: none;
  }

  .xyframe-area > path {
    stroke: var(--theme-app-fg);
  }

  .axis-baseline {
    stroke-opacity: 0.25;
    stroke: var(--theme-app-fg);
  }
  circle.frame-hover {
    fill: none;
    stroke: gray;
  }
  .rect {
    stroke: green;
    stroke-width: 5px;
    stroke-opacity: 0.5;
  }
  rect.selection {
    opacity: 0.5;
  }
`;class pt extends a.PureComponent{constructor(e){super(e),this.updateChart=(e=>{const{view:t,dimensions:r,metrics:n,chart:i,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:d,hierarchyType:h,colors:u,primaryKey:y,data:g}=Object.assign({},this.state,e);if(!this.props.data&&!this.props.metadata&&!this.props.initialView)return;const{data:b,height:f,onMetadataChange:x}=this.props,{Frame:E,chartGenerator:k}=me[t],v=at({view:t,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:d,hierarchyType:h,chart:i}),w=k(g,b.schema,{metrics:n,dimensions:r,chart:i,colors:u,height:f,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:d,hierarchyType:h,primaryKey:y,setColor:this.setColor}),C=a.createElement(mt,null,a.createElement(E,Object.assign({responsiveWidth:!0,size:nt},w)),a.createElement(tt,Object.assign({},{data:g,view:t,chart:i,metrics:n,dimensions:r,selectedDimensions:s,selectedMetrics:c,hierarchyType:h,summaryType:p,networkType:d,updateChart:this.updateChart,updateDimensions:this.updateDimensions,setLineType:this.setLineType,updateMetrics:this.updateMetrics,lineType:o,setAreaType:this.setAreaType,areaType:l})));x&&x(Object.assign({},this.props.metadata,{dx:{view:t,lineType:o,areaType:l,selectedDimensions:s,selectedMetrics:c,pieceType:m,summaryType:p,networkType:d,hierarchyType:h,colors:u,chart:i}}),rt),this.setState(t=>Object.assign({},e,{displayChart:Object.assign({},t.displayChart,{[v]:C})}))}),this.setView=(e=>{this.updateChart({view:e})}),this.setGrid=(()=>{this.setState({view:"grid"})}),this.setColor=(e=>{this.updateChart({colors:e})}),this.setLineType=(e=>{this.updateChart({lineType:e})}),this.setAreaType=(e=>{this.updateChart({areaType:e})}),this.updateDimensions=(e=>{const t=this.state.selectedDimensions,r=-1===t.indexOf(e)?[...t,e]:t.filter(t=>t!==e);this.updateChart({selectedDimensions:r})}),this.updateMetrics=(e=>{const t=this.state.selectedMetrics,r=-1===t.indexOf(e)?[...t,e]:t.filter(t=>t!==e);this.updateChart({selectedMetrics:r})});const{metadata:t,initialView:r}=e,n=t.dx||{},i=n.chart||{},{fields:o=[],primaryKey:l=[]}=e.data.schema,s=o.filter(e=>"string"===e.type||"boolean"===e.type||"datetime"===e.type),c=e.data.data.map(e=>{const t=Object.assign({},e);return o.forEach(e=>{"datetime"===e.type&&(t[e.name]=new Date(t[e.name]))}),t}),m=o.filter(e=>"integer"===e.type||"number"===e.type||"datetime"===e.type).filter(e=>!l.find(t=>t===e.name));this.state=Object.assign({view:r,lineType:"line",areaType:"hexbin",selectedDimensions:[],selectedMetrics:[],pieceType:"bar",summaryType:"violin",networkType:"force",hierarchyType:"dendrogram",dimensions:s,metrics:m,colors:He,chart:Object.assign({metric1:m[0]&&m[0].name||"none",metric2:m[1]&&m[1].name||"none",metric3:"none",dim1:s[0]&&s[0].name||"none",dim2:s[1]&&s[1].name||"none",dim3:"none",timeseriesSort:"array-order",networkLabel:"none"},i),displayChart:{},primaryKey:l,data:c},n)}componentDidMount(){"grid"!==this.state.view&&this.updateChart(this.state)}render(){const{view:e,dimensions:t,chart:r,lineType:n,areaType:i,selectedDimensions:o,selectedMetrics:l,pieceType:s,summaryType:c,networkType:m,hierarchyType:p}=this.state;let d=null;if("grid"===e)d=a.createElement(E,Object.assign({},this.props));else if(["line","scatter","bar","network","summary","hierarchy","hexbin","parallel"].includes(e)){const t=at({view:e,lineType:n,areaType:i,selectedDimensions:o,selectedMetrics:l,pieceType:s,summaryType:c,networkType:m,hierarchyType:p,chart:r});d=this.state.displayChart[t]}return a.createElement("div",null,a.createElement(lt,{metadata:this.props.metadata}),a.createElement(st,null,a.createElement(ct,null,d),a.createElement(Le,{dimensions:t,setGrid:this.setGrid,setView:this.setView,currentView:e})))}}pt.MIMETYPE=rt,pt.defaultProps={metadata:{dx:{}},height:500,mediaType:rt,initialView:"grid"};t.default=pt}}]);