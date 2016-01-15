
# -*- coding: utf-8 -*-
import wx
from Senti import Senti
import wx.stc

# works, uses the wxWidgets library

frameWidth = 400
frameHeight = 300

class MainFrame(wx.Frame):
    def __init__(self, parent):
        frame = wx.Frame.__init__(self, parent, id = wx.ID_ANY, title="Åsiktsutvärderare", style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
#        self.setSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
#        self.Layout()
        bkg = wx.Panel(frame)

        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputPanel = InputPanel(self)
        inputSizer.Add(self.inputPanel, proportion = 1, flag = wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border = 5)

        sentimentSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sentimentPanel = SentimentPanel(self)
        sentimentSizer.Add(self.sentimentPanel, proportion = 1, flag = wx.EXPAND|wx.BOTTOM|wx.RIGHT, border = 5)

        self.analyzeButton = AnalyzeButton(self)
        self.analyzeButton.Bind(wx.EVT_BUTTON, self.inputPanel.buttonClicked)
        

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(inputSizer, proportion = 0, flag = wx.EXPAND|wx.ALL)
        mainSizer.Add(self.analyzeButton, flag = wx.ALL|wx.CENTER, border = 5)
        mainSizer.Add(sentimentSizer, proportion = 0, flag = wx.EXPAND|wx.ALL)

        self.SetSizer(mainSizer)

        self.sentimentPanel.setInputPanel(self.inputPanel)
        self.inputPanel.setSentimentPanel(self.sentimentPanel)
        self.inputPanel.setButton(self.analyzeButton)

        self.sentimentAnalyzer = Senti()
        self.inputPanel.setAnalyzer(self.sentimentAnalyzer)

#        self.setAnalyzer(self)
        

class InputPanel(wx.TextCtrl):
    def __init__(self, parent):
        print "InputPanel"
        wx.TextCtrl.__init__(self, parent, id = wx.ID_ANY) #, size = wx.Size(400, 50))
        self.Layout()
#        self.parent = parent

    def setSentimentPanel(self, sentimentPanel):
        self.sentimentPanel = sentimentPanel

    def setAnalyzer(self, analyzer):
        self.SentiAnalyzer = analyzer

    def setButton(self, analyzeButton):
        self.analyzeButton = analyzeButton
#        self.SentiAnalyzer = Senti()
        self.Bind(wx.EVT_BUTTON, self.buttonClicked, self.analyzeButton)

    def buttonClicked(self, evt):
        text = self.GetValue()
#        SentiAnalyzer = Senti()
        sentiment = self.SentiAnalyzer.predictsentiment(text)
        print sentiment
        print "buttonClicked"
        if(sentiment == 0):
            self.sentimentPanel.SetBackgroundColour((0, 255, 0))
        if(sentiment == 1):
            self.sentimentPanel.SetBackgroundColour((255, 0, 0))
        self.sentimentPanel.writeText(self.GetValue())

        
#class SentimentPanel(wx.Static):
class SentimentPanel(wx.TextCtrl):
    def __init__(self, parent):
        print "SentimentPanel"
#        wx.StaticCtrl.__init__(self, parent)
        wx.TextCtrl.__init__(self, parent, id=wx.ID_ANY) #, size = wx.Size(400, 100))
        self.Layout()
#        self.parent = parent

    def setInputPanel(self, inputPanel):
        self.inputPanel = inputPanel

    def writeText(self, text):
        self.SetValue(text)

        
class AnalyzeButton(wx.Button):
    def __init__(self, parent):
        print "AnalyzeButton"
        wx.Button.__init__(self, parent, id = wx.ID_ANY, label = "analysera") #, size = wx.Size(50, 50), label = "chek")
#        self.Layout()


def main():
    app = wx.App()
    window = MainFrame(None)
    window.Show(True)
    app.MainLoop()
        
if __name__ == '__main__':
    main()
