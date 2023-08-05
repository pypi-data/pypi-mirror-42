(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{1216:function(e,t,o){"use strict";var r=o(63),n=o(207),l=o(2),a=o(81),i=o(44);const c=i.c.div`
  display: none;
  background: var(--theme-cell-creator-bg);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
  pointer-events: all;
  position: relative;
  top: -5px;

  button {
    display: inline-block;

    width: 22px;
    height: 20px;
    padding: 0px 4px;

    text-align: center;

    border: none;
    outline: none;
    background: none;
  }

  button span {
    font-size: 15px;
    line-height: 1;

    color: var(--theme-cell-creator-fg);
  }

  button span:hover {
    color: var(--theme-cell-creator-fg-hover);
  }

  .octicon {
    transition: color 0.5s;
  }
`,s=i.c.div`
  display: block;
  position: relative;
  overflow: visible;
  height: 0px;
`,d=i.c.div`
  position: relative;
  overflow: visible;
  top: -10px;
  height: 60px;
  text-align: center;

  &:hover ${c} {
    display: inline-block;
  }
`;class p extends l.PureComponent{constructor(){super(...arguments),this.createMarkdownCell=(()=>{this.props.createCell("markdown")}),this.createCodeCell=(()=>{this.props.createCell("code")})}render(){return l.createElement(s,null,l.createElement(d,null,l.createElement(c,null,l.createElement("button",{onClick:this.createMarkdownCell,title:"create text cell",className:"add-text-cell"},l.createElement("span",{className:"octicon"},l.createElement(n.g,null))),l.createElement("button",{onClick:this.createCodeCell,title:"create code cell",className:"add-code-cell"},l.createElement("span",{className:"octicon"},l.createElement(n.c,null))))))}}t.a=Object(a.b)(null,e=>({createCellAbove:t=>e(r.createCellAbove(t)),createCellAppend:t=>e(r.createCellAppend(t)),createCellBelow:t=>e(r.createCellBelow(t))}))(class extends l.PureComponent{constructor(){super(...arguments),this.createCell=(e=>{const{above:t,createCellBelow:o,createCellAppend:r,createCellAbove:n,id:l,contentRef:a}=this.props;void 0!==l&&"string"==typeof l?t?n({cellType:e,id:l,contentRef:a}):o({cellType:e,id:l,source:"",contentRef:a}):r({cellType:e,contentRef:a})})}render(){return l.createElement(p,{above:this.props.above,createCell:this.createCell})}})},1217:function(e,t,o){"use strict";var r=o(2),n=o(586),l=o(44);const a=["data:image/png;base64,","iVBORw0KGgoAAAANSUhEUgAAADsAAAAzCAYAAAApdnDeAAAAAXNSR0IArs4c6QAA","AwNJREFUaAXtmlFL3EAUhe9MZptuoha3rLWgYC0W+lj/T3+26INvXbrI2oBdE9km","O9Nzxu1S0LI70AQScyFmDDfkfvdMZpNwlCCccwq7f21MaVM4FPtkU0o59RdoJBMx","WZINBg+DQWGKCAk+2kIKFh9JlSzLYVmOilEpR1Kh/iUbQFiNQTSbzWJrbYJximOJ","cSaulpVRoqh4K8JhjprIVJWqFlCpQNG51roYj8cLjJcGf5RMZWC1TYw1o2LxcEmy","0jeEo3ZFWVHIx0ji4eeKHFOx8l4sVVVZnBE6tWLHq7xO7FY86YpPeVjeo5y61tlR","JyhXEOQhF/lw6BGWixHvUWXVTpdgyUMu8q1h/ZJbqQhdiLsESx4FLvL9gcV6q3Cs","0liq2IHuBHjItYIV3rMvJnrYrkrdK9sr24EO9NO4AyI+i/CilOXbTi1xeXXFTyAS","GSOfzs42XmM+v5fJ5JvP29/fl8PDw43nhCbUpuzFxYXs7OxKmqZb1WQGkc/P80K+","T6dbnROaVJuyfPY+Pj7aup7h66HP/1Uu5O7u59bnhSTWpmxIEU3l9rBNdbrp6/TK","Nt3xpq7XK9tUp5u+Tm2/s/jYJdfX12LwBHVycrKRK89zmeJhYnZ7K3Fcz3e/2mDP","z7/waZEf8zaC+gSkKa3l4OBA3uztbXdOYFZtsKcfToNKSZNUPp6GnRN0AST3C1Ro","x9qS3yvbFqVC6+yVDe1YW/J7ZduiVGidvbKhHWtLfq9sW5QKrdMri9cxB6OFhQmO","TrDuBHjIRT5CEZZj0i7xOkYnWGeCPOQiHqC8lc/R60cLnNPuvjOkns7dk4t8/Jfv","s46mRlWqQiudxebVV3gAj7C9hXsmgZeztnfe/91YODEr3IoF/JY/sE2gbGaVLci3","hh0tRtWNvsm16JmNcOs6N9dW72LP7yOtWbEhjAUkZ+icoJ5HbE6+NSxMjKWe6cKb","GkUWgMwiFbXSlRpFkXelUlF4F70rVd7Bd4oZ/LL8xiDmtPV2Nwyf2zOlTfHERY7i","Haa1+w2+iFqx0aIgvgAAAABJRU5ErkJggg=="].join(""),i={beginDrag:e=>({id:e.id})},c=l.c.div.attrs({role:"presentation"})`
  position: absolute;
  z-index: 200;
  width: var(--prompt-width, 50px);
  height: 100%;
  cursor: move;
`,s=l.c.div.attrs(e=>({style:{opacity:e.isDragging?.25:1,borderTop:e.isOver&&e.hoverUpperHalf?"3px lightgray solid":"3px transparent solid",borderBottom:e.isOver&&!e.hoverUpperHalf?"3px lightgray solid":"3px transparent solid"}}))`
  position: relative;
  padding: 10px;
`;function d(e,t,o){const r=o.getBoundingClientRect(),n=(r.bottom-r.top)/2;return t.getClientOffset().y-r.top<n}const p={drop(e,t,o){if(t){const r=d(0,t,o.el);e.moveCell({id:t.getItem().id,destinationId:e.id,above:r,contentRef:e.contentRef})}},hover(e,t,o){t&&o.setState({hoverUpperHalf:d(0,t,o.el)})}};const h=Object(n.DragSource)("CELL",i,function(e,t){return{connectDragSource:e.dragSource(),isDragging:t.isDragging(),connectDragPreview:e.dragPreview()}}),m=Object(n.DropTarget)("CELL",p,function(e,t){return{connectDropTarget:e.dropTarget(),isOver:t.isOver()}});t.a=h(m(class extends r.Component{constructor(){super(...arguments),this.state={hoverUpperHalf:!0},this.selectCell=(()=>{const{focusCell:e,id:t,contentRef:o}=this.props;e({id:t,contentRef:o})})}componentDidMount(){const e=this.props.connectDragPreview,t=new window.Image;t.src=a,t.onload=(()=>{e(t)})}render(){return this.props.connectDropTarget(r.createElement("div",null,r.createElement(s,{isDragging:this.props.isDragging,hoverUpperHalf:this.state.hoverUpperHalf,isOver:this.props.isOver,ref:e=>{this.el=e}},this.props.connectDragSource(r.createElement("div",null,r.createElement(c,{onClick:this.selectCell}))),this.props.children)))}}))},1234:function(e,t,o){"use strict";o.r(t);var r=o(66),n=o.n(r);o(603),o(601);n.a.defineMode("ipython",(e,t)=>{const o=Object.assign({},t,{name:"python",singleOperators:new RegExp("^[\\+\\-\\*/%&|@\\^~<>!\\?]"),identifiers:new RegExp("^[_A-Za-z¡-￿][_A-Za-z0-9¡-￿]*")});return n.a.getMode(e,o)},"python"),n.a.defineMIME("text/x-ipython","ipython")},1235:function(e,t,o){"use strict";o.d(t,"a",function(){return n});var r=o(2);class n extends r.Component{constructor(){super(...arguments),this.el=null}scrollIntoViewIfNeeded(e){const t=this.el&&this.el.parentElement&&this.el.parentElement.querySelector(":hover")===this.el;this.props.focused&&e!==this.props.focused&&!t&&(this.el&&"scrollIntoViewIfNeeded"in this.el?this.el.scrollIntoViewIfNeeded():this.el&&this.el.scrollIntoView())}componentDidUpdate(e){this.scrollIntoViewIfNeeded(e.focused)}componentDidMount(){this.scrollIntoViewIfNeeded()}render(){return r.createElement("div",{onClick:this.props.onClick,role:"presentation",ref:e=>{this.el=e}},this.props.children)}}},1236:function(e,t,o){"use strict";o.d(t,"a",function(){return c});var r=o(693),n=o(689),l=o(2),a=o.n(l);const i=()=>{};class c extends a.a.Component{constructor(e){super(e),this.state={view:!0},this.openEditor=this.openEditor.bind(this),this.editorKeyDown=this.editorKeyDown.bind(this),this.renderedKeyDown=this.renderedKeyDown.bind(this),this.closeEditor=this.closeEditor.bind(this)}componentDidMount(){this.updateFocus()}componentWillReceiveProps(e){this.setState({view:!e.editorFocused})}componentDidUpdate(){this.updateFocus()}updateFocus(){this.rendered&&this.state&&this.state.view&&this.props.cellFocused&&(this.rendered.focus(),this.props.editorFocused&&this.openEditor())}editorKeyDown(e){const t=e.shiftKey,o=e.ctrlKey;(t||o)&&"Enter"===e.key&&this.closeEditor()}closeEditor(){this.setState({view:!0}),this.props.unfocusEditor()}openEditor(){this.setState({view:!1}),this.props.focusEditor()}renderedKeyDown(e){const t=e.shiftKey,o=e.ctrlKey;if(!t&&!o||"Enter"!==e.key)switch(e.key){case"Enter":return this.openEditor(),void e.preventDefault();case"ArrowUp":this.props.focusAbove();break;case"ArrowDown":this.props.focusBelow()}else{if(this.state.view)return;this.closeEditor()}}render(){const e=this.props.source;return this.state&&this.state.view?a.a.createElement("div",{onDoubleClick:this.openEditor,onKeyDown:this.renderedKeyDown,ref:e=>{this.rendered=e},tabIndex:this.props.cellFocused?0:void 0,style:{outline:"none"}},a.a.createElement(n.e,null,a.a.createElement(r.a,{source:e||"*Empty markdown cell, double click me to add content.*"}))):a.a.createElement("div",{onKeyDown:this.editorKeyDown},a.a.createElement(n.c,null,a.a.createElement(n.h,null),this.props.children),a.a.createElement(n.e,{hidden:""===e},a.a.createElement(r.a,{source:e||"*Empty markdown cell, double click me to add content.*"})))}}c.defaultProps={cellFocused:!1,editorFocused:!1,focusAbove:i,focusBelow:i,focusEditor:i,unfocusEditor:i,source:""}},1237:function(e,t,o){"use strict";var r=o(121),n=o(1238),l=o.n(n),a=o(2),i=o.n(a),c=o(81),s=o(44);const d=s.c.div`
  float: left;
  display: block;
  padding-left: 10px;
`,p=s.c.div`
  float: right;
  padding-right: 10px;
  display: block;
`,h=s.c.div`
  padding-top: 8px;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  font-size: 12px;
  line-height: 0.5em;
  background: var(--status-bar);
  z-index: 99;
`;t.a=Object(c.b)((e,t)=>{const{contentRef:o}=t;return e=>{const t=r.content(e,{contentRef:o});if(!t||"notebook"!==t.type)return{kernelStatus:"not connected",kernelSpecDisplayName:"no kernel",lastSaved:null};const n=t.model.kernelRef;let l=null;n&&(l=r.kernel(e,{kernelRef:n}));const a=t&&t.lastSaved?t.lastSaved:null,i=null!=l&&null!=l.status?l.status:"not connected";let c=" ";return"not connected"===i?c="no kernel":null!=l&&null!=l.kernelSpecName?c=l.kernelSpecName:void 0!==t&&"notebook"===t.type&&(c=r.notebook.displayName(t.model)||" "),{kernelSpecDisplayName:c,kernelStatus:i,lastSaved:a}}})(class extends i.a.Component{shouldComponentUpdate(e){return this.props.lastSaved!==e.lastSaved||this.props.kernelStatus!==e.kernelStatus}render(){const e=this.props.kernelSpecDisplayName||"Loading...";return i.a.createElement(h,null,i.a.createElement(p,null,this.props.lastSaved?i.a.createElement("p",null," Last saved ",l()(this.props.lastSaved)," "):i.a.createElement("p",null," Not saved yet ")),i.a.createElement(d,null,i.a.createElement("p",null,e," | ",this.props.kernelStatus)))}})},1252:function(e,t,o){"use strict";var r=o(2),n=o.n(r),l=o(81),a=o(89),i=o(359);const c=Object(l.b)((e,t)=>{const{contentRef:o,index:r,cellId:n}=t,l=Object(i.default)(e=>e?e.toJS():{});return e=>{const t=e.core.entities.contents.byRef.getIn([o,"model","notebook","cellMap",n,"outputs",r],null);if(!t||"display_data"!==t.output_type&&"execute_result"!==t.output_type)return console.warn("connected transform media managed to get a non media bundle output"),{Media:()=>null};const i=a.r.transformsById(e),c=((e,t,o)=>{const r=e.data;return t.find(e=>r.hasOwnProperty(e)&&(o.hasOwnProperty(e)||o.get(e,!1)))})(t,a.r.displayOrder(e),i);if(c){const o=l(t.metadata.get(c)),r=t.data[c];return{Media:a.r.transform(e,{id:c}),mediaType:c,data:r,metadata:o}}return{Media:()=>null,mediaType:c,output:t}}},(e,t)=>{const{cellId:o,contentRef:r,index:n}=t;return e=>({mediaActions:{onMetadataChange:(t,l)=>{e(a.a.updateOutputMetadata({id:o,contentRef:r,metadata:t,index:n,mediaType:l}))}}})})(e=>{const{Media:t,mediaActions:o,mediaType:r,data:l,metadata:a}=e;return r&&l?n.a.createElement(t,Object.assign({},o,{data:l,metadata:a})):null});t.a=c},1667:function(e,t,o){"use strict";var r=o(63),n=o(483),l=o(66),a=o.n(l);const i={value:!1,mode:!0,theme:!1,indentUnit:!0,smartIndent:!0,tabSize:!0,indentWithTabs:!0,electricChars:!0,rtlMoveVisually:!0,keyMap:!0,extraKeys:!1,lineWrapping:!0,lineNumbers:!0,firstLineNumber:!0,lineNumberFormatter:!0,gutters:!0,fixedGutter:!0,readOnly:!0,showCursorWhenSelecting:!0,undoDepth:!0,historyEventDelay:!0,tabindex:!0,autofocus:!0,dragDrop:!0,onDragEvent:!0,onKeyEvent:!0,cursorBlinkRate:!0,cursorHeight:!0,workTime:!0,workDelay:!0,pollInterval:!0,flattenSpans:!0,maxHighlightLength:!0,viewportMargin:!0,lint:!0,placeholder:!0,showHint:!0,hintOptions:!1};function c(e){return!!i[e]}var s=o(168),d=o(2),p=o(3),h=o.n(p),m=o(1704),u=o(1683),g=o(169),b=o(1688),f=o(199),v=o(1690),x=o(1724),k=o(1705),y=o(1696),w=o(1706),C=o(198),E=o(1693);const M={8:"backspace",9:"tab",13:"enter",16:"shift",17:"ctrl",18:"alt",19:"pause",20:"capslock",27:"escape",32:"space",33:"pageup",34:"pagedown",35:"end",36:"home",37:"left",38:"up",39:"right",40:"down",45:"insert",46:"delete",91:"left window key",92:"right window key",93:"select",107:"add",109:"subtract",110:"decimal point",111:"divide",112:"f1",113:"f2",114:"f3",115:"f4",116:"f5",117:"f6",118:"f7",119:"f8",120:"f9",121:"f10",122:"f11",123:"f12",144:"numlock",145:"scrolllock",186:"semicolon",187:"equalsign",188:"comma",189:"dash",192:"graveaccent",220:"backslash",222:"quote"};var O=o(167),R=o(76),S=o(1719),N=o(1721),T=o(44);function D(e){return d.createElement(d.Fragment,null,e.type?d.createElement(j,{type:e.type}):null,e.displayText||e.text)}const j=T.c.span.attrs(e=>({className:`completion-type-${e.type}`,title:e.type}))`
  & {
    background: transparent;
    border: transparent 1px solid;
    width: 17px;
    height: 17px;
    margin: 0;
    padding: 0;
    display: inline-block;
    margin-right: 5px;
    top: 18px;
  }

  &:before {
    /* When experimental type completion isn't available render the left side as "nothing" */
    content: " ";
    bottom: 1px;
    left: 4px;
    position: relative;
    color: white;
  }
  /* color and content for each type of completion */
  &.completion-type-keyword:before {
    content: "K";
  }
  &.completion-type-keyword {
    background-color: darkred;
  }
  &.completion-type-class:before {
    content: "C";
  }
  &.completion-type-class {
    background-color: blueviolet;
  }
  &.completion-type-module:before {
    content: "M";
  }
  &.completion-type-module {
    background-color: chocolate;
  }
  &.completion-type-statement:before {
    content: "S";
  }
  &.completion-type-statement {
    background-color: forestgreen;
  }
  &.completion-type-function:before {
    content: "ƒ";
  }
  &.completion-type-function {
    background-color: yellowgreen;
  }
  &.completion-type-instance:before {
    content: "I";
  }
  &.completion-type-instance {
    background-color: teal;
  }
  &.completion-type-null:before {
    content: "ø";
  }
  &.completion-type-null {
    background-color: black;
  }
`;let z=(e,t)=>{let o=e;for(let r=0;r+1<t.length&&r<e;r++){const e=t.charCodeAt(r);if(e>=55296&&e<=56319){const e=t.charCodeAt(r+1);e>=56320&&e<=57343&&(o--,r++)}}return o},I=(e,t)=>{let o=e;for(let e=0;e+1<t.length&&e<o;e++){const r=t.charCodeAt(e);if(r>=55296&&r<=56319){const r=t.charCodeAt(e+1);r>=56320&&r<=57343&&(o++,e++)}}return o};function P(e,t){t.pick()}1==="𝐚".length&&(I=z=((e,t)=>e));const F=e=>t=>{let o=t.cursor_start,r=t.cursor_end;if(null===r)r=e.indexFromPos(e.getCursor()),null===o?o=r:o<0&&(o=r+o);else{const t=e.getValue();r=I(r,t),o=I(o,t)}const n=e.posFromIndex(o),l=e.posFromIndex(r);let a=t.matches;function i(e,t,o){h.a.render(d.createElement(D,Object.assign({},o)),e)}return t.metadata&&t.metadata._jupyter_types_experimental&&(a=t.metadata._jupyter_types_experimental),{list:a.map(e=>"string"==typeof e?{to:l,from:n,text:e,render:i}:Object.assign({to:l,from:n,render:i},e)),from:n,to:l}};const A=(e,t)=>Object(O.createMessage)("complete_request",{content:{code:e,cursor_pos:t}});function V(e,t){const o=t.getCursor();let r=t.indexFromPos(o);const n=t.getValue();return r=z(r,n),function(e,t,o){const r=e.pipe(Object(O.childOf)(o),Object(O.ofMessageType)("complete_reply"),Object(C.a)(e=>e.content),Object(S.a)(),Object(C.a)(F(t)),Object(N.a)(15e3));return R.a.create(t=>{const n=r.subscribe(t);return e.next(o),n})}(e,t,A(n,r))}function H(e,t){const o=t.getCursor(),r=z(t.indexFromPos(o),t.getValue());return function(e,t,o){const r=e.pipe(Object(O.childOf)(o),Object(O.ofMessageType)("inspect_reply"),Object(C.a)(e=>e.content),Object(S.a)(),Object(C.a)(e=>({dict:e.data})));return R.a.create(t=>{const n=r.subscribe(t);return e.next(o),n})}(e,0,function(e,t){return Object(O.createMessage)("inspect_request",{content:{code:e,cursor_pos:t,detail_level:0}})}(t.getValue(),r))}const B=T.c.textarea.attrs({autoComplete:"off"})`
  font-family: "Dank Mono", dm, "Source Code Pro", "Monaco", monospace;
  font-size: 14px;
  line-height: 20px;

  height: inherit;

  background: none;

  border: none;
  overflow: hidden;

  -webkit-scrollbar: none;
  -webkit-box-shadow: none;
  -moz-box-shadow: none;
  box-shadow: none;
  width: 100%;
  resize: none;
  padding: 10px 0 5px 10px;
  letter-spacing: 0.3px;
  word-spacing: 0px;

  &:focus {
    outline: none;
    border: none;
  }
`;T.a`
  /* BASICS */

  .CodeMirror {
    /* Set height, width, borders, and global font properties here */
    font-family: monospace;
    height: 300px;
    color: black;
    direction: ltr;
  }

  /* PADDING */

  .CodeMirror-lines {
    padding: 4px 0; /* Vertical padding around content */
  }
  .CodeMirror pre {
    padding: 0 4px; /* Horizontal padding of content */
  }

  .CodeMirror-scrollbar-filler,
  .CodeMirror-gutter-filler {
    background-color: white; /* The little square between H and V scrollbars */
  }

  /* GUTTER */

  .CodeMirror-gutters {
    border-right: 1px solid #ddd;
    background-color: #f7f7f7;
    white-space: nowrap;
  }
  .CodeMirror-linenumbers {
  }
  .CodeMirror-linenumber {
    padding: 0 3px 0 5px;
    min-width: 20px;
    text-align: right;
    color: #999;
    white-space: nowrap;
  }

  .CodeMirror-guttermarker {
    color: black;
  }
  .CodeMirror-guttermarker-subtle {
    color: #999;
  }

  /* CURSOR */

  .CodeMirror-cursor {
    border-left: 1px solid black;
    border-right: none;
    width: 0;
  }
  /* Shown when moving in bi-directional text */
  .CodeMirror div.CodeMirror-secondarycursor {
    border-left: 1px solid silver;
  }
  .cm-fat-cursor .CodeMirror-cursor {
    width: auto;
    border: 0 !important;
    background: #7e7;
  }
  .cm-fat-cursor div.CodeMirror-cursors {
    z-index: 1;
  }
  .cm-fat-cursor-mark {
    background-color: rgba(20, 255, 20, 0.5);
    -webkit-animation: blink 1.06s steps(1) infinite;
    -moz-animation: blink 1.06s steps(1) infinite;
    animation: blink 1.06s steps(1) infinite;
  }
  .cm-animate-fat-cursor {
    width: auto;
    border: 0;
    -webkit-animation: blink 1.06s steps(1) infinite;
    -moz-animation: blink 1.06s steps(1) infinite;
    animation: blink 1.06s steps(1) infinite;
    background-color: #7e7;
  }
  @-moz-keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }
  @-webkit-keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }
  @keyframes blink {
    0% {
    }
    50% {
      background-color: transparent;
    }
    100% {
    }
  }

  /* Can style cursor different in overwrite (non-insert) mode */
  .CodeMirror-overwrite .CodeMirror-cursor {
  }

  .cm-tab {
    display: inline-block;
    text-decoration: inherit;
  }

  .CodeMirror-rulers {
    position: absolute;
    left: 0;
    right: 0;
    top: -50px;
    bottom: -20px;
    overflow: hidden;
  }
  .CodeMirror-ruler {
    border-left: 1px solid #ccc;
    top: 0;
    bottom: 0;
    position: absolute;
  }

  /* DEFAULT THEME */

  .cm-s-default .cm-header {
    color: blue;
  }
  .cm-s-default .cm-quote {
    color: #090;
  }
  .cm-negative {
    color: #d44;
  }
  .cm-positive {
    color: #292;
  }
  .cm-header,
  .cm-strong {
    font-weight: bold;
  }
  .cm-em {
    font-style: italic;
  }
  .cm-link {
    text-decoration: underline;
  }
  .cm-strikethrough {
    text-decoration: line-through;
  }

  .cm-s-default .cm-keyword {
    color: #708;
  }
  .cm-s-default .cm-atom {
    color: #219;
  }
  .cm-s-default .cm-number {
    color: #164;
  }
  .cm-s-default .cm-def {
    color: #00f;
  }
  .cm-s-default .cm-variable,
  .cm-s-default .cm-punctuation,
  .cm-s-default .cm-property,
  .cm-s-default .cm-operator {
  }
  .cm-s-default .cm-variable-2 {
    color: #05a;
  }
  .cm-s-default .cm-variable-3,
  .cm-s-default .cm-type {
    color: #085;
  }
  .cm-s-default .cm-comment {
    color: #a50;
  }
  .cm-s-default .cm-string {
    color: #a11;
  }
  .cm-s-default .cm-string-2 {
    color: #f50;
  }
  .cm-s-default .cm-meta {
    color: #555;
  }
  .cm-s-default .cm-qualifier {
    color: #555;
  }
  .cm-s-default .cm-builtin {
    color: #30a;
  }
  .cm-s-default .cm-bracket {
    color: #997;
  }
  .cm-s-default .cm-tag {
    color: #170;
  }
  .cm-s-default .cm-attribute {
    color: #00c;
  }
  .cm-s-default .cm-hr {
    color: #999;
  }
  .cm-s-default .cm-link {
    color: #00c;
  }

  .cm-s-default .cm-error {
    color: #f00;
  }
  .cm-invalidchar {
    color: #f00;
  }

  .CodeMirror-composing {
    border-bottom: 2px solid;
  }

  /* Default styles for common addons */

  div.CodeMirror span.CodeMirror-matchingbracket {
    color: #0b0;
  }
  div.CodeMirror span.CodeMirror-nonmatchingbracket {
    color: #a22;
  }
  .CodeMirror-matchingtag {
    background: rgba(255, 150, 0, 0.3);
  }
  .CodeMirror-activeline-background {
    background: #e8f2ff;
  }

  /* STOP */

  /* The rest of this file contains styles related to the mechanics of
   the editor. You probably shouldn't touch them. */

  .CodeMirror {
    position: relative;
    overflow: hidden;
    background: white;
  }

  .CodeMirror-scroll {
    overflow: scroll !important; /* Things will break if this is overridden */
    /* 30px is the magic margin used to hide the element's real scrollbars */
    /* See overflow: hidden in .CodeMirror */
    margin-bottom: -30px;
    margin-right: -30px;
    padding-bottom: 30px;
    height: 100%;
    outline: none; /* Prevent dragging from highlighting the element */
    position: relative;
  }
  .CodeMirror-sizer {
    position: relative;
    border-right: 30px solid transparent;
  }

  /* The fake, visible scrollbars. Used to force redraw during scrolling
   before actual scrolling happens, thus preventing shaking and
   flickering artifacts. */
  .CodeMirror-vscrollbar,
  .CodeMirror-hscrollbar,
  .CodeMirror-scrollbar-filler,
  .CodeMirror-gutter-filler {
    position: absolute;
    z-index: 6;
    display: none;
  }
  .CodeMirror-vscrollbar {
    right: 0;
    top: 0;
    overflow-x: hidden;
    overflow-y: scroll;
  }
  .CodeMirror-hscrollbar {
    bottom: 0;
    left: 0;
    overflow-y: hidden;
    overflow-x: scroll;
  }
  .CodeMirror-scrollbar-filler {
    right: 0;
    bottom: 0;
  }
  .CodeMirror-gutter-filler {
    left: 0;
    bottom: 0;
  }

  .CodeMirror-gutters {
    position: absolute;
    left: 0;
    top: 0;
    min-height: 100%;
    z-index: 3;
  }
  .CodeMirror-gutter {
    white-space: normal;
    height: 100%;
    display: inline-block;
    vertical-align: top;
    margin-bottom: -30px;
  }
  .CodeMirror-gutter-wrapper {
    position: absolute;
    z-index: 4;
    background: none !important;
    border: none !important;
  }
  .CodeMirror-gutter-background {
    position: absolute;
    top: 0;
    bottom: 0;
    z-index: 4;
  }
  .CodeMirror-gutter-elt {
    position: absolute;
    cursor: default;
    z-index: 4;
  }
  .CodeMirror-gutter-wrapper ::selection {
    background-color: transparent;
  }
  .CodeMirror-gutter-wrapper ::-moz-selection {
    background-color: transparent;
  }

  .CodeMirror-lines {
    cursor: text;
    min-height: 1px; /* prevents collapsing before first draw */
  }
  .CodeMirror pre {
    /* Reset some styles that the rest of the page might have set */
    -moz-border-radius: 0;
    -webkit-border-radius: 0;
    border-radius: 0;
    border-width: 0;
    background: transparent;
    font-family: inherit;
    font-size: inherit;
    margin: 0;
    white-space: pre;
    word-wrap: normal;
    line-height: inherit;
    color: inherit;
    z-index: 2;
    position: relative;
    overflow: visible;
    -webkit-tap-highlight-color: transparent;
    -webkit-font-variant-ligatures: contextual;
    font-variant-ligatures: contextual;
  }
  .CodeMirror-wrap pre {
    word-wrap: break-word;
    white-space: pre-wrap;
    word-break: normal;
  }

  .CodeMirror-linebackground {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 0;
  }

  .CodeMirror-linewidget {
    position: relative;
    z-index: 2;
    padding: 0.1px; /* Force widget margins to stay inside of the container */
  }

  .CodeMirror-widget {
  }

  .CodeMirror-rtl pre {
    direction: rtl;
  }

  .CodeMirror-code {
    outline: none;
  }

  /* Force content-box sizing for the elements where we expect it */
  .CodeMirror-scroll,
  .CodeMirror-sizer,
  .CodeMirror-gutter,
  .CodeMirror-gutters,
  .CodeMirror-linenumber {
    -moz-box-sizing: content-box;
    box-sizing: content-box;
  }

  .CodeMirror-measure {
    position: absolute;
    width: 100%;
    height: 0;
    overflow: hidden;
    visibility: hidden;
  }

  .CodeMirror-cursor {
    position: absolute;
    pointer-events: none;
  }
  .CodeMirror-measure pre {
    position: static;
  }

  div.CodeMirror-cursors {
    visibility: hidden;
    position: relative;
    z-index: 3;
  }
  div.CodeMirror-dragcursors {
    visibility: visible;
  }

  .CodeMirror-focused div.CodeMirror-cursors {
    visibility: visible;
  }

  .CodeMirror-selected {
    background: #d9d9d9;
  }
  .CodeMirror-focused .CodeMirror-selected {
    background: #d7d4f0;
  }
  .CodeMirror-crosshair {
    cursor: crosshair;
  }
  .CodeMirror-line::selection,
  .CodeMirror-line > span::selection,
  .CodeMirror-line > span > span::selection {
    background: #d7d4f0;
  }
  .CodeMirror-line::-moz-selection,
  .CodeMirror-line > span::-moz-selection,
  .CodeMirror-line > span > span::-moz-selection {
    background: #d7d4f0;
  }

  .cm-searching {
    background-color: #ffa;
    background-color: rgba(255, 255, 0, 0.4);
  }

  /* Used to force a border model for a node */
  .cm-force-border {
    padding-right: 0.1px;
  }

  @media print {
    /* Hide the cursor when printing */
    .CodeMirror div.CodeMirror-cursors {
      visibility: hidden;
    }
  }

  /* See issue #2901 */
  .cm-tab-wrap-hack:after {
    content: "";
  }

  /* Help users use markselection to safely style text background */
  span.CodeMirror-selectedtext {
    background: none;
  }

/*************************** OVERRIDES ***************************/
/* These styles override CodeMirror styling, to ease our theming */

.CodeMirror {
    height: "100%";
    font-family: "Dank Mono", dm, "Source Code Pro", "Monaco", monospace;
    font-size: 14px;
    line-height: 20px;

    height: auto;

    background: none;
  }

  .CodeMirror-cursor {
    border-left-width: 1px;
    border-left-style: solid;
    border-left-color: var(--cm-color, black);
  }

  .CodeMirror-scroll {
    overflow-x: auto !important;
    overflow-y: hidden !important;
    width: 100%;
  }

  .CodeMirror-lines {
    padding: 0.4em;
  }

  .CodeMirror-linenumber {
    padding: 0 8px 0 4px;
  }

  .CodeMirror-gutters {
    border-top-left-radius: 2px;
    border-bottom-left-radius: 2px;
  }

  /** Override particular styles to allow for theming via CSS Variables */
  .cm-s-composition.CodeMirror {
    font-family: "Source Code Pro", monospace;
    letter-spacing: 0.3px;
    word-spacing: 0px;
    background: var(--cm-background, #fafafa);
    color: var(--cm-color, black);
  }
  .cm-s-composition .CodeMirror-lines {
    padding: 10px;
  }
  .cm-s-composition .CodeMirror-gutters {
    background-color: var(--cm-gutter-bg, white);
    padding-right: 10px;
    z-index: 3;
    border: none;
  }

  .cm-s-composition span.cm-comment {
    color: var(--cm-comment, #a86);
  }
  .cm-s-composition span.cm-keyword {
    line-height: 1em;
    font-weight: bold;
    color: var(--cm-keyword, blue);
  }
  .cm-s-composition span.cm-string {
    color: var(--cm-string, #a22);
  }
  .cm-s-composition span.cm-builtin {
    line-height: 1em;
    font-weight: bold;
    color: var(--cm-builtin, #077);
  }
  .cm-s-composition span.cm-special {
    line-height: 1em;
    font-weight: bold;
    color: var(--cm-special, #0aa);
  }
  .cm-s-composition span.cm-variable {
    color: var(--cm-variable, black);
  }
  .cm-s-composition span.cm-number,
  .cm-s-composition span.cm-atom {
    color: var(--cm-number, #3a3);
  }
  .cm-s-composition span.cm-meta {
    color: var(--cm-meta, #555);
  }
  .cm-s-composition span.cm-link {
    color: var(--cm-link, #3a3);
  }
  .cm-s-composition span.cm-operator {
    color: var(--cm-operator, black);
  }
  .cm-s-composition span.cm-def {
    color: var(--cm-def, black);
  }
  .cm-s-composition .CodeMirror-activeline-background {
    background: var(--cm-activeline-bg, #e8f2ff);
  }
  .cm-s-composition .CodeMirror-matchingbracket {
    border-bottom: 1px solid var(--cm-matchingbracket-outline, grey);
    color: var(--cm-matchingbracket-color, black) !important;
  }


`,T.a`
/* From codemirror/addon/hint/show-hint.css */
/* There are overrides at the bottom of this stylesheet to cooperate with nteract */

.CodeMirror-hints {
  position: absolute;
  z-index: 10;
  overflow: hidden;
  list-style: none;

  margin: 0;
  padding: 2px;

  -webkit-box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  -moz-box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  border-radius: 3px;
  border: 1px solid silver;

  background: white;
  font-size: 90%;
  font-family: monospace;

  max-height: 20em;
  overflow-y: auto;
}

.CodeMirror-hint {
  margin: 0;
  padding: 0 4px;
  border-radius: 2px;
  white-space: pre;
  color: black;
  cursor: pointer;
}

li.CodeMirror-hint-active {
  background: #08f;
  color: white;
}

/*************************** OVERRIDES ***************************/
/* These styles override hint styling, used for code completion */

.CodeMirror-hints {
    -webkit-box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.2);
    -moz-box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.2);
    box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.2);
    border-radius: 0px;
    border: none;
    padding: 0;

    background: var(--cm-hint-bg, white);
    font-size: 90%;
    font-family: "Source Code Pro", monospace;

    /*_________*/
    z-index: 9001;  /* known as wow just bring it to the front, ignore the rest of the UI */

    overflow-y: auto;
  }

  .CodeMirror-hint {
    border-radius: 0px;
    white-space: pre;
    cursor: pointer;
    color: var(--cm-hint-color, black);
  }

  li.CodeMirror-hint-active {
    background: var(--cm-hint-bg-active, #abd1ff);
    color: var(--cm-hint-color-active, black);
  }

  /** Handle the type hint segment */
  .CodeMirror-hint {
    padding-left: 0;
    border-bottom: none;
  }
`;const K=T.c.button`
  float: right;
  display: inline-block;
  position: absolute;
  top: 0px;
  right: 0px;
  font-size: 11.5px;
`,L=T.c.div`
  padding: 20px 20px 50px 20px;
  margin: 30px 20px 50px 20px;
  box-shadow: 2px 2px 50px rgba(0, 0, 0, 0.2);
  white-space: pre-wrap;
  background-color: var(--theme-app-bg);
  z-index: 9999999;
`;function U(e){return e?e.replace(/\r\n|\r/g,"\n"):e}class _ extends d.PureComponent{constructor(e){super(e),this.textareaRef=d.createRef(),this.hint=this.hint.bind(this),this.hint.async=!0,this.tips=this.tips.bind(this),this.deleteTip=this.deleteTip.bind(this),this.debounceNextCompletionRequest=!0,this.state={isFocused:!0,tipElement:null},this.fullOptions=this.fullOptions.bind(this),this.cleanMode=this.cleanMode.bind(this);const t={"Cmd-.":this.tips,"Cmd-/":"toggleComment","Ctrl-.":this.tips,"Ctrl-/":"toggleComment","Ctrl-Space":e=>(this.debounceNextCompletionRequest=!1,e.execCommand("autocomplete")),Down:this.goLineDownOrEmit,"Shift-Tab":e=>e.execCommand("indentLess"),Tab:this.executeTab,Up:this.goLineUpOrEmit},o={completeSingle:!1,extraKeys:{Right:P},hint:this.hint};this.defaultOptions=Object.assign({extraKeys:t,hintOptions:o,theme:"composition"})}fullOptions(e={}){return Object.keys(this.props).filter(c).reduce((e,t)=>(e[t]=this.props[t],e),e)}cleanMode(){return this.props.mode?"string"==typeof this.props.mode?this.props.mode:"object"==typeof this.props.mode&&"toJS"in this.props.mode?this.props.mode.toJS():this.props.mode:"text/plain"}componentWillMount(){this.componentWillReceiveProps=Object(s.debounce)(this.componentWillReceiveProps,0)}componentDidMount(){o(1218),o(1219),o(1220),o(1221),o(1222),o(601),o(1223),o(1224),o(1225),o(1226),o(1227),o(1228),o(1229),o(1230),o(602),o(1232),o(1234);const{completion:e,editorFocused:t,focusAbove:r,focusBelow:n}=this.props,l=Object.assign({},this.fullOptions,this.defaultOptions,{mode:this.cleanMode()});this.cm=a.a.fromTextArea(this.textareaRef.current,l),this.cm.setValue(this.props.value||""),t&&this.cm.focus(),this.cm.on("topBoundary",r),this.cm.on("bottomBoundary",n),this.cm.on("focus",this.focusChanged.bind(this,!0)),this.cm.on("blur",this.focusChanged.bind(this,!1)),this.cm.on("change",this.codemirrorValueChanged.bind(this));const i=Object(m.a)(this.cm,"keyup",(e,t)=>({editor:e,ev:t}));this.keyupEventsSubscriber=i.pipe(Object(v.a)(e=>Object(u.a)(e))).subscribe(({editor:t,ev:o})=>{if(e&&!t.state.completionActive&&!M[(o.keyCode||o.which).toString()]){const e=t.getDoc().getCursor(),o=t.getTokenAt(e);"tag"!==o.type&&"variable"!==o.type&&" "!==o.string&&"<"!==o.string&&"/"!==o.string&&"."!==o.string||t.execCommand("autocomplete")}}),this.completionSubject=new g.b;const[c,s]=Object(x.a)(e=>!0===e.debounce)(this.completionSubject),d=Object(b.a)(s,c.pipe(Object(k.a)(150),Object(y.a)(s),Object(w.a)())).pipe(Object(v.a)(e=>{const{channels:t}=this.props;if(!t)throw new Error("Unexpectedly received a completion event when channels were unset");return V(t,e.editor).pipe(Object(C.a)(t=>()=>e.callback(t)),Object(y.a)(this.completionSubject),Object(E.a)(e=>(console.log(`Code completion error: ${e.message}`),Object(f.b)())))}));this.completionEventsSubscriber=d.subscribe(e=>e())}componentDidUpdate(e){if(!this.cm)return;const{editorFocused:t,theme:o}=this.props;e.theme!==o&&this.cm.refresh(),e.editorFocused!==t&&(t?this.cm.focus():this.cm.getInputField().blur()),e.cursorBlinkRate!==this.props.cursorBlinkRate&&(this.cm.setOption("cursorBlinkRate",this.props.cursorBlinkRate),t&&(this.cm.getInputField().blur(),this.cm.focus())),e.mode!==this.props.mode&&this.cm.setOption("mode",this.cleanMode())}componentWillReceiveProps(e){if(this.cm&&void 0!==e.value&&U(this.cm.getValue())!==U(e.value))if(this.props.preserveScrollPosition){const t=this.cm.getScrollInfo();this.cm.setValue(e.value),this.cm.scrollTo(t.left,t.top)}else this.cm.setValue(e.value);for(const t in e)c(t)&&e[t]!==this.props[t]&&this.cm.setOption(t,e[t])}componentWillUnmount(){this.cm&&this.cm.toTextArea(),this.keyupEventsSubscriber.unsubscribe(),this.completionEventsSubscriber.unsubscribe()}focusChanged(e){this.setState({isFocused:e}),this.props.onFocusChange&&this.props.onFocusChange(e)}hint(e,t){const{completion:o,channels:r}=this.props,n=this.debounceNextCompletionRequest;if(this.debounceNextCompletionRequest=!0,o&&r){const o={editor:e,callback:t,debounce:n};this.completionSubject.next(o)}}deleteTip(){this.setState({tipElement:null})}tips(e){const{tip:t,channels:o}=this.props;t&&H(o,e).subscribe(t=>{const o=t.dict;if(0===Object.keys(o).length)return;const r=document.getElementsByClassName("tip-holder")[0],l=h.a.createPortal(d.createElement(L,{className:"CodeMirror-hint"},d.createElement(n.d,{data:o,metadata:{expanded:{expanded:!0}}},d.createElement(n.b.Plain,null)),d.createElement(K,{onClick:this.deleteTip},"✕")),r);this.setState({tipElement:l}),e.addWidget({line:e.getCursor().line,ch:0},r,!0);const a=document.body;if(null!=r&&null!=a){const e=r.getBoundingClientRect();a.appendChild(r),r.style.top=`${e.top}px`}})}goLineDownOrEmit(e){const t=e.getCursor(),o=e.lastLine(),r=e.getLine(o);t.line!==o||t.ch!==r.length||e.somethingSelected()?e.execCommand("goLineDown"):a.a.signal(e,"bottomBoundary")}goLineUpOrEmit(e){const t=e.getCursor();0!==t.line||0!==t.ch||e.somethingSelected()?e.execCommand("goLineUp"):a.a.signal(e,"topBoundary")}executeTab(e){e.somethingSelected()?e.execCommand("indentMore"):e.execCommand("insertSoftTab")}codemirrorValueChanged(e,t){this.props.onChange&&"setValue"!==t.origin&&this.props.onChange(e.getValue(),t)}render(){return d.createElement(d.Fragment,null,d.createElement("div",{className:"tip-holder"}),d.createElement(B,{ref:this.textareaRef,defaultValue:this.props.value}),this.state.tipElement)}}_.defaultProps={value:"",channels:null,completion:!1,editorFocused:!1,kernelStatus:"not connected",theme:"light",tip:!1,autofocus:!1,matchBrackets:!0,indentUnit:4,lineNumbers:!1,cursorBlinkRate:530};var q=o(121),W=o(81);const J={name:"gfm",tokenTypeOverrides:{emoji:"emoji"}},Y={name:"text/plain",tokenTypeOverrides:{emoji:"emoji"}};t.a=Object(W.b)((e,t)=>{const{id:o,contentRef:r,focusAbove:n,focusBelow:l}=t;return function(e){const t=q.model(e,{contentRef:r});if(!t||"notebook"!==t.type)throw new Error("Connected Editor components should not be used with non-notebook models");const a=q.notebook.cellById(t,{id:o});if(!a)throw new Error("cell not found inside cell map");t.cellFocused;const i=t.editorFocused===o,c=q.userTheme(e);let s=null,d="not connected",p=Y,h=!1;switch(a.cell_type){case"markdown":h=!0,p=J;break;case"raw":h=!0,p=Y;break;case"code":{const o=t.kernelRef,r=o?e.core.entities.kernels.byRef.get(o):null;s=r?r.channels:null,r&&(d=r.status||"not connected"),p=r&&r.info?r.info.codemirrorMode:q.notebook.codeMirrorMode(t)}}return{tip:!0,completion:!0,editorFocused:i,focusAbove:n,focusBelow:l,theme:c,value:a.source,channels:s,kernelStatus:d,cursorBlinkRate:e.config.get("cursorBlinkRate",530),mode:p,lineWrapping:h}}},(e,t)=>{const{id:o,contentRef:n}=t;return e=>({onChange:t=>{e(r.updateCellSource({id:o,value:t,contentRef:n}))},onFocusChange(t){t&&(e(r.focusCellEditor({id:o,contentRef:n})),e(r.focusCell({id:o,contentRef:n})))}})})(_)},1682:function(e,t,o){"use strict";var r=o(2),n=o(574),l=o(44);const a=l.c.div`
  z-index: 10000;
  display: inline-block;
`;a.displayName="DropdownDiv";class i extends r.PureComponent{constructor(e){super(e),this.state={menuHidden:!0}}render(){return r.createElement(a,null,r.Children.map(this.props.children,e=>{const t=e;return Object(n.areComponentsEqual)(t.type,s)?r.cloneElement(t,{onClick:()=>{this.setState({menuHidden:!this.state.menuHidden})}}):Object(n.areComponentsEqual)(t.type,p)?this.state.menuHidden?null:r.cloneElement(t,{onItemClick:()=>{this.setState({menuHidden:!0})}}):e}))}}const c=l.c.div`
  user-select: none;
  margin: 0px;
  padding: 0px;
`;c.displayName="DropdownTriggerDiv";class s extends r.PureComponent{render(){return r.createElement(c,{onClick:this.props.onClick},this.props.children)}}const d=l.c.div`
  user-select: none;
  margin: 0px;
  padding: 0px;

  width: 200px;

  opacity: 1;
  position: absolute;
  top: 0.2em;
  right: 0;
  border-style: none;
  padding: 0;
  font-family: var(--nt-font-family-normal);
  font-size: var(--nt-font-size-m);
  line-height: 1.5;
  margin: 20px 0;
  background-color: var(--theme-cell-menu-bg);

  ul {
    list-style: none;
    text-align: left;
    padding: 0;
    margin: 0;
    opacity: 1;
  }

  ul li {
    padding: 0.5rem;
  }

  ul li:hover {
    background-color: var(--theme-cell-menu-bg-hover, #e2dfe3);
    cursor: pointer;
  }
`;d.displayName="DropdownContentDiv";class p extends r.PureComponent{render(){return r.createElement(d,null,r.createElement("ul",null,r.Children.map(this.props.children,e=>{const t=e;return r.cloneElement(t,{onClick:e=>{t.props.onClick(e),this.props.onItemClick(e)}})})))}}p.defaultProps={onItemClick:()=>{}};var h=o(207);o.d(t,"a",function(){return u});const m=l.c.div`
  background-color: var(--theme-cell-toolbar-bg);
  opacity: 0.4;
  transition: opacity 0.4s;

  & > div {
    display: inline-block;
  }

  :hover {
    opacity: 1;
  }

  button {
    display: inline-block;

    width: 22px;
    height: 20px;
    padding: 0px 4px;

    text-align: center;

    border: none;
    outline: none;
    background: none;
  }

  span {
    font-size: 15px;
    line-height: 1;
    color: var(--theme-cell-toolbar-fg);
  }

  button span:hover {
    color: var(--theme-cell-toolbar-fg-hover);
  }

  .octicon {
    transition: color 0.5s;
  }

  span.spacer {
    display: inline-block;
    vertical-align: middle;
    margin: 1px 5px 3px 5px;
    height: 11px;
  }
`,u=l.c.div.attrs(e=>({style:{display:e.cellFocused?"block":e.sourceHidden?"block":"none"}}))`
  z-index: 9999;
  position: absolute;
  top: 0px;
  right: 0px;
  height: 34px;

  /* Set the left padding to 50px to give users extra room to move their
              mouse to the toolbar without causing the cell to go out of focus and thus
              hide the toolbar before they get there. */
  padding: 0px 0px 0px 50px;
`;class g extends r.PureComponent{render(){const{executeCell:e,deleteCell:t,sourceHidden:o}=this.props;return r.createElement(u,{sourceHidden:o,cellFocused:this.props.cellFocused},r.createElement(m,null,"markdown"!==this.props.type&&r.createElement("button",{onClick:e,title:"execute cell",className:"executeButton"},r.createElement("span",{className:"octicon"},r.createElement(h.j,null))),r.createElement(i,null,r.createElement(s,null,r.createElement("button",{title:"show additional actions"},r.createElement("span",{className:"octicon toggle-menu"},r.createElement(h.b,null)))),"code"===this.props.type?r.createElement(p,null,r.createElement("li",{onClick:this.props.clearOutputs,className:"clearOutput",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Clear Cell Output")),r.createElement("li",{onClick:this.props.toggleCellInputVisibility,className:"inputVisibility",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Input Visibility")),r.createElement("li",{onClick:this.props.toggleCellOutputVisibility,className:"outputVisibility",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Output Visibility")),r.createElement("li",{onClick:this.props.toggleOutputExpansion,className:"outputExpanded",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Expanded Output")),r.createElement("li",{onClick:this.props.toggleParameterCell,role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Toggle Parameter Cell")),r.createElement("li",{onClick:this.props.changeCellType,className:"changeType",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Convert to Markdown Cell"))):r.createElement(p,null,r.createElement("li",{onClick:this.props.changeCellType,className:"changeType",role:"option","aria-selected":"false",tabIndex:0},r.createElement("a",null,"Convert to Code Cell")))),r.createElement("span",{className:"spacer"}),r.createElement("button",{onClick:t,title:"delete cell",className:"deleteButton"},r.createElement("span",{className:"octicon"},r.createElement(h.i,null)))))}}g.defaultProps={type:"code"};t.b=g},1703:function(e,t,o){"use strict";o.r(t);var r=o(966);t.default=r.a},689:function(e,t,o){"use strict";var r=o(44),n=o(2);const l=Object(r.c)(e=>e.blank?null:n.createElement("div",{className:e.className},function(e){return e.running?"[*]":e.queued?"[…]":"number"==typeof e.counter?`[${e.counter}]`:"[ ]"}(e)))`
  font-family: monospace;
  font-size: 12px;
  line-height: 22px;
  /* For creating a buffer area for <Prompt blank /> */
  min-height: 22px;

  color: black;

  width: var(--prompt-width, 50px);
  padding: 9px 0;

  text-align: center;

  color: var(--theme-cell-prompt-fg, black);
  background-color: var(--theme-cell-prompt-bg, #fafafa);
`;l.defaultProps={counter:null,running:!1,queued:!1,blank:!1},l.displayName="Prompt";const a=Object(r.c)(l)``;a.defaultProps={blank:!0};const i={FLAT:"none",HOVERED:"var(\n    --theme-cell-shadow-hover,\n    1px 1px 3px rgba(0, 0, 0, 0.12),\n    -1px -1px 3px rgba(0, 0, 0, 0.12)\n  )",SELECTED:"var(\n    --theme-cell-shadow-focus,\n    3px 3px 9px rgba(0, 0, 0, 0.12),\n    -3px -3px 9px rgba(0, 0, 0, 0.12)\n  )"};function c(e){return e.isSelected?i.SELECTED:e._hovered?i.HOVERED:i.FLAT}const s=r.c.div.attrs(e=>({className:e.isSelected?"selected":"",style:{boxShadow:c(e)}}))`
  & {
    position: relative;
    background: var(--theme-cell-bg, white);
    transition: all 0.1s ease-in-out;
  }

  /* The box shadow for hovered should only apply when not already selected */
  &:hover:not(.selected) {
    box-shadow: ${i.HOVERED};
  }

  /*
  Our cells conditionally style the prompt contained within based on if the cell is
  selected or hovered. To do this with styled-components we use their method of
  referring to other components:

  https://www.styled-components.com/docs/advanced#referring-to-other-components

  */
  & ${l} {
    /* We change nothing when the cell is not selected, focused, or hovered */
  }
  &.selected ${l} {
    background-color: var(--theme-cell-prompt-bg-focus, hsl(0, 0%, 90%));
    color: var(--theme-cell-prompt-fg-focus, hsl(0, 0%, 51%));
  }

  &:hover:not(.selected) ${l}, &:active:not(.selected) ${l} {
    background-color: var(--theme-cell-prompt-bg-hover, hsl(0, 0%, 94%));
    color: var(--theme-cell-prompt-fg-hover, hsl(0, 0%, 15%));
  }

  &:focus ${l} {
    background-color: var(--theme-cell-prompt-bg-focus, hsl(0, 0%, 90%));
    color: var(--theme-cell-prompt-fg-focus, hsl(0, 0%, 51%));
  }
`;s.displayName="Cell",s.defaultProps={isSelected:!1,_hovered:!1,children:null},r.c.div`
  & > * {
    margin: 20px 0;
  }

  & {
    font-family: "Source Sans Pro", Helvetica Neue, Helvetica, sans-serif;
    font-size: 16px;
    background-color: var(--theme-app-bg);
    color: var(--theme-app-fg);

    padding-bottom: 10px;
  }
`.displayName="Cells";var d=o(967),p=o.n(d),h=o(1130);const m=e=>{let t=e.language;return"ipython"===t?t="python":"text/x-scala"===t?t="scala":t.startsWith("text/x-")&&(t=t.slice("text/x-".length)),n.createElement(p.a,{style:"light"===e.theme?h.vs:h.xonokai,language:t,className:e.className,customStyle:{padding:"10px 0px 10px 10px",margin:"0px",backgroundColor:"var(--cm-background, #fafafa)",border:"none"}},e.children)};m.defaultProps={theme:"light",language:"text",children:"",className:"input"};var u=m;class g extends n.Component{render(){return"string"==typeof this.props.children?n.createElement(u,{language:this.props.language||"text",className:this.props.className||"input"},this.props.children):n.createElement("div",{className:this.props.className},this.props.children)}}g.defaultProps={children:"",language:"text",className:"input",theme:"light"};const b=Object(r.c)(g)``;b.defaultProps={children:"",language:"text",className:"input",theme:"light"},b.displayName="Source";class f extends n.Component{render(){return this.props.hidden?null:n.createElement("div",{className:this.props.className},this.props.children)}}f.defaultProps={children:null,hidden:!1};const v=Object(r.c)(f)`
  & {
    display: flex;
    flex-direction: row;
  }

  &.invisible {
    height: 34px;
  }

  & ${l} {
    flex: 0 0 auto;
  }

  & ${b} {
    flex: 1 1 auto;
    overflow: auto;
    background-color: var(--theme-cell-input-bg, #fafafa);
  }
`;v.displayName="Input";const x=r.c.div.attrs(e=>({style:{maxHeight:e.expanded?"100%":null}}))`
  padding: 10px 10px 10px calc(var(--prompt-width, 50px) + 10px);
  word-wrap: break-word;
  overflow-y: hidden;
  outline: none;
  /* When expanded, this is overtaken to 100% */
  text-overflow: ellipsis;

  &:empty {
    display: none;
  }

  /* NOTE: All these styles should get moved into some sort of
           "Default Output Style" that an output type can opt in to,
           like with HTML, Markdown, VDOM
           */
  & a {
    color: var(--link-color-unvisited, blue);
  }

  & a:visited {
    color: var(--link-color-visited, blue);
  }

  & code {
    font-family: "Source Code Pro";
    white-space: pre-wrap;
    font-size: 14px;
  }

  & pre {
    white-space: pre-wrap;
    font-size: 14px;
    word-wrap: break-word;
  }

  & img {
    display: block;
    max-width: 100%;
  }

  & kbd {
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0.1em 0.5em;
    margin: 0 0.2em;
    box-shadow: 0 1px 0px rgba(0, 0, 0, 0.2), 0 0 0 2px #fff inset;
    background-color: #f7f7f7;
  }

  & table {
    border-collapse: collapse;
  }

  & th,
  & td,
  /* for legacy output handling */
  & .th,
  & .td {
    padding: 0.5em 1em;
    border: 1px solid var(--theme-app-border, #cbcbcb);
  }

  & th {
    text-align: left;
  }

  & blockquote {
    padding: 0.75em 0.5em 0.75em 1em;
    background: var(--theme-cell-output-bg, white);
    border-left: 0.5em solid #ddd;
  }

  & blockquote::before {
    display: block;
    height: 0;
    content: "“";
    margin-left: -0.95em;
    font: italic 400%/1 Open Serif, Georgia, "Times New Roman", serif;
    color: solid var(--theme-app-border, #cbcbcb);
  }

  /* for nested paragraphs in block quotes */
  & blockquote p {
    display: inline;
  }

  & dd {
    display: block;
    -webkit-margin-start: 40px;
  }
  & dl {
    display: block;
    -webkit-margin-before: 1__qem;
    -webkit-margin-after: 1em;
    -webkit-margin-start: 0;
    -webkit-margin-end: 0;
  }

  & dt {
    display: block;
  }

  & dl {
    width: 100%;
    overflow: hidden;
    padding: 0;
    margin: 0;
  }

  & dt {
    font-weight: bold;
    float: left;
    width: 20%;
    /* adjust the width; make sure the total of both is 100% */
    padding: 0;
    margin: 0;
  }

  & dd {
    float: left;
    width: 80%;
    /* adjust the width; make sure the total of both is 100% */
    padding: 0;
    margin: 0;
  }

  /** Adaptation for the R kernel's inline lists **/
  & .list-inline li {
    display: inline;
    padding-right: 20px;
    text-align: center;
  }
`;class k extends n.PureComponent{render(){return this.props.hidden?null:this.props.children?n.createElement(x,{expanded:this.props.expanded,className:this.props.className},this.props.children):null}}k.defaultProps={children:null,expanded:!1,hidden:!1};const y=Object(r.c)(k)`
  background-color: var(--theme-pager-bg, #fafafa);
`;y.displayName="Pagers";r.a`
:root {
  --nt-color-alabaster-darkest: var(--nt-color-alabaster-darker);
  --nt-color-alabaster-darker: var(--nt-color-alabaster-dark);
  --nt-color-alabaster-dark: var(--nt-color-alabaster);
  --nt-color-alabaster: hsl(0, 0%, 97%);
  --nt-color-alabaster-light: var(--nt-color-alabaster);
  --nt-color-alabaster-lighter: var(--nt-color-alabaster-light);
  --nt-color-alabaster-lightest: var(--nt-color-alabaster-lighter);
  --nt-color-asparagus-darkest: var(--nt-color-asparagus-darker);
  --nt-color-asparagus-darker: var(--nt-color-asparagus-dark);
  --nt-color-asparagus-dark: hsl(91, 28%, 37%);
  --nt-color-asparagus: hsl(91, 28%, 55%);
  --nt-color-asparagus-light: hsl(91, 28%, 73%);
  --nt-color-asparagus-lighter: hsl(91, 28%, 88%);
  --nt-color-asparagus-lightest: hsl(91, 28%, 98%);
  --nt-color-danube-darkest: var(--nt-color-danube-darker);
  --nt-color-danube-darker: var(--nt-color-danube-dark);
  --nt-color-danube-dark: hsl(208, 54%, 35%);
  --nt-color-danube: hsl(208, 54%, 53%);
  --nt-color-danube-light: hsl(208, 54%, 71%);
  --nt-color-danube-lighter: hsl(208, 54%, 86%);
  --nt-color-danube-lightest: hsl(208, 54%, 98%);
  --nt-color-gold-darkest: var(--nt-color-gold-darker);
  --nt-color-gold-darker: var(--nt-color-gold-dark);
  --nt-color-gold-dark: hsl(41, 89%, 35%);
  --nt-color-gold: hsl(41, 89%, 53%);
  --nt-color-gold-light: hsl(41, 89%, 71%);
  --nt-color-gold-lighter: hsl(41, 89%, 86%);
  --nt-color-gold-lightest: hsl(41, 89%, 98%);
  --nt-color-nteract-darkest: var(--nt-color-nteract-darker);
  --nt-color-nteract-darker: var(--nt-color-nteract-dark);
  --nt-color-nteract-dark: var(--nt-color-nteract);
  --nt-color-nteract: #8518f2;
  --nt-color-nteract-light: #af8afa;
  --nt-color-nteract-lighter: #ccb3ff;
  --nt-color-nteract-lightest: var(--nt-color-nteract-lighter);
  --nt-color-red-darkest: var(--nt-color-red-darker);
  --nt-color-red-darker: var(--nt-color-red-dark);
  --nt-color-red-dark: hsl(0, 67%, 25%);
  --nt-color-red: hsl(0, 67%, 43%);
  --nt-color-red-light: hsl(0, 67%, 61%);
  --nt-color-red-lighter: hsl(0, 67%, 76%);
  --nt-color-red-lightest: hsl(0, 67%, 88%);
  --nt-color-grey-darkest: hsl(0, 0%, 10%);
  --nt-color-grey-darker: hsl(0, 0%, 17%);
  --nt-color-grey-dark: hsl(0, 0%, 40%);
  --nt-color-grey: hsl(0, 0%, 63%);
  --nt-color-grey-light: hsl(0, 0%, 90%);
  --nt-color-grey-lighter: hsl(0, 0%, 94%);
  --nt-color-grey-lightest: hsl(0, 0%, 98%);
  --nt-color-midnight-darkest: hsl(0, 0%, 0%);
  --nt-color-midnight-darker: hsl(0, 0%, 5%);
  --nt-color-midnight-dark: hsl(0, 0%, 10%);
  --nt-color-midnight: hsl(0, 0%, 15%);
  --nt-color-midnight-light: hsl(0, 0%, 51%);
  --nt-color-midnight-lighter: hsl(0, 0%, 75%);
  --nt-color-midnight-lightest: hsl(0, 0%, 85%);
  --nt-color-sky-darkest: var(--nt-color-sky-darker);
  --nt-color-sky-darker: var(--nt-color-sky-dark);
  --nt-color-sky-dark: hsl(208, 54%, 35%);
  --nt-color-sky: hsl(208, 54%, 53%);
  --nt-color-sky-light: hsl(208, 54%, 71%);
  --nt-color-sky-lighter: hsl(208, 54%, 86%);
  --nt-color-sky-lightest: hsl(208, 54%, 98%);
  --nt-color-slate-darkest: var(--nt-color-slate-darker);
  --nt-color-slate-darker: var(--nt-color-slate-dark);
  --nt-color-slate-dark: hsl(207, 29%, 14%);
  --nt-color-slate: hsl(207, 29%, 32%);
  --nt-color-slate-light: hsl(207, 29%, 50%);
  --nt-color-slate-lighter: hsl(207, 29%, 65%);
  --nt-color-slate-lightest: hsl(207, 29%, 77%);
  --nt-color-clementine-darkest: var(--nt-color-clementine-darker);
  --nt-color-clementine-darker: var(--nt-color-clementine-dark);
  --nt-color-clementine-dark: hsl(33, 75%, 34%);
  --nt-color-clementine: hsl(33, 75%, 52%);
  --nt-color-clementine-light: hsl(33, 75%, 70%);
  --nt-color-clementine-lighter: hsl(33, 75%, 85%);
  --nt-color-clementine-lightest: hsl(33, 75%, 97%);
  --nt-border-radius-none: 0;
  --nt-border-radius-s: 1px;
  --nt-border-radius-m: 2px;
  --nt-border-radius-l: 4px;
  --nt-border-width-none: 0;
  --nt-border-width-xs: 1px;
  --nt-border-width-s: 2px;
  --nt-border-width-m: 3px;
  --nt-border-width-l: 5px;
  --nt-font-size-none: 0;
  --nt-font-size-xxs: 10px;
  --nt-font-size-xs: 10px;
  --nt-font-size-s: 12px;
  --nt-font-size-m: 14px;
  --nt-font-size-l: 20px;
  --nt-font-size-xl: 25px;
  --nt-font-size-xxl: 30px;
  --nt-font-weight-light: 300;
  --nt-font-weight-normal: 400;
  --nt-font-weight-bold: 600;
  --nt-font-weight-bolder: 700;
  --nt-font-family-normal: 'Source Sans Pro', sans-serif;
  --nt-font-family-mono: 'Source Code Pro', courier;
  --nt-opacity-disabled: 0.4;
  --nt-opacity-faded: 0.3;
  --nt-spacing-none: 0;
  --nt-spacing-xxs: 1px;
  --nt-spacing-xs: 3px;
  --nt-spacing-s: 5px;
  --nt-spacing-m: 10px;
  --nt-spacing-l: 15px;
  --nt-spacing-xl: 20px;
  --nt-spacing-xxl: 25px;
  --nt-transition-duration-normal: 250ms;
  --nt-z-index-menu: 100;
  --nt-z-index-notification: 200;
  --nt-z-index-modal: 300;
  --nt-color-actionable-darkest: var(--nt-color-danube-darkest);
  --nt-color-actionable-darker: var(--nt-color-danube-darker);
  --nt-color-actionable-dark: var(--nt-color-danube-dark);
  --nt-color-actionable: var(--nt-color-danube);
  --nt-color-actionable-light: var(--nt-color-danube-light);
  --nt-color-actionable-lighter: var(--nt-color-danube-lighter);
  --nt-color-actionable-lightest: var(--nt-color-danube-lightest);
  --nt-color-brand-darkest: var(--nt-color-nteract-darkest);
  --nt-color-brand-darker: var(--nt-color-nteract-darker);
  --nt-color-brand-dark: var(--nt-color-nteract-dark);
  --nt-color-brand: var(--nt-color-nteract);
  --nt-color-brand-light: var(--nt-color-nteract-light);
  --nt-color-brand-lighter: var(--nt-color-nteract-lighter);
  --nt-color-brand-lightest: var(--nt-color-nteract-lightest);
  --nt-color-danger-darkest: var(--nt-color-red-darkest);
  --nt-color-danger-darker: var(--nt-color-red-darker);
  --nt-color-danger-dark: var(--nt-color-red-dark);
  --nt-color-danger: var(--nt-color-red);
  --nt-color-danger-light: var(--nt-color-red-light);
  --nt-color-danger-lighter: var(--nt-color-red-lighter);
  --nt-color-danger-lightest: var(--nt-color-red-lightest);
  --nt-color-info-darkest: var(--nt-color-danube-darkest);
  --nt-color-info-darker: var(--nt-color-danube-darker);
  --nt-color-info-dark: var(--nt-color-danube-dark);
  --nt-color-info: var(--nt-color-danube);
  --nt-color-info-light: var(--nt-color-danube-light);
  --nt-color-info-lighter: var(--nt-color-danube-lighter);
  --nt-color-info-lightest: var(--nt-color-danube-lightest);
  --nt-color-nav-darkest: var(--nt-color-slate-darkest);
  --nt-color-nav-darker: var(--nt-color-slate-darker);
  --nt-color-nav-dark: var(--nt-color-slate-dark);
  --nt-color-nav: var(--nt-color-slate);
  --nt-color-nav-light: var(--nt-color-slate-light);
  --nt-color-nav-lighter: var(--nt-color-slate-lighter);
  --nt-color-nav-lightest: var(--nt-color-slate-lightest);
  --nt-color-selected-darkest: var(--nt-color-sky-darkest);
  --nt-color-selected-darker: var(--nt-color-sky-darker);
  --nt-color-selected-dark: var(--nt-color-sky-dark);
  --nt-color-selected: var(--nt-color-sky);
  --nt-color-selected-light: var(--nt-color-sky-light);
  --nt-color-selected-lighter: var(--nt-color-sky-lighter);
  --nt-color-selected-lightest: var(--nt-color-sky-lightest);
  --nt-color-success-darkest: var(--nt-color-asparagus-darkest);
  --nt-color-success-darker: var(--nt-color-asparagus-darker);
  --nt-color-success-dark: var(--nt-color-asparagus-dark);
  --nt-color-success: var(--nt-color-asparagus);
  --nt-color-success-light: var(--nt-color-asparagus-light);
  --nt-color-success-lighter: var(--nt-color-asparagus-lighter);
  --nt-color-success-lightest: var(--nt-color-asparagus-lightest);
  --nt-color-textcontrast-darkest: var(--nt-color-alabaster-darkest);
  --nt-color-textcontrast-darker: var(--nt-color-alabaster-darker);
  --nt-color-textcontrast-dark: var(--nt-color-alabaster-dark);
  --nt-color-textcontrast: var(--nt-color-alabaster);
  --nt-color-textcontrast-light: var(--nt-color-alabaster-light);
  --nt-color-textcontrast-lighter: var(--nt-color-alabaster-lighter);
  --nt-color-textcontrast-lightest: var(--nt-color-alabaster-lightest);
  --nt-color-text-darkest: var(--nt-color-midnight-darkest);
  --nt-color-text-darker: var(--nt-color-midnight-darker);
  --nt-color-text-dark: var(--nt-color-midnight-dark);
  --nt-color-text: var(--nt-color-midnight);
  --nt-color-text-light: var(--nt-color-midnight-light);
  --nt-color-text-lighter: var(--nt-color-midnight-lighter);
  --nt-color-text-lightest: var(--nt-color-midnight-lightest);
  --nt-color-warning-darkest: var(--nt-color-clementine-darkest);
  --nt-color-warning-darker: var(--nt-color-clementine-darker);
  --nt-color-warning-dark: var(--nt-color-clementine-dark);
  --nt-color-warning: var(--nt-color-clementine);
  --nt-color-warning-light: var(--nt-color-clementine-light);
  --nt-color-warning-lighter: var(--nt-color-clementine-lighter);
  --nt-color-warning-lightest: var(--nt-color-clementine-lightest);
}
`;const w=r.a`
:root {
  --theme-app-bg: #2b2b2b;
  --theme-app-fg: var(--nt-color-midnight-lightest);
  --theme-app-border: var(--nt-color-midnight-light);

  --theme-primary-bg: var(--nt-color-midnight);
  --theme-primary-bg-hover: var(--nt-color-midnight);
  --theme-primary-bg-focus: var(--nt-color-midnight-light);

  --theme-primary-fg: var(--nt-color-midnight-light);
  --theme-primary-fg-hover: var(--nt-color-midnight-lighter);
  --theme-primary-fg-focus: var(--theme-app-fg);

  --theme-secondary-bg: var(--theme-primary-bg);
  --theme-secondary-bg-hover: var(--theme-primary-bg-hover);
  --theme-secondary-bg-focus: var(--theme-primary-bg-focus);

  --theme-secondary-fg: var(--nt-color-midnight-light);
  --theme-secondary-fg-hover: var(--nt-color-midnight-lighter);
  --theme-secondary-fg-focus: var(--theme-primary-fg);

  --theme-primary-shadow-hover: 1px  1px 3px rgba(255, 255, 255, 0.12), -1px -1px 3px rgba(255, 255, 255, 0.12);
  --theme-primary-shadow-focus: 3px  3px 9px rgba(255, 255, 255, 0.12), -3px -3px 9px rgba(255, 255, 255, 0.12);

  --theme-title-bar-bg: var(--nt-color-midnight-darkest);

  --theme-menu-bg: var(--theme-primary-bg);
  --theme-menu-bg-hover: var(--theme-primary-bg-hover);
  --theme-menu-bg-focus: var(--theme-primary-bg-focus);
  --theme-menu-shadow: var(--theme-primary-shadow-hover);

  --theme-menu-fg: var(--theme-app-fg);
  --theme-menu-fg-hover: var(--theme-app-fg);
  --theme-menu-fg-focus: var(--theme-app-fg);

  --theme-cell-bg: var(--theme-app-bg);
  --theme-cell-shadow-hover: var(--theme-primary-shadow-hover);
  --theme-cell-shadow-focus: var(--theme-primary-shadow-focus);

  --theme-cell-prompt-bg: var(--theme-primary-bg);
  --theme-cell-prompt-bg-hover: var(--theme-primary-bg);
  --theme-cell-prompt-bg-focus: var(--theme-primary-bg);

  --theme-cell-prompt-fg: var(--theme-primary-fg);
  --theme-cell-prompt-fg-hover: var(--theme-primary-fg-hover);
  --theme-cell-prompt-fg-focus: var(--theme-primary-fg-focus);

  --theme-cell-toolbar-bg: var(--theme-primary-bg);
  --theme-cell-toolbar-bg-hover: var(--theme-primary-bg-hover);
  --theme-cell-toolbar-bg-focus: var(--theme-primary-bg-focus);

  --theme-cell-toolbar-fg: var(--theme-secondary-fg);
  --theme-cell-toolbar-fg-hover: var(--theme-secondary-fg-hover);
  --theme-cell-toolbar-fg-focus: var(--theme-secondary-fg-focus);

  --theme-cell-menu-bg: var(--theme-primary-bg);
  --theme-cell-menu-bg-hover: var(--theme-primary-bg-hover);
  --theme-cell-menu-bg-focus: var(--theme-primary-bg-focus);

  --theme-cell-menu-fg: var(--theme-primary-fg);
  --theme-cell-menu-fg-hover: var(--theme-primary-fg-hover);
  --theme-cell-menu-fg-focus: var(--theme-primary-fg-focus);

  --theme-cell-input-bg: var(--theme-secondary-bg);
  --theme-cell-input-fg: var(--theme-app-fg);

  --theme-cell-output-bg: var(--theme-app-bg);
  --theme-cell-output-fg: var(--theme-primary-fg);

  --theme-cell-creator-bg: var(--theme-app-bg);

  --theme-cell-creator-fg: var(--theme-secondary-fg);
  --theme-cell-creator-fg-hover: var(--theme-secondary-fg-hover);
  --theme-cell-creator-fg-focus: var(--theme-secondary-fg-focus);

  --theme-pager-bg: #111;

  --cm-background: #111;
  --cm-color: #ecf0f1;

  --cm-gutter-bg: #777;

  --cm-comment: #777;
  --cm-keyword: #3498db;
  --cm-string: #f1c40f;
  --cm-builtin: #16a085;
  --cm-special: #1abc9c;
  --cm-variable: #ecf0f1;
  --cm-number: #2ecc71;
  --cm-meta: #95a5a6;
  --cm-link: #2ecc71;
  --cm-operator: #ecf0f1;
  --cm-def: #ecf0f1;

  --cm-activeline-bg: #e8f2ff;
  --cm-matchingbracket-outline: grey;
  --cm-matchingbracket-color: white;

  --cm-hint-color: var(--theme-app-fg);
  --cm-hint-color-active: var(--cm-color);
  --cm-hint-bg: var(--theme-app-bg);
  --cm-hint-bg-active: #111;

  --status-bar: #111;
}
`,C=r.a`
:root {
  --theme-app-bg: white;
  --theme-app-fg: var(--nt-color-midnight);
  --theme-app-border: var(--nt-color-grey-light);

  --theme-primary-bg: var(--nt-color-grey-lightest);
  --theme-primary-bg-hover: var(--nt-color-grey-lighter);
  --theme-primary-bg-focus: var(--nt-color-grey-light);

  --theme-primary-fg: var(--nt-color-midnight-light);
  --theme-primary-fg-hover: var(--nt-color-midnight);
  --theme-primary-fg-focus: var(--theme-app-fg);

  --theme-secondary-bg: var(--theme-primary-bg);
  --theme-secondary-bg-hover: var(--theme-primary-bg-hover);
  --theme-secondary-bg-focus: var(--theme-primary-bg-focus);

  --theme-secondary-fg: var(--nt-color-midnight-lighter);
  --theme-secondary-fg-hover: var(--nt-color-midnight-light);
  --theme-secondary-fg-focus: var(--theme-primary-fg);

  --theme-primary-shadow-hover: 1px  1px 3px rgba(0, 0, 0, 0.12), -1px -1px 3px rgba(0, 0, 0, 0.12);
  --theme-primary-shadow-focus: 3px  3px 9px rgba(0, 0, 0, 0.12), -3px -3px 9px rgba(0, 0, 0, 0.12);

  --theme-title-bar-bg: var(--theme-primary-bg-hover);

  --theme-menu-bg: var(--theme-primary-bg);
  --theme-menu-bg-hover: var(--theme-primary-bg-hover);
  --theme-menu-bg-focus: var(--theme-primary-bg-focus);
  --theme-menu-shadow: var(--theme-primary-shadow-hover);

  --theme-menu-fg: var(--theme-app-fg);
  --theme-menu-fg-hover: var(--theme-app-fg);
  --theme-menu-fg-focus: var(--theme-app-fg);

  --theme-cell-bg: var(--theme-app-bg);
  --theme-cell-shadow-hover: var(--theme-primary-shadow-hover);
  --theme-cell-shadow-focus: var(--theme-primary-shadow-focus);

  --theme-cell-prompt-bg: var(--theme-primary-bg);
  --theme-cell-prompt-bg-hover: var(--theme-primary-bg-hover);
  --theme-cell-prompt-bg-focus: var(--theme-primary-bg-focus);

  --theme-cell-prompt-fg: var(--theme-secondary-fg);
  --theme-cell-prompt-fg-hover: var(--theme-secondary-fg-hover);
  --theme-cell-prompt-fg-focus: var(--theme-secondary-fg-focus);

  --theme-cell-toolbar-bg: var(--theme-primary-bg);
  --theme-cell-toolbar-bg-hover: var(--theme-primary-bg-hover);
  --theme-cell-toolbar-bg-focus: var(--theme-primary-bg-focus);

  --theme-cell-toolbar-fg: var(--theme-secondary-fg);
  --theme-cell-toolbar-fg-hover: var(--theme-secondary-fg-hover);
  --theme-cell-toolbar-fg-focus: var(--theme-secondary-fg-focus);

  --theme-cell-menu-bg: var(--theme-primary-bg);
  --theme-cell-menu-bg-hover: var(--theme-primary-bg-hover);
  --theme-cell-menu-bg-focus: var(--theme-primary-bg-focus);

  --theme-cell-menu-fg: var(--theme-primary-fg);
  --theme-cell-menu-fg-hover: var(--theme-primary-fg-hover);
  --theme-cell-menu-fg-focus: var(--theme-primary-fg-focus);

  --theme-cell-input-bg: var(--theme-secondary-bg);
  --theme-cell-input-fg: var(--theme-app-fg);

  --theme-cell-output-bg: var(--theme-app-bg);
  --theme-cell-output-fg: var(--theme-primary-fg);

  --theme-cell-creator-bg: var(--theme-app-bg);

  --theme-cell-creator-fg: var(--theme-secondary-fg);
  --theme-cell-creator-fg-hover: var(--theme-secondary-fg-hover);
  --theme-cell-creator-fg-focus: var(--theme-secondary-fg-focus);

  --theme-pager-bg: #fafafa;

  --cm-background: #fafafa;
  --cm-color: black;

  --cm-gutter-bg: white;

  --cm-comment: #a86;
  --cm-keyword: blue;
  --cm-string: #a22;
  --cm-builtin: #077;
  --cm-special: #0aa;
  --cm-variable: black;
  --cm-number: #3a3;
  --cm-meta: #555;
  --cm-link: #3a3;
  --cm-operator: black;
  --cm-def: black;

  --cm-activeline-bg: #e8f2ff;
  --cm-matchingbracket-outline: grey;
  --cm-matchingbracket-color: black;

  --cm-hint-color: var(--cm-color);
  --cm-hint-color-active: var(--cm-color);
  --cm-hint-bg: var(--theme-app-bg);
  --cm-hint-bg-active: #abd1ff;

  --status-bar: #eeedee;
}
`;o.d(t,"b",function(){return w}),o.d(t,"d",function(){return C}),o.d(t,"c",function(){return v}),o.d(t,"e",function(){return k}),o.d(t,"f",function(){return y}),o.d(t,"g",function(){return l}),o.d(t,"h",function(){return a}),o.d(t,"i",function(){return b}),o.d(t,"a",function(){return s})},966:function(e,t,o){"use strict";(function(e){var r=o(89),n=o(483),l=o(689),a=o(53),i=o(2),c=o(586),s=o(1205),d=o.n(s),p=o(81),h=o(1216),m=o(1217),u=o(1667),g=o(1235),b=o(1236),f=o(1237),v=o(1682),x=o(1252),k=o(44);const y=a.List(),w=a.Set(),C=Object(k.c)(l.a).attrs(e=>({className:e.isSelected?"selected":""}))`
  /*
   * Show the cell-toolbar-mask if hovering on cell,
   * cell was the last clicked
   */
  &:hover ${v.a}, &.selected ${v.a} {
    display: block;
  }
`;C.displayName="Cell";const E=k.c.div`
  background-color: darkblue;
  color: ghostwhite;
  padding: 9px 16px;

  font-size: 12px;
  line-height: 20px;
`;E.displayName="CellBanner";const M=Object(p.b)((e,{id:t,contentRef:o})=>{return e=>{const n=r.r.model(e,{contentRef:o});if(!n||"notebook"!==n.type)throw new Error("Cell components should not be used with non-notebook models");const l=n.kernelRef,a=r.r.notebook.cellById(n,{id:t});if(!a)throw new Error("cell not found inside cell map");const i=a.cell_type,c=a.get("outputs",y),s="code"===i&&(a.getIn(["metadata","inputHidden"])||a.getIn(["metadata","hide_input"]))||!1,d="code"===i&&(0===c.size||a.getIn(["metadata","outputHidden"])),p="code"===i&&a.getIn(["metadata","outputExpanded"]),h=a.getIn(["metadata","tags"])||w,m=n.getIn(["cellPagers",t])||y;let u;if(l){const t=r.r.kernel(e,{kernelRef:l});t&&(u=t.channels)}return{cellFocused:n.cellFocused===t,cellStatus:n.transient.getIn(["cellMap",t,"status"]),cellType:i,channels:u,contentRef:o,editorFocused:n.editorFocused===t,executionCount:a.get("execution_count",null),outputExpanded:p,outputHidden:d,outputs:c,pager:m,source:a.get("source",""),sourceHidden:s,tags:h,theme:r.r.userTheme(e)}}},(e,{id:t,contentRef:o})=>{return e=>({focusAboveCell:()=>{e(r.a.focusPreviousCell({id:t,contentRef:o})),e(r.a.focusPreviousCellEditor({id:t,contentRef:o}))},focusBelowCell:()=>{e(r.a.focusNextCell({id:t,createCellIfUndefined:!0,contentRef:o})),e(r.a.focusNextCellEditor({id:t,contentRef:o}))},focusEditor:()=>e(r.a.focusCellEditor({id:t,contentRef:o})),selectCell:()=>e(r.a.focusCell({id:t,contentRef:o})),unfocusEditor:()=>e(r.a.focusCellEditor({id:void 0,contentRef:o})),changeCellType:n=>e(r.a.changeCellType({contentRef:o,id:t,to:n})),clearOutputs:()=>e(r.a.clearOutputs({id:t,contentRef:o})),deleteCell:()=>e(r.a.deleteCell({id:t,contentRef:o})),executeCell:()=>e(r.a.executeCell({id:t,contentRef:o})),toggleCellInputVisibility:()=>e(r.a.toggleCellInputVisibility({id:t,contentRef:o})),toggleCellOutputVisibility:()=>e(r.a.toggleCellOutputVisibility({id:t,contentRef:o})),toggleOutputExpansion:()=>e(r.a.toggleOutputExpansion({id:t,contentRef:o})),toggleParameterCell:()=>e(r.a.toggleParameterCell({id:t,contentRef:o})),updateOutputMetadata:(n,l,a)=>{e(r.a.updateOutputMetadata({id:t,contentRef:o,metadata:l,index:n,mediaType:a}))}})})(class extends i.PureComponent{constructor(){super(...arguments),this.toggleCellType=(()=>{this.props.changeCellType("markdown"===this.props.cellType?"code":"markdown")})}render(){const{executeCell:e,deleteCell:t,clearOutputs:o,toggleParameterCell:r,toggleCellInputVisibility:a,toggleCellOutputVisibility:c,toggleOutputExpansion:s,changeCellType:d,cellFocused:p,cellStatus:h,cellType:m,editorFocused:f,focusAboveCell:k,focusBelowCell:y,focusEditor:w,id:M,tags:O,selectCell:R,unfocusEditor:S,contentRef:N,sourceHidden:T}=this.props,D="busy"===h,j="queued"===h;let z=null;switch(m){case"code":z=i.createElement(i.Fragment,null,i.createElement(l.c,{hidden:this.props.sourceHidden},i.createElement(l.g,{counter:this.props.executionCount,running:D,queued:j}),i.createElement(l.i,null,i.createElement(u.a,{id:M,contentRef:N,focusAbove:k,focusBelow:y}))),i.createElement(l.f,null,this.props.pager.map((e,t)=>i.createElement(n.d,{data:e.data,metadata:e.metadata},i.createElement(n.b.Json,null),i.createElement(n.b.JavaScript,null),i.createElement(n.b.HTML,null),i.createElement(n.b.Markdown,null),i.createElement(n.b.LaTeX,null),i.createElement(n.b.SVG,null),i.createElement(n.b.Image,null),i.createElement(n.b.Plain,null)))),i.createElement(l.e,{hidden:this.props.outputHidden,expanded:this.props.outputExpanded},this.props.outputs.map((e,t)=>i.createElement(n.c,{output:e,key:t},i.createElement(x.a,{output_type:"display_data",cellId:M,contentRef:N,index:t}),i.createElement(x.a,{output_type:"execute_result",cellId:M,contentRef:N,index:t}),i.createElement(n.a,null),i.createElement(n.e,null)))));break;case"markdown":z=i.createElement(b.a,{focusAbove:k,focusBelow:y,focusEditor:w,cellFocused:p,editorFocused:f,unfocusEditor:S,source:this.props.source},i.createElement(l.i,null,i.createElement(u.a,{id:M,contentRef:N,focusAbove:k,focusBelow:y})));break;case"raw":z=i.createElement(l.i,null,i.createElement(u.a,{id:M,contentRef:N,focusAbove:k,focusBelow:y}));break;default:z=i.createElement("pre",null,this.props.source)}return i.createElement(g.a,{focused:p,onClick:R},i.createElement(C,{isSelected:p},O.has("parameters")?i.createElement(E,null,"Papermill - Parametrized"):null,O.has("default parameters")?i.createElement(E,null,"Papermill - Default Parameters"):null,i.createElement(v.b,{type:m,cellFocused:p,executeCell:e,deleteCell:t,clearOutputs:o,toggleParameterCell:r,toggleCellInputVisibility:a,toggleCellOutputVisibility:c,toggleOutputExpansion:s,changeCellType:this.toggleCellType,sourceHidden:T}),z))}}),O=k.c.div`
  padding-top: var(--nt-spacing-m, 10px);
  padding-left: var(--nt-spacing-m, 10px);
  padding-right: var(--nt-spacing-m, 10px);
`;class R extends i.PureComponent{constructor(e){super(e),this.keyDown=this.keyDown.bind(this)}componentDidMount(){document.addEventListener("keydown",this.keyDown)}componentWillUnmount(){document.removeEventListener("keydown",this.keyDown)}keyDown(t){if(13!==t.keyCode)return;const{executeFocusedCell:o,focusNextCell:r,focusNextCellEditor:n,contentRef:l}=this.props;let a=t.ctrlKey;"darwin"===e.platform&&(a=(t.metaKey||t.ctrlKey)&&!(t.metaKey&&t.ctrlKey)),(t.shiftKey||a)&&!(t.shiftKey&&a)&&(t.preventDefault(),o({contentRef:l}),t.shiftKey&&(r({id:void 0,createCellIfUndefined:!0,contentRef:l}),n({id:void 0,contentRef:l})))}render(){return i.createElement(i.Fragment,null,i.createElement(O,null,i.createElement(h.a,{id:this.props.cellOrder.get(0),above:!0,contentRef:this.props.contentRef}),this.props.cellOrder.map(e=>i.createElement("div",{className:"cell-container",key:`cell-container-${e}`},i.createElement(m.a,{moveCell:this.props.moveCell,id:e,focusCell:this.props.focusCell,contentRef:this.props.contentRef},i.createElement(M,{id:e,contentRef:this.props.contentRef})),i.createElement(h.a,{key:`creator-${e}`,id:e,above:!1,contentRef:this.props.contentRef})))),i.createElement(f.a,{contentRef:this.props.contentRef}),function(e){switch(e){case"dark":return i.createElement(l.b,null);case"light":default:return i.createElement(l.d,null)}}(this.props.theme))}}R.defaultProps={theme:"light"};const S=Object(c.DragDropContext)(d.a)(R);t.a=Object(p.b)((e,t)=>{const{contentRef:o}=t;if(!o)throw new Error("<Notebook /> has to have a contentRef");return e=>{const t=r.r.content(e,{contentRef:o}),n=r.r.model(e,{contentRef:o});if(!n||!t)throw new Error("<Notebook /> has to have content & model that are notebook types");const l=r.r.userTheme(e);if("notebook"!==n.type)return{cellOrder:a.List(),contentRef:o,theme:l};if("notebook"!==n.type)throw new Error("<Notebook /> has to have content & model that are notebook types");return{cellOrder:n.notebook.cellOrder,contentRef:o,theme:l}}},e=>({executeFocusedCell:t=>e(r.a.executeFocusedCell(t)),focusCell:t=>e(r.a.focusCell(t)),focusNextCell:t=>e(r.a.focusNextCell(t)),focusNextCellEditor:t=>e(r.a.focusNextCellEditor(t)),moveCell:t=>e(r.a.moveCell(t)),updateOutputMetadata:t=>e(r.a.updateOutputMetadata(t))}))(S)}).call(this,o(87))}}]);