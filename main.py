# DRAWING PROGRAM BY TIM
# main.py file (RUN THIS)
# Description: This program draws a grid of 600, 600 with a given
# pixel size/rows and cols. The user can then interact with the grid
# using a variety of tools from the menu bar on the bottom. They can draw
# by selecting a color from the pallet and clicking the "D" button. This program
# also offers a save feature where a user can save their work to a selected directory.
# It can then be opened by selecting the file from the file nav within the program.
#
#Input: Input is taken at the beginning of the program for the pixel size/rows and cols.
# It is also taken whenever the user clicks.

try:
   import pygame
except:
   import install_requirements
   import pygame
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import gridModule
from gridModule import colorPallet
from gridModule import pixelArt
from gridModule import menu
from gridModule import grid
import sys
import time

sys.setrecursionlimit(1000000)

pygame.init() #initalize pygame
paintBrush = pygame.image.load("Paintbrush.png")
currentVersion = 1.1

#Set defaults for our screen size and rows and columns
rows = 50
cols = 50
wid = 600
heigh = 600

checked = []
def fill(spot, grid, color, c):
   if spot.color != c:
      pass
   else:
      spot.click(grid.screen, color)
      pygame.display.update()
      
      i = spot.col #the var i is responsible for denoting the current col value in the grid
      j = spot.row #the var j is responsible for denoting the current row value in the grid

      #Horizontal and vertical neighbors
      if i < cols-1: #Right
         fill(grid.getGrid()[i + 1][j], grid, color, c)
      if i > 0: #Left
         fill(grid.getGrid()[i - 1][j], grid, color, c)
      if j < rows-1: #Up
         fill(grid.getGrid()[i][j + 1], grid, color, c)
      if j > 0 : #Down
         fill(grid.getGrid()[i][j - 1], grid, color, c)
      

# Saves the current project into a text file that contains the size of the screen, if the gird is showing and all the colors of all the pixels
def save(cols, rows, show, grid, path):
   if len(path) >= 4: # This just makes sure we have .txt at the end of our file selection
      if path[-4:] != '.txt':
         path = path + '.txt'
   else:
      path = path + '.txt'

   # Overwrite the current file, or if it doesn't exist create a new one
   file = open(path, 'w')
   file.write(str(cols) + ' ' + str(rows) + ' ' + str(show) +'\n')

   for pixel in grid:
       for p in pixel: #For every pixel write the color in the text file
           wr = str(p.color[0]) + ',' + str(p.color[1]) + ',' + str(p.color[2])
           file.write(wr + '\n')
   file.write(str(currentVersion))

   file.close()
   name = path.split("/")
   changeCaption(name[-1])


#Opens the file from the given path and displays it to the screen
def openFile(path):
    global grid
    
    file = open(path, 'r')
    f = file.readlines()
    if f[-1] == str(currentVersion):
       
       dimensions = f[0].split() #Dimesnions for the rows and cols
       columns = int(dimensions[0])
       rows = int(dimensions[1])
       
       if dimensions[2] == '0': #If the show grid attribute at the end of our dimensions line is 0 then don't show grid
          v = False
       else:
          v = True
       initalize(columns, rows, v) #Redraw the grid, tool bars, menu bars etc. 
       name = path.split("/")
       changeCaption(name[-1])
       
       line = 0
       for i in range(columns): # For every pixel, read the color and format it into a tuple
          for j in range(rows):
             line += 1
             nColor = []
             for char in f[line].strip().split(','):
                nColor.append(int(char))
                
             
             grid.getGrid()[i][j].show(win, tuple(nColor), 0) #Show the color on the grid
    else:
      window = Tk()
      window.withdraw()
      messagebox.showerror("Unsupported Version", "The file you have opened is created using a previous version of this program. Please open it in that version.")


#Change pygame caption
def changeCaption(txt):
   pygame.display.set_caption(txt)
          

# This shows the file navigator for opening and saving files
def showFileNav(op=False):
   #Op is short form for open as open is a key word
    window = Tk()
    window.attributes("-topmost", True)
    window.withdraw()
    myFormats = [('Windows Text File','*.txt')]
    if op:
       filename = askopenfilename(title="Open File",filetypes=myFormats) # Ask the user which file they want to open
    else:
       filename = asksaveasfilename(title="Save File",filetypes=myFormats) # Ask the user choose a path to save their file to
       
    if filename: #If the user seletced something 
       x = filename[:] # Make a copy
       return x

