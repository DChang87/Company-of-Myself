import os
count=0
for k in range(0,4):
    for m in range(0,7):
        count+=1
        os.rename("guy [www.imagesplitter.net]-"+str(k)+"-"+str(m)+".png","guy"+str(count)+".png")
