const fs = require("fs");
const docx = require("docx");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
        HeadingLevel, AlignmentType, BorderStyle, LevelFormat, ShadingType } = docx;
const [,, src, out] = process.argv;
const lines = fs.readFileSync(src, "utf8").split("\n");
const FONT = "Calibri";
function runs(text) {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g).filter(Boolean);
  return parts.map(p => {
    if (p.startsWith("**")) return new TextRun({ text: p.slice(2, -2), bold: true, font: FONT, size: 22 });
    if (p.startsWith("*")) return new TextRun({ text: p.slice(1, -1), italics: true, font: FONT, size: 22 });
    if (p.startsWith("`")) return new TextRun({ text: p.slice(1, -1), font: "Consolas", size: 20 });
    return new TextRun({ text: p, font: FONT, size: 22 });
  });
}
const children = [];
let i = 0, para = [];
const flush = () => { if (para.length) { children.push(new Paragraph({ children: runs(para.join(" ")), spacing: { after: 120 } })); para = []; } };
const cellP = (t, bold) => new Paragraph({ children: runs(bold ? `**${t}**` : t), spacing: { after: 0 } });
while (i < lines.length) {
  const l = lines[i];
  if (/^\s*$/.test(l)) { flush(); i++; continue; }
  if (l.startsWith("```")) {
    flush(); i++;
    while (i < lines.length && !lines[i].startsWith("```")) {
      children.push(new Paragraph({ children: [new TextRun({ text: lines[i] || " ", font: "Consolas", size: 17 })],
        shading: { type: ShadingType.CLEAR, fill: "F2F2F2", color: "auto" }, spacing: { after: 0, line: 240 }, keepNext: true }));
      i++;
    }
    children.push(new Paragraph({ spacing: { after: 120 } }));
    i++; continue;
  }
  if (l.startsWith("---")) { flush(); children.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "999999" } }, spacing: { after: 200 } })); i++; continue; }
  const h = l.match(/^(#+)\s+(.*)/);
  if (h) { flush(); const lvl = h[1].length; children.push(new Paragraph({ children: runs(h[2]), heading: lvl === 1 ? HeadingLevel.HEADING_1 : lvl === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3 })); i++; continue; }
  if (l.startsWith("|")) {
    flush();
    const rows = [];
    while (i < lines.length && lines[i].startsWith("|")) { rows.push(lines[i]); i++; }
    const parse = r => r.replace(/^\||\|$/g, "").split("|").map(s => s.trim());
    const body = rows.filter(r => !/^\|\s*-+/.test(r)).map(parse);
    const ncol = body[0].length; const total = 9360; const w = Math.floor(total / ncol);
    const widths = Array(ncol).fill(w); widths[ncol - 1] = total - w * (ncol - 1);
    children.push(new Table({
      width: { size: total, type: WidthType.DXA }, columnWidths: widths,
      rows: body.map((cells, ri) => new TableRow({
        tableHeader: ri === 0,
        children: cells.map((c, ci) => new TableCell({
          width: { size: widths[ci], type: WidthType.DXA },
          shading: ri === 0 ? { type: ShadingType.CLEAR, fill: "E7E6E6", color: "auto" } : undefined,
          margins: { top: 40, bottom: 40, left: 80, right: 80 },
          children: [cellP(c, ri === 0)] })) })) }));
    children.push(new Paragraph({ spacing: { after: 120 } }));
    continue;
  }
  const ol = l.match(/^(\d+)\.\s+(.*)/), ul = l.match(/^-\s+(.*)/);
  if (ol || ul) {
    flush();
    let text = (ol ? ol[2] : ul[1]);
    while (i + 1 < lines.length && /^\s{2,}\S/.test(lines[i + 1]) && !/^\s*[-|]/.test(lines[i + 1])) { i++; text += " " + lines[i].trim(); }
    children.push(new Paragraph({ children: runs(text), numbering: { reference: ol ? "nums" : "bullets", level: 0 }, spacing: { after: 80 } }));
    i++; continue;
  }
  para.push(l.trim()); i++;
}
flush();
const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 32, bold: true }, paragraph: { spacing: { before: 240, after: 160 }, keepNext: true } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 240, after: 120 }, keepNext: true } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 23, bold: true }, paragraph: { spacing: { before: 200, after: 100 }, keepNext: true } } ] },
  numbering: { config: [
    { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] } ] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("wrote", out, b.length); });
