"""
6.177 Problem Set (IAP 2016)
Completed by Paul Gallagher (pgal@mit.edu)
"""

"""
*** Warm-up Exercises ***
"""

### 1. Numerical Operations

# Fill in the function below which takes in two positive integers
# and returns either ((a - b) to the power of b) OR ((a + b) modulo 10)
# depending on which formula produces a greater value.
#
# operate(10, 2)
# ==> 64
# operate(2, 3)
# ==> 5

def operate(a, b):
    val1 = (a-b) ** b
    val2 = (a+b) % 10
    if val1 > val2:
        return val1
    return val2



### 2. String and list operation

# Fill in the function below. It takes in a list of strings (of length >= 3)
# called myStrings and trims the strings to exclude the first and last
# character of each string. It then returns the list in reverse order
# with *only* the first alphabetical letter of each new string capitalized
# (not always the first character!).
# Do NOT modify the original passed-in list.
#
# myList = ['25maroon', 'ComBInE', 'apple', '0315']
# fix_strings(myList) 
# ==> ['31', 'Ppl', 'Ombin', '5Maroo']
# myList 
# ==> ['25maroon', 'ComBInE', 'apple', '0315']

def fix_strings(myStrings):
    myStrings1 = myStrings[:] #copy the list 
    ##
    #if len(myStrings1) == 0:
    #    return myStrings1
    new_list = [fix_string(str) for str in myStrings1[:]]
    new_list.reverse()
    return new_list
    #lastStr = myStrings1.pop()
    
    #lastStr = lastStr[1:-1]
    #firstChar = lastStr[0]
    #lastChar = lastStr[-1]
    #lastStr = firstChar.upper() + lastStr[1:-1].lower() + lastChar.upper()
    #sillyList = [lastStr]
    #return sillyList.extend(fix_strings(myStrings1))
    
    
def fix_string(str):
    str = str[1:-1]
    i = 0 
    
    for x in str:
        if x.isalpha():
            break
        i += 1
    
    if i < len(str):
        return str[:i].lower() + str[i].upper() + str[i+1:].lower()
    
    return str


### 3. Class instances and methods

# Using the Car class defined below as reference, 
# fill in the modify() method below so that it takes in a Car instance
# and changes the name of the instance to 'Python' and its color to 'Ruby'.
# Then, pass in parameters into the combineTrips() method
# so that it sums together all weighted trips (miles divided by
# miles per gallon) and stores the decimal value in self.__combination.
# Your function should return True if successful.
#
# class Car(object):
#  def __init__(self, name, color):
#      self.__name = name
#      self.__color = color
#      # This dict saves trips in the format (miles, miles_per_gallon).
#      self.__trips = {
#          "ski trip": (101, 28),
#          "groceries": (15, 18),
#          "leisure": (3, 9),
#          "apple store": (17, 22),
#          "airport": (93, 30),
#          "canada": (1337, 26),
#          "engine check": (0, 0)
#      }
#      self.__combination = None

#  def get_color(self):
#      return self.__color

#  def change_color(self, color):
#      self.__color = color

#  def get_name(self):
#      return self.__name

#  def new_name(self, name):
#      self.__name = name

#  def get_combination(self):
#      return self.__combination

#  def get_miles_per_gallon(self):
#      return self.__mpg

#  def combine_trips(self, reduce_function):
#      self.__combination = reduce_function(self.__trips)

# myCar = Car('Moriarty', 'Sherlock')
# modify(myCar)
# ==> True
# myCar.get_name()
# ==> 'Python'
# myCar.get_color()
# ==> 'Ruby'
# myCar.get_combination()
# ==> 60.07

def reduce_function(tripsDict):
    tripsList = tripsDict.values()
    
    tripsList.remove((0,0))
    
    gallonsList = map(lambda (x,y): float(x)/y, tripsList)
    
    return sum(gallonsList)

def modify(carInstance):
    carInstance.new_name("Python")
    carInstance.change_color("Ruby")
    carInstance.combine_trips(reduce_function)
    return True



# carInstance.combine_trips(reduce_function = computeGallons)
"""
***** Langton's Ant *****
"""

# Algorithm described at http://en.wikipedia.org/wiki/Langton%27s_ant

import pygame, sys
import tests as T

### Global Variables
WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return (rowNum)*height + 10 

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return (colNum)*width + 10

