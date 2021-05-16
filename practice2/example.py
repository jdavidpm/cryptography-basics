from PIL import Image

im = Image.open('japan.bmp')
rgb_im = im.convert('RGB')
pix = im.load()
#r, g, b = rgb_im.getpixel((0, 0))
for w in range(im.size[0]):
    for h in range(im.size[1]):
        r, g, b = rgb_im.getpixel((w, h))
        pix[w, h] = (r + 231, g + 334, b + 143)
        #im.putpixel((w, h), (r + 23, g + 34, b + 13))
im.save("new.bmp")