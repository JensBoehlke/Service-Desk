from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

root=Path(__file__).resolve().parent
doc=Document()

def xml(tag, **data):
    out=OxmlElement('w:'+tag)
    for key,val in data.items():
        out.set(qn('w:'+key),str(val))
    return out

def style(name,size,bold=False,before=0,after=7,spacing=1.18,keep=False):
    s=doc.styles[name] if name in doc.styles else doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
    s.font.name='Arial'
    s.font.color.rgb=RGBColor.from_string('000000')
    s.font.bold=bold
    s.font.italic=False
    s.font.size=Pt(size)
    for font in s.element.get_or_add_rPr().findall(qn('w:rFonts')):
        for a in ('asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme'):
            font.attrib.pop(qn('w:'+a),None)
    for n in s.element.get_or_add_pPr().findall(qn('w:pBdr')):
        n.getparent().remove(n)
    p=s.paragraph_format
    p.space_before=Pt(before)
    p.space_after=Pt(after)
    p.line_spacing=spacing
    p.keep_with_next=keep
    p.widow_control=True

style('Normal',11,after=7,spacing=1.16)
style('Title',31,True,after=10,keep=True)
style('Subtitle',15,after=24,keep=True)
style('Heading 1',20,True,after=11,keep=True)
style('Heading 2',13,True,9,5,keep=True)
style('Tabelleninhalt',9.5,after=0,spacing=1.04)
style('Tabellenabstand',3,after=1,spacing=1)
style('Bild',10,after=2,spacing=1,keep=True)
style('Bildunterschrift',9,after=7)
style('Verzeichnis',10.5,after=5,spacing=1.1)
style('Quelle',10,after=6)
style('Code',9.5,after=4)
doc.styles['Code'].font.name='Consolas'
doc.styles['Bild'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.styles['Normal'].element.get_or_add_rPr().append(xml('lang',val='de-DE'))
doc.settings.element.append(xml('updateFields',val='true'))
doc.core_properties.title='Projektdokumentation ServiceDesk'
doc.core_properties.author='Babak Najafpoursarabi, Jens Böhlke und Daniel Kowalczyk'
s=doc.sections[0]
s.page_width=Cm(21)
s.page_height=Cm(29.7)
s.left_margin=s.right_margin=Cm(2.2)
s.top_margin=Cm(2.15)
s.bottom_margin=Cm(1.9)
s.header_distance=Cm(.82)
s.footer_distance=Cm(.84)

def header(section,fmt,cached,new):
    for old in section._sectPr.findall(qn('w:pgNumType')):
        section._sectPr.remove(old)
    section._sectPr.insert_element_before(xml('pgNumType',fmt=fmt,start=1),'w:cols')
    if new:
        section.header.is_linked_to_previous=False
        p=section.header.paragraphs[0]
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16.6),WD_TAB_ALIGNMENT.RIGHT)
        p.add_run('ServiceDesk\tWestfalen Office Solutions GmbH').font.size=Pt(9)
    section.footer.is_linked_to_previous=False
    p=section.footer.paragraphs[0]
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16.6),WD_TAB_ALIGNMENT.RIGHT)
    p.add_run('Najafpoursarabi · Böhlke · Kowalczyk\t').font.size=Pt(9)
    field=xml('fldSimple',instr='PAGE')
    run=xml('r')
    rpr=xml('rPr')
    rpr.append(xml('sz',val=18))
    run.append(rpr)
    val=xml('t')
    val.text=cached
    run.append(val)
    field.append(run)
    p._p.append(field)

def para(text,name=None):
    return doc.add_paragraph(text,style=name)

def h(text,l=1):
    return doc.add_heading(text,l)

def fig(key,caption):
    p=para('','Bild')
    pic=p.add_run().add_picture(str(root/(key+'.png')),width=Cm(16.5))
    pic._inline.docPr.set('descr',caption)
    para(caption,'Bildunterschrift')