def update_text(screen, message, size = 10):
    """
    Used to display the text on the right-hand part of the screen.
    You don't need to code anything, but you may want to read and
    understand this part.
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = (size + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def new_game(size = 10):
    """
    Sets up all necessary components to start a new game
    of Langton's Ant.
    """
    pygame.init() # initialize all imported pygame modules

    window_size = [size * WIDTH + 200, size * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Langton's Ant") # caption sets title of Window 

    board = Board(size)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False)

def draw_grid(screen, size):
    
    for i in range(size + 1):
        #vertical lines
        pygame.draw.line(screen, red, (i*WIDTH + 10, 10), 
                                (i*WIDTH+10,10 + size*HEIGHT))
        #horizontal lines
        pygame.draw.line(screen, red, (10, i*HEIGHT + 10), 
                                (10 + size*WIDTH, i*HEIGHT + 10))
    pass

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen, board.size)
    board.theAnt.draw(screen) # draw ant Sprite
    pygame.display.flip() # update screen
    
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True

        if stop == False and pause == False: 
            board.squares.draw(screen) # draw Sprites (Squares)
            
            draw_grid(screen, board.size) # ** draw the grid **
            
            board.theAnt.draw(screen) # draw ant Sprite
        
            update_text(screen, "Move #" + str(moveCount), board.size)
            pygame.display.flip() # update screen
            clock.tick(10)

            #--- Do next move ---#

            # Step 1: Rotate class Ant(pygame.sprite.Sprite):
            s = board.rotate_ant_get_square() # rotate the ant and save it's current square **
            
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            
            draw_grid(screen, board.size) # draw the grid here **
            
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            # Step 2: Flip color of square:
            
            s.flip_color() # flip the color of the square here **
            
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            
            draw_grid(screen, board.size)# draw the grid here **
            
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() #update screen
            
            clock.tick(5)
            
            # Step 3: Move Ant
            board.ant.step_forward(board) # make the ant step forward here **
            
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            
            draw_grid(screen, board.size)# draw the grid here **

            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            moveCount += 1
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.color = color   

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect
        

    def flip_color(self):
        """
        Flips the color of the square (white -> black or 
        black -> white)
        """
        if self.color == black:
            self.color = white
        else:   
            self.color = black
        self.image.fill(self.color)
        
   
class Board:
    def __init__(self, size):

        self.size = size
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = {}
        
        #---Populate boardSquares with Squares---#
        for row in range(0,size):
            for col in range(0,size):
                s = Square(row,col,white)
                self.boardSquares[(col, row)] = s
                self.squares.add(s)
        
        #---Initialize the Ant---#
        self.ant = Ant(self, size/2, size/2)
                          
        #---Adds Ant to the "theAnt" Sprite List---#
        self.theAnt = pygame.sprite.RenderPlain()
        self.theAnt.add(self.ant)

    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        return self.boardSquares[(x,y)]

    def rotate_ant_get_square(self):
        """ 
        Rotate the ant, depending on the color of the square that it's on,
        and returns the square that the ant is currently on
        """
        s = self.ant.get_current_square()
        if s.color == white:
            self.ant.rotate_left()
        else: self.ant.rotate_right()
        return s

class Ant(pygame.sprite.Sprite):
    def __init__(self, board, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.set_pic()
        self.rect = self.image.get_rect()
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.rotation = (0, 1) # pointing up
        self.board = board
        
        
    def get_current_square(self):
        """
        Returns the square that the ant is currently on
        """
        return self.board.get_square(self.col,self.row)
        
    def rotate_left(self):
        """
        Rotates the ant 90 degrees counterclockwise
        """
        if self.rotation == (0,1):
            self.rotation = (-1,0)
        elif self.rotation == (-1,0):
            self.rotation = (0,-1)
        elif self.rotation == (0,-1):
            self.rotation = (1,0)
        else:
            self.rotation = (0,1)
        self.image = pygame.transform.rotate(self.image, 90)
    
    def rotate_right(self):
        for i in range(0,3):
            self.rotate_left()
    
    def step_forward(self, board):
        """
        Make the ant take a step forward in whatever direction it's currently pointing.
        Don't forget - row numbers increase from top to bottom and column numbers
        increase from left to right!
        """
        if self.rotation == (0,1):
            self.row = (self.row - 1) % board.size 
        elif self.rotation == (-1,0):
            self.col = (self.col - 1) % board.size
        elif self.rotation == (0,-1):
            self.row = (self.row + 1) % board.size
        else:
            self.col = (self.col + 1) % board.size
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
    
    def set_pic(self):
        """
        Sets the picture that represents our Ant.
        If you want to use a new picture, you'll need to change
        this method.
        """
        self.image = pygame.image.load("ant.png").convert_alpha()

if __name__ == "__main__":
    # Uncomment this line to test your warmup answers:
    #T.test_warmup()

    # Uncomment this line to test Part 2:
    #T.test_part_two()

    # Uncomment this line to test Part 3:
    #T.test_part_three()

    # Uncomment this line to call new_game when this file is run:
    new_game()
    
    pass
