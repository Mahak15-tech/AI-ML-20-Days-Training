const $ = id => document.getElementById(id);
let data = { model_comparison: [], data_quality: [], confusion_matrix: null, class_metrics: [], misclassified_examples: [] };
let theme = localStorage.getItem("day10-dashboard-theme") || "light";
const reportBase = "/reports/";
const metricLabels = { test_f1:"Test F1", test_accuracy:"Test accuracy", test_precision:"Test precision", test_recall:"Test recall", cv_f1_mean:"CV F1 mean" };

function safeNum(v) { if (v === null || v === undefined || String(v).trim() === "") return NaN; const n = Number(v); return Number.isFinite(n) ? n : NaN; }
function fmt(v, digits=3) { const n=safeNum(v); return Number.isFinite(n) ? n.toFixed(digits) : "—"; }
function pct(v) { const n=safeNum(v); return Number.isFinite(n) ? (n*100).toFixed(1)+"%" : "—"; }
function esc(v) { return String(v ?? "").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function norm(s) { return String(s||"").toLowerCase().replace(/[^a-z0-9]/g,""); }
function keyFor(row, aliases) { const keys=Object.keys(row||{}); return keys.find(k=>aliases.map(norm).includes(norm(k))); }
function getVal(row, aliases, fallback="") { const k=keyFor(row,aliases); return k===undefined?fallback:row[k]; }
function parseCSV(text) {
  const rows=[]; let row=[], cell="", quoted=false;
  for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];if(c==='"'&&quoted&&n==='"'){cell+='"';i++;}else if(c==='"'){quoted=!quoted;}else if(c===","&&!quoted){row.push(cell);cell="";}else if((c==="\n"||c==="\r")&&!quoted){if(c==="\r"&&n==="\n")i++;row.push(cell);if(row.some(x=>x.trim()!==""))rows.push(row);row=[];cell="";}else cell+=c;}
  if(cell.length||row.length){row.push(cell);rows.push(row);} if(!rows.length)return [];
  const headers=rows.shift().map(h=>h.replace(/^\uFEFF/,"").trim());
  return rows.map(r=>Object.fromEntries(headers.map((h,i)=>[h,(r[i]??"").trim()])));
}
async function fetchCSV(name, required=false) {
  const res=await fetch(reportBase+name+"?t="+Date.now());
  if(!res.ok){if(required)throw new Error(`${name} was not found. Run the Python training script and export the reports first.`);return [];}
  return parseCSV(await res.text());
}
async function fetchJSON(name) {const res=await fetch(reportBase+name+"?t="+Date.now());if(!res.ok)return null;return res.json();}
function modelRows() {
  return data.model_comparison.map(r=>({
    model:String(getVal(r,["model","name","estimator"],"Unknown model")),
    cv_f1_mean:safeNum(getVal(r,["cv_f1_mean","mean_cv_f1","cv_f1"])),
    cv_f1_std:safeNum(getVal(r,["cv_f1_std","std_cv_f1","cv_f1_std_dev"])),
    test_accuracy:safeNum(getVal(r,["test_accuracy","accuracy","test_acc"])),
    test_precision:safeNum(getVal(r,["test_precision","precision"])),
    test_recall:safeNum(getVal(r,["test_recall","recall"])),
    test_f1:safeNum(getVal(r,["test_f1","f1","f1_score","test_f1_score"]))
  })).filter(r=>r.model!=="Unknown model");
}
function bestModel(){return [...modelRows()].filter(r=>Number.isFinite(r.cv_f1_mean)).sort((a,b)=>b.cv_f1_mean-a.cv_f1_mean)[0]||modelRows()[0]||null;}
function pal(){const d=theme==="dark";return{text:d?"#fff4ee":"#34272b",muted:d?"#c0aab1":"#887579",grid:d?"#4c3742":"#e6d6d3",burgundy:d?"#d9a1aa":"#51283b",rose:d?"#d58b98":"#b76e79",gold:d?"#e3c79e":"#d9b98c",green:d?"#8bc6a0":"#56866e",surface:d?"#291d25":"#fffaf7"};}
function layout(extra={}){const p=pal();return{paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",font:{family:"DM Sans, sans-serif",color:p.muted,size:10},margin:{l:44,r:18,t:16,b:48},xaxis:{gridcolor:p.grid,zerolinecolor:p.grid,linecolor:p.grid,tickfont:{color:p.muted,size:10}},yaxis:{gridcolor:p.grid,zerolinecolor:p.grid,linecolor:p.grid,tickfont:{color:p.muted,size:10},rangemode:"tozero"},legend:{orientation:"h",y:-.22,font:{size:10,color:p.muted}},hoverlabel:{bgcolor:p.surface,bordercolor:p.grid,font:{color:p.text,family:"DM Sans, sans-serif"}},...extra};}
function chart(id,traces,opts={}){const el=$(id);if(el&&window.Plotly)Plotly.react(el,traces,layout(opts),{responsive:true,displayModeBar:false});}
function tableRows(id, rows, headers, formatter) {const body=$(id);if(!body)return;body.innerHTML=rows.length?rows.map(r=>"<tr>"+headers.map(h=>`<td>${formatter?formatter(r,h):esc(r[h]??"—")}</td>`).join("")+"</tr>").join(""):`<tr><td colspan="${headers.length}">No report data available yet.</td></tr>`;}
function renderOverview(){
 const ms=modelRows(),b=bestModel(),cm=data.confusion_matrix;
 $("kpiAccuracy").textContent=b?pct(b.test_accuracy):"—";$("kpiF1").textContent=b?fmt(b.test_f1):"—";$("kpiCV").textContent=b?fmt(b.cv_f1_mean):"—";
 const total=cm&&cm.matrix?cm.matrix.flat().reduce((s,n)=>s+(Number(n)||0),0):NaN;
 $("kpiSamples").textContent=Number.isFinite(total)?total:"—";$("testSplitNote").textContent=Number.isFinite(total)?"Current confusion matrix total":"Held-out test records";
 $("winnerName").textContent=b?b.model:"Awaiting model report";$("winnerCV").textContent=b?fmt(b.cv_f1_mean):"—";$("winnerF1").textContent=b?fmt(b.test_f1):"—";$("winnerPR").textContent=b?`${fmt(b.test_precision)} / ${fmt(b.test_recall)}`:"—";
 $("winnerInsight").textContent=b?`${b.model} had the highest mean cross-validation F1 in the current comparison. This does not guarantee performance on new real-world data.`:"Run the Day 10 Python workflow to populate this summary.";
 $("perfBestF1").textContent=b?fmt(b.test_f1):"—";$("perfBestCV").textContent=b?fmt(b.cv_f1_mean):"—";$("perfModelCount").textContent=ms.length;$("perfCVStd").textContent=b?fmt(b.cv_f1_std):"—";
 const dq=data.data_quality;const rows=dq.map(r=>({column:getVal(r,["column","feature","name"],"—"),missing:safeNum(getVal(r,["missing_values","missing_count","missing","missing values"],0))||0,duplicates:getVal(r,["duplicate_rows","duplicates"],"—")}));
 const missing=rows.reduce((s,r)=>s+r.missing,0);
 $("overviewQuality").innerHTML=`<div class="quality-row"><div class="quality-icon rose-bg">∅</div><div class="quality-copy"><b>Missing values</b><span>${rows.filter(r=>r.missing>0).map(r=>`${esc(r.column)}: ${r.missing}`).join(" · ")||"No missing values reported"}</span></div><strong>${missing}</strong></div><div class="quality-row"><div class="quality-icon green-bg">✓</div><div class="quality-copy"><b>Duplicate rows</b><span>From the data quality report</span></div><strong>${getVal(dq[0]||{},["duplicate_rows","duplicates"],"0")}</strong></div><div class="quality-row"><div class="quality-icon gold-bg">▦</div><div class="quality-copy"><b>Columns audited</b><span>Rows in data quality report</span></div><strong>${dq.length||"—"}</strong></div>`;
 tableRows("modelTableBody",ms,["model","cv_f1_mean","cv_f1_std","test_accuracy","test_precision","test_recall","test_f1"],(r,k)=>k==="model"?`<span class="model-name">${esc(r.model)}</span>${b&&r.model===b.model?'<span class="best-label">SELECTED</span>':""}`:fmt(r[k]));
}
function renderPerformance(){
 const rows=modelRows(),p=pal(),metric=$("metricSelector").value||"test_f1";
 chart("overviewModelChart",[{type:"bar",x:rows.map(r=>r.model),y:rows.map(r=>r.test_f1),marker:{color:rows.map(r=>r.model===bestModel()?.model?p.burgundy:p.rose)},hovertemplate:"%{x}<br>Test F1: %{y:.3f}<extra></extra>"}],{yaxis:{range:[0,1],tickformat:".0%",gridcolor:p.grid},showlegend:false,margin:{l:42,r:12,t:12,b:55}});
 chart("metricChart",[{type:"bar",x:rows.map(r=>r.model),y:rows.map(r=>r[metric]),marker:{color:rows.map(r=>r.model===bestModel()?.model?p.burgundy:p.rose)},text:rows.map(r=>fmt(r[metric])),textposition:"outside",cliponaxis:false,hovertemplate:"%{x}<br>"+metricLabels[metric]+": %{y:.3f}<extra></extra>"}],{yaxis:{range:[0,Math.min(1.12,Math.max(.2,...rows.map(r=>Number.isFinite(r[metric])?r[metric]:0)+.12))],gridcolor:p.grid},showlegend:false,margin:{l:42,r:20,t:25,b:55}});
 chart("cvChart",[{type:"bar",x:rows.map(r=>r.model),y:rows.map(r=>r.cv_f1_mean),error_y:{type:"data",array:rows.map(r=>Number.isFinite(r.cv_f1_std)?r.cv_f1_std:0),visible:true,color:p.rose},marker:{color:rows.map(r=>r.model===bestModel()?.model?p.burgundy:p.rose)},hovertemplate:"%{x}<br>CV F1 mean: %{y:.3f}<extra></extra>"}],{yaxis:{range:[0,1],gridcolor:p.grid},showlegend:false,margin:{l:42,r:12,t:12,b:55}});
}
function matrixPayload(){
 const cm=data.confusion_matrix;if(!cm)return null;
 if(Array.isArray(cm.matrix))return{matrix:cm.matrix,labels:cm.labels||["0","1"]};
 if(Array.isArray(cm.rows)) {
   const rows=cm.rows;const actualKey=keyFor(rows[0]||{},["actual","true_label","true"]);const predictedKey=keyFor(rows[0]||{},["predicted","predicted_label","prediction"]);const countKey=keyFor(rows[0]||{},["count","n","value"]);
   if(actualKey&&predictedKey){const labels=[...new Set(rows.flatMap(r=>[r[actualKey],r[predictedKey]]))].sort();return{labels,matrix:labels.map(a=>labels.map(p=>rows.filter(r=>String(r[actualKey])===String(a)&&String(r[predictedKey])===String(p)).reduce((s,r)=>s+(countKey?Number(r[countKey])||0:1),0))) };}
 }
 return null;
}
function renderPrediction(){
 const p=pal(),cm=matrixPayload();
 if(cm&&cm.matrix.length){chart("confusionChart",[{type:"heatmap",x:cm.labels.map(x=>"Predicted "+x),y:cm.labels.map(x=>"Actual "+x),z:cm.matrix,colorscale:[[0,theme==="dark"?"#352630":"#f5e9e7"],[.5,p.rose],[1,p.burgundy]],text:cm.matrix.map(row=>row.map(v=>String(v))),texttemplate:"%{text}",textfont:{size:20,color:theme==="dark"?"#fff4ee":"#fffaf7"},hovertemplate:"%{y}<br>%{x}<br>Count: %{z}<extra></extra>"}],{margin:{l:90,r:18,t:12,b:60},xaxis:{side:"bottom",gridcolor:p.grid},yaxis:{autorange:"reversed",gridcolor:p.grid}});
 const flat=cm.matrix.flat().map(Number),total=flat.reduce((a,b)=>a+b,0),correct=cm.matrix.reduce((s,row,i)=>s+(Number(row[i])||0),0),incorrect=total-correct;
 $("correctCount").textContent=correct;$("incorrectCount").textContent=incorrect;
 chart("predictionDonut",[{type:"pie",labels:["Correct","Incorrect"],values:[correct,incorrect],hole:.7,sort:false,marker:{colors:[p.green,p.rose],line:{color:p.surface,width:3}},textinfo:"none",hovertemplate:"%{label}: %{value} (%{percent})<extra></extra>"}],{showlegend:false,margin:{l:8,r:8,t:10,b:10},annotations:[{text:`${total?Math.round(correct/total*100):0}%<br><span style="font-size:10px">correct</span>`,showarrow:false,font:{size:21,color:p.text}}]});
 }else{$("confusionChart").innerHTML='<div class="chart-placeholder">Confusion matrix report not found. Re-run the updated Python script.</div>';$("predictionDonut").innerHTML='<div class="chart-placeholder">Prediction counts will appear when confusion_matrix.csv is available.</div>';}
 const classes=data.class_metrics||[];
 tableRows("classMetricsBody",classes,["class","precision","recall","f1-score","support"],(r,k)=>esc(getVal(r,k==="class"?["class","label"]:k==="f1-score"?["f1-score","f1_score","f1"]: [k], "—")));
 const classLabels=classes.map(r=>String(getVal(r,["class","label"],"—"))),precision=classes.map(r=>safeNum(getVal(r,["precision"]))),recall=classes.map(r=>safeNum(getVal(r,["recall"]))),f1=classes.map(r=>safeNum(getVal(r,["f1-score","f1_score","f1"])));
 if(classes.length)chart("classMetricsChart",[{type:"bar",name:"Precision",x:classLabels,y:precision,marker:{color:p.burgundy}},{type:"bar",name:"Recall",x:classLabels,y:recall,marker:{color:p.rose}},{type:"bar",name:"F1",x:classLabels,y:f1,marker:{color:p.gold}}],{barmode:"group",yaxis:{range:[0,1],gridcolor:p.grid},margin:{l:42,r:12,t:12,b:45}});
 const errors=data.misclassified_examples||[];const errorHeaders=errors.length?Object.keys(errors[0]):[];
 $("errorCountBadge").textContent=`${errors.length} records`;
 $("errorsTableHead").innerHTML=errorHeaders.length?`<tr>${errorHeaders.map(h=>`<th>${esc(h)}</th>`).join("")}</tr>`:"";
 $("errorsTableBody").innerHTML=errors.length?errors.slice(0,100).map(r=>`<tr>${errorHeaders.map(h=>`<td>${esc(r[h])}</td>`).join("")}</tr>`).join(""):'<tr><td>No misclassified examples found, or report is missing.</td></tr>';
}
function renderQuality(rows=data.data_quality){
 const normalized=rows.map(r=>({column:getVal(r,["column","feature","name"],"—"),missing:safeNum(getVal(r,["missing_values","missing_count","missing","missing values"],0))||0,duplicates:getVal(r,["duplicate_rows","duplicates"],"—"),dtype:getVal(r,["dtype","data_type","type"],"—"),unique:getVal(r,["unique_values","unique"],"—")}));
 const missing=normalized.reduce((s,r)=>s+r.missing,0);
 $("dataRows").textContent=getVal(rows[0]||{},["rows","row_count","dataset_rows"],"400");$("dataCols").textContent=getVal(rows[0]||{},["columns","column_count","dataset_columns"],String(rows.length||4));
 $("missingTotal").textContent=missing;$("duplicateTotal").textContent=getVal(rows[0]||{},["duplicate_rows","duplicates"],"0");
 chart("missingChart",[{type:"bar",x:normalized.map(r=>r.column),y:normalized.map(r=>r.missing),marker:{color:normalized.map(r=>r.missing>0?pal().rose:pal().green)},text:normalized.map(r=>String(r.missing)),textposition:"outside",hovertemplate:"%{x}<br>Missing: %{y}<extra></extra>"}],{yaxis:{rangemode:"tozero",gridcolor:pal().grid},showlegend:false,margin:{l:42,r:12,t:15,b:60}});
 $("qualityList").innerHTML=[["Rows",getVal(rows[0]||{},["rows","row_count","dataset_rows"],"400")],["Columns",getVal(rows[0]||{},["columns","column_count","dataset_columns"],String(rows.length||4))],["Missing cells",missing],["Duplicate rows",getVal(rows[0]||{},["duplicate_rows","duplicates"],"0")]].map(([a,b])=>`<div class="quality-list-item"><span>${esc(a)}</span><b>${esc(b)}</b></div>`).join("");
 const keys=[...new Set(rows.flatMap(r=>Object.keys(r)))];
 $("qualityTableHead").innerHTML=`<tr>${keys.map(k=>`<th>${esc(k)}</th>`).join("")}</tr>`;
 $("qualityTableBody").innerHTML=rows.map(r=>`<tr>${keys.map(k=>`<td>${esc(r[k]??"—")}</td>`).join("")}</tr>`).join("")||'<tr><td>No data quality rows found.</td></tr>';
}
function renderAll(){renderOverview();renderPerformance();renderPrediction();renderQuality();renderOverviewChart();$("lastUpdated").textContent="Reports loaded · "+new Date().toLocaleTimeString();}
function renderOverviewChart(){renderPerformance();}
function showNotice(message){$("loadNotice").textContent=message;$("loadNotice").classList.remove("hidden");}
async function loadReports(){
 try{
   const [model,quality,confusion,classMetrics,errors]=await Promise.all([
    fetchCSV("model_comparison.csv",true),fetchCSV("data_quality.csv"),fetchJSON("confusion_matrix.json"),fetchCSV("class_metrics.csv"),fetchCSV("misclassified_examples.csv")
   ]);
   data.model_comparison=model;data.data_quality=quality;data.confusion_matrix=confusion;data.class_metrics=classMetrics;data.misclassified_examples=errors;
   if(!model.length)throw new Error("model_comparison.csv has no rows. Run the Day 10 training script.");
   renderAll();
   if(!confusion)showNotice("Model and data reports loaded. Prediction charts need confusion_matrix.json. Add the export block from the dashboard README to your Python script, then rerun it.");
   else $("loadNotice").classList.add("hidden");
 }catch(err){showNotice(`${err.message} Make sure the dashboard server is running from the day-10 folder and reports/ contains the CSV files.`);$("lastUpdated").textContent="Waiting for reports";}
}
function setTheme(next){theme=next;document.documentElement.dataset.theme=theme;localStorage.setItem("day10-dashboard-theme",theme);$("themeToggle").textContent=theme==="dark"?"☾":"☼";if(data.model_comparison.length)renderAll();}
function activateTab(tab){currentTab=tab;document.querySelectorAll(".nav-link").forEach(b=>b.classList.toggle("active",b.dataset.tab===tab));document.querySelectorAll(".tab-panel").forEach(p=>p.classList.toggle("active",p.id===`tab-${tab}`));const names={overview:"Overview",performance:"Model Performance",prediction:"Prediction Analysis",data:"Data Intelligence",project:"Project & Methodology"};$("pageTitle").textContent=names[tab]||"Overview";$("mainNav").classList.remove("open");setTimeout(()=>window.dispatchEvent(new Event("resize")),80);}
function downloadText(filename,text,type="text/csv"){const blob=new Blob([text],{type});const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=filename;a.click();URL.revokeObjectURL(url);}
async function downloadReport(name){try{const r=await fetch(reportBase+name);if(!r.ok)throw new Error();downloadText(name,await r.text());}catch{showNotice(`${name} is not available yet. Run the Python workflow and confirm the report was exported.`);}}
function csvEscape(v){const s=String(v??"");return /[",\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}
function exportSummary(){const b=bestModel();const rows=[["Metric","Value"],["Selected model",b?.model||"Not available"],["Test accuracy",b?.test_accuracy??""],["Test precision",b?.test_precision??""],["Test recall",b?.test_recall??""],["Test F1",b?.test_f1??""],["CV F1 mean",b?.cv_f1_mean??""],["CV F1 std",b?.cv_f1_std??""],["Dataset type","Synthetic demonstration dataset"]];downloadText("day10_dashboard_summary.csv",rows.map(r=>r.map(csvEscape).join(",")).join("\r\n"));}
document.querySelectorAll(".nav-link").forEach(b=>b.addEventListener("click",()=>activateTab(b.dataset.tab)));
$("themeToggle").addEventListener("click",()=>setTheme(theme==="dark"?"light":"dark"));
$("refreshBtn").addEventListener("click",loadReports);$("mobileMenu").addEventListener("click",()=>$("mainNav").classList.toggle("open"));
$("metricSelector").addEventListener("change",renderPerformance);$("downloadSummary").addEventListener("click",exportSummary);$("downloadQuality").addEventListener("click",()=>downloadReport("data_quality.csv"));
document.querySelectorAll("[data-download]").forEach(b=>b.addEventListener("click",()=>downloadReport(b.dataset.download)));
setTheme(theme);loadReports();