# Onsubmit function for tkinter form for choosing pixel size
def onsubmit(x=0):
    global cols, rows, wid, heigh
    
    st = rowsCols.get().split(',') # Get the input from the text box
    window.quit()
    window.destroy()
    try: # Make sure both cols and rows are integers
        if st[0].isdigit(): 
            cols = int(st[0])
            while 600//cols != 600/cols:
               if cols < 300:
                  cols += 1
               else:
                  cols -= 1
        if st[1].isdigit():
            rows = int(st[1])
            while 600//rows != 600/rows:
               if rows < 300:
                  rows += 1
               else:
                  rows -= 1
        if cols > 300:
          cols = 300
        if rows > 300:
          rows = 300

    except:
        pass

# Update the lbale which shows the pixel size by getting input on rows and cols
def updateLabel(a, b, c):
   sizePixel = rowsCols.get().split(',') #Get the contents of the label
   l = 12
   w = 12
   
   try:
      l = 600/int(sizePixel[0])
   except:
      pass

   try:
      w = 600/(int(sizePixel[1]))
   except:
      pass

   label1.config(text='Pixel Size: ' + str(l) + ', ' + str(w)) #Change label to show pixel size


#CREATE SCREEN
def initalize(cols, rows, showGrid=False):
   global pallet, grid, win, tools, lineThickness, saveMenu

   #if grid already exsists delete it then recreate it
   try:
      del grid
   except:
      pass
   
   pygame.display.set_icon(paintBrush)   
   win = pygame.display.set_mode((int(wid), int(heigh) + 100))
   pygame.display.set_caption('Untitled')
   win.fill((255,255,255))

   #CREATION OF OBJECTS
   grid = pixelArt(win, int(wid), int(heigh), cols, rows, showGrid)
   grid.drawGrid()

   pallet = colorPallet(win, 90, 90, 3, 3, True, 10, grid.height + 2)
   pallet.drawGrid()

   colorList = [(0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,168,0), (244, 66, 173), (65, 244, 226)]
   pallet.setColor(colorList)

   tools = menu(win, 200, 40, 5, 1, True, grid.width - 210, grid.height + 50)
   tools.drawGrid()

   buttons = ['D', 'E', 'F', 'R', 'C']
   tools.setText(buttons)
   tools.drawGrid()

   l = tools.getGrid()
   l[0][0].show(grid.screen, (255,0,0),1, True)

   lineThickness = menu(win, 180, 40, 4, 1, True, grid.width - 200, grid.height + 10)
   lineThickness.drawGrid()

   buttons = ['1', '2', '3', '4']
   lineThickness.setText(buttons)

   saveMenu = menu(win, 140, 40, 2, 1, True, grid.width - 400, grid.height + 25)
   saveMenu.drawGrid()

   buttons = ['Save', 'Open']
   saveMenu.setText(buttons)

   pygame.display.update()

#-----------------------------------------------------------------------#
    #TKINTER FORM FOR GETTING INPUT#
window = Tk()
window.title('Paint Program')

t_var = StringVar()
t_var.trace('w', updateLabel)

label = Label(window, text='# Of Rows and Columns (25,50): ')
rowsCols = Entry(window, textvariable=t_var)

label1 = Label(window, text="Pixel Size: 12.0, 12.0")
var = IntVar()
c = Checkbutton(window, text="View Grid", variable=var)
submit = Button(window, text='Submit', command=onsubmit)
window.bind('<Return>', onsubmit)

submit.grid(columnspan=1, row=3, column=1,pady=2)
c.grid(column=0, row=3)
label1.grid(row=2)
rowsCols.grid(row=0, column=1, pady=3, padx=8)
label.grid(row=0, pady=3)

window.update()
mainloop()

#------------------------------------------------------------------------#


#MAIN LOOP
initalize(cols, rows, var.get())
pygame.display.update()
color = (0,0,0) # Current drawing color
thickness = 1
replace = False
doFill = False
savedPath = '' #Current path of file

