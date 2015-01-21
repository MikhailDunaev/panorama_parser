import requests
import argparse
import os
import re
import urllib.parse
from functools import reduce

CUBE_SIDES=['front','back','right','left','down','up']

def link_generator(base_url, magnification, side):

    if side:
        sides=[side,]
    else:
        sides=CUBE_SIDES
    
    for current_side in sides:
        for ttt in [(i,j,k) for i in range(magnification+1) for j in range(i+1) for k in range(i+1)]:
            print(current_side)
            yield base_url.format(current_side,ttt[0],ttt[1],ttt[2]), ttt
            #yield base_url.format(current_side,i,j,k), ttt

def generate_base_url(url):

    url = re.sub('https','http',url)
    base = re.sub('/\d+/\d+/\d+.jpg','/{}/{}/{}.jpg',url)
    base = re.sub('/({})/'.format('|'.join(CUBE_SIDES)),'/{}/',base)
    print(base)
    return base

def generate_base_path(url):

    baseurl = re.sub('/\d+/\d+/\d+.jpg','',url)
    path = reduce(os.path.join, urllib.parse.urlparse(baseurl).path.split('/'), '.')
    return path

def main(url, magnification, side):

    base_url = generate_base_url(url)

    for current_url,ttt in link_generator(base_url,magnification,side):
        try:
            r = requests.get(current_url)
            path = generate_base_path(current_url)
            if not os.path.exists(path):
                os.makedirs(path)
            filename = os.path.join(path,"{}_{}_{}.jpg".format(*ttt))
            with open(filename,'wb') as fw:
                fw.write(r.content)
                print("Succesfully wrote {}".format(filename))
        except:
            print("Failed to get url", current_url)
            import traceback
            traceback.print_exc()



if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Panorama Image Grabber")

    parser.add_argument("--side", type = str, default = None, help = "Which side of cube to parse. If not supplied parse all 6.")
    parser.add_argument("--magnification", type = int, default = 2, help = "Bigger value means more pictures")
    parser.add_argument("url", type =str, help = "Base url for parser to work with. For example http://cdn2.360cities.net/pano/alexander-peskov/00301992_web.jpg/cube/right/tile/512/2/3/3.jpg")

    args = parser.parse_args()
    main(url=args.url,magnification=args.magnification,side=args.side)
