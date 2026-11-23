
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const {Presentation, PresentationFile}=await import(pathToFileURL(process.argv[2]).href);
const dir=path.dirname(fileURLToPath(import.meta.url));
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={dark:'#102B22',ink:'#13342A',accent:'#176447',mint:'#A6DCC4',olive:'#CDD09A',
  bg:'#F2F6F4',white:'#FFFFFF',muted:'#425E53',border:'#CADCD3',soft:'#E4F1EA',
  blue:'#DFEAFC',yellow:'#FFF0CB',red:'#F9E8E6',redInk:'#8F2F32',sand:'#77601D'};
const phases=['Projekt','Vorbereitung','Analyse','Konzeption','Realisierung','Validierung','Fazit'];
const project='Quelle: Aufgabenblatt_ServiceDesk_Softwareprojekt.pdf';
const guide='Quelle: Inhalte Präsentation Softwareprojekt DO1.pdf';
const repo='Quelle: Service-Desk-Repository, lokaler Stand vom 19.11.2026';
const X=248,W=987, right=X+W, font='Segoe UI';
const layoutScale=1168/W;
const contentX=(x)=>56+(x-X)*layoutScale;
const slidePos=(left,top,width,height)=>({left,top,width,height});
const pos=(x,y,w,h)=>slidePos(contentX(x),y,w*layoutScale,h);
const noLine={fill:'none',width:0};
const named=(text)=>text.slice(0,70);
function rect(s,x,y,w,h,fill='none',stroke='none',weight=0,radius=0,name='Fläche'){
  return s.shapes.add({name,position:pos(x,y,w,h),geometry:radius?'roundRect':'rect',fill,
   line:stroke==='none'?noLine:{fill:stroke,width:weight,style:'solid'},...(radius?{borderRadius:radius}:{})});
}
function text(s,value,x,y,w,h,cfg={}){
  const {size=23,color=C.ink,bold=false,align='left',family=font,valign='middle',name=named(value)}=cfg;
  const sh=s.shapes.add({name,position:pos(x,y,w,h),geometry:'textbox',fill:'none',line:noLine});
  sh.text=value;
  sh.text.style={typeface:family,fontSize:size,bold,color,alignment:align,verticalAlignment:valign,wrap:'none',insets:0};
  return sh;
}
function rule(s,x,y,w,col=C.border){rect(s,x,y,w,1,col);}
const imgs={};
for(const stem of ['logo','home','support']){
  const a=await fs.readFile(path.join(dir,stem+'.png'));
  imgs[stem]=a.buffer.slice(a.byteOffset,a.byteOffset+a.byteLength);
}
function pic(s,key,x,y,w,h){
  return s.images.add({name:key,alt:{logo:'Logo Westfalen Office Solutions GmbH',home:'Screenshot der Startseite',support:'Screenshot der Supportübersicht'}[key],
    blob:imgs[key],contentType:'image/png',fit:'contain',position:key==='logo'?slidePos(contentX(x),y,w,h):pos(x,y,w,h)});
}
function capsule(s,label,x,y,w,fill=C.soft,color=C.accent){
  rect(s,x,y,w,32,fill,'none',0,9);
  text(s,label,x+10,y,w-20,32,{size:16,bold:true,color,align:'center'});
}
function chrome(s,phase,person){
  s.background.fill=C.bg;
  rect(s,X-56/layoutScale,0,1280/layoutScale,7,C.dark);
  const labelWidth=102;
  capsule(s,person,right-labelWidth,27,labelWidth,C.soft,C.accent);
  // Fortschritt steht auf jeder Folie an derselben Stelle.
  rule(s,X,646,W);
  const step=133,gap=6;
  phases.forEach((p,i)=>{
    const x=X+(step+gap)*i;
    rect(s,x,661,step,6,i===phase?C.accent:i<phase?'#87B7A2':'#D6E4DD','none',0,3);
    text(s,p,x,672,step,23,{size:14,color:i===phase?C.ink:C.muted,bold:i===phase});
  });
  const n=P.slides.items.length;
  text(s,folio || String(n).padStart(2,'0'),1193,697,42,18,{size:14,bold:true,color:C.accent,align:'right'});
}
function slide(phase,person,title,sub,notes){
  const s=P.slides.add();
  chrome(s,phase,person);
  if(title) text(s,title,X,49,W,64,{size:48,bold:true});
  if(sub) text(s,sub,X,120,W,31,{size:22,color:C.muted});
  s.speakerNotes.text=notes;
  return s;
}
function bullet(s,label,x,y,w,size=22,color=C.ink){
  rect(s,x,y+15,7,7,C.accent,'none',0,3);
  text(s,label,x+19,y,w-19,38,{size,color});
}
function panel(s,x,y,w,h,title,items,{fill=C.white,bodySize=22}={}){
  rect(s,x,y,w,h,fill,C.border,1,15,title+' – Karte');
  text(s,title,x+23,y+17,w-46,38,{size:27,bold:true});
  rule(s,x+23,y+65,w-46);
  items.forEach((v,i)=>bullet(s,v,x+23,y+78+i*46,w-46,bodySize));
}
function band(s,title,desc,y=554,fill=C.soft){
  rect(s,X,y,W,63,fill,'none',0,10);
  const labelWidth=title.length>24?345:284;
  text(s,title,X+17,y+7,labelWidth-15,48,{size:23,bold:true});
  text(s,desc,X+labelWidth,y+7,W-labelWidth-17,48,{size:20,color:C.muted});
}
function slot(s,x,y,w,h,type,title){
  const code=type==='CODE';
  const bg=code?C.dark:C.white, inks=code?C.white:C.ink, edge=code?'#508873':'#78A28F';
  rect(s,x,y,w,h,bg,edge,2,14,'Einfügefläche '+title);
  rect(s,x+2,y+2,w-4,48,code?'#224638':C.soft,'none',0,12);
  text(s,title,x+18,y+4,w-36,44,{size:21,bold:true,color:inks});
  const dashed=s.shapes.add({name:'Rahmen '+title,geometry:'rect',position:pos(x+24,y+68,w-48,h-92),fill:'none',
    line:{fill:edge,width:1.6,style:'dashed'}});
  text(s,code?'C#-Ausschnitt hier einfügen':(type==='MOCKUP'?'Mockup hier einfügen':'Diagramm hier einfügen'),
    x+31,y+68,w-62,h-92,{size:20,color:code?C.mint:C.muted,align:'center',name:'Platzhaltertext '+title});
}
function table(s,values,y,heights,widths,{size=21}={}){
  const t=s.tables.add({rows:values.length,columns:values[0].length,left:contentX(X),top:y,
    width:W*layoutScale,height:heights.reduce((a,b)=>a+b,0),columnWidths:widths.map(w=>w*layoutScale),values});
  t.styleOptions={headerRow:false,bandedRows:false};
  t.borders.assign({fill:C.border,width:1,style:'solid'});
  values.forEach((row,i)=>{
    t.rows[i].height=heights[i];
    row.forEach((v,j)=>{
      const color=i===0?C.white:v==='Offen'?C.redInk:v==='Zu prüfen'?C.sand:C.ink;
      t.cells.block({row:i,column:j,rowCount:1,columnCount:1}).assign({
        fill:i===0?C.accent:v==='Offen'?C.red:v==='Zu prüfen'?C.yellow:i%2?C.white:'#EAF3EE',
        textStyle:{typeface:font,fontSize:size,bold:i===0||j===0||v==='Offen'||v==='Zu prüfen',color},
        margins:{left:13,right:8,top:6,bottom:6},anchor:'middle'
      });
    });
  });
}
function ticket(s,x,y,w,h){
  rect(s,x,y,w,h,C.white,C.border,2,20);
  rect(s,x+16,y+15,w-32,42,C.soft,'none',0,10);
  text(s,'IT-SUPPORT',x+30,y+17,w-55,38,{size:18,bold:true,color:C.accent});
  text(s,'Drucker nicht erreichbar',x+27,y+87,w-54,72,{size:31,bold:true});
  text(s,'Beispielticket',x+29,y+157,w-58,30,{size:19,color:C.muted});
  for(let i=0;i<21;i++) rect(s,x+24+i*(w-48)/21,y+211,8,1,'#9FC0B0');
  capsule(s,'Offen',x+27,y+237,94,C.blue,'#225A80');
  capsule(s,'Priorität Mittel',x+133,y+237,144,C.yellow,C.sand);
}


