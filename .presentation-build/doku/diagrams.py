from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

folder = Path(__file__).resolve().parent
fontdir = Path('C:/Windows/Fonts')
ink = '#202824'
gray = '#91A39A'
dark = '#27483B'
pale = '#EDF3EF'

def f(size, bold=False):
    return ImageFont.truetype(str(fontdir / ('arialbd.ttf' if bold else 'arial.ttf')), size)

def tc(d, point, s, size=24, bold=False):
    d.multiline_text(point, s, font=f(size,bold), anchor='mm', fill=ink, align='center', spacing=3)

def rect(d, xy, fill='white', rounded=False):
    if rounded:
        d.rounded_rectangle(xy, 9, fill=fill, outline=gray, width=2)
    else:
        d.rectangle(xy, fill=fill, outline=gray, width=2)

def usecase():
    im=Image.new('RGB',(1420,370),'white')
    d=ImageDraw.Draw(im)
    rect(d,(338,8,1404,361))
    d.text((360,18),'ServiceDesk',font=f(23,True),fill=dark)
    for row,(actor,a,b) in enumerate([
        ('Meldende Person','Tickets melden','Status und Details anzeigen'),
        ('IT-Support','Tickets filtern und bearbeiten','Zuweisen, löschen, wieder öffnen'),
        ('Administration','IT-Mitarbeitende verwalten','Kategorien verwalten')]):
        y=87+107*row
        d.ellipse((32,y-23,56,y+1),outline=dark,width=3)
        d.line((44,y+1,44,y+26),fill=dark,width=3)
        d.line((27,y+10,61,y+10),fill=dark,width=3)
        d.line((44,y+26,30,y+43),fill=dark,width=3)
        d.line((44,y+26,58,y+43),fill=dark,width=3)
        tc(d,(174,y+5),actor,25,True)
        # Both associations leave the actor label and end at a separate oval.
        d.line((283,y+3,423,y+3),fill=dark,width=2)
        d.line((283,y-5,310,y-5,310,y-43,1110,y-43,1110,y-34),fill=dark,width=2)
        for x,s in ((422,a),(907,b)):
            d.ellipse((x,y-34,x+410,y+42),outline=gray,fill=pale,width=2)
            tc(d,(x+205,y+3),s,24)
    im.save(folder/'usecase.png')

def modelbox(d,x,y,w,title,fields):
    height=61+len(fields)*34+10
    rect(d,(x,y,x+w,y+height))
    d.rectangle((x+1,y+1,x+w-1,y+50),fill=pale)
    d.line((x,y+51,x+w,y+51),fill=gray,width=2)
    tc(d,(x+w/2,y+25),title,25,True)
    for i,s in enumerate(fields):
        d.text((x+15,y+61+i*34),s,font=f(22),fill=ink)

def classes():
    im=Image.new('RGB',(1420,392),'white')
    d=ImageDraw.Draw(im)
    modelbox(d,10,90,318,'IT_Mitarbeiter',['MitarbeiterId : int','Name : string','Tickets : ICollection<Ticket>'])
    modelbox(d,470,12,480,'Ticket',['TicketId : int','ErstelltVon, Titel, Beschreibung : string','Erstellungsdatum : DateTime','Prioritaet : Prioritaet','Status : TicketStatus','MitarbeiterId : int?','KategorieId : int?'])
    modelbox(d,1090,90,318,'Kategorie',['KategorieId : int','KategorieName : string','Tickets : ICollection<Ticket>'])
    for x1,x2,l,r in [(328,470,'0..1','0..*'),(950,1090,'0..*','0..1')]:
        d.line((x1,193,x2,193),fill=dark,width=3)
        d.text((x1+9,163),l,font=f(22,True),fill=dark)
        d.text((x2-51,163),r,font=f(22,True),fill=dark)
    tc(d,(710,356),'Prioritaet und TicketStatus sind Aufzählungen.',24)
    im.save(folder/'classes.png')

def mockup():
    im=Image.new('RGB',(1420,387),'white')
    d=ImageDraw.Draw(im)
    for i,(x,title) in enumerate([(12,'Mitarbeiterbereich'),(722,'IT-Support')]):
        rect(d,(x,12,x+685,369),rounded=True)
        d.rectangle((x+2,14,x+129,366),fill=pale)
        for j,label in enumerate(['Startseite','Mitarbeiter','Support','Admin']):
            d.text((x+13,40+j*38),label,font=f(19,j==i+1),fill=dark)
        d.text((x+150,36),title,font=f(28,True),fill=ink)
        if i==0:
            controls=[('Neues Ticket',160),('Status auswählen',230)]
            top=96
            cols='Titel                         Status                    Details'
        else:
            controls=[('Offen',122),('In Bearbeitung',160),('Abgeschlossen',175)]
            top=96
            cols='Ticket       Priorität       Zuständigkeit       Aktionen'
        left=x+150
        for label,w in controls:
            rect(d,(left,top,left+w,top+44),fill=pale,rounded=True)
            tc(d,(left+w/2,top+22),label,19,True)
            left+=w+12
        if i:
            rect(d,(x+150,158,x+653,201),rounded=True)
            tc(d,(x+401,179),'Status       Priorität       Kategorie       Datum',18)
        y=224 if i else 167
        d.rectangle((x+150,y,x+653,y+40),fill=pale)
        d.text((x+163,y+9),cols,font=f(19,True),fill=dark)
        for n in range(2):
            line_y=y+61+n*37
            d.line((x+150,line_y+12,x+653,line_y+12),fill=gray,width=1)
            for col,width in [(164,91),(305,64),(453,59),(586,40)]:
                d.rounded_rectangle((x+col,line_y-3,x+col+width,line_y+3),radius=3,fill='#C9D6D0')
    im.save(folder/'mockup.png')

if __name__=='__main__':
    usecase()
    classes()
    mockup()
    previous=folder.parent/'support.png'
    if previous.is_file():
        with Image.open(previous) as im:
            im.crop((7,2,im.width,431)).save(folder/'support-detail.png')

