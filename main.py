from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
from gachaGame import Game
from time import sleep
import random as rd

gm = Game()


class NamefromPicture(Screen):
    switch = True

    def starUp(self):
        self.nextSign()
        self.ids.right.color = "#FFFFFF"
        self.ids.wrong.color = "#FFFFFF"
        self.ids.right.text = "next"
        self.ids.wrong.text = "next"
        self.switch = not self.switch
        self.parent.parent.parent.ids.coins.text = gm.getPlayerStatsStr()

    def PickAction(self, answ):
        if self.switch:
            self.nextSign()
            gm.guessReward(answ, 1)
            self.ids.right.color = "#FFFFFF"
            self.ids.wrong.color = "#FFFFFF"
            self.ids.right.text = "next"
            self.ids.wrong.text = "next"
        else:
            self.showAnswer()
            self.ids.right.color = "#00FF00"
            self.ids.wrong.color = "#FF0000"
            self.ids.right.text = "right"
            self.ids.wrong.text = "wrong"
        self.switch = not self.switch
        self.parent.parent.parent.ids.coins.text = gm.getPlayerStatsStr()

    def nextSign(self):
        gm.getBehaviorForNameGuesser()
        self.ids.behavImg.source = "imgs/" + gm.nameGuesserData[2]
        self.ids.behavName.text = "whats it called?"
        if self.ids.behavImg._coreimage == None:
            self.nextSign()

    def showAnswer(self):
        self.ids.behavName.text = f"{gm.nameGuesserData[1]}: {gm.nameGuesserData[0]}"


class GestureFromName(Screen):
    gestNames = {0: "open", 1: "closed", 2: "unsure", 3: "aggr"}

    def nextSign(self):
        gm.getDataForGestureGuesser()
        self.ids.behavImg.source = "imgs/" + gm.GestureGuesserData["general"][2]
        self.ids.behavName.text = f"{gm.GestureGuesserData['general'][1]}: {gm.GestureGuesserData['general'][0]}\n"
        self.parent.parent.parent.ids.coins.text = gm.getPlayerStatsStr()

    def buttonPress(self, gesture):
        res = gm.CalcGesture(gesture)
        if res[0]:
            gid = gm.gids.copy()
            self.nextSign()
            if res[1]:
                self.ids.behavName.color = "#00FF00"
            else:
                self.ids.behavName.color = "#FF0000"

            for i in gid:
                self.ids.behavName.text += f"{self.gestNames[i]}, "
            self.resetColorButtons()

        else:
            self.ids[self.gestNames[gesture]].background_color = get_color_from_hex("#00FF00")

    def resetColorButtons(self):
        for i in range(4):
            self.ids[self.gestNames[i]].background_color = get_color_from_hex("#909399")

class ReadDescription(Screen):
    def nextSign(self):
        gm.getDescriptionReadData()
        self.ids.behaveDesc.text = f"{gm.descriptionReadData[1]}:" \
                                   f" {gm.descriptionReadData[0]}\n\n{gm.descriptionReadData[3]} "
        self.ids.behavImg.source = "imgs/" + gm.descriptionReadData[2]
        self.parent.parent.parent.ids.coins.text = gm.getPlayerStatsStr()
    def buttonPress(self):
        gm.guessReward(4,3)
        self.nextSign()


class RollGacha(Screen):
    def roll(self):
        if gm.enoughCoins():
            gacha = gm.gachaRoll()
            self.ids.rollGacha.source = gacha[0]
            sleep(1)

            if gacha[1]:
                self.ids.statsRoll.color = "#FF0000"
            else:
                self.ids.statsRoll.color = "#0000FF"
            self.ids.statsRoll.text = f"You rolled a {gacha[2]} Star!"
            self.parent.parent.parent.ids.coins.text = gm.getPlayerStatsStr()
            with self.ids.rollGacha.canvas.before:
                Color(rgb=get_color_from_hex(gm.rarityColors[gacha[2]]))
                Rectangle(size=(self.ids.rollGacha.width + 2, self.ids.rollGacha.height + 2),
                          pos=(self.ids.rollGacha.x + 1, self.ids.rollGacha.y + 1))
        else:
            self.ids.statsRoll.text = f"You need {gm.SingleRollPrice - gm.getCoins()} more coins :( Go Grind some more"


class AppScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Main(BoxLayout):
    pass


kv = Builder.load_file('app.kv')


class MainApp(App):
    gm.resetDay()

    def build(self):
        return Main()


if __name__ == '__main__':
    MainApp().run()