let s;
let folio='';
function extra(code,phase,title,sub,notes){
  folio=code;
  return slide(phase,'Person 2',title,sub,notes);
}
function shape(s,geometry,x,y,w,h,fill,stroke='none',name=geometry){
  return s.shapes.add({name,geometry,position:pos(x,y,w,h),fill,
    line:stroke==='none'?noLine:{fill:stroke,width:1.5,style:'solid'}});
}
function segment(s,x1,y1,x2,y2,color=C.accent,width=2,name='Verbindung'){
  const a=contentX(x1), b=contentX(x2);
  const length=Math.hypot(b-a,y2-y1);
  const left=(a+b-length)/2, top=(y1+y2-width)/2;
  return s.shapes.add({name,geometry:'rect',
    position:{...slidePos(left,top,length,width),rotation:Math.atan2(y2-y1,b-a)*180/Math.PI},
    fill:color,line:noLine});
}
s=extra('06a',3,'UML-Use-Case-Diagramm','Anwendungsfälle aus Sicht der drei Nutzergruppen',
  '0:20 · Person 2\nMitarbeitende melden Tickets und sehen Details. Der Support filtert, weist zu und ändert den Status. Die Verwaltung pflegt die IT-Mitarbeiter und Kategorien. Die Akteure sind fachliche Nutzergruppen. Das Projekt verlangt keine Benutzerkonten oder Rollenverwaltung.\nMit den vier ergänzten Folien liegt die geplante Vortragszeit bei 14:45 Minuten inklusive Demo.\n'+project+'\n'+repo);
