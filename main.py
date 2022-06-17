import struct, json, zlib, os, shutil, random

# TFN Encryptor by RickL - Base code by WodsonKun
print("TFN Encryptor by RickL")
filename=input("Please input your TFN here: ")

with open(filename, 'r', encoding="utf-8-sig") as json_file:
  tape=json.load(json_file)


tfnenc=open("output" + "//" + "enc_"+filename,"wb")


# INFOS FROM TFN #
TFNInfoData = tape["info"]


#header
header=struct.pack(">I",1)#00000001
header+=struct.pack(">I",int((212*len(tape["chars"]))+238-36888))#tape version
header+=bytes.fromhex("433A0C96") # before __class info
tfnenc.write(header)

# Gets the total length of Clips inside of the KTAPE
totalINFO = len(TFNInfoData) + 1


# Read info data 
faceDATA=TFNInfoData['face']
sizeDATA=TFNInfoData['size']
boldDATA=TFNInfoData['bold']
italicDATA=TFNInfoData['italic']
charsetDATA=TFNInfoData['charset']
unicodeDATA=TFNInfoData['unicode']
stretchHDATA=TFNInfoData['stretchH']
smoothDATA=TFNInfoData['smooth']
aaDATA=TFNInfoData['aa'] # QUE?
paddingLeftDATA=TFNInfoData['paddingLeft']
paddingRightDATA=TFNInfoData['paddingRight']
paddingTopDATA=TFNInfoData['paddingTop']
paddingBottomDATA=TFNInfoData['paddingBottom']
spacingLeftDATA=TFNInfoData['spacingLeft']
spacingTopDATA=TFNInfoData['spacingTop']
outlineDATA=TFNInfoData['outline']


# info + common
ly_running = True
cK = 1
while ly_running:
    if cK + 1 == totalINFO:
        ly_running = False

    if cK < totalINFO:
        clips=bytes.fromhex("000000EC00000050")
        clips+=struct.pack(">I",len(faceDATA)) + faceDATA.encode()
        clips+=struct.pack(">I",sizeDATA)
        clips+=struct.pack(">I",boldDATA)
        clips+=struct.pack(">I",italicDATA)
        clips+=struct.pack(">I",len(charsetDATA)) + charsetDATA.encode()
        clips+=struct.pack(">I",unicodeDATA)
        clips+=struct.pack(">I",stretchHDATA)
        clips+=struct.pack(">I",smoothDATA)
        clips+=struct.pack(">I",aaDATA)
        clips+=struct.pack(">I",paddingLeftDATA)
        clips+=struct.pack(">I",paddingRightDATA)
        clips+=struct.pack(">I",paddingTopDATA)
        clips+=struct.pack(">I",paddingBottomDATA)
        clips+=struct.pack(">I",spacingLeftDATA)
        clips+=struct.pack(">I",spacingTopDATA)
        clips+=struct.pack(">I",outlineDATA)
        cK += 1
tfnenc.write(clips)

#Common#
TFNCommonData = tape["common"]
totalCommon = len(TFNCommonData) + 1

lineHeightDATA = TFNCommonData['lineHeight']#Read info data 
baseDATA = TFNCommonData['base']
scaleWDATA = TFNCommonData['scaleW']
scaleHDATA = TFNCommonData['scaleH']

TFNPageData = tape["pages"]#...
totalPages = len(TFNPageData)

idDATA = tape["pages"][0]['id']# Read info data 
fileDATA = tape["pages"][0]['file']


#LINES/SCALE#
cy_running = True
cS = 1
while cy_running:
    if cS + 1 == totalCommon:
        cy_running = False

    if cS < totalCommon:
        commonenc=bytes.fromhex("00000010")
        commonenc+=struct.pack(">I",lineHeightDATA)
        commonenc+=struct.pack(">I",baseDATA)
        commonenc+=struct.pack(">I",scaleWDATA)
        commonenc+=struct.pack(">I",scaleHDATA)
        commonenc+=struct.pack(">i",totalPages) 
        commonenc+=bytes.fromhex("00000020") #page id
        cS += 1
    
tfnenc.write(commonenc)


#Pages#
totalPage = len(TFNPageData)
cr_running = True
cT = 1
while cr_running:
    if cT + 1 == totalPage:
        cr_running = False

    if cT < totalPage:
        filename=[tape["pages"][cT - 1]["file"].replace(tape["pages"][cT - 1]["file"].split("/")[-1],""),tape["pages"][cT - 1]["file"].split("/")[-1]]
        pageenc=struct.pack(">I",tape["pages"][cT - 1]["id"])
        pageenc+=struct.pack(">I",len(filename[1]))+filename[1].encode()
        pageenc+=struct.pack(">I",len(filename[0]))+filename[0].encode()
        pageenc+=struct.pack("<I",zlib.crc32(filename[1].encode()))
        pageenc+=bytes.fromhex("0000000000000020") #page id

        cT += 1 
    tfnenc.write(pageenc)
    
filename=[tape["pages"][cT - 1]["file"].replace(tape["pages"][cT - 1]["file"].split("/")[-1],""),tape["pages"][cT - 1]["file"].split("/")[-1]]
pageenc=struct.pack(">I",tape["pages"][cT - 1]["id"])
pageenc+=struct.pack(">I",len(filename[1]))+filename[1].encode()
pageenc+=struct.pack(">I",len(filename[0]))+filename[0].encode()
pageenc+=struct.pack("<I",zlib.crc32(filename[1].encode()))
pageenc+=bytes.fromhex("00000000") #page id
tfnenc.write(pageenc)


#Chars#
charslen=struct.pack(">I",int((len(tape["chars"]))))
tfnenc.write(charslen)

TFNCharData = tape["chars"]
totalChar = len(TFNCharData) + 1

cN_running = True
cM = 1
while cN_running:
    if cM + 1 == totalChar:
        cN_running = False

    if cM < totalChar:
        charenc=bytes.fromhex("00000028")
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["id"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["x"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["y"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["width"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["height"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["xoffset"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["yoffset"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["xadvance"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["page"])
        charenc+=struct.pack(">i",TFNCharData[cM - 1]["chnl"])
        cM += 1

    tfnenc.write(charenc)