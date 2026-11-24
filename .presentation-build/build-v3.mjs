
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
  text(s,String(n).padStart(2,'0'),1193,697,42,18,{size:14,bold:true,color:C.accent,align:'right'});
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
s=slide(0,'Person 1','','',
  '0:20 · Person 1\nEinstieg: Ein Drucker fällt aus. Ein Anruf und eine E-Mail zum selben Problem können zwei Bearbeitungen auslösen. Unser Service Desk bündelt solche Meldungen als Tickets.\n'+project);
pic(s,'logo',X,111,96,96);
text(s,'Westfalen Office Solutions GmbH',X+94,138,455,40,{size:25,bold:true,color:C.accent});
text(s,'S\u2009E\u2009R\u2009V\u2009I\u2009C\u2009E\u2009-\u2009D\u2009E\u2009S\u2009K',X,235,553,90,{size:60,bold:true,color:C.accent,name:'SERVICE-DESK'});
text(s,'Webbasiertes IT-Ticketsystem',X,335,510,40,{size:29,color:C.muted});
text(s,'Person 1   /   Person 2   /   Person 3',X+2,416,480,35,{size:21,bold:true,color:C.accent});
ticket(s,820,217,415,305);

s=slide(1,'Person 1','Unser Team','Drei Vortragsblöcke mit eigenen technischen Schwerpunkten',
  '0:35 · Person 1\nProbezeit mit der Live-Demo: insgesamt 13:25 Minuten. Person 1 spricht etwa 3:20, Person 2 etwa 3:55 und Person 3 etwa 6:10 inklusive 2:55 Demonstration. Das ist eine vorgeschlagene Vortragsaufteilung. Bitte vor der Abgabe die Schwerpunkte mit den tatsächlichen Teambeiträgen abgleichen. Jede Person nennt ihren eigenen Beitrag und eine Entscheidung, die sie fachlich erklären kann.\n'+guide);
const card=(W-2*17)/3;
for (const [i, label, lines] of [
  [0,'Projekt & Analyse',['Kundenauftrag','Anforderungen & Zeitplan','Technischer Schwerpunkt','Mitarbeiteransicht']],
  [1,'Entwurf & Umsetzung',['Datenmodell & MVC','Codeausschnitte','Technischer Schwerpunkt','Controller & Datenbank']],
  [2,'Demo & Validierung',['Live-Demo & Tests','Soll-Ist-Vergleich','Technischer Schwerpunkt','Support & Ticketablauf']],
]){
  const x=X+i*(card+17);
  rect(s,x,198,card,357,C.white,C.border,1,16);
  capsule(s,'Person '+(i+1),x+20,219,103,C.olive,C.dark);
  text(s,label,x+20,267,card-40,40,{size:25,bold:true});
  lines.forEach((l,j)=>text(s,l,x+20,324+j*43,card-40,35,{size:j===2?17:21,color:j===2?C.accent:C.ink,bold:j===2}));
}

s=slide(1,'Person 1','Kunde und Projektauftrag','Westfalen Office Solutions GmbH',
  '0:40 · Person 1\nDer Auftrag beschreibt ein mittelständisches Unternehmen in Dortmund. Rund 250 Beschäftigte benötigen internen IT-Support. Unser aktueller Prototyp bietet eine zentrale Ticketliste, die Bearbeitung im Support und eine Verwaltung für IT-Mitarbeiter und Kategorien.\n'+project+'\n'+repo);
panel(s,X,189,386,327,'Der Kunde',['Dortmund','Rund 250 Beschäftigte','Vertrieb und Wartung von Bürotechnik'],{bodySize:18});
panel(s,X+406,189,581,327,'Der Service Desk heute',['Mitarbeiteransicht zur Ticketmeldung','Supportansicht mit Ticketübersicht','Bearbeitung, Zuweisung und Statuswechsel','Verwaltung von IT-Mitarbeitern und Kategorien']);
band(s,'Projektziel','Zentrale Erfassung und nachvollziehbare Bearbeitung von IT-Anfragen');

s=slide(2,'Person 1','Ist-Analyse und Soll-Konzept','Vom Telefonanruf zur zentralen Ticketübersicht',
  '0:50 · Person 1\nVorher kamen Anfragen per Telefon oder E-Mail. Das Team konnte schlecht erkennen, welche Anfragen offen sind und wer sich kümmert. Im Soll gibt es einen Datensatz pro Meldung, eine Zuweisung, drei Prioritäten und drei Bearbeitungsstände. Anhand des Druckerbeispiels kurz den Mehrwert erläutern.\n'+project);
