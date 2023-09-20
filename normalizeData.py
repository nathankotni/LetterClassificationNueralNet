import installLibraries
import os
import numpy as np
from PIL import Image
from pathlib import Path
import random


resizeDim = 150
resizeDimSmall = resizeDim - (int((random.random() * 4) + 2) * 10)



inputDir = Path.cwd() / "Images"
images = list(inputDir.rglob('*.png'))
for image in images:
    img = Image.open(image)
    if(img.width > img.height):
        resizePercent = (resizeDimSmall/float(img.width))
        smallDimSize = int((float(img.height)*float(resizePercent)))
        img = img.resize((resizeDimSmall, smallDimSize))

    elif(img.width == img.height):
        img = img.resize((resizeDimSmall, resizeDimSmall))

    else:
        resizePercent = (resizeDimSmall/float(img.height))
        smallDimSize = int((float(img.width)*float(resizePercent)))
        img = img.resize((smallDimSize, resizeDimSmall))

    npArr = np.array(img)
    imgArr = npArr.tolist()
    newArr = [[] for rowCount in range(len(imgArr))]
    whiteFillArr = []
    rowCount =  0
    for row in imgArr:
        for col in row:
            if col[0] < 200:
                (newArr[rowCount]).append(0.0)
            else:
                (newArr[rowCount]).append(1.0)
        rowCount += 1

    rowCount = 0

    for row in imgArr:
        for _ in range((resizeDim - img.width) // 2):
            (newArr[rowCount]).insert(0, 1.0)
            (newArr[rowCount]).append(1.0)
        if(img.width % 2 == 1):
            (newArr[rowCount]).insert(0, 1.0)
        rowCount += 1


    for _ in range(len(newArr[0])):
        whiteFillArr.append(1.0)

    for _ in range((resizeDim - img.height) // 2): 
        newArr.insert(0, whiteFillArr)
        newArr.append(whiteFillArr)
    if(img.height % 2 == 1):
        newArr.append(whiteFillArr)
        
    numpArr = np.array(newArr)

    img = Image.fromarray(np.int8(numpArr * 255)).convert('RGB')

    os.remove(image)
    img.save(image)
    resizeDimSmall = 120



inputDir = Path.cwd() / "ImagesTest"
images = list(inputDir.rglob('*.png'))
for image in images:
    img = Image.open(image)
    if(img.width > img.height):
        resizePercent = (resizeDimSmall/float(img.width))
        smallDimSize = int((float(img.height)*float(resizePercent)))
        img = img.resize((resizeDimSmall, smallDimSize))

    elif(img.width == img.height):
        img = img.resize((resizeDimSmall, resizeDimSmall))

    else:
        resizePercent = (resizeDimSmall/float(img.height))
        smallDimSize = int((float(img.width)*float(resizePercent)))
        img = img.resize((smallDimSize, resizeDimSmall))

    npArr = np.array(img)
    imgArr = npArr.tolist()
    newArr = [[] for rowCount in range(len(imgArr))]
    whiteFillArr = []
    rowCount =  0
    for row in imgArr:
        for col in row:
            if col[0] < 255:
                (newArr[rowCount]).append(0.0)
            else:
                (newArr[rowCount]).append(1.0)
        rowCount += 1

    rowCount = 0

    for row in imgArr:
        for _ in range((resizeDim - img.width) // 2):
            (newArr[rowCount]).insert(0, 1.0)
            (newArr[rowCount]).append(1.0)
        if(img.width % 2 == 1):
            (newArr[rowCount]).insert(0, 1.0)
        rowCount += 1


    for _ in range(len(newArr[0])):
        whiteFillArr.append(1.0)

    for _ in range((resizeDim - img.height) // 2): 
        newArr.insert(0, whiteFillArr)
        newArr.append(whiteFillArr)
    if(img.height % 2 == 1):
        newArr.append(whiteFillArr)
        
    numpArr = np.array(newArr)

    img = Image.fromarray(np.int8(numpArr * 255)).convert('RGB')

    os.remove(image)
    img.save(image)