rect(s,533,167,702,433,C.white,C.border,1.4,13,'Systemgrenze Service Desk');
text(s,'Service Desk',552,172,180,25,{size:18,bold:true,color:C.accent});
const useCases=[
  {label:'Mitarbeitende',y:255,top:205,cases:['Ticket melden','Ticketliste ansehen','Ticketdetails ansehen']},
  {label:'IT-Support',y:397,top:332,cases:['Tickets filtern','Tickets anlegen oder löschen','Ticket zuweisen und bearbeiten','Ticket abschließen oder wieder öffnen']},
  {label:'Verwaltung',y:542,top:509,cases:['IT-Mitarbeiter verwalten','Kategorien verwalten']},
];
useCases.forEach(({label,y,top,cases})=>{
  const cx=366, ink=C.accent, ovalX=664, oHeight=33;
  cases.forEach((t,i)=>segment(s,cx+15,y-3,ovalX,top+i*36+oHeight/2,'#6B9282',1.6,label+' – '+t));
  shape(s,'ellipse',cx-8,y-31,16,19,C.bg,ink,'Akteur '+label);
  segment(s,cx,y-12,cx,y+12,ink,2.2);
  segment(s,cx-15,y-3,cx+15,y-3,ink,2.2);
  segment(s,cx,y+12,cx-13,y+28,ink,2.2);
  segment(s,cx,y+12,cx+13,y+28,ink,2.2);
  text(s,label,cx-104,y+32,208,26,{size:18,bold:true,align:'center'});
  cases.forEach((t,i)=>{
    const oy=top+i*36;
    shape(s,'ellipse',ovalX,oy,449,oHeight,C.soft,'#AECBBC',t+' – Use Case');
    text(s,t,ovalX+15,oy,419,oHeight,{size:18,align:'center'});
  });
});
text(s,'Akteure als Nutzergruppen der Anwendung',X,608,W,25,{size:17,color:C.muted});