panel(s,X,188,481,347,'Ist · Telefon und E-Mail',['Verteilte IT-Meldungen','Verlorene oder doppelte Anfragen','Unklare Zuständigkeiten','Fehlender Überblick über den Status'],{fill:C.white});
panel(s,X+506,188,481,347,'Soll · Webanwendung',['Zentrale Ticketliste','Kategorie und Priorität je Ticket','Zuweisung an den IT-Support','Sichtbarer Bearbeitungsstand'],{fill:C.soft});
band(s,'Pflichtregel','Abgeschlossene Tickets erst nach Wiederöffnung bearbeiten',554,C.yellow);


s=slide(2,'Person 1','Erweitertes Wasserfallmodell','Zeitplanvorschlag für 13 Unterrichtstage',
  '0:55 · Person 1\nDie fünf Stufen zeigen unseren Zeitplanvorschlag. Dunkelgrün steht für den Vorwärtsablauf. Goldene Pfeile zeigen den Rücksprung in die vorige Phase, etwa wenn ein Blackbox-Test eine Korrektur in der Implementierung erfordert. Danach wird erneut getestet. Die Dokumentation begleitet alle Phasen. Vor dem Vortrag die Tagesaufteilung mit dem tatsächlichen Gruppenplan abgleichen. Übergabe an Person 2: Wie sind die Anforderungen technisch umgesetzt?\n'+project+'\nGestaltungsreferenz: ZSK-Rechner-Praesentation-Wasserfall.pptx, Folie 2.');
const stgs=[['Analyse','Tag 1–2'],['Entwurf','Tag 3–4'],['Implementierung','Tag 5–9'],['Validierung','Tag 10–11'],['Abschluss','Tag 12–13']];
const gold='#9B762A', cwf=174, stepx=198, stepy=63, startY=167;
const phaseColors=[C.soft,C.olive,C.accent,C.blue,C.soft];
function tip(left,top,dir,color,name) {
  s.shapes.add({name,geometry:dir==='forward'?'rightArrow':'leftArrow',position:pos(left,top,10,10),fill:color,line:noLine});
}
rect(s,X+666,167,31,3,C.accent);
tip(X+693,163.5,'forward',C.accent,'Legende Vorwärts');
text(s,'Vorwärts',X+709,154,94,29,{size:17,color:C.muted});
rect(s,X+814,167,32,3,gold);
tip(X+811,163.5,'back',gold,'Legende Rücksprung');
text(s,'Rücksprung',X+852,154,118,29,{size:17,color:C.muted});
stgs.forEach(([name,days],i)=>{
  const x=X+i*stepx, y=startY+i*stepy, last=i===stgs.length-1, isImpl=i===2;
  rect(s,x,y,cwf,62,phaseColors[i],C.border,1,10,name+' · Phase');
  text(s,name,x+8,y+4,cwf-16,27,{size:20,bold:true,color:isImpl?C.white:C.ink,align:'center'});
  text(s,days,x+8,y+32,cwf-16,22,{size:17,color:isImpl?C.white:C.muted,align:'center'});
  if(last)return;
  const right=x+cwf, next=x+stepx, top=y+20, endY=top+stepy, nextPhase=stgs[i+1][0];
  rect(s,right,top,15,2,C.accent,'none',0,0,name+' zu '+nextPhase);
  rect(s,right+14,top,2,stepy+2,C.accent);
  rect(s,right+14,endY,next-right-14,2,C.accent);
  tip(next-10,endY-4,'forward',C.accent,nextPhase+' · Vorwärtspfeil');
  const back=y+44, backEnd=back+stepy;
  rect(s,right+6,backEnd,next-right-6,2,gold,'none',0,0,nextPhase+' zurück zu '+name);
  rect(s,right+6,back,2,stepy+2,gold);
  tip(right,back-4,'back',gold,name+' · Rücksprungpfeil');
});
band(s,'Dokumentation','Begleitend über alle Phasen',513);
text(s,'Ressourcen',X,585,116,32,{size:19,bold:true,color:C.accent});
text(s,'3 Personen, Visual Studio, Git/GitHub, .NET SDK, SQL Server und Browser',X+122,585,W-122,32,{size:19,color:C.muted});

s=slide(3,'Person 2','Technischer Entwurf','ASP.NET Core MVC mit relationaler Datenbank',
  '0:40 · Person 2\nMVC trennt Darstellung, Ablaufsteuerung und Daten. Die Oberfläche nutzt Razor und Bootstrap. EF Core überträgt die C#-Modelle mit Migrationen in SQL Server. Der ServiceDeskContext wird in Program.cs registriert und den Controllern per Dependency Injection übergeben.\n'+repo+'\nDateien: Program.cs, Service-Desk.csproj, Models/ServiceDeskContext.cs und Migrations/.');