def table(lines,weights):
    rows=[s.split('|') for s in lines]
    assert all(len(r)==len(weights) for r in rows)
    t=doc.add_table(rows=len(rows),cols=len(weights))
    t.autofit=False
    border=xml('tblBorders')
    for k in ('top','left','bottom','right','insideH','insideV'):
        border.append(xml(k,val='single',sz=5,color='D9D9D9'))
    t._tbl.tblPr.append(border)
    margins=xml('tblCellMar')
    for k,v in (('top',63),('bottom',63),('left',101),('right',101)):
        margins.append(xml(k,w=v,type='dxa'))
    t._tbl.tblPr.append(margins)
    widths=[Cm(16.6*w/sum(weights)) for w in weights]
    for col,w in zip(t.columns,widths):
        col.width=w
    for i,row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(xml('cantSplit'))
        if i==0:
            row._tr.get_or_add_trPr().append(xml('tblHeader'))
        for j,c in enumerate(row.cells):
            c.width=widths[j]
            c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if i==0:
                c._tc.get_or_add_tcPr().append(xml('shd',fill='E9EEEB'))
            p=c.paragraphs[0]
            p.style='Tabelleninhalt'
            p.add_run(rows[i][j]).bold=(i==0)
    para('','Tabellenabstand')

p=para('Softwareprojekt DO1')
p.paragraph_format.space_before=Pt(86)
p.runs[0].bold=True
para('ServiceDesk','Title')
para('Projektdokumentation zur Entwicklung eines webbasierten IT-Ticketsystems','Subtitle')
para('Abgabetermin   25. November 2026')
para('Projektteam').runs[0].bold=True
for member in ('Babak Najafpoursarabi','Jens Böhlke','Daniel Kowalczyk'):
    para(member)
para('Ausbildungsstätte').runs[0].bold=True
para('BITLC Business IT Learning Center GmbH\nIm Defdahl 10 G\n44141 Dortmund')
para('Auftraggeber im Schulprojekt').runs[0].bold=True
para('Westfalen Office Solutions GmbH, Dortmund')
para('Dokumentationsstand   20. November 2026')

header(doc.add_section(WD_SECTION.NEW_PAGE),'upperRoman','I',True)
h('Inhaltsverzeichnis')
entries=[
('1 Einleitung','1'),('2 Projektplanung','2'),('3 Analysephase','3'),
('   3.3 Anwendungsfälle und Anforderungen','4'),('4 Entwurfsphase','5'),
('   4.3 Datenmodell, Geschäftsregeln und Testplanung','6'),('5 Implementierungsphase','7'),
('   5.1 Mitarbeiterbereich · Jens Böhlke','7'),('   5.2 IT-Support · Daniel Kowalczyk','8'),
('   5.3 und 5.4 Administration und SQL · Babak Najafpoursarabi','9'),
('   5.5 bis 5.7 Migrationen, Layout und Zusammenführung','10'),
('6 Testphase und Qualitätskontrolle','11'),('7 Dokumentation','12'),
('8 Fazit','12'),('A Anhang','i')]
for label,num in entries:
    p=para('','Verzeichnis')
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16.6),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
    p.add_run(label+'\t'+num).bold=not label.startswith(' ')
h('Abbildungsverzeichnis',2)
for label,num in (('1 UML-Anwendungsfalldiagramm','4'),('2 Mockup der Ticketbereiche','5'),
                  ('3 UML-Klassendiagramm','6'),('4 Supportansicht','ii')):
    p=para('','Verzeichnis')
    p.paragraph_format.tab_stops.add_tab_stop(Cm(16.6),WD_TAB_ALIGNMENT.RIGHT,WD_TAB_LEADER.DOTS)
    p.add_run(label+'\t'+num)
