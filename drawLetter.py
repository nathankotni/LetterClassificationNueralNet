import installLibraries
import sys, os
import pygame
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class pixel(object):
    def __init__(self, xInput, yInput, widthInput, heightInput, rowsInput, colsInput):
        self.x = xInput
        self.y = yInput
        self.width = widthInput
        self.height = heightInput
        self.rows = rowsInput
        self.cols = colsInput
        self.color = (255,255,255)
        self.neighborsList = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.x + self.width, self.y + self.height))

    def getDirectNeighbors(self, g, offsetI, offsetJ):
        j = (self.x  // 2) + offsetJ
        i = (self.y // 2) + offsetI
        rowsCheck = self.rows
        colsCheck = self.cols
        newNeighborsList = []
        if i < colsCheck - 1:
            newNeighborsList.append(g.pixelsList[i + 1][j])
        if i > 0:
            newNeighborsList.append(g.pixelsList[i - 1][j])
        if j < rowsCheck - 1: 
            newNeighborsList.append(g.pixelsList[i][j + 1])
        if j > 0:
            newNeighborsList.append(g.pixelsList[i][j - 1])

        if j > 0 and i > 0: 
            newNeighborsList.append(g.pixelsList[i - 1][j - 1])

        if j < rowsCheck - 1 and i > 0:
            newNeighborsList.append(g.pixelsList[i - 1][j + 1])

        if i < colsCheck - 1 and j > 0: 
            newNeighborsList.append(g.pixelsList[i + 1][j - 1])

        if j < rowsCheck - 1 and i < colsCheck - 1:
            newNeighborsList.append(g.pixelsList[i + 1][j + 1])

        return newNeighborsList

    def getNeighborsList(self, g):
        j = self.x // 2 
        i = self.y // 2 
        rows = self.rows
        cols = self.cols

        if i < cols - 1:
            self.neighborsList.append(g.pixelsList[i + 1][j])
            neighborsList = self.getDirectNeighbors(g, 1, 0)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)
        if i > 0:
            self.neighborsList.append(g.pixelsList[i - 1][j])
            neighborsList = self.getDirectNeighbors(g, -1, 0)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)
        if j < rows - 1:
            self.neighborsList.append(g.pixelsList[i][j + 1])
            neighborsList = self.getDirectNeighbors(g, 0, 1)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)
        if j > 0: 
            self.neighborsList.append(g.pixelsList[i][j - 1])
            neighborsList = self.getDirectNeighbors(g, 0, -1)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)

        if j > 0 and i > 0:
            self.neighborsList.append(g.pixelsList[i - 1][j - 1])
            neighborsList = self.getDirectNeighbors(g, -1, -1)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)

        if j < rows - 1 and i > 0:
            self.neighborsList.append(g.pixelsList[i - 1][j + 1])
            neighborsList = self.getDirectNeighbors(g, -1, 1)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)

        if i < cols - 1 and j > 0: 
            self.neighborsList.append(g.pixelsList[i + 1][j - 1])
            neighborsList = self.getDirectNeighbors(g, 1, -1)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)

        if j < rows - 1 and i < cols - 1:
            self.neighborsList.append(g.pixelsList[i + 1][j + 1])
            neighborsList = self.getDirectNeighbors(g, 1, 1)
            for neighbor in neighborsList:
                self.neighborsList.append(neighbor)


class pixelGrid(object):
    pixelsList = []

    def __init__(self, rowInput, colInput, widthInput, heightInput):
        self.rows = rowInput
        self.cols = colInput
        self.len = rowInput * colInput
        self.width = widthInput
        self.height = heightInput
        self.setGrid()
        pass

    def drawGrid(self, surface):
        for row in self.pixelsList:
            for pixelInstance in row:
                pixelInstance.draw(surface)

    def setGrid(self):
        xSpacing = self.width // self.cols
        ySpacing = self.height // self.rows
        self.pixelsList = []
        for r in range(self.rows):
            self.pixelsList.append([])
            for c in range(self.cols):
                self.pixelsList[r].append(pixel(xSpacing * c, ySpacing * r, xSpacing, ySpacing, self.rows, self.cols))

        for r in range(self.rows):
            for c in range(self.cols):
                self.pixelsList[r][c].getNeighborsList(self)

    def clicked(self, pos):
        try:
            xPos = pos[0]
            yPos = pos[1]
            i = int(xPos) // self.pixelsList[0][0].width
            j = int(yPos) // self.pixelsList[0][0].height

            return self.pixelsList[j][i]
        except:
            pass


def takeScreenshot(arrPixels):
    saveFileName = "testImageTemp.png"
    newArr = [[] for row in range(len(arrPixels))]

    for i in range(len(arrPixels)):
        for j in range(len(arrPixels[i])):
            if arrPixels[i][j].color == (255,255,255):
                newArr[i].append(1.0)
            else:
                newArr[i].append(0.0)

    numpArr = np.array(newArr)

    im = Image.fromarray(np.int8(numpArr * 255)).convert('RGB')
    im.save(saveFileName)
    return saveFileName

def guess(imageName):
    img = tf.keras.utils.load_img(imageName, target_size=(150, 150))
    img = tf.image.rgb_to_grayscale(img)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    model = tf.keras.models.load_model('letterModel.model')

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print("I predict this letter is:", chr(97 + np.argmax(score)))
    try:
        os.remove("testImageTemp.png")
    except:
        print("Drawn test image file not found")





pygame.init()
width = height = 300
windowSize = width, height

window = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Letter Guesser")
gridInstance = pixelGrid(150, 150, width, height)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            imgName = takeScreenshot(gridInstance.pixelsList)
            guess(imgName)
            run = False
        elif pygame.mouse.get_pressed()[2]:
            try:
                pos = pygame.mouse.get_pos()
                clickedElement = gridInstance.clicked(pos)
                clickedElement.color = (255,255,255)
            except:
                pass
        elif pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            clickedElement = gridInstance.clicked(pos)
            clickedElement.color = (0,0,0)
            for n in clickedElement.neighborsList:
                n.color = (0,0,0)

        gridInstance.drawGrid(window)
        pygame.display.update()


sys.exit()
