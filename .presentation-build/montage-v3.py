from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
base=Path(__file__).parent
images=sorted((base/'render-v3').glob('*.png'))
for offset in range(0,len(images),6):
    batch=images[offset:offset+6]
    sheet=Image.new('RGB',(1286,3*377),'#dce6e1')
    for k, f in enumerate(batch):
        im=Image.open(f).convert('RGB')
        im=ImageOps.contain(im,(630,355))
        x=(k%2)*645+5
        y=(k//2)*377+7
        sheet.paste(im,(x,y))
        ImageDraw.Draw(sheet).text((x+3,y+356),f.stem,fill='#193d31')
    sheet.save(base/f'montage-v3-{offset}.png')