const gap=18, cw=(W-2*gap)/3;
panel(s,X,202,cw,303,'Oberfläche',['Razor Views','Bootstrap','HTML und CSS'],{bodySize:22});
panel(s,X+cw+gap,202,cw,303,'Anwendung',['ASP.NET Core MVC','C# und .NET 10','Controller und Models'],{bodySize:22});
panel(s,X+2*(cw+gap),202,cw,303,'Datenzugriff',['Entity Framework Core','SQL Server','Code First & Migrationen'],{bodySize:21});
band(s,'Dependency Injection','Registrierung und Übergabe des ServiceDeskContext',551);

s=slide(3,'Person 2','Datenmodell','Drei Entitäten mit Ticket als zentralem Datensatz',
  '0:40 · Person 2\nVortrag vorbereiten: Rechts das aktuelle UML-Klassendiagramm einfügen. Eine Kategorie und ein IT-Mitarbeiter können mehreren Tickets zugeordnet sein. Pro Ticket ist die einzelne Zuordnung jeweils optional. ErstelltVon ist ein Textfeld im Ticket.\n'+repo+'\nDateien: Models/Ticket.cs, Models/Kategorie.cs, Models/IT_Mitarbeiter.cs und Migrations/.');
panel(s,X,180,330,382,'Entitäten',['Ticket','IT-Mitarbeiter','Kategorie','Jeweils 1:n zu Tickets','Optionale Fremdschlüssel'],{bodySize:21});
slot(s,X+351,180,636,382,'DIAGRAMM','UML-Klassendiagramm');

s=slide(3,'Person 2','Mockup und Ticketablauf','Erster Oberflächenentwurf und geplanter Bearbeitungsweg',
  '0:30 · Person 2\nLinks das eigene Mockup einsetzen, rechts bei Bedarf EPK oder Ablaufdiagramm. Im Vortrag kurz zeigen, wie aus Meldung, Zuweisung und Abschluss der Ticketablauf entsteht. Falls das Mockup erst ergänzt wird, vor der Abgabe mit dem Entwurfsstand abgleichen.\n'+guide);
slot(s,X,180,481,394,'MOCKUP','Oberflächenentwurf');
slot(s,X+506,180,481,394,'DIAGRAMM','EPK oder Ablaufdiagramm');

s=slide(4,'Person 2','Aufbau der Anwendung','MVC-Struktur am Beispiel der Supportübersicht',
  '0:45 · Person 2\nEin GET auf die Supportübersicht erreicht den SupportController. Er baut die Abfrage über den Kontext auf und übergibt die Ticketliste an die Razor-View. Die View rendert daraus Tabelle und Statusanzeige. Rechts ein eigenes MVC-Ablaufdiagramm ergänzen.\n'+repo+'\nDateien: Controllers/SupportController.cs, Views/Support/Index.cshtml, Models/ServiceDeskContext.cs.');
panel(s,X,181,445,398,'Ordner und Aufgaben',['Controllers · Anfragen und Aktionen','Models · Ticket und Beziehungen','Views · Razor-Oberfläche','Migrations · Datenbankschema','wwwroot · CSS und Bilder'],{bodySize:20});
slot(s,X+465,181,522,398,'DIAGRAMM','MVC-Architektur oder GET-Ablauf');

s=slide(4,'Person 2','Codebeispiele für Tickets','Von der Eingabe bis zur gefilterten Liste',
  '0:50 · Person 2\nIn beide Rahmen kurze, lesbare C#-Ausschnitte einfügen. Links bietet sich TicketController.Create (POST) mit ModelState, Erstellungsdatum und Speichern an. Rechts die Where-Filter aus SupportController.Index. Je einen entscheidenden Ausdruck mit einer sichtbaren PowerPoint-Umrandung markieren und kurz erklären.\n'+repo);
slot(s,X,180,481,366,'CODE','TicketController.Create (POST)');
slot(s,X+506,180,481,366,'CODE','SupportController.Index');
band(s,'Ausschnitte im Vortrag','ModelState und Speichern links, Filter nach Status und Priorität rechts',558);

