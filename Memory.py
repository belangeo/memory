# encoding: utf-8
import wx, os, random
import wx.lib.buttons as buttons

PATH = os.path.join(os.getcwd(), "images")

class MemoryFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u"Jeu de Mémoire")
        self.pane = wx.Panel(self)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

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
        menubar.Append(fileMenu, "Fichier")
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ABOUT, "About Memory")
        self.Bind(wx.EVT_MENU, self.onShowAbout, id=wx.ID_ABOUT)
        menubar.Append(helpMenu, "Help")
        self.SetMenuBar(menubar)

    def createButton(self, id, img):
        bitmap = wx.Bitmap(os.path.join(PATH, img), wx.BITMAP_TYPE_PNG)
        button = buttons.GenBitmapToggleButton(self.pane, id, self.back)
        button.SetBitmapSelected(bitmap)
        button.Bind(wx.EVT_BUTTON, self.OnToggleButton)
        return button

    def createButtons(self):
        self.back = wx.EmptyImage(64, 64).ConvertToBitmap()
        self.imgs = [f for f in os.listdir(PATH) if f.endswith(".png")] * 2
        self.togs = [self.createButton(i,im) for i,im in enumerate(self.imgs)]

    def createLabelBox(self):
        self.labelbox = wx.BoxSizer(wx.HORIZONTAL)
        self.trialCount = wx.StaticText(self.pane, -1, u"Coups joués:   0")
        self.showTime = wx.StaticText(self.pane, -1, u"| Temps écoulé: 00:00")
        self.labelbox.Add(self.trialCount, 0, wx.LEFT | wx.TOP, 7)
        self.labelbox.Add(self.showTime, 0, wx.LEFT | wx.TOP, 7)

    def createGameBox(self):
        self.gamebox = wx.BoxSizer()
        self.grid = wx.GridSizer(6, 6, 1, 1)
        self.grid.AddMany(self.togs)
        self.gamebox.Add(self.grid, 0, wx.ALL, 5)

    def layout(self):
        box = wx.BoxSizer(wx.VERTICAL)
        box.AddMany([self.labelbox, self.gamebox])
        self.pane.SetSizerAndFit(box)
        self.SetClientSize(self.pane.GetSize())
        self.SetSizeHintsSz(self.GetSize(), self.GetSize())
        self.CenterOnScreen()
        self.Show()

    def initGame(self, evt=None):
        random.shuffle(self.imgs)
        for i, img in enumerate(self.imgs):
            bit = wx.Bitmap(os.path.join(PATH, img), wx.BITMAP_TYPE_PNG)
            self.togs[i].SetBitmapSelected(bit)
            self.togs[i].SetToggle(False)
        self.timer.Stop()
        self.clicked = []
        self.found = self.time = self.trials = 0
        self.trialCount.SetLabel(u"Coups joués:   0")
        self.showTime.SetLabel(u"| Temps écoulé: 00:00")

    def OnToggleButton(self, evt):
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
                self.trialCount.SetLabel(u"Coups joués: %3d" % self.trials)
        else:
            self.togs[id].SetToggle(True)

    def hide(self):
        while self.clicked:
            self.togs[self.clicked.pop()[0]].SetToggle(False)
        self.Enable()

    def OnTimer(self, evt):
        self.time += 1
        t = u"| Temps écoulé: %02d:%02d" % (self.time / 60, self.time % 60)
        self.showTime.SetLabel(t)

    def onShowAbout(self, evt):
        info = wx.AboutDialogInfo()
        info.SetVersion("0.0.1")
        info.SetName("Memory")
        info.SetDescription("A simple memory game written with wxpython.")
        info.SetCopyright(u"Olivier Bélanger (2016)")
        wx.AboutBox(info)

if __name__ == "__main__":
    app = wx.App()
    frame = MemoryFrame()
    app.MainLoop()