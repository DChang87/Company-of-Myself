from pygame import *
piclist = []
for i in range(1,28):
    pic = image.load("sh"+str(i)+".png")
    wid, hi = pic.get_size()
    #screen = display.set_mode(pic.get_size())
    for c in range(wid):
        for b in range(hi):
            r,g,l,a = pic.get_at((c,b))
            if a != 0:
                pic.set_at((c,b),(0,0,0))
    image.save(pic,"sh%d.png" % i)
quit()
