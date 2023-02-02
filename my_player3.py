"""
Name: Fernando Torres
"""

import math
import sys
from host import GO

edges = {(0,1), (0,2), (0,3), (4,1), (4,2), (4,3), (1,0), (2,0), (3,0), (1,4), (2,4),(3,4)}
corners = {(0,0), (0,4), (4,0), (4,4)}

#taken from read.py
def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board

#taken from write.py
def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)

def readMove(path="moves.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()

        moveNum = int(lines[0])

    return moveNum

def writeMoves(moveNum, path="moves.txt"):
    with open(path, 'w') as f:
        f.write(str(moveNum))

def getPlacements(go, piece_type):
    possible_placement = []

    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check(i, j, piece_type, test_check = True):
                possible_placement.append((i,j))
    return possible_placement

def isTerminal(moveNum, depth):
    if(depth > 3 or moveNum > 24):
        return True
    else:
        return False

def libertyNum(place, go, piece_type, my_piece):
    num = 0

    allies = go.ally_dfs(place[0], place[1])

    for member in allies:
        neighbors = go.detect_neighbor(member[0], member[1])
        for piece in neighbors:
            if go.board[piece[0]][piece[1]] == 0:
                num = num + 10

    if(my_piece == piece_type):
        return num
    else:
        return -num

def scoreNum(place, go, piece_type, my_piece):
    score = 0
    if(my_piece == piece_type):
        score = score + go.score(piece_type)
    else:
        score = score + -go.score(piece_type)

    if place in edges or place in corners:
        score = score - 5

    return score

def getUtility(place, go, piece_type, my_piece):
    v = 0

    v = v + scoreNum(place, go, piece_type, my_piece) + libertyNum(place, go, piece_type, my_piece)

    return v

def minValue(place, alpha, beta, go, piece_type, opponent_type, depth, moveNum):

    score = getUtility(place, go, opponent_type, piece_type)

    if isTerminal(moveNum, depth):
        return score

    possible_placement = getPlacements(go,piece_type)

    for i in possible_placement:
        goCopy = go.copy_board()
        boardCopy = goCopy.board
        boardCopy[i[0]][i[1]] = piece_type
        goCopy.remove_died_pieces(opponent_type)
        goCopy.update_board(boardCopy)
        score = min(score, maxValue(i, alpha, beta, goCopy, piece_type, opponent_type, depth+1, moveNum+1))
        v = score

        if(v <= alpha):
            return v
        
        beta = min(beta, v)

    return score

def maxValue(place, alpha, beta, go, piece_type, opponent_type, depth, moveNum):
    score = getUtility(place, go, piece_type, piece_type)
    if isTerminal(moveNum, depth):
        return score

    possible_placement = getPlacements(go,opponent_type)

    for i in possible_placement:
        goCopy = go.copy_board()
        boardCopy = goCopy.board
        boardCopy[i[0]][i[1]] = opponent_type
        goCopy.remove_died_pieces(piece_type)
        goCopy.update_board(boardCopy)
        score = max(score, minValue(i, alpha, beta, goCopy, piece_type,opponent_type, depth+1, moveNum+1))
        v = score

        if(v >= beta):
            return v
        alpha = max(alpha,v)
    
    return score

def alphaBetaSearch(go, piece_type, opponent_type, depth):
    bestVal = -math.inf

    possible_placement = getPlacements(go, piece_type)

    moveNum = readMove() - 2

    if not possible_placement:
        return "PASS"

    action = possible_placement[0]

    for i in possible_placement:
        goCopy = go.copy_board()
        boardCopy = goCopy.board
        boardCopy[i[0]][i[1]] = piece_type
        goCopy.remove_died_pieces(opponent_type)
        goCopy.update_board(boardCopy)
        v = maxValue(i, -math.inf, math.inf, goCopy, piece_type, opponent_type, depth+1, moveNum)

        if(v > bestVal):
            bestVal = v
            action = i

    
    return action

def get_input(go, piece_type):

    if(board == start):
        writeMoves(piece_type + 2)
    elif(previous_board == start):
        writeMoves(piece_type+2)
    else:
        moveNum = readMove()
        writeMoves(moveNum+2)

    opponent_type = 3-piece_type

    if piece_type == 1 and go.board[2][2] == 0:
        return (2,2)
    
    return alphaBetaSearch(go, piece_type, opponent_type, 0)

N=5
start = [[0 for x in range(N)] for y in range(N)]
piece_type, previous_board, board = readInput(N)
go = GO(N)
go.set_board(piece_type, previous_board, board)
action = get_input(go, piece_type)
writeOutput(action)  