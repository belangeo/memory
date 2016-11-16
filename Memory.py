#!/usr/bin/env python
# encoding: utf-8
import os, random, wx, wx.lib.buttons as buttons

if "phoenix" in wx.version():
    from wx.adv import AboutDialogInfo, AboutBox
    wx.EmptyImage = wx.Image # EmptyImage has been removed in phoenix.
else:
    from wx import AboutDialogInfo, AboutBox
    

PATH = os.path.join(os.getcwd(), "images")

class MemoryFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u"Jeu de Mémoire")
        self.createMenuBar()
        self.createButtons()
        self.createLabelBox()
        self.createGameBox()
        self.layout()
        self.initGame()

    def createMenuBar(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, "Nouvelle Partie\tCtrl+N")
        self.Bind(wx.EVT_MENU, self.initGame, id=wx.ID_NEW)
        fileMenu.Append(wx.ID_EXIT, "Quitter\tCtrl+Q")
        self.Bind(wx.EVT_MENU, lambda x: self.Destroy(), id=wx.ID_EXIT)
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ABOUT, "About Memory")
        self.Bind(wx.EVT_MENU, self.onShowAbout, id=wx.ID_ABOUT)
        menubar.SetMenus([(fileMenu, "Fichier"), (helpMenu, "Help")])
        self.SetMenuBar(menubar)

    def createButton(self, id):
        button = buttons.GenBitmapToggleButton(self, id, self.back)
        button.Bind(wx.EVT_BUTTON, self.onToggleButton)
        return button

    def createButtons(self):
        self.back = wx.EmptyImage(64, 64).ConvertToBitmap()
        self.imgs = [f for f in os.listdir(PATH) if f.endswith(".png")] * 2
        self.togs = [self.createButton(id) for id in range(len(self.imgs))]

    def createLabelBox(self):
        self.labelbox = wx.BoxSizer(wx.HORIZONTAL)
        self.counted = wx.StaticText(self, -1, u"Coups joués:   0")
        self.elapsed = wx.StaticText(self, -1, u"| Temps écoulé: 00:00")
        self.labelbox.Add(self.counted, 0, wx.ALL, 7)
        self.labelbox.Add(self.elapsed, 0, wx.ALL, 7)

    def createGameBox(self):
        self.gamebox = wx.GridSizer(6, 6, 1, 1)
        self.gamebox.AddMany(self.togs)

    def layout(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.AddMany([self.labelbox, self.gamebox])
        self.SetSizerAndFit(box)
        self.CenterOnScreen()

    def initGame(self, evt=None):
        random.shuffle(self.imgs)
        for i, img in enumerate(self.imgs):
            bitmap = wx.Bitmap(os.path.join(PATH, img), wx.BITMAP_TYPE_PNG)
            self.togs[i].SetBitmapSelected(bitmap)
            self.togs[i].SetToggle(False)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.clicked = []
        self.found = self.time = self.trials = 0
        self.counted.SetLabel(u"Coups joués:   0")
        self.elapsed.SetLabel(u"| Temps écoulé: 00:00")

    def onToggleButton(self, evt):
        if not self.timer.IsRunning():
            self.timer.Start(1000)
        id = evt.GetId()
        if self.togs[id].GetToggle():
            self.clicked.append((id, self.imgs[id]))
            if len(self.clicked) == 2:
                if self.clicked[0][1] != self.clicked[1][1]:
                    wx.CallLater(1000, self.hide)
                    self.Disable()
                else:
                    self.clicked = []
                    self.found += 1
                    if self.found == len(self.imgs) / 2:
                        self.timer.Stop()
                self.trials += 1
                self.counted.SetLabel(u"Coups joués: %3d" % self.trials)
        else:
            self.togs[id].SetToggle(True)

    def hide(self):
        while self.clicked:
            self.togs[self.clicked.pop()[0]].SetToggle(False)
        self.Enable()

    def onTimer(self, evt):
        self.time += 1
        t = u"| Temps écoulé: %02d:%02d" % (self.time / 60, self.time % 60)
        self.elapsed.SetLabel(t)

    def onShowAbout(self, evt):
        info = AboutDialogInfo()
        info.SetVersion("1.0")
        info.SetName("Memory")
        info.SetDescription("A simple memory game written with WxPython.")
        info.SetCopyright(u"Olivier Bélanger (2016)")
        AboutBox(info)

if __name__ == "__main__":
    app = wx.App()
    frame = MemoryFrame()
    frame.Show()
    app.MainLoop()