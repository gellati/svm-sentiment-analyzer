
# -*- encoding: utf-8 -*-

from Tkinter import *
from Senti import Senti

# works, uses the Tk window library
# output window is green if sentiment is positive, red if negative
# modelled after SentiFrame.py

frameWidth=400
frameHeight=300

class MainFrame(Frame):
    def __init__(self, parent):
        frame = Frame(parent, width=frameWidth, height=frameHeight)
        frame.pack()

        self.inputArea = InputArea(frame)
        self.outputArea = OutputArea(frame)
        self.analyzeButton = AnalyzeButton(frame)
        
        self.sentimentAnalyzer = Senti()
        self.inputArea.setAnalyzer(self.sentimentAnalyzer)
        self.inputArea.setOutputArea(self.outputArea)
        self.inputArea.setButton(self.analyzeButton)
        self.quitbutton = Button(frame, text="Quit", command=frame.quit)
        
        self.inputArea.pack()
        self.analyzeButton.pack()
        self.outputArea.pack()
        self.quitbutton.pack()

class InputArea(Entry):
    def __init__(self, parent):
        print "inputarea"
        Entry.__init__(self, parent)
#        self.grid()

    def setOutputArea(self, outputArea):
        self.outputArea = outputArea

    def setAnalyzer(self, analyzer):
        self.sentimentAnalyzer = analyzer

    def setButton(self, analyzeButton):
        self.analyzeButton = analyzeButton
        self.analyzeButton.bind('<Button-1>', self.buttonClicked)

    def buttonClicked(self, evt):
        text = self.get()
        sentiment = self.sentimentAnalyzer.predictsentiment(text)
        print sentiment
        if(sentiment == 0):
            self.outputArea.configure(background='red')
        if(sentiment == 1):
            self.outputArea.configure(background='green')
        self.outputArea.writeText(self.get())
        
        

class OutputArea(Text):
    def __init__(self, parent):
        Text.__init__(self, parent)

    def clearText(self):
        self.delete("1.0", END)

    def writeText(self, text):
        print "writeText"
        self.clearText()
        self.insert("1.0", text)

        
class AnalyzeButton(Button):
    def __init__(self, parent):
        Button.__init__(self, parent, text="Get sentiment")
        
        
        
root = Tk()
mf = MainFrame(root)
root.mainloop()
root.destroy()


#if __name__ == '__main__':
#    root = Tk()
#    root.title("åsikt")
#    mf = MainFrame(root)
#    root.mainloop
    




