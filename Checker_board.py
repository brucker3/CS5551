w, h = 8, 8;
board= [[0 for x in range(w)] for y in range(h)] #8*8 array

def initboard(): # This function will mark the each tile of the bord  with '-' or '*'
                 # '-'  means light tile and '*' means dark tile 
    
    y = 0

    while y < 8 :

        x = 0

        while x < 8 :

            if ((x + y) % 2) == 0: #even 

                board[x][y] = '' 

            else :

                board[x][y] = ''

            x +=1

        y +=1     
            

def printboard():            # This function will only  print the board (with without the players)

    y = 0
    while y < 8:

        x = 0

        while x < 8:

            print (board[y][x],end=" ")

            x +=1

        print("\n")    

        y +=1

    piece_select()

            



def update_board_cordinate_players():

    board[0][1] = 'b'
    board[0][3] = 'b'          #Black Pieces Cordinates 1st row
    board[0][5] = 'b'
    board[0][7] = 'b'

    board[1][0] = 'b'
    board[1][2] = 'b'                 #Black Pieces Cordinates 2nd row
    board[1][4] = 'b'
    board[1][6] = 'b'


    board[2][1] = 'b'
    board[2][3] = 'b'                    #Black Pieces Cordinates 3rd row
    board[2][5] = 'b'
    board[2][7] = 'b'

    board[3][0] = '-'
    board[3][2] = '-'
    board[3][4] = '-'                            #Free Row 4th row
    board[3][6] = '-'

    board[4][1] = '-'
    board[4][3] = '-'                            #Free Row 5th row 
    board[4][5] = '-'
    board[4][7] = '-'

    board[5][0] = 'r'
    board[5][2] = 'r'                 #Red Pieces Cordinates 6th row
    board[5][4] = 'r'
    board[5][6] = 'r'

    board[6][1] = 'r'
    board[6][3] = 'r'                        #Red Pieces Cordinates 7th row
    board[6][5] = 'r'
    board[6][7] = 'r'
    
    board[7][0] = 'r'
    board[7][2] = 'r'                             #Red Pieces Cordinates  8th row
    board[7][4] = 'r'
    board[7][6] = 'r'


    i = 0
    while i < 7:
        j = 0
        while j < 7:
            board[i][j] = '*'           # '*' illegal cordinates


            j += 2

        i += 2



    q = 1
    while q <= 7:
        j = 1
        while j <= 7:
            board[q][j] = '*'             # '*' illegal cordinates

            j += 2

        q += 2      

   
Rkx0 = []
Rkx = []  #red king blocks cordinates.
Rky0 = []
Rky = []


Bkx0 = []
Bkx = []  #Black king blocks cordinates.
Bky0 = []
Bky = []


def pname():
    pname1 = input("Enter 1st Player Name: ")

    pname2 = input("Enter 2nd Player Name: ")

    print ("\n")

def piece_select():
    

    x, y = [int(x) for x in input("select piece to move: ").split()] 

    a, b = [int(a) for a in input("select the new cordinates: ").split()]

    # Validate_selection(x, y)

    movement(x,y,a,b)

# def Validate_selection(x, y):
#     # validate the selection of piece and and the co-ordinate.



def movement(x,y,a,b):

    m = []                               # x, y = 2, 3
    m = board[a][b]                      # a, b = 4, 5
    board[a][b] = board[x][y]            # a, b = m (m = 4, 5)                                   
    board[x][y] = m                      # a, b  = x, y (a,b = 2, 3 )
                                         # x, y =  m ( x, y = 4, 5 )
    printboard()



pname()    
initboard()
update_board_cordinate_players()
printboard() 

 

