import tkinter as tk
import time
from datetime import date
import csv
import keyboard
import winsound
from os import path

class Main():
    inSession = False
    currentEntry = []
    currentFile = ''
    amountOfEntries = 0

    def __init__(self, standard_example= ''):

        self.example = standard_example

        self.window = tk.Tk()
        self.window.title("Capture Keystroke Data")
        self.window.geometry("500x200")

        self.exampleEntry = tk.Entry(self.window, text='template')
        self.exampleButton = tk.Button(self.window, text="Enter text to type", command=self.getExample)

        if standard_example == '':
            self.startButton = tk.Button(self.window, text='Start session',state=tk.DISABLED, command=self.switchSessionState)
            self.exampleText = tk.Label(self.window, text="")
            self.exampleEntry.pack()
            self.exampleButton.pack()
        else:
            self.startButton = tk.Button(self.window, text='Start session', command=self.switchSessionState)
            self.exampleText = tk.Label(self.window, text="typing: " + self.example)

        self.exampleText.pack()
        self.startButton.pack()

        self.instructionText = tk.Label(self.window, text='Press \'enter\' After each entry. Entries: {}'.format(self.amountOfEntries))
        self.instructionText.pack()

        self.progressText = tk.Label(self.window, text='')
        self.progressText.pack()

        self.typedText = tk.Label(self.window, text='')
        self.typedText.pack()

        self.writtenText = tk.Label(self.window, text='')
        self.writtenText.pack()

        self.window.mainloop()

    def getExample(self, set_to=''):
        self.example = self.exampleEntry.get()
        self.exampleText['text'] = "typing: " + self.example
        self.startButton['state'] = tk.NORMAL

    def switchSessionState(self):
        if not self.inSession:
            self.startButton['text'] = 'Stop session'
            self.inSession = True
            self.startSession()
        else:
            self.startButton['text'] = 'Start session'
            self.inSession = False
            self.exampleEntry['state'] = tk.NORMAL
            self.exampleButton['state'] = tk.NORMAL
            self.window.unbind("<KeyPress>")
            self.window.unbind("<KeyRelease>")
            self.window.unbind('<Return>')

    def startSession(self):
        self.exampleEntry['state'] = tk.DISABLED
        self.exampleButton['state'] = tk.DISABLED
        self.initFile()
        self.window.bind("<KeyPress>", self.keyDown)
        self.window.bind("<KeyRelease>", self.keyUp)
        self.window.bind('<Return>', self.evaluateEntry)
        self.window.bind('<Shift_L>', self.shiftKey)
        self.lettersLeft = self.example
        self.noMistake = True
        self.currentEntry = []
        self.waitingForRelease = False


    def shiftKey(self, e):
        self.currentEntry.append(('shift', e.time, 'down'))

    def keyDown(self, e):
        if e.char == '\n' or e.char=='':
            self.evaluateEntry()
        else:
            self.typedText['text'] = self.typedText['text'] + e.char
            self.currentEntry.append((e.char, e.time, 'down'))

    def keyUp(self, e):
        if e.char=='':
            self.currentEntry.append(('shift', e.time, 'up'))
        elif not e.char=='\r':
            self.currentEntry.append((e.char, e.time, 'up'))

    def addGoodEntryCount(self):
        self.amountOfEntries += 1
        self.instructionText['text'] = 'Press \'enter\' After each entry. {} Good Entries'.format(self.amountOfEntries)


    def evaluateEntry(self, e):
        '''
        self.progressText['text'] = "SUCCESFUL ENTRY"
        self.typedText['text'] = ''
        self.writeEntry()
        '''

        goodEntry = True
        leadingText = self.example
        for event in self.currentEntry:
            if event[2] == 'down' and event[0]!='shift':
                if leadingText == '' or event[0] != leadingText[0]:
                    print(self.currentEntry)
                    goodEntry = False
                else:
                    leadingText = leadingText[1::]

        if goodEntry:
            print('I get called')
            self.progressText['text'] = "SUCCESFUL ENTRY"
            self.progressText['fg'] = '#329932'
            self.addGoodEntryCount()
            self.changeTimes()
            self.writeEntry()
            self.typedText['text'] = ''
            winsound.Beep(440, 200)
        elif not goodEntry:
            self.progressText['text'] = "BAD ENTRY"
            self.progressText['fg'] = '#ff0000'
            self.typedText['text'] = ''
            self.currentEntry = []
            winsound.Beep(349, 200)

    def initFile(self):

        fp = self.example + "_" + str(date.today()) + ".csv"
        if not path.isfile(fp):
            with open(fp, 'w', encoding='utf8') as f:
                writer = csv.writer(f)

        self.currentFile = fp

    def changeTimes(self):
        firstTime = self.currentEntry[0][1]
        for i in range(len(self.currentEntry)):
            item =  self.currentEntry[i]
            self.currentEntry[i] = (item[0], item[1]-firstTime, item[2])

    def writeEntry(self):
        with open(self.currentFile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.currentEntry)

        self.currentEntry = []

if __name__ == "__main__":
    #main = Main(standard_example="Thanks 4 fish")
    main = Main()