s=extra('07a',3,'UML-Klassendiagramm','Ticket, IT-Mitarbeiter und Kategorie im aktuellen C#-Modell',
  '0:20 · Person 2\nEin Ticket hat jeweils null oder eine Kategorie und null oder einen zuständigen IT-Mitarbeiter. Eine Kategorie oder ein IT-Mitarbeiter kann jeweils vielen Tickets zugeordnet sein. Die nullable Fremdschlüssel bilden die Optionen ab. ErstelltVon speichert den Namen als Text.\n'+repo+'\nDateien: Models/Ticket.cs, Models/IT_Mitarbeiter.cs, Models/Kategorie.cs, Models/TicketStatus.cs, Models/Prioritaet.cs.');
function uml(x,y,w,title,rows,h){
  rect(s,x,y,w,h,C.white,C.border,1.5,12,title+' – Klasse');
  rect(s,x+1,y+1,w-2,47,C.accent,'none',0,10);
  text(s,title,x+14,y+2,w-28,43,{size:23,bold:true,color:C.white,align:'center'});
  rule(s,x,y+48,w,C.border);
  rows.forEach((v,i)=>text(s,v,x+12,y+56+i*27,w-24,24,{size:title==='Ticket'?17:15,family:'Consolas'}));
}
const uY=181, tX=561,tW=362,lW=246,rX=989,rW=246;
uml(X,249,lW,'IT_Mitarbeiter',
  ['+ MitarbeiterId: int','+ Name: string','+ Tickets: ICollection<Ticket>'],166);
uml(tX,uY,tW,'Ticket',
  ['+ TicketId: int','+ ErstelltVon: string','+ Titel: string','+ Beschreibung: string',
   '+ Erstellungsdatum: DateTime','+ Prioritaet: Prioritaet','+ Status: TicketStatus',
   '+ MitarbeiterId: int?','+ KategorieId: int?','+ Mitarbeiter: IT_Mitarbeiter?','+ Kategorie: Kategorie?'],374);
uml(rX,249,rW,'Kategorie',
  ['+ KategorieId: int','+ KategorieName: string','+ Tickets: ICollection<Ticket>'],166);
segment(s,X+lW,330,tX,330,C.accent,2,'IT-Mitarbeiter hat Tickets');
segment(s,tX+tW,330,rX,330,C.accent,2,'Kategorie enthält Tickets');
text(s,'0..1',X+lW+1,305,43,21,{size:16,bold:true,color:C.accent,align:'left'});
text(s,'0..*',tX-39,331,38,22,{size:16,bold:true,color:C.accent,align:'right'});
text(s,'0..*',tX+tW+1,331,43,22,{size:16,bold:true,color:C.accent,align:'left'});
text(s,'0..1',rX-44,305,43,21,{size:16,bold:true,color:C.accent,align:'right'});
band(s,'Optionale Zuordnungen','Pro Ticket jeweils höchstens ein IT-Mitarbeiter und eine Kategorie',564);

s=extra('08a',3,'Mockup der Ticketerfassung','Nachgezeichneter Grobentwurf für die Mitarbeiteransicht',
  '0:20 · Person 2\nDas Mockup wurde für diese Präsentation anhand des Ticketformulars rekonstruiert. Die Mitarbeiteransicht erfasst Name, Titel und Beschreibung sowie Kategorie und Priorität. Das Team kann bei Bedarf seinen ursprünglichen Entwurf auf der vorhandenen Mockup-Folie einsetzen.\n'+project+'\n'+repo+'\nDatei: Views/Ticket/Create.cshtml.');
