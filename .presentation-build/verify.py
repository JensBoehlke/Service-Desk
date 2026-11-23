
import zipfile
from pathlib import Path
from lxml import etree as E
d=Path(__file__).parent
z=zipfile.ZipFile(d/'candidate.pptx')
print('zip:',z.testzip())
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
print('Canvas:', E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns).attrib)
for i in range(1,18):
    t=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
    n=E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
    txt=t.xpath('//a:t/text()',namespaces=ns)
    ntx=n.xpath('//a:t/text()',namespaces=ns)
    print(i,len(txt),len(t.xpath('//a:tbl',namespaces=ns)),len(t.xpath('//p:pic',namespaces=ns)),ntx[0][:65],sum('hier einfügen' in x for x in txt))
