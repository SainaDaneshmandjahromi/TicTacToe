from collections import deque

board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
# board = [['X','O','X'],['O','O','X'],[' ',' ',' ']]
#board ra neshan midahad
def showBoard():
    print(board[0][0],' || ',board[0][1],' || ',board[0][2])
    print('- - - - - - - - -')
    print(board[1][0],' || ',board[1][1],' || ',board[1][2])
    print('- - - - - - - - -')
    print(board[2][0],' || ',board[2][1],' || ',board[2][2])
    print("=================")
    print (' ')

#agar winner bashad character winner ra return mikonad
def isWinner(newBoard):
    #agar 3 ta dar yek row yeki bashand
    for i in range(3):
        if(newBoard[i][0] == newBoard[i][1] and newBoard[i][1] == newBoard[i][2]):
            if(newBoard[i][0] == 'X' or newBoard[i][0] == 'O'):
                return newBoard[i][0]
    #agar 3 ta dar yek column yeki bashand
    for i in range(3):
        if (newBoard[0][i] == newBoard[1][i] and newBoard[1][i] == newBoard[2][i]):
            if(newBoard[0][i] == 'X' or newBoard[0][i] == 'O'):
                return newBoard[0][i]
    #agar 3 ta diagonally yeki bashand az chap b rast
    if(newBoard[0][0] == newBoard[1][1] and newBoard[1][1] == newBoard[2][2]):
        if(newBoard[0][0] == 'X' or newBoard[0][0] == 'O'):
            return newBoard[0][0]
    #agar 3 ta diagonally yeki bashand az rast b chap
    elif(newBoard[0][2] == newBoard[1][1] and  newBoard[1][1] == newBoard[2][0]):
        if(newBoard[0][2] == 'X' or newBoard[0][2] == 'O'):
            return newBoard[0][2]
    return

def numOfEmpty(newBoard): #yek list az khanehaie khali bar migardanad
    empty = []
    for i in range(3):
        for j in range(3):
            if(newBoard[i][j] != 'X' and newBoard[i][j] != 'O'):
                empty.append((i,j))

    return empty


def playerMove(currentPlayer): #player yek khane ra entekhab mikonad
    print("Choose a place 1 to 9 : ")
    x = int(input()) - 1
    while(board[x//3][x%3] == "X" or board[x//3][x%3] == "O"):
        print("This Place Is Filled, Please Choose Another Place.")
        x = int(input()) - 1
    board[x//3][x%3] = currentPlayer


def aiMove(currentPlayer):#ba tabe minimax harekate monaseb ra peyda mikonad
    if(currentPlayer == 'O'):
        myRoot = createNode(board,False,None)
    else:
        myRoot = createNode(board,True,None)
    answer = minimaxprune(myRoot,float('-inf'),float('inf'))
    moves = numOfEmpty(board)
    root = answer[1]
    value = answer[0] #value behtarin harekat
    cnt = 0
    for child in root.childs: #beine farzandan kodam yek behtain harekat ra darad
        cnt += 1
        if(value == child.value):
            break
    move = moves[cnt-1]
    board[move[0]][move[1]] = currentPlayer
    return

def createNode(newBoard,isMaximiznig,parent):
    if(isMaximiznig):
        newValue = float('-inf')
    else: #agar minimizer
        newValue = float('inf')
    #agar yeki borde bashad ya hmeie khaneha por bashad leaf ast
    if ((isWinner(newBoard) != None) or len(numOfEmpty(newBoard)) == 0):
        if (isWinner(newBoard) == 'X'):
            newValue = 10 #agar X borde bashad
        elif (isWinner(newBoard) == 'O'):
            newValue = -10 #agar O borde bashad
        else:
            newValue = 0 #agar bazi mosavi shavad
    return Node(newBoard,isMaximiznig,newValue,parent)

def minimaxprune(state,alpha,beta):
    #sharte payane recursive
    if(isWinner(state.board) == 'X'):
        return 10,0
    elif(isWinner(state.board) == 'O'):
        return -10,0
    elif(len(numOfEmpty(state.board)) == 0):
        return 0,0
    if(state.isMaximizing):
        maxEval = float('-inf')
        childs = createChild(state)
        for child in childs:
            eval = minimaxprune(child,alpha,beta)[0]
            maxEval = max(maxEval,eval)
            alpha = max(alpha,eval)
            if(beta <= alpha): #baghieie farzandan ra peimaiesh nemikonad
                break
        state.value = maxEval #bishtarin value farzandan ra dar parent migozarim
        return maxEval,state

    else:
        minEval = float('inf')
        childs = createChild(state)
        for child in childs:
            eval = minimaxprune(child,alpha,beta)[0]
            minEval = min(minEval, eval)
            beta = min(beta,eval)
            if(beta <= alpha):
                break
        state.value = minEval #min value farzandan ra dar parent migozarim
        return minEval,state





def createChild(parent): #hameie harekat haie momken az parent ra misazad
    Childs = []
    emptyPlaces = numOfEmpty(parent.board)
    for i in range(len(emptyPlaces)):
        newBoard  = []
        for j in range(3):
            newBoard.append(parent.board[j][:])
        if(parent.isMaximizing):
            newBoard[emptyPlaces[i][0]][emptyPlaces[i][1]] = 'X'
        else:
            newBoard[emptyPlaces[i][0]][emptyPlaces[i][1]] = 'O'
        newNode = createNode(newBoard,not parent.isMaximizing,parent)
        Childs.append(newNode)
    parent.childs = Childs
    return Childs

class Node:
    def __init__(self,board,isMaximizing,value,parent ):
        self.isMaximizing = isMaximizing
        self.board = board
        self.parent = parent
        self.value = value
        self.childs = []


def start():
    print("Do you want to play First ? (Y/N)")
    choice = input()
    if(choice == 'Y' or choice == 'y'):
        currentPlayer = 'X'
        aiPlayer = 'O'
        while (isWinner(board) != 'X' and isWinner(board) != 'O' and (len(numOfEmpty(board)) != 0)):
            playerMove(currentPlayer)
            print("Player : ")
            showBoard()
            if(checkState(currentPlayer) == 1):
                break;
            aiMove(aiPlayer)
            print("AI : ")
            showBoard()
            if(checkState(currentPlayer) == 1):
                break;

    else:
        currentPlayer = 'O'
        aiPlayer = 'X'
        while (isWinner(board) != 'X' and isWinner(board) != 'O' and (len(numOfEmpty(board)) != 0)):
            aiMove(aiPlayer)
            print("AI : ")
            showBoard()
            if(checkState(currentPlayer) == 1):
                break;
            playerMove(currentPlayer)
            print("Player : ")
            showBoard()
            if(checkState(currentPlayer) == 1):
                break;

#check mikonad k kac borde ya bazi b akhar recde ya na
def checkState(currentPlayer):
    if(currentPlayer == 'X'):
        if (isWinner(board) == 'X'):
            print("You Won The Game ")
        elif (isWinner(board) == 'O'):
            print("AI Won The Game ")
        elif(len(numOfEmpty(board)) == 0):
            print("No One Won The Game")
        else:
            return 0
    else:
        if (isWinner(board) == 'O'):
            print("You Won The Game ")
        elif (isWinner(board) == 'X'):
            print("AI Won The Game ")
        elif(len(numOfEmpty(board)) == 0):
            print("No One Won The Game")
        else:
            return 0
    return 1



start()