rect(s,X,171,613,428,C.white,C.border,1.5,14,'Mockup – Mitarbeiteransicht');
rect(s,X+1,172,611,48,C.soft,'none',0,12);
text(s,'Mitarbeiteransicht  /  Neues Ticket',X+18,176,570,40,{size:21,bold:true,color:C.accent});
function field(label,placeholder,x,y,w,h=33){
  text(s,label,x,y,w,24,{size:17,bold:true});
  rect(s,x,y+25,w,h,C.bg,C.border,1,7,label+' – Formularfeld');
  text(s,placeholder,x+9,y+25,w-18,h,{size:16,color:C.muted});
}
field('Name','z. B. Alex Muster',X+20,231,275);
field('Titel','z. B. Drucker nicht erreichbar',X+311,231,282);
field('Beschreibung','Fehlerbild und betroffener Arbeitsplatz',X+20,297,573,62);
field('Kategorie','Hardware',X+20,390,275);
field('Priorität','Mittel',X+311,390,282);
capsule(s,'Ticket erstellen',X+20,483,155,C.accent,C.white);
text(s,'Ansichtsskizze',X+20,538,550,28,{size:17,color:C.muted});
panel(s,X+635,171,352,311,'Bedienidee',[
 'Pflichtfelder im Formular','Kategorie und Priorität','Ticketstatus beim Speichern: Offen',
 'Meldung bei ungültiger Eingabe'
],{bodySize:20});

s=extra('10a',4,'Codeausschnitt: Ticket anlegen','Pflichtfelder im Modell und Speichern im Controller',
  '0:20 · Person 2\nLinks markiert die Umrandung das Pflichtfeld im Ticket-Modell. Rechts markiert sie die Entscheidung des Controllers: Bei gültigem ModelState setzt der Controller den Status auf Offen und speichert. Bei ungültigen Daten zeigt die View das Formular mit den Eingaben und Validierungsmeldungen erneut.\n'+repo+'\nDateien: Models/Ticket.cs und Controllers/TicketController.cs, Create (POST).');
function codeCard(x,y,w,h,title,lines,marked){
  rect(s,x,y,w,h,C.dark,'#508873',1,14,title+' – Code');
  rect(s,x+2,y+2,w-4,44,'#224638','none',0,10);
  text(s,title,x+16,y+4,w-32,39,{size:20,bold:true,color:C.white});
  const base=y+60;
  rect(s,x+13,base+marked*29-2,w-26,title.startsWith('Ticket.cs')?57:28,'none',C.olive,2,4,'Umrandung – '+title);
  lines.forEach((line,i)=>text(s,line,x+21,base+i*29,w-42,24,
    {size:17,family:'Consolas',color:i===marked?'#EDF4BF':C.white}));
}
codeCard(X,188,468,335,'Ticket.cs · Titel',[
 '[Required(ErrorMessage =',
 '    "Bitte einen Titel angeben.")]',
 '[StringLength(100)]',
 'public string Titel { get; set; }',
 '    = string.Empty;'
],0);
codeCard(X+487,188,500,335,'TicketController.Create (POST)',[
 'if (ModelState.IsValid)',
 '{',
 '    ticket.Status = TicketStatus.Offen;',
 '    _context.Add(ticket);',
 '    await _context.SaveChangesAsync();',
 '    return RedirectToAction("Index");',
 '}',
 'return View(ticket);'
],0);
band(s,'Eingabevalidierung','Pflichtfeld im Modell, Entscheidung über ModelState im Controller',548);


await fs.mkdir(path.join(dir,'render-audit'),{recursive:true});
const out=path.join(dir,'additions.pptx');
await (await PresentationFile.exportPptx(P)).save(out);
for(const [i,slide] of P.slides.items.entries()){
  const png=await P.export({slide,format:'png',scale:1});
  await fs.writeFile(path.join(dir,'render-audit',String(i+1).padStart(2,'0')+'.png'),new Uint8Array(await png.arrayBuffer()));
}
console.log('Exported',P.slides.items.length,'slides to',out);
