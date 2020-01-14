import threading
import time
from ctypes import *

lock = threading.Lock()

STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    pass


COORD._fields_ = [("X", c_short), ("Y", c_short)]


def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)


def turing_machine(coordinate1, coordinate2, name):
    file = open(name, "r")
    numLines = 0
    with open(name, 'r') as line:
        for x in line:
            numLines += 1
    numLines = numLines - 2
    position_string = file.readline()
    position = int(position_string)
    tape = list(file.readline())
    tapeposition = []
    for x in range(len(tape)):
        tapeposition.append(" ")
    program = []
    for x in range(numLines):
        newLine = file.readline()
        if newLine.strip():
            program.append(newLine)

    i = 0
    state = []
    oldSym = []
    newSym = []
    dir = []
    newState = []

    for x in program:
        state.append(program[i].split(' ', 5)[0])
        oldSym.append(program[i].split(' ', 5)[1])
        newSym.append(program[i].split(' ', 5)[2])
        dir.append(program[i].split(' ', 5)[3])
        newState.append((program[i].split(' ', 5)[4]).split('\n')[0])
        i = i + 1

    currentState = "0"
    stepCounter = 0

    while currentState != "X":
        for x in range(len(state)):
            if tape[position] == oldSym[x] and currentState == state[x]:
                stepCounter += 1
                tape[position] = newSym[x]
                if dir[x] == "R":
                    position += 1
                else:
                    position -= 1
                currentState = newState[x]
                with lock:
                    str1 = ''.join(tape)
                    time.sleep(0.02)
                    tapeposition[position] = "^"
                    str2 = ''.join(tapeposition)
                    print_at(coordinate1-2, coordinate2, name)
                    print_at(coordinate1, coordinate2, str1)
                    print_at(coordinate1+1, coordinate2, str2)
                    print_at(coordinate1+2, coordinate2, "Steps: " + str(stepCounter))
                    tapeposition[position] = " "
                    del str1
                    del str2
                break
        if position == -1 or position > len(tape):
            break

print("Welcome to Turing Machine Simulator!")
print("© Simonas Riska")
howMany = input("How many files do you want to run? ")
number = int(howMany)
files = []
for x in range(number):
    whichOne = x + 1
    name = input("Enter " + str(whichOne) + " file name: ")
    files.append(name)
threads = []

coordinate1 = 3
coordinate2 = 0

for x in range(number):
    coordinate1 += 10
    t = threading.Thread(target=turing_machine, args=[coordinate1, coordinate2, files[x]])
    t.start()
    threads.append(t)
    time.sleep(0.2)

for thread in threads:
    thread.join()

input("")