s=slide(4,'Person 2','Codebeispiel für die Wiederöffnung','Statuswechsel von „Abgeschlossen“ zu „Offen“',
  '0:30 · Person 2\nDen Ausschnitt aus SupportController.Reopen einfügen. Die Statuszuweisung und SaveChangesAsync markieren. Wiederöffnen ist im Code vorhanden. Die separate Sperre des Bearbeitens vor der Wiederöffnung fehlt im geprüften Projektstand. Übergabe an Person 3 für Oberfläche und Live-Demo.\n'+repo);
slot(s,X,182,650,382,'CODE','SupportController.Reopen');
panel(s,X+674,182,313,382,'Schritte',['Ticket laden','Status auf „Offen“ setzen','Änderung speichern','Zur Übersicht zurück'],{bodySize:20});

s=slide(4,'Person 3','Die fertige Oberfläche','Startseite und Supportübersicht',
  '0:30 · Person 3\nRechts die Supportübersicht zeigen: Statuskarten, Prioritätsfarben, Filter und Ticketliste. Links kurz die Startseite und die drei Zugänge für Mitarbeiter, Support und Verwaltung nennen. Die Zahlen im Dashboard stammen aus den Screenshots zur Demonstration.\nQuelle: die zwei bereitgestellten App-Screenshots vom 19.11.2026.');
rect(s,X,179,238,176,C.white,C.border,1,10);
text(s,'Startseite',X+14,183,209,32,{size:18,bold:true});
pic(s,'home',X+9,217,220,122);
text(s,'Supportansicht',X+264,179,700,32,{size:20,bold:true,color:C.accent});
rect(s,X+254,213,733,407,C.white,C.border,1,8);
pic(s,'support',X+259,218,723,397);
['Statuskarten','Prioritätsfarben','Filter und Sortierung','Ticketaktionen'].forEach((v,i)=>bullet(s,v,X+1,377+i*46,235,19));

s=slide(4,'Person 3','Live-Demonstration','Beispielfall „Drucker nicht erreichbar“',
  '2:55 · Person 3\nApp und Browser vor dem Vortrag starten. 0:45: Im Mitarbeiterbereich ein Ticket mit Titel, kurzer Beschreibung und Name anlegen. 0:50: In der Supportübersicht nach „Offen“ oder „Mittel“ filtern, das Ticket öffnen, einen IT-Mitarbeiter zuweisen und „In Bearbeitung“ speichern. 0:50: Im Support abschließen und über „Wieder öffnen“ zurück auf „Offen“ setzen. 0:30: Status und Liste zeigen und zur Testfolie wechseln. Bei einer Demostörung den Screenshot auf der vorherigen Folie nutzen.\n'+project+'\n'+repo);
[
 ['01','Ticket melden','Mitarbeiteransicht','Name, Titel, Beschreibung'],
 ['02','Ticket übernehmen','Supportübersicht','Filtern, zuweisen, bearbeiten'],
 ['03','Ticket abschließen','Statuswechsel','Abschließen und wieder öffnen']
].forEach(([num,title,label,body],i)=>{
  const y=177+i*128;
  rect(s,X,y,W,105,i===0?C.soft:C.white,C.border,1,13);
  capsule(s,num,X+19,y+36,54,C.olive,C.dark);
  text(s,title,X+90,y+14,480,39,{size:30,bold:true});
  text(s,label,X+91,y+59,460,28,{size:19,color:C.accent,bold:true});
  text(s,body,X+582,y+24,380,55,{size:23,color:C.muted});
});

s=slide(5,'Person 3','Validierung mit Blackbox-Tests','Manuelle Funktionsprüfung im Browser anhand von Ein- und Ausgaben',
  '0:45 · Person 3\nDie Tabelle enthält Beispieldaten und Soll-Ergebnisse. Vor dem Vortrag ausführen und die tatsächlichen Ergebnisse in der letzten Spalte eintragen. Ein Blackbox-Test prüft das sichtbare Verhalten unabhängig davon, wie der Code intern arbeitet. Einen Positivfall und einen Negativfall kurz gegenüberstellen. In der Demo gezeigte Funktionen nur dann als bestanden eintragen, wenn sie im Testprotokoll bestätigt sind.\n'+project+'\n'+guide);
table(s,[
 ['Fall','Eingabe oder Aktion','Erwartetes Ergebnis','Ist / Ergebnis'],
 ['T01','Titel „Drucker nicht erreichbar“','Ticket gespeichert, Status „Offen“','Eintragen'],
 ['T02','Titel leer, Formular absenden','Titel-Fehlermeldung, kein Ticket','Eintragen'],
 ['T03','Filter „Offen“ und „Mittel“','Nur passende Tickets in der Liste','Eintragen'],
 ['T04','Abgeschl. Ticket bearbeiten','Bearbeitung erst nach Wiederöffnung','Eintragen'],
 ['T05','Verknüpften Bearbeiter löschen','Löschen blockiert / Zuordnung gelöst','Eintragen']
],182,[47,60,60,60,60,60],[72,320,406,189],{size:20});
band(s,'Testdaten im Projekt','Vorbereitete Beispieltickets aus dem DatabaseSeeder',550);