header(doc.add_section(WD_SECTION.NEW_PAGE),'decimal','1',False)
lines=(root/'document.txt').read_text(encoding='utf-8').splitlines()
i=0
n=0
img=0
while i<len(lines):
    s=lines[i]
    if s.startswith('# '):
        if n:
            doc.add_page_break()
        n+=1
        if 'Fortsetzung' not in s:
            h(s[2:])
    elif s.startswith('## '):
        h(s[3:],1 if s[3:]=='8 Fazit' else 2)
    elif s.startswith('@table'):
        end=lines.index('@end',i+1)
        table(lines[i+1:end],[float(v) for v in s.split()[1:]])
        i=end
    elif s.startswith('@diagram '):
        img+=1
        i+=1
        fig(s.split()[1],f'Abbildung {img}. '+lines[i].split('. ',1)[1])
    elif s and not s.startswith('@'):
        para(s)
    i+=1

header(doc.add_section(WD_SECTION.NEW_PAGE),'lowerRoman','i',False)
h('A Anhang')
h('A.1 Startanleitung',2)
para('Für den lokalen Start unter Windows werden das .NET 10 SDK und SQL Server Express LocalDB benötigt. Im Projektordner mit der Datei Service-Desk.slnx werden die Pakete wiederhergestellt und die Anwendung gestartet.')
para('dotnet restore Service-Desk.slnx','Code')
para('dotnet run --project Service-Desk/Service-Desk.csproj --launch-profile http','Code')
para('Im Browser http://localhost:5226 öffnen. Beim Start wendet die Anwendung ausstehende Migrationen an und richtet die vorgesehenen Demodaten ein. Die Verbindungszeichenfolge DeskData in Service-Desk/appsettings.json verweist standardmäßig auf die lokale Instanz MSSQLLocalDB und die Datenbank DeskDb.')
para('Wenn die Anwendung bei der Migration abbricht, lässt sich die lokale Instanz mit sqllocaldb info prüfen. Für einen Testlauf auf einer anderen SQL-Server-Instanz kann ConnectionStrings__DeskData vor dem Start auf eine separate Testdatenbank zeigen. Der Startvorgang verändert deren Schema durch die Projektmigrationen.')
h('A.2 Kurzanleitung',2)
para('Im Mitarbeiterbereich über „Neues Ticket“ eine Meldung erfassen. Name, Titel und Beschreibung eintragen, eine Priorität auswählen und bei Bedarf eine Kategorie zuordnen. Nach dem Speichern steht die Meldung mit dem Status Offen in der Übersicht.')
para('Im Supportbereich lässt sich die Meldung nach Status oder Priorität finden. Über „Bearbeiten“ können die Zuständigkeit und der Status gesetzt werden. Nach Abschluss kann der Support das Ticket über „Wieder öffnen“ auf Offen zurücksetzen.')
h('A.3 Quellen und Arbeitsgrundlagen',2)
for item in (
    'BITLC · Aufgabenblatt ServiceDesk Softwareprojekt DO1, insbesondere die Abschnitte 3 bis 7.',
    'BITLC · Vorlage Dokumentation Softwareprojekt.',
    'Projektteam · ServiceDesk_Präsi.pptx, Arbeitsstand vom 20. November 2026.',
    'Projektteam · Repository Service-Desk, Git-Stand e53a7d7, einschließlich Projektkonfiguration, Migrationen, Controller und Razor-Views.',
):
    para(item,'Quelle')

doc.add_page_break()
h('A.4 Supportansicht im Projektstand',2)
fig('support-detail','Abbildung 4. Ausschnitt aus der Supportansicht mit Prioritätsübersicht und Statusanzeige. Quelle: Screenshot des Projektteams.')
para('Die Kennzahlen zeigen, wie viele Vorgänge pro Priorität vorliegen und wie viele Tickets abgeschlossen sind. Darunter stehen die Filter und die Ticketliste für die tägliche Bearbeitung.')

assert n==12 and img==3
doc.save(root/'ServiceDesk_Projektdokumentation.docx')

