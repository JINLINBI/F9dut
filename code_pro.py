#coding:utf8
#!/usr/bin/python
from PIL import Image
import hashlib
import time 
import math
import os
class VectorCompare:
    def magnitude(self,concordance):
        total=0
        for word,count in concordance.iteritems():
            total+=count ** 2
        return math.sqrt(total)
    def relation(self,concordance1,concordance2):
        relevance=0
        topvalue=0
        for word,count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue+=count*concordance2[word]
        return topvalue/(self.magnitude(concordance1)*self.magnitude(concordance2))
class Code_pro(object):
    def __init__(self):
        self.v=VectorCompare()
        self.iconset=['0','1','2','3','4','5','6','7','8','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']
        self.imageset=[]
        for letter in self.iconset:
            for img in os.listdir('./iconset/%s/'%(letter)):
                temp=[]
                if img!='Thumbs.db' and img!=".DS_Store":
                    temp.append(self.buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
                self.imageset.append({
                    letter:temp
                    })
    def crackCode(self,codePath):
        im=Image.open(codePath)
        im.convert("P")
        im2=Image.new("P",im.size,255)
        for x in range(im.size[1]):
            for y in range(im.size[0]):
                pix=im.getpixel((y,x))
                if pix==43:
                    im2.putpixel((y,x),0)
         #########################333
        inletter=False
        foundletter=False
        start=0 
        end=0 
        letters=[]
        for y in range(im2.size[0]):
            for x in range(im2.size[1]):
                pix=im2.getpixel((y,x))
                if pix!=255:
                    inletter=True
            if foundletter ==False and inletter == True:
                foundletter=True
                start=y
            if foundletter ==True and inletter == False:
                foundletter =False
                end=y
                letters.append((start,end))
            inletter=False

        #pre deal with cover

        fuckcount =0
        for fuck in letters:
            if(fuck[1]-fuck[0])<5:
                del letters[fuckcount]
                break
            fuckcount+=1
        countIndex=0
        for i in letters:
            if i[0]>65 and len(letters)>4:
                del letters[countIndex]
                break
            if (i[1]-i[0])>20 and len(letters)>4:
                start=i[0]
                end=i[0]
                mid=(start+end)/2
                letters.insert(countIndex,(mid,end))
                letters.insert(countIndex,(start,mid+1))
                del letters[countIndex+2]
                break
            if len(letters)==1:
                start=i[0]
                end=i[1]
                pivot=(end-start)/4
                letters.insert(countIndex,(start+pivot*3,end))
                letters.insert(countIndex,(start+pivot*2,start+pivot*3))
                letters.insert(countIndex,(start+pivot,start+pivot*2))
                letters.insert(countIndex,(start,pivot+start))
                del letters[countIndex+4]
                break
            if (i[1]-i[0])>=26 and len(letters)==2:
                start=i[0]
                end=i[1]
                pivot=(end-start)/3
                letters.insert(countIndex,(start+pivot*2,end))
                letters.insert(countIndex,(start+pivot,start+pivot*2))
                letters.insert(countIndex,(start,start+pivot))
                del letters[countIndex+3]
                break
            elif (i[1]-i[0])>=19 and (i[1]-i[0])<26 and len(letters)==2:
                start=i[0]
                end=i[1]
                pivot=(start+end)/2
                letters.insert(countIndex,(pivot,end))
                letters.insert(countIndex,(start,pivot))
                del letters[countIndex+2]
                break
            elif len(letters)==2:
                break
            if (i[1]-i[0])>13 and len(letters)==3:
                start=i[0]
                end=i[1]
                mid=(start+end)/2
                letters.insert(countIndex,(mid,end))
                letters.insert(countIndex,(start,mid))
                del letters[countIndex+2]
                break
            countIndex+=1
        countIndex=0
        for letter in letters:
            if(letter[1]-letter[0])>=30 and len(letters)==2:
                start=letter[0]
                end=letter[1]
                pivot=(end-start)/3
                letters.insert(countIndex,(start+pivot*2,end))
                letters.insert(countIndex,(start+pivot,start+pivot*2))
                letters.insert(countIndex,(start,start+pivot))
                del letters[countIndex]
                break
            elif (letter[1]-letter[0])>=18 and len(letters)==3:
                start=letter[0]
                end=letter[1]
                mid=(start+end)/2
                letters.insert(countIndex,(mid,end))
                letters.insert(countIndex,(start,mid))
                del letters[countIndex+2]
            countIndex+=1
        print letters
        code=""
        for letter in letters:
            im3=im2.crop((letter[0],0,letter[1],im2.size[1]))

            guess=[]
            for image in self.imageset:
                for x,y in image.iteritems():
                    if len(y)!=0:
                        guess.append((self.v.relation(y[0],self.buildvector(im3)),x))
            guess.sort(reverse=True)
            code+=guess[0][1]
        return code
    def buildvector(self,im):
        d1={}
        count=0
        for i in im.getdata():
            d1[count]=i
            count+=1
        return d1