s=slide(6,'Person 3','Soll-Ist-Vergleich','Pflichtanforderungen und aktueller Projektstand',
  '1:05 · Person 3\nDie Einstufung basiert auf dem lokalen Quellcode, nicht auf einem vollständigen Laufzeittest. Ticket- und IT-Mitarbeiterverwaltung sowie Kategorie-Zuordnung und Statusfilter sind im Code vorhanden. Die Support-Übersicht bietet für abgeschlossene Tickets weiterhin „Bearbeiten“. Auch die beiden Edit-Aktionen im SupportController prüfen den Abschlussstatus nicht. Kategorie-Löschen löst die Ticketzuordnung im Controller auf. Den Fall „verknüpften IT-Mitarbeiter löschen“ im Browser prüfen, da beim Löschen keine zugeordneten Tickets geladen werden.\n'+project+'\n'+repo+'\nDateien: Controllers/SupportController.cs, Controllers/IT_MitarbeiterController.cs, Controllers/KategorieController.cs, Views/Support/Index.cshtml.');
table(s,[
 ['Anforderung','Umsetzung im Projektstand','Status'],
 ['Tickets und IT-Mitarbeiter','Anlegen, Anzeigen, Bearbeiten und Löschen','Im Code vorhanden'],
 ['Zuweisung und Kategorien','IT-Mitarbeiter und verwaltbare Kategorien','Im Code vorhanden'],
 ['Priorität, Status und Filter','Je drei Stufen, Filter im Support','Im Code vorhanden'],
 ['Pflichtfeldvalidierung','ModelState und Eingabemeldungen','Im Code vorhanden'],
 ['Bearbeitung nach Wiederöffnung','Wiederöffnung da, Bearbeitungssperre fehlt','Offen'],
 ['Löschen verknüpfter IT-Mitarbeiter','Löschverhalten mit Ticketzuweisung','Zu prüfen']
],179,[42,54,54,54,54,54,54],[362,424,201],{size:20});

s=slide(6,'Person 3','Fazit und Ausblick','Erkenntnisse aus der Umsetzung und mögliche Erweiterungen',
  '0:45 · Person 3\nDiese Fazit-Stichpunkte sind Gesprächsimpulse. Jede Person kann einen Satz mit ihrer eigenen Erfahrung ergänzen. Als nächstes zuerst die Bearbeitungssperre und den Löschfall absichern. Erst nach der Validierung über Komfortfunktionen wie die Volltextsuche entscheiden.\n'+project+'\n'+repo);
panel(s,X,180,481,375,'Persönliches Fazit',['Person 1 · Anforderungen als Grundlage für Tests','Person 2 · Datenmodell vor der ersten Migration','Person 3 · Statuswechsel als eigener Testfall'],{bodySize:20});
panel(s,X+506,180,481,375,'Nächste Schritte',['Bearbeitungssperre für geschlossene Tickets','Löschregel mit verknüpften Tickets testen','Volltextsuche für Tickets','Kommentare zum Bearbeitungsverlauf'],{bodySize:20,fill:C.soft});

s=slide(6,'Person 3','','',
  '0:10 · Person 3\nBedanken und zum Fachgespräch überleiten. Alle drei Personen stehen für Rückfragen zu ihren jeweiligen Beiträgen bereit.\n'+project);
pic(s,'logo',X,127,104,104);
text(s,'Vielen Dank!',X,258,W,110,{size:83,bold:true});
text(s,'Fragen zum Service Desk?',X+3,380,W-3,51,{size:32,color:C.muted});
text(s,'Person 1   /   Person 2   /   Person 3',X+4,480,W-4,33,{size:22,bold:true,color:C.accent});

await fs.mkdir(path.join(dir,'render-v3'),{recursive:true});
const out=path.join(dir,'candidate-v3.pptx');
await (await PresentationFile.exportPptx(P)).save(out);
for(const [i,slide] of P.slides.items.entries()){
  const png=await P.export({slide,format:'png',scale:1});
  await fs.writeFile(path.join(dir,'render-v3',String(i+1).padStart(2,'0')+'.png'),new Uint8Array(await png.arrayBuffer()));
}
console.log('Exported',P.slides.items.length,'slides to',out);
