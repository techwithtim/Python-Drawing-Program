# GRID MODULE BY TIM
#This module contains 5 classes (grid, menu, pixelArt, pixel,colorPallet)
#the grid class is the abstract/parent class, the pixelArt and menu class inherit from it.(they are childs)
#The color pallet class inherits from pixel art class as they both use similar methods.
#The pixel art and colorPallet class creates pixel objects to
#populate the grid, therfore they are dependant of pixel.
#------------------------------------------------------
#Class Descriptions are given above each class.
import pygame
pygame.init()

#Main abstract class (parent)
#This class is capable of creating a grid containing different rows and different columns, bases upon those arguments it
#will automatically alter the pixel size. To display the grid simply call ____.drawGrid(). To find the item in the grid
#that was clicked on call ____.clicked().
class grid(object):
    def __init__(self, win, width, height, cols, rows, showGrid=False, startx = 0, starty = 0, bg=(255,255,255)):
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.bg = bg
        self.startx = startx
        self.starty = starty
        self.lineThick = 1
        self.showGrid = showGrid #If we should show the black outline
        self.isSelected = None
        self.grid = None

        self.screen = win
        pygame.display.update()
                    
    def getGrid(self):
        return self.grid #Return the grid list

    def drawGrid(self, lineColor=(0,0,0)): #This will draw the lines to create the grid, this is done so by simply creating overlapping boxes
        x = self.startx
        y = self.starty
        
        for i in range(self.cols):
            y = self.starty + self.height
            if i > 0:
                x += (self.width / self.cols)
            for j in range(self.rows):
                y -= self.height / self.rows 
                pygame.draw.rect(self.screen, (0,0,0),(x, y, self.width / self.cols, self.height/ self.rows), 1)

    def clicked(self, pos): #Return the position in the grid that user clicked on
        try:
            t = pos[0]
            w = pos[1]
            g1 = int((t - self.startx) / self.grid[0][0].w)
            g2 = int((w - self.starty) / self.grid[0][0].h)

            self.selected = self.grid[g1][g2]

            return self.grid[g1][g2]
        
        except IndexError: #If we run into an index error that means that the user did not click on a position in the grid
            return False

    def isSelected(self): #Return the currently selected object
        return self.selected


#This is the concrete class used to draw pixels in a grid
#The draw grid function in this class uses polymorphism to create a grid
#full of pixel objects. It still contains the methods from the aboce class
#has its own specific clearGrid(). Using ____.clearGrid() will simply set the color
#to the original background color.
class pixelArt(grid):  
    def drawGrid(self):
        self.grid = []
        # Create pixels in the grid
        for i in range(self.cols):
            self.grid.append([])
            for j in range(self.rows):
                self.grid[i].append(pixel(i, j, self.width, self.height, self.cols, self.rows, self.startx, self.starty, self.showGrid))
                self.grid[i][j].show(self.screen, (255,255,255), self.lineThick)
                if self.showGrid:
                    self.grid[i][j].show(self.screen, (0,0,0), 1,False,True)
                    
        #This generates the neighbours of each pixel so that we can draw multiple thickness of lines
        for c in range(self.cols):
            for r in range(self.rows):
                self.grid[c][r].getNeighbors(self.grid)
        
        self.selected = self.grid[self.cols - 1][self.rows - 1]

        
    def clearGrid(self): #This will set all of the pixels to the same color as the background color
        for pixels in self.grid:
            for p in pixels:
                if self.showGrid: #If the grid is to be showing we must redraw the pixels so that we can see the grid after we change their color
                    p.show(self.screen, self.bg, 0)
                    p.show(self.screen, (0,0,0), 1)
                else:
                    p.show(self.screen, self.bg, 0)


#This class is responsible for creating the color pallet in the bottom left hand side of the screen
#and is a concrete class. The setColor() method simply takes a list of colors and assigns them to pixels
#in the grid. This can only be called after the grid has been created.
class colorPallet(pixelArt):
    def setColor(self, colorList): #The colorList argument passed to the function must be equal to the number of pixels in the grid
        colourCount = 0

        for pixels in self.getGrid():
            for p in pixels:
                p.show(self.screen, colorList[colourCount],0)
                colourCount += 1


