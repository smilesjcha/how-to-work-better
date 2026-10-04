import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const out = path.join(root, 'materials', '01-data');

function parseCsv(text) {
  return text.trim().split(/\r?\n/).map(line => line.split(','));
}

const sales = parseCsv(await fs.readFile(path.join(out, 'sales-quality-sample.csv'), 'utf8'));
const targets = parseCsv(await fs.readFile(path.join(out, 'july-targets.csv'), 'utf8'));
const targetByProduct = Object.fromEntries(targets.slice(1).map(row => [row[1], Number(row[2])]));
const productNames = { A_plain: 'A 플레인', B_string: 'B 스트링', C_yogurt: 'C 요거트' };
const inputs = sales.slice(1).map(row => [row[0], productNames[row[1]], Number(row[2]), Number(row[3]), row[0] === '2026-07' ? targetByProduct[row[1]] : null]);

const wb = Workbook.create();
const summary = wb.worksheets.add('Summary');
const source = wb.worksheets.add('Inputs');
summary.showGridLines = false;
source.showGridLines = false;

source.getRange('A1').values = [['한빛유업 가상 실습 데이터']];
source.getRange('A2').values = [['수치는 교육용 가상 값입니다. 실제 기업 데이터가 아닙니다.']];
source.getRange('A3:E3').values = [['월', '제품', '판매 수량(개)', '반품 접수(건)', '7월 목표(개)']];
source.getRange('A4:E9').values = inputs;
source.getRange('A1:E9').format.font = { name: 'Arial', size: 10, color: '#17212B' };
source.getRange('A1').format.font = { name: 'Arial', size: 14, bold: true, color: '#17212B' };
source.getRange('A3:E3').format = { fill: '#0B1F3A', font: { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' } };
source.getRange('A4:E9').format.rowHeight = 25;
source.getRange('A1:A9').format.columnWidth = 17;
source.getRange('B1:B9').format.columnWidth = 19;
source.getRange('C1:E9').format.columnWidth = 20;
source.getRange('C4:E9').setNumberFormat('#,##0');
source.freezePanes.freezeRows(3);

summary.getRange('A1').values = [['월별 판매·반품 요약']];
summary.getRange('A2').values = [['교육용 가상 데이터 · 반품률 = 반품 접수 건수 ÷ 판매 수량']];
summary.getRange('A4:E4').values = [['월', '판매 수량(개)', '반품 접수(건)', '연습용 반품률', '목표 달성률']];
summary.getRange('A5:A6').values = [['2026-06'], ['2026-07']];
summary.getRange('B5:C6').formulas = [
  ['=SUMIFS(Inputs!$C$4:$C$9,Inputs!$A$4:$A$9,A5)', '=SUMIFS(Inputs!$D$4:$D$9,Inputs!$A$4:$A$9,A5)'],
  ['=SUMIFS(Inputs!$C$4:$C$9,Inputs!$A$4:$A$9,A6)', '=SUMIFS(Inputs!$D$4:$D$9,Inputs!$A$4:$A$9,A6)'],
];
summary.getRange('D5:D6').formulas = [['=C5/B5'], ['=C6/B6']];
summary.getRange('E5').values = [['n.a.']];
summary.getRange('E6').formulas = [['=B6/SUMIFS(Inputs!$E$4:$E$9,Inputs!$A$4:$A$9,A6)']];
summary.getRange('A8:E8').values = [['제품', '6월 반품률', '7월 반품률', '7월 목표(개)', '7월 달성률']];
summary.getRange('A9:A11').values = [['A 플레인'], ['B 스트링'], ['C 요거트']];
for (let row = 9; row <= 11; row++) {
  summary.getRange(`B${row}`).formulas = [[`=SUMIFS(Inputs!$D$4:$D$9,Inputs!$A$4:$A$9,"2026-06",Inputs!$B$4:$B$9,A${row})/SUMIFS(Inputs!$C$4:$C$9,Inputs!$A$4:$A$9,"2026-06",Inputs!$B$4:$B$9,A${row})`]];
  summary.getRange(`C${row}`).formulas = [[`=SUMIFS(Inputs!$D$4:$D$9,Inputs!$A$4:$A$9,"2026-07",Inputs!$B$4:$B$9,A${row})/SUMIFS(Inputs!$C$4:$C$9,Inputs!$A$4:$A$9,"2026-07",Inputs!$B$4:$B$9,A${row})`]];
  summary.getRange(`D${row}`).formulas = [[`=SUMIFS(Inputs!$E$4:$E$9,Inputs!$A$4:$A$9,"2026-07",Inputs!$B$4:$B$9,A${row})`]];
  summary.getRange(`E${row}`).formulas = [[`=SUMIFS(Inputs!$C$4:$C$9,Inputs!$A$4:$A$9,"2026-07",Inputs!$B$4:$B$9,A${row})/D${row}`]];
}
summary.getRange('A13').values = [['원인·유형·안전성·법규 적합성은 이 파일로 판단할 수 없습니다.']];
summary.getRange('A1:E13').format.font = { name: 'Arial', size: 10, color: '#17212B' };
summary.getRange('A1').format.font = { name: 'Arial', size: 14, bold: true, color: '#17212B' };
summary.getRange('A4:E4').format = { fill: '#0B1F3A', font: { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' } };
summary.getRange('A8:E8').format = { fill: '#0B1F3A', font: { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' } };
summary.getRange('A4:E11').format.rowHeight = 25;
summary.getRange('A1:A13').format.columnWidth = 17;
summary.getRange('B1:C13').format.columnWidth = 20;
summary.getRange('D1:E13').format.columnWidth = 21;
summary.getRange('B5:C6').setNumberFormat('#,##0');
summary.getRange('D5:D6').setNumberFormat('0.00%');
summary.getRange('E6').setNumberFormat('0.0%');
summary.getRange('E5').format.horizontalAlignment = 'center';
summary.getRange('B9:C11').setNumberFormat('0.00%');
summary.getRange('D9:D11').setNumberFormat('#,##0');
summary.getRange('E9:E11').setNumberFormat('0.0%');

wb.recalculate();
const check = await wb.inspect({ kind: 'table', range: 'Summary!A4:E11', include: 'values,formulas', tableMaxRows: 12, tableMaxCols: 5, maxChars: 7000 });
console.log(check.ndjson);
const errors = await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!', options: { useRegex: true, maxResults: 30 }, maxChars: 2000 });
console.log(errors.ndjson);
for (const name of ['Summary', 'Inputs']) {
  const preview = await wb.render({ sheetName: name, autoCrop: 'all', scale: 1.4, format: 'png' });
  await fs.writeFile(path.join(root, 'output', `qa-workbook-${name.toLowerCase()}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(path.join(out, 'training-data.xlsx'));
console.log(path.join(out, 'training-data.xlsx'));
