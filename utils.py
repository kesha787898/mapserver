from PIL import Image
key='AIzaSyBdGopaR8rEjxbHCwSH94rSA4II-DrxtNQ'
import json
from urllib.parse import quote_plus
import urllib
import torch
from torchvision.transforms import transforms

def coord(adress):
    try:
        adress=quote_plus(adress)
        url=f'https://maps.googleapis.com/maps/api/geocode/json?address={adress}&key={key}'
        content = urllib.request.urlopen(url).read()
    except BaseException as e:
        print(e)
        print(e.args)

    try:
        my_json = content.decode('utf8')
    except BaseException as e:
        print(e)
        print(e.args)

    try:
        data = json.loads(my_json)
    except BaseException as e:
        print(e)
        print(e.args)
        print(my_json)
    x = data['results'][0]['geometry']['location']['lat'] 
    y = data['results'][0]['geometry']['location']['lng'] 
    return x, y

def get_empty_photo_url(x, y):
    return f"https://maps.googleapis.com/maps/api/staticmap?key={key}&center={x}," \
           f"{y}&zoom=15&format=png&maptype=roadmap" \
           f"&style=element:labels.icon%7Ccolor:0x010101%" \
           f"7Clightness:-100%7Cvisibility:off&style=element:labels.text" \
           f"%7Cvisibility:off&size=480x360"

def get_img(name,g):
  url=get_empty_photo_url(*coord(name))
  rez=urllib.request.urlopen(url)
  img=Image.open(rez)
  width = img.size[0]
  height = img.size[1]
  img = img.crop( (0,0,width,height-40) )
  gen=g.cpu()
  x1=transforms.ToTensor()((img).convert('RGB')).unsqueeze (0)
  rez1=gen(x1)
  return transforms.ToPILImage()(rez1[0].cpu())