#This class creates basic grid menus that can contain text.
#It uses all of the methods from the parent grid class and is a concrete class
#The setText method takes a list of strings and displays them in the grid.
class menu(grid):
    def setText(self, textList): #The textList argument passed must be equal to the number of spots in the grid
        
        self.grid = []
        # Create textObjects in the grid
        for i in range(self.cols):
            self.grid.append([])
            for j in range(self.rows):
                self.grid[i].append(textObject(i, j, self.width, self.height, self.cols, self.rows, self.startx, self.starty))
        #Set the text for each of those objects
        c = 0
        for spots in self.getGrid():
            for s in spots:
                s.showText(self.screen, textList[c])
                c += 1

                 
#This class is responsible for displaying text and these objects are added into the grid.               
#The showText() method will display the text while the show() method will draw a square showing thr grid.
class textObject():
    def __init__(self, i, j, width, height, cols, rows, startx=0, starty=0):
        self.col = i #The column of the current instance in the grid
        self.row = j #The row of the current instance in the grid
        self.rows = rows #Total amount of rows
        self.cols = cols #Total amount of columns
        self.w = width / cols
        self.h = height / rows
        self.x = self.col * self.w + startx
        self.y = self.row * self.h + starty
        self.text = ''
    
    def showText(self, win, txt): #This will render and draw the text on the screen
        self.text = txt
        myFont = pygame.font.SysFont('comicsansms', 15)
        text = myFont.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + (self.w /2 - text.get_width() / 2), self.y + (self.h/2 - text.get_height() / 2))) #This will make sure the text is center in the screen.

    def show(self, screen, color, st, outline=False): #Draws a square displaying the area in the grid  
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), st)


#This pixel object is responsible for stroing a color and displaying it to the screen. These objects are added into the grid.
#The methods are named according to what they do.
class pixel():
    def __init__(self, i,j, width, height, cols, rows, startx=0, starty=0, showGrid=False):
        self.col = i #The column of the current instance
        self.row = j #The row of the current instance
        self.color = (255,255,255)
        self.rows = rows #Amount of rows in whole grid
        self.cols = cols #Amount of cols in whole grid
        self.showGrid = showGrid
        self.w = width / cols
        self.h = height / rows
        self.x = self.col * self.w + startx
        self.y = self.row * self.h + starty
        self.neighbors = [] 
        
    def show(self, screen, color, st, outline=False, first=False): #Display the current pixel
        if not(first):
            self.color = color
            
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), st)
        if self.showGrid and not(outline):
            pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.w, self.h), 1)
        
    def getPos(self):
        return (self.col * self.w, self.row * self.h)#Return a tuple (x,y) of the top left co-ords of the pixel

    def click(self, screen, color): #If the pixel has been clicked on call this and it will display the new color and set the color attribute for that pixel
        self.show(screen, color, 0)
        self.color = color

    def getColor(self):
        return self.color

    def getNeighbors(self, grid):
        # Get the neighbours of each pixel in the grid, this is used for drawing thicker lines
        i = self.col #the var i is responsible for denoting the current col value in the grid
        j = self.row #the var j is responsible for denoting the current row value in the grid
        rows = self.rows
        cols = self.cols

        #Horizontal and vertical neighbors
        if i < cols-1: #Right
            self.neighbors.append(grid[i + 1][j])
        if i > 0: #Left
            self.neighbors.append(grid[i - 1][j])
        if j < rows-1: #Up
            self.neighbors.append(grid[i][j + 1])
        if j > 0 : #Down
            self.neighbors.append(grid[i][j - 1])

            
        #Diagonal neighbors  
        if j > 0 and i > 0: #Top Left
            self.neighbors.append(grid[i - 1][j - 1])

        if j + 1 < rows and i > -1 and i - 1 > 0: #Bottom Left
            self.neighbors.append(grid[i - 1][j + 1])

        if j - 1 < rows and i < cols - 1 and j - 1 > 0: #Top Right
            self.neighbors.append(grid[i + 1][j - 1])
            
        if j < rows - 1 and i < cols - 1: #Bottom Right
            self.neighbors.append(grid[i + 1][j + 1])
        
    def neighborsReturn(self):
        return self.neighbors #Return a list of the neighbours of the current pixel

        


