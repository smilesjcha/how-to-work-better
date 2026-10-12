import fs from 'node:fs/promises';
import path from 'node:path';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const caseDir=path.join(root,'materials/08-realistic-admin-case');
const data=JSON.parse(await fs.readFile(path.join(caseDir,'data/case-data.json'),'utf8'));
const out=path.join(root,'tmp/workbook-review');
await fs.mkdir(out,{recursive:true});
const wb=Workbook.create();
const sheets={};
for(const name of ['운영집계','일정','WBS','등록원장','상담기록','설문','집행원장','기업연계']) {
  const s=wb.worksheets.add(name); sheets[name]=s; s.showGridLines=false;
}
const navy='#0B1F33', teal='#007C83';
function base(s,title,cols,rows) {
  const area=s.getRangeByIndexes(0,0,rows,cols);
  area.format.font={name:'Arial',size:11,color:'#17212B'};
  area.format.verticalAlignment='center'; area.format.rowHeight=25;
  area.format.columnWidth=18;
  s.getRange('A2').values=[[title]];
  s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:navy};
  s.getRange('A3').values=[['교육용 가상 자료 / 실제 사람·기업·집행 정보 없음']];
  s.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#5C6973'};
}
function header(s,cols) {
  const h=s.getRangeByIndexes(4,0,1,cols);
  h.format.fill=navy; h.format.font={name:'Arial',size:11,bold:true,color:'#FFFFFF'};
  h.format.rowHeight=32; h.format.horizontalAlignment='center';
}
const mapping={'participants.csv':'등록원장','counseling.csv':'상담기록','surveys.csv':'설문','budget-ledger.csv':'집행원장','employer-links.csv':'기업연계'};
for(const d of data.datasets.filter(d=>mapping[d.name])) {
  const s=sheets[mapping[d.name]], n=d.rows.length, k=d.headers.length;
  base(s,mapping[d.name]+' 원자료',k,n+5);
  s.getRangeByIndexes(4,0,1,k).values=[d.headers]; header(s,k);
  const values=d.rows.map(row=>row.map((v,c)=>
    (d.name==='counseling.csv'&&c===3)||(d.name==='budget-ledger.csv'&&c===1)?new Date(v+'T00:00:00Z'):v));
  s.getRangeByIndexes(5,0,n,k).values=values;
  s.tables.add(`A5:${String.fromCharCode(64+k)}${n+5}`,true,'Source'+Object.keys(mapping).indexOf(d.name));
  s.freezePanes.freezeRows(5); s.freezePanes.freezeColumns(2);
  if(d.name==='counseling.csv') {s.getRange(`D6:D${n+5}`).setNumberFormat('yyyy-mm-dd'); s.getRange(`I6:I${n+5}`).setNumberFormat('0'); s.getRange(`J6:J${n+5}`).setNumberFormat('0.00');}
  if(d.name==='budget-ledger.csv') {s.getRange(`B6:B${n+5}`).setNumberFormat('yyyy-mm-dd'); s.getRange(`F6:F${n+5}`).setNumberFormat('#,##0'); s.getRange(`E6:E${n+5}`).format.columnWidth=32;}
  s.getRangeByIndexes(0,k-1,n+5,1).format.columnWidth=34;
}
const summary=sheets['운영집계']; base(summary,'2026년 9월 취업역량 지원사업 운영',4,33); summary.tabColor=navy;
summary.getRange('A5:C5').values=[['지표','2026-08','2026-09']]; header(summary,3);
summary.getRange('A6:A15').values=[['등록 명'],['수료 명'],['수료율'],['취업확인 명'],['수료 대비 취업확인율'],['상담 건'],['최초응답 평균 시간'],['설문 응답 명'],['설문 응답률'],['만족도 5점']];
for(const col of ['B','C']) {
  const month=`${col}$5`;
  for(const [row,formula] of [
    [6,`COUNTIFS('등록원장'!$B$6:$B$365,${month})`],
    [7,`COUNTIFS('등록원장'!$B$6:$B$365,${month},'등록원장'!$F$6:$F$365,"수료")`],
    [8,`${col}7/${col}6`],
    [9,`COUNTIFS('등록원장'!$B$6:$B$365,${month},'등록원장'!$G$6:$G$365,"취업확인")`],
    [10,`${col}9/${col}7`],
    [11,`COUNTIFS('상담기록'!$C$6:$C$1445,${month})`],
    [12,`AVERAGEIFS('상담기록'!$J$6:$J$1445,'상담기록'!$C$6:$C$1445,${month})`],
    [13,`COUNTIFS('설문'!$C$6:$C$325,${month})`],
    [14,`${col}13/${col}6`],
    [15,`AVERAGEIFS('설문'!$E$6:$E$325,'설문'!$C$6:$C$325,${month})`]
  ]) summary.getRange(`${col}${row}`).formulas=[['='+formula]];
}
summary.getRange('B6:C15').setNumberFormat('#,##0');
for(const row of [8,10,14]) summary.getRange(`B${row}:C${row}`).setNumberFormat('0.0%');
for(const row of [12,15]) summary.getRange(`B${row}:C${row}`).setNumberFormat('0.00');
summary.getRange('A18').values=[['9월 사업 예산 원']];
summary.getRange('A20:D20').values=[['비목','승인 예산 원','집행 원','잔액 원']];
summary.getRange('A20:D20').format.fill=navy; summary.getRange('A20:D20').format.font={color:'#FFFFFF',bold:true};
summary.getRange('A21:B26').values=data.categories;
summary.getRange('B21:B26').format.font={color:'#1F5A99'};
summary.getRange('C21').formulas=[['=SUMIFS(\'집행원장\'!$F$6:$F$65,\'집행원장\'!$C$6:$C$65,$A21)']];
summary.getRange('C21:C26').fillDown(); summary.getRange('D21').formulas=[['=B21-C21']]; summary.getRange('D21:D26').fillDown();
summary.getRange('A27').values=[['합계']]; summary.getRange('B27:D27').formulas=[['=SUM(B21:B26)','=SUM(C21:C26)','=SUM(D21:D26)']];
summary.getRange('A27:D27').format.borders={preset:'doubleBottom',style:'thin',color:navy}; summary.getRange('A27:D27').format.font={bold:true};
summary.getRange('B21:D27').setNumberFormat('#,##0');
summary.getRange('A30').values=[['취업확인율의 분모는 수료 인원이다. 상담 건수는 고유 인원 수가 아니다.']];
summary.getRange('A31').values=[['자료의 지표 정의와 가상 예산 승인액은 source/01-case-brief.pdf에 설명한다.']];
summary.getRange('A1:A33').format.columnWidth=34; summary.getRange('B1:D33').format.columnWidth=21;
const source=data.datasets.find(d=>d.name==='wbs.csv'), wbs=sheets['WBS'], schedule=sheets['일정'];
base(wbs,'4주 문서 개선 시험 WBS',12,33); header(wbs,12); wbs.getRange('A5:L5').values=[[...source.headers,'기간 일','선행 검사']];
wbs.getRange('A6:J29').values=source.rows.map(row=>row.map((v,c)=>c===5||c===6?new Date(v+'T00:00:00Z'):v));
wbs.getRange('F6:G29').setNumberFormat('yyyy-mm-dd'); wbs.getRange('J6:J29').setNumberFormat('0%');
wbs.getRange('K6').formulas=[['=G6-F6+1']]; wbs.getRange('K6:K29').fillDown();
wbs.getRange('L6:L29').formulas=source.rows.map((_,i)=>{const r=i+6;return [`=IF(G${r}<F${r},"날짜 역전",IF(E${r}="","정상",IF(COUNTIFS($A$6:$A$29,E${r})<>1,"선행 ID 확인",IF(F${r}<=INDEX($G$6:$G$29,MATCH(E${r},$A$6:$A$29,0)),"선행 충돌","정상"))))`];});
wbs.getRange('L6:L29').conditionalFormats.add('expression',{formula:'L6<>"정상"',format:{fill:'#FDE9E7',font:{color:'#B42318',bold:true}}});
wbs.getRange('I6:I29').dataValidation={rule:{type:'list',values:['미착수','진행중','검토대기','완료']}};
wbs.getRange('A31').values=[['승인 전 가정 / 달력 일수 기준 / 선행 종료 다음 날부터 시작 / 공휴일 미반영']];
wbs.getRange('A32').values=[['T08 종료일을 10/30로 바꾸면 T10이 선행 충돌로 표시된다. 원본을 복사한 뒤 시험한다.']];
[10,12,32,19,12,16,16,42,13,12,12,18].forEach((v,i)=>wbs.getRangeByIndexes(0,i,33,1).format.columnWidth=v);
wbs.freezePanes.freezeRows(5); wbs.freezePanes.freezeColumns(3);
base(schedule,'4주 예정 Gantt',9,33); header(schedule,9);
schedule.getRange('A5:I5').values=[['업무ID','업무','담당','시작일','종료일',new Date('2026-10-19T00:00:00Z'),new Date('2026-10-26T00:00:00Z'),new Date('2026-11-02T00:00:00Z'),new Date('2026-11-09T00:00:00Z')]];
schedule.getRange('F5:I5').setNumberFormat('mm/dd'); schedule.getRange('D6:E29').setNumberFormat('yyyy-mm-dd');
schedule.getRange('A6:I29').formulas=source.rows.map((_,i)=>{const r=i+6;return ['A','C','D','F','G'].map(c=>`='WBS'!${c}${r}`).concat(['F','G','H','I'].map(c=>`=IF(AND($D${r}<=${c}$5+6,$E${r}>=${c}$5),"예정","")`));});
schedule.getRange('F6:I29').conditionalFormats.add('expression',{formula:'F6="예정"',format:{fill:'#DCEFF0',font:{color:teal,bold:true}}});
schedule.getRange('F6:I29').format.horizontalAlignment='center'; schedule.getRange('A31').values=[['예정 구간을 표시한다. 실제 진행·완료율은 WBS의 상태와 완료율에 별도로 기록한다.']];
[10,32,19,16,16,12,12,12,12].forEach((v,i)=>schedule.getRangeByIndexes(0,i,33,1).format.columnWidth=v);
schedule.freezePanes.freezeRows(5); schedule.freezePanes.freezeColumns(2);
wb.recalculate();
const close=(a,b)=>Math.abs(a-b)<1e-8;
if(summary.getRange('C6:C15').values[0][0]!==180||summary.getRange('C7').values[0][0]!==144||summary.getRange('C9').values[0][0]!==54) throw Error('원장 집계 불일치');
if(!close(summary.getRange('C10').values[0][0],0.375)||summary.getRange('C27').values[0][0]!==12360000) throw Error('비율 또는 집행 불일치');
if(!wbs.getRange('L6:L29').values.every(r=>r[0]==='정상')) throw Error('초기 WBS 충돌');
// 실제 입력 변경으로 수식 연결과 후속 충돌 검사를 확인한다.
wbs.getRange('G13').values=[[new Date('2026-10-30T00:00:00Z')]]; wb.recalculate();
if(wbs.getRange('L15').values[0][0]!=='선행 충돌') throw Error('T08 지연의 T10 영향 누락');
wbs.getRange('G13').values=[[new Date('2026-10-27T00:00:00Z')]];
summary.getRange('B21').values=[[5000000]]; wb.recalculate();
if(summary.getRange('D21').values[0][0]!==2200000) throw Error('예산 변경 재계산 오류');
summary.getRange('B21').values=[[4800000]]; wb.recalculate();
const errorScan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:20},maxChars:2000});
await fs.writeFile(path.join(out,'formula-check.ndjson'),errorScan.ndjson);
for(const name of Object.keys(sheets)) {
  const range=name==='운영집계'?'A1:D28':name==='일정'?'A1:I13':name==='WBS'?'A1:L13':'A1:'+String.fromCharCode(64+(name==='상담기록'?11:name==='기업연계'?9:name==='등록원장'?8:name==='설문'?7:8))+'12';
  const png=await wb.render({sheetName:name,range,scale:1.4,format:'png'});
  await fs.writeFile(path.join(out,`sheet-${Object.keys(sheets).indexOf(name)+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const exportFile=await SpreadsheetFile.exportXlsx(wb); await exportFile.save(path.join(caseDir,'data/admin-workbook.xlsx'));
console.log(JSON.stringify({sheets:Object.keys(sheets),registered:360,counseling:1440,spent:12360000,changedInputVerified:true}));