run = True
while run:
    #Main loop for mouse collision
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            window = Tk()
            window.withdraw()
            #Ask the user if they want to save before closing
            if pygame.display.get_caption()[0].count('*') > 0: 
               if messagebox.askyesno("Save Work?", "Would you like to save before closing?"):
                  # If they have already saved the file simply save to that path otherwise they need to chose a location
                  if savedPath != "":
                     save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
                  else:
                     path = showFileNav()
                     if path:
                        savedPath = path
                        save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
            run = False
         
        if pygame.mouse.get_pressed()[0]: #See if the user has clicked or dragged their mouse
            try:
                pos = pygame.mouse.get_pos()
                if pos[1] >= grid.height: # If the mouse is below the main drawing grid
                    if pos[0] >= tools.startx and pos[0] <= tools.startx + tools.width and pos[1] >= tools.starty and pos[1] <+ tools.starty + tools.height: #If the mouse ic clicking on the tools grid
                        replace = False
                        doFill = False
                        tools.drawGrid() #Redraw the grid so that we dont see the red highlight
                        buttons = ['D', 'E', 'F', 'R', 'C']
                        tools.setText(buttons)
                        
                        clicked = tools.clicked(pos)
                        clicked.show(grid.screen, (255,0,0), 1, True)

                        #Depending what tool they click
                        if clicked.text == 'D': #Draw tool  
                            color = (0,0,0)
                        elif clicked.text == 'E': #Erase tool
                            color = (255,255,255)
                        elif clicked.text == 'F':# Fill tool
                            doFill = True
                        elif clicked.text == 'R':# Replace tool
                            replace = True
                        elif clicked.text == 'C':# Clear grid tool
                            grid.clearGrid()
                            tools.drawGrid() #Redraw the grid so that we dont see the red highlight
                            buttons = ['D', 'E', 'F', 'R', 'C']
                            tools.setText(buttons)
                            l = tools.getGrid()
                            l[0][0].show(grid.screen, (255,0,0),1, True)
                            
                    #If they click on the color pallet
                    elif pos[0] >= pallet.startx and pos[0] <= pallet.startx + pallet.width and pos[1] >= pallet.starty and pos[1] <= pallet.starty + pallet.height:
                        clicked = pallet.clicked(pos)
                        color = clicked.getColor() # Set current drawing color

                        pallet = colorPallet(win, 90, 90, 3, 3, True, 10, grid.height + 2)
                        pallet.drawGrid()

                        colorList = [(0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,168,0), (244, 66, 173), (65, 244, 226)]
                        pallet.setColor(colorList)
                        clicked.show(grid.screen, (255,0,0), 3, True)
                        
                    elif pos[0] >= lineThickness.startx and pos[0] <= lineThickness.startx + lineThickness.width and pos[1] >= lineThickness.starty and pos[1] <= lineThickness.starty + lineThickness.height:
                        lineThickness.drawGrid() #Redraw the grid so that we dont see the red highlight
                        buttons = ['1', '2', '3', '4']
                        lineThickness.setText(buttons)
                        
                        clicked = lineThickness.clicked(pos)
                        clicked.show(grid.screen, (255,0,0), 1, True)

                        thickness = int(clicked.text) # set line thickness

                    #If they click on the save menu 
                    elif pos[0] >= saveMenu.startx and pos[0] <= saveMenu.startx + saveMenu.width and pos[1] >= saveMenu.starty and pos[1] <= saveMenu.starty + saveMenu.height:
                        clicked = saveMenu.clicked(pos)

                        if clicked.text == 'Save': # save if they click save
                            path = showFileNav()
                            if path:
                               savedPath = path
                               save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
                        else: #otherwise open
                            path = showFileNav(True)
                            if path:
                               openFile(path)
                               savedPath = path
                              #open file

                            
                else:
                    if replace: #If we have the replace tool selected then replace the color
                        tools.drawGrid() #Redraw the grid so that we dont see the red highlight
                        buttons = ['D', 'E', 'F', 'R', 'C']
                        tools.setText(buttons)
                        
                        tools.getGrid()[0][0].show(grid.screen, (255,0,0), 1, True)

                        clicked = grid.clicked(pos)
                        c = clicked.color
                        replace = False

                        for x in grid.getGrid():
                            for y in x:
                                if y.color == c:
                                    y.click(grid.screen, color)
                    elif doFill:
                       clicked = grid.clicked(pos)
                       if clicked.color != color:
                          fill(clicked, grid, color, clicked.color)
                          pygame.display.update()
                                    
                    else: #otherwise draw the pixels accoding to the line thickness
                        name = pygame.display.get_caption()[0]
                        if name.find("*") < 1:
                           changeCaption(name + '*')

                        clicked = grid.clicked(pos)
                        clicked.click(grid.screen,color)
                        if thickness == 2:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                        elif thickness == 3:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                                for p in pixel.neighbors:
                                    p.click(grid.screen, color)
                        elif thickness == 4:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                                for p in pixel.neighbors:
                                    p.click(grid.screen, color)
                                    for x in p.neighbors:
                                        x.click(grid.screen, color)
                                         
                pygame.display.update()
            except AttributeError:
                pass

pygame.quit()
