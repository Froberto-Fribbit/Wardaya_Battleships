import time
import curses
from curses import wrapper

a = [["."] * 10 for _ in range(10)]
b = [["."] * 10 for _ in range(10)]
ta = [["."] * 10 for _ in range(10)]
tb = [["."] * 10 for _ in range(10)]

def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_CYAN)
    REED = curses.color_pair(1)
    BLU = curses.color_pair(2)
    global a, b, ta, tb
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.mousemask(curses.BUTTON1_CLICKED)

    def DrawBoard(y, x, id):
        global a, b, ta, tb
        if id == 1:
            for i in range(10):
                s = ""
                for j in range(10):
                    s += ta[i][j] + " "
                stdscr.addstr(y+i, x, s, REED)
        elif id == 2:
            for i in range(10):
                s = ""
                for j in range(10):
                    s += tb[i][j] + " "
                stdscr.addstr(y+i, x, s, BLU)
    
    logo = '''                                             .
                           .                 |
                           +                 |
                  .        |                *+W+-*
     .           +y        +W+              . H                 .
  .  +y            |I.   y  |               ! H= .           .  ^
  !   \     .     |H '. /   |  ___.        .! H  !   +--.--y !  V
  !    \     \  +=|H|=='.=+ | |====\   _  '_H_H__H_. H_/=  J !  !
. !     \'    VVV_HHH_/__'._H |  E  \_|=|_|========|_|==|____H. ! _______.
I-H_I=I=HH_==_|I_IIIII_I_I_=HH|======.I-I-I-=======-I=I=I=I_=H|=H'===I=I/
\                                                                      ,
 |                                                                    /
 .___________________________________________________________________' 
 '''
    stdscr.addstr(logo)
    title = '''
    
__________         __    __  .__           _________.__    .__              
\______   \_____ _/  |__/  |_|  |   ____  /   _____/|  |__ |__|_____  ______
 |    |  _/\__  \    __\   __\  | _/ __ \ \_____  \ |  |  \|  \____ \/  ___/
 |    |   \ / __ \|  |  |  | |  |_\  ___/ /        \|   Y  \  |  |_> >___ \ 
 |______  /(____  /__|  |__| |____/\___  >_______  /|___|  /__|   __/____  >
        \/      \/                     \/        \/      \/   |__|       \/ 
        
        
                           '''
    stdscr.addstr(title)
    time.sleep(1)
    stdscr.refresh()
    time.sleep(1)
    stdscr.addstr("Hit any key to start!", curses.A_BLINK)
    stdscr.getch()
    stdscr.clear()
    stdscr.refresh()
    time.sleep(3)
    s = "PHASE 1: FLEET ASSEMBLY"
    for i in range(len(s)):
        stdscr.addstr(s[0:i])
        stdscr.refresh()
        stdscr.clear()
        if i == 7:
            time.sleep(1.2)
        else:
            time.sleep(0.1)
    stdscr.addstr(s)
    stdscr.refresh()
    time.sleep(3)

    x = 0
    y = 0
    dir = 0

    DrawBoard(6, 2, 1)
    stdscr.refresh()
    Plac = curses.newwin(5, 70, 0, 0)
    Plac.addstr(0, 0, "PHASE 1: FLEET ASSEMBLY / PLAYER 1 - RED", REED)
    Plac.addstr(2, 0, "Use mouse to select starting position for your ship.", REED)
    Plac.addstr(3, 0, "Press 'r' to rotate ship. Press SPACE to confirm placement.", REED)
    Plac.refresh()

    #Ship Placement Loop 1
    for l in range(2, 6):
        while True:
            DrawBoard(6, 2, 1)
            stdscr.refresh()
            Plac.refresh()
            key = stdscr.getch()
            Plac.clear()
            Plac.addstr(0, 0, "PHASE 1: FLEET ASSEMBLY / PLAYER 1 - RED", REED)
            Plac.addstr(2, 0, "Use mouse to select starting position for your ship.", REED)
            Plac.addstr(3, 0, "Press 'r' to rotate ship. Press SPACE to confirm placement.", REED)
            Plac.refresh()
            if key == curses.KEY_MOUSE:
                try:
                    id, x, y, z, bstate = curses.getmouse()
                    if bstate & curses.BUTTON1_CLICKED:
                        RCrash = False
                        SCrash = False
                        if dir == 0:
                            if x//2 + l-1 <= 10 and y <= 15 and y >= 6 and (x//2) - 1 >= 0:
                                for i in range(l):
                                    if a[y-6][(x//2)+i-1] == "#":
                                        SCrash = True
                                        break
                                if not SCrash:
                                    ta = [row.copy() for row in a]
                                    for i in range(l):
                                        ta[y-6][(x//2)+i-1] = "#"
                                    DrawBoard(6, 2, 1)
                                    stdscr.refresh()
                            else:
                                RCrash = True
                            if RCrash: Plac.addstr(4, 0, "Out of bounds!! Choose another position.", REED)
                            elif SCrash: Plac.addstr(4, 0, "Ship collision!! Choose another position.", REED)
                        elif dir == 1:
                            if y + l <= 16 and x >= 2 and y >= 6 and x <= 20:
                                for i in range(l):
                                    if a[y-6+i][(x//2)-1] == "#":
                                        SCrash = True
                                        break
                                if not SCrash:
                                    ta = [row.copy() for row in a]
                                    for i in range(l):
                                        ta[y-6+i][(x//2)-1] = "#"
                                    DrawBoard(6, 2, 1)
                                    stdscr.refresh()
                            else:
                                RCrash = True
                            if RCrash: Plac.addstr(4, 0, "Out of bounds!! Choose another position.", REED)
                            elif SCrash: Plac.addstr(4, 0, "Ship collision!! Choose another position.", REED)
                except curses.error:
                    Plac.addstr(4, 0, "Don't mess with the code!! ERR:getmouse. Choose another position.", REED)
            elif key == ord('r'):
                dir = 1 - dir
            elif key == ord(' '):
                blank = True
                for i in range(10):
                    for j in range(10):
                        if a[i][j] != ta[i][j]:
                            blank = False
                            break
                    if not blank:
                        break
                if not blank:
                    a = [row.copy() for row in ta]
                    break
            
    Plac.addstr(0, 0, "PHASE 1: FLEET ASSEMBLY / PLAYER 2 - BLUE", BLU)
    Plac.addstr(2, 0, "Use mouse to select starting position for your ship.", BLU)
    Plac.addstr(3, 0, "Press 'r' to rotate ship. Press SPACE to confirm placement.", BLU)
    Plac.refresh()
    #Ship Placement Loop 2
    for l in range(2, 6):
        while True:
            DrawBoard(6, 2, 2)
            stdscr.refresh()
            Plac.refresh()
            key = stdscr.getch()
            Plac.clear()
            Plac.addstr(0, 0, "PHASE 1: FLEET ASSEMBLY / PLAYER 2 - BLUE", BLU)
            Plac.addstr(2, 0, "Use mouse to select starting position for your ship.", BLU)
            Plac.addstr(3, 0, "Press 'r' to rotate ship. Press SPACE to confirm placement.", BLU)
            Plac.refresh()
            if key == curses.KEY_MOUSE:
                try:
                    id, x, y, z, bstate = curses.getmouse()
                    if bstate & curses.BUTTON1_CLICKED:
                        RCrash = False
                        SCrash = False
                        if dir == 0:
                            if x//2 + l-1 <= 10 and y <= 15 and y >= 6 and (x//2) - 1 >= 0:
                                for i in range(l):
                                    if b[y-6][(x//2)+i-1] == "#":
                                        SCrash = True
                                        break
                                if not SCrash:
                                    tb = [row.copy() for row in b]
                                    for i in range(l):
                                        tb[y-6][(x//2)+i-1] = "#"
                                    DrawBoard(6, 2, 2)
                                    stdscr.refresh()
                            else:
                                RCrash = True
                            if RCrash: Plac.addstr(4, 0, "Out of bounds!! Choose another position.", BLU)
                            elif SCrash: Plac.addstr(4, 0, "Ship collision!! Choose another position.", BLU)
                        elif dir == 1:
                            if y + l <= 16 and x >= 2 and y >= 6 and x <= 20:
                                for i in range(l):
                                    if b[y-6+i][(x//2)-1] == "#":
                                        SCrash = True
                                        break
                                if not SCrash:
                                    tb = [row.copy() for row in b]
                                    for i in range(l):
                                        tb[y-6+i][(x//2)-1] = "#"
                                    DrawBoard(6, 2, 2)
                                    stdscr.refresh()
                            else:
                                RCrash = True
                            if RCrash: Plac.addstr(4, 0, "Out of bounds!! Choose another position.", BLU)
                            elif SCrash: Plac.addstr(4, 0, "Ship collision!! Choose another position.", BLU)
                except curses.error:
                    Plac.addstr(4, 0, "Don't mess with the code!! ERR:getmouse. Choose another position.", BLU)
            elif key == ord('r'):
                dir = 1 - dir
            elif key == ord(' '):
                blank = True
                for i in range(10):
                    for j in range(10):
                        if b[i][j] != tb[i][j]:
                            blank = False
                            break
                    if not blank:
                        break
                if not blank:
                    b = [row.copy() for row in tb]
                    break

    Plac.clear()
    Plac.refresh()
    stdscr.clear()
    stdscr.refresh()
    time.sleep(2)
    s = "PHASE 2: TO BATTLE!!!"
    for i in range(len(s)):
        Plac.addstr(0, 0, s[0:i])
        Plac.refresh()
        Plac.clear()
        if i == 7:
            time.sleep(1.2)
        else:
            time.sleep(0.1)
    Plac.addstr(0, 0, s)
    Plac.refresh()
    time.sleep(2)

    asc = 0
    bsc = 0
    ta = [["."] * 10 for _ in range(10)]
    tb = [["."] * 10 for _ in range(10)]
    while asc < 14 and bsc < 14:
        Plac.clear()
        Plac.addstr(0, 0, "PHASE 2: TO BATTLE!!!", REED)
        Plac.addstr(1, 0, "Player 1's turn to attack!", REED)
        Plac.addstr(2, 0, "Click on the board to attack that position.", REED)
        Plac.refresh()
        DrawBoard(6, 2, 1)
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                try:
                    id, x, y, z, bstate = curses.getmouse()
                    if bstate & curses.BUTTON1_CLICKED:
                        tx = (x//2) - 1
                        ty = y - 6
                        if tx >= 0 and tx < 10 and ty >= 0 and ty < 10 and x%2 == 0:
                            if ta[ty][tx] == "X" or ta[ty][tx] == "O":
                                Plac.addstr(4, 0, "You have already attacked this position. Choose another.", REED)
                                Plac.refresh()
                            else:
                                if b[ty][tx] == "#":
                                    ta[ty][tx] = "X"
                                    asc += 1
                                    Plac.clear()
                                    Plac.addstr(0, 0, "PHASE 2: TO BATTLE!!!", REED)
                                    Plac.addstr(1, 0, "Player 1's turn to attack!", REED)
                                    Plac.addstr(2, 0, "Click on the board to attack that position.", REED)
                                    Plac.addstr(4, 0, "Hit!", REED)
                                    DrawBoard(6, 2, 1)
                                    stdscr.refresh()
                                    Plac.refresh()
                                    time.sleep(1)
                                else:
                                    ta[ty][tx] = "O"
                                    Plac.clear()
                                    Plac.addstr(0, 0, "PHASE 2: TO BATTLE!!!", REED)
                                    Plac.addstr(1, 0, "Player 1's turn to attack!", REED)
                                    Plac.addstr(2, 0, "Click on the board to attack that position.", REED)
                                    Plac.addstr(4, 0, "Miss!", REED)
                                    DrawBoard(6, 2, 1)
                                    stdscr.refresh()
                                    Plac.refresh()
                                    time.sleep(1)
                                break
                except curses.error:
                    pass
        if asc == 14:
            break
        Plac.clear()
        Plac.addstr(0, 0, "PHASE 2: TO BATTLE!!!", BLU)
        Plac.addstr(1, 0, "Player 2's turn to attack!", BLU)
        Plac.addstr(2, 0, "Click on the board to attack that position.", BLU)
        Plac.refresh()
        DrawBoard(6, 2, 2)
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                try:
                    id, x, y, z, bstate = curses.getmouse()
                    if bstate & curses.BUTTON1_CLICKED:
                        tx = (x//2) - 1
                        ty = y - 6
                        if tx >= 0 and tx < 10 and ty >= 0 and ty < 10 and x%2 == 0:
                            if tb[ty][tx] == "X" or tb[ty][tx] == "O":
                                Plac.addstr(4, 0, "You have already attacked this position. Choose another.", BLU)
                                Plac.refresh()
                            else:
                                if a[ty][tx] == "#":
                                    tb[ty][tx] = "X"
                                    bsc += 1
                                    Plac.clear()
                                    Plac.addstr(0, 0, "PHASE 2: TO BATTLE!!!", BLU)
                                    Plac.addstr(1, 0, "Player 2's turn to attack!", BLU)
                                    Plac.addstr(2, 0, "Click on the board to attack that position.", BLU)
                                    Plac.addstr(4, 0, "Hit!", BLU)
                                    DrawBoard(6, 2, 2)
                                    stdscr.refresh()
                                    Plac.refresh()
                                    time.sleep(1)
                                else:
                                    tb[ty][tx] = "O"
                                    Plac.clear()
                                    Plac.addstr(0, 0, "PHASE 2: TO BATTLE!!!", BLU)
                                    Plac.addstr(1, 0, "Player 2's turn to attack!", BLU)
                                    Plac.addstr(2, 0, "Click on the board to attack that position.", BLU)
                                    Plac.addstr(4, 0, "Miss!", BLU)
                                    DrawBoard(6, 2, 2)
                                    stdscr.refresh()
                                    Plac.refresh()
                                    time.sleep(1)
                                break
                except curses.error:
                    pass
    Plac.clear()
    Plac.refresh()
    del Plac
    stdscr.clear()
    stdscr.refresh()
    time.sleep(2)
    s = "Congratulations!"
    for i in range(len(s)):
        stdscr.addstr(s[0:i])
        stdscr.refresh()
        stdscr.clear()
        time.sleep(0.1)
    stdscr.addstr(s)
    stdscr.refresh()
    time.sleep(2)
    stdscr.clear()
    if asc == 14:
        title = '''
    
                                                                                
▄▄▄▄▄▄▄   ▄▄                             ▄▄▄▄   ▄▄▄▄  ▄▄▄  ▄▄▄▄                 
███▀▀███▄ ██                           ▄█████   ▀███  ███  ███▀ ▀▀              
███▄▄███▀ ██  ▀▀█▄ ██ ██ ▄█▀█▄ ████▄      ███    ███  ███  ███  ██  ████▄ ▄█▀▀▀ 
███▀▀▀▀   ██ ▄█▀██ ██▄██ ██▄█▀ ██ ▀▀      ███    ███▄▄███▄▄███  ██  ██ ██ ▀███▄ 
███       ██ ▀█▄██  ▀██▀ ▀█▄▄▄ ██         ███     ▀████▀████▀   ██▄ ██ ██ ▄▄▄█▀ 
                     ██                                                         
                   ▀▀▀                                                          
        
        
                           '''
        stdscr.addstr(title, REED)
    else:
        title = '''
    
                                                                                                                                                             
  ▄▄▄▄▄▄  ▄▄                             ▄▄▄▄      ▄▄▄                       
 █▀██▀▀▀█▄ ██                          ▄██████    █▀██  ██  ██▀▀             
   ██▄▄▄█▀ ██                   ▄      ▀█▄  ██      ██  ██  ██ ▀▀ ▄          
   ██▀▀▀   ██ ▄▀▀█▄ ██ ██ ▄█▀█▄ ████▄      ▄█▀      ██  ██  ██ ██ ████▄ ▄██▀█
 ▄ ██      ██ ▄█▀██ ██▄██ ██▄█▀ ██       ▄█▀        ██▄ ██▄ ██ ██ ██ ██ ▀███▄
 ▀██▀     ▄██▄▀█▄██▄▄▀██▀▄▀█▄▄▄▄█▀     ██████▄      ▀████▀███▀▄██▄██ ▀██▄▄██▀
                      ██                                                     
                    ▀▀▀                                                      
        
        
                           '''
        stdscr.addstr(title, BLU)
    time.sleep(2)
    stdscr.addstr("\n\nPress any key to exit.")
    stdscr.getch()

wrapper(main)