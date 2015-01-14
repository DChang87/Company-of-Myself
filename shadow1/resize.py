from pygame import *
for i in range(1,28):
    pic = image.load("shl"+str(i)+".png")
    pic = transform.scale(pic,(40,47))
    image.save(pic,"shl%d.png" % i)
