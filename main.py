class Battleship(object):
    
    def __init__(self, body):
        self.body = body
    
    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i) # because 0,0 is the top left of the board, when we reduce the y coordinate, we're going closer to the top
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "E":
                el = (head[0] + i, head[1])
            elif direction == "W":
                el = (head[0] - i, head[1])
                
            body.append(el)
        return Battleship(body)

# b = BattleShip.build((1,1), 5, "S")
# b2 = BattleShip([(1,2), (1,3), (1,4), (1,5)])
#these two are the same object but different initalization

def render(board_width, board_height, shots):
    header = "+" + "-" * board_width + "+"
    print(header)
    
    #using a set is faster than a list of tuples b/c it's unique
    shot_sets = set(shots)
    #board height
    for y in range(board_height):
        row = []
        #board width
        for x in range(board_width):
            if (x,y) in shot_sets:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|" + "".join(row) + "|") 

    print(header)
    
def render_battleships(board_width, board_height, battleships):
    header = "+" + "-" * board_width + "+"
    print(header)
    
    #Construct empty board
    board = []
    for _ in range(board_width):
        board.append([None for _ in range(board_height)])
    
    #Add battleships to the board
    for b in battleships:
        for x, y in b.body:
            board[x][y] = "O"
        
    for y in range(board_height):
        row = []
        for x in range(board_width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")
        
    print(header)
    

if __name__ == '__main__':
    # render(10,10, [(3,1), (4,5), (8,1)])
    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]
    
    for battleship in battleships:
        print(battleship.body)
    
    render_battleships(10,10, battleships)
    
    exit(0)
    shots = []
    
    while True:
        inp = input("Where do you want to shoot?\n")
        #TODO: DEAL WITH INVALID INPUTS
        #assign first num to be x and second to y
        xstr, ystr = inp.split(",") 
        x = int(xstr)
        y = int(ystr)
        
        shots.append((x,y))
        render(10,10, shots)
