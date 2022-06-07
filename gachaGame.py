import httpx
from database import DataBase
import random as rd


class Game():
    def __init__(self):
        self.db = DataBase('app.db')
        self.coins = self.db.getCoinValue()
        self.nextID = 1
        self.rollOdds = [1, 2, 2, 3, 3, 3, 4, 5]
        self.expMulti = 137
        self.expVars = [1000,7,3]
        self.expNeeded = 0
        self.recalcExpNeeded()
        self.capTimes2 = {1: [False, 170], 2: [False, 170], 3: [False, 140]}
        self.capTimes4 = {1: [False, 90], 2: [False, 90], 3: [False, 80]}
        self.SingleRollPrice = 80
        self.listIDs = []
        self.gacha = {"picture": "cat", "mode":1}
        self.rarityColors = {1: "#696460", 2: "#592a0b", 3: "#257310", 4: "#1d46a3", 5: "#460fa6", 6: "#c98a0c"}

    def getRandomCat(self):
        url = "https://api.thecatapi.com/v1/images/search"
        r = httpx.get(url).json()
        return r[0]
    def getRandomDog(self):
        url = "https://dog.ceo/api/breeds/image/random"
        r = httpx.get(url).json()
        return r

    def gachaRoll(self):
        pick = rd.randint(0, len(self.rollOdds) - 1)
        stars = self.rollOdds[pick]
        if self.gacha["picture"] == "cat":
            w = self.getRandomCat()
            return [w['url'],False,stars]
        elif self.gacha["picture"] == "dog":
            w = self.getRandomDog()
            return [w['message'],False,stars]
    def recalcExpNeeded(self):
        x = self.db.getLevel()
        self.expNeeded = 0
        for i in range(3):
            print(x**i*self.expVars[i])
            self.expNeeded+=x**i*self.expVars[i]
    def getRandomID(self):
        if len(self.listIDs) == 0:
            self.listIDs = [*range(1, self.db.getMaxID() + 1)]
            rd.shuffle(self.listIDs)
        return self.listIDs.pop()

    def getBehaviorForNameGuesser(self):
        while True:
            self.nextID = self.getRandomID()
            self.nameGuesserData = self.db.getValuesForNameGuesser(self.nextID)
            if self.nameGuesserData:
                break

    def getDataForGestureGuesser(self):
        while True:
            self.nextID = self.getRandomID()
            self.gids = self.db.getGestures(self.nextID)
            if len(self.gids) != 0:
                self.gids = [x[0] for x in self.gids]
                break
        self.GestureGuesserData = {"general": self.db.getGeneralBehaviorData(self.nextID), "gestures": self.gids.copy()}

    def getDescriptionReadData(self):
        self.nextID = self.getRandomID()
        self.descriptionReadData = self.db.getGeneralBehaviorData(self.nextID)

    def CalcGesture(self, ans):
        self.GestureGuesserData["gestures"]
        if ans in self.GestureGuesserData["gestures"]:
            self.GestureGuesserData["gestures"].remove(ans)
            if len(self.GestureGuesserData["gestures"]) == 0:
                self.guessReward(1, 2)
                return [True, True]
            else:
                return [False, True]
        else:
            self.guessReward(0, 2)
            return [True, False]

    def resetDay(self):
        if not self.db.sameDay():
            self.db.updateDate()
            self.db.resetDailyCoins()
            self.db.resetBonusCoins()

    def addCoins(self, c, calc=0):
        self.db.addToCoins(c)
        if calc != 0:
            self.recalcCoinsAndBonus(c, calc)

    def recalcCoinsAndBonus(self, c, calc):
        dc = self.db.getDailyCoins(calc) + c
        self.db.updateDailyCoins(dc, calc)
        if dc >= self.capTimes2[calc][1] and not self.capTimes2[calc][0]:
            self.capTimes2[calc][0] = True
            self.capTimes4[calc][0] = True
            print("bonus1")
            self.db.updateBonus(1, calc)
        elif dc >= self.capTimes4[calc][1] and not self.capTimes4[calc][0]:
            self.capTimes4[calc][0] = True
            print("bonus2")
            self.db.updateBonus(2, calc)

    def enoughCoins(self):
        if self.getCoins() >= self.SingleRollPrice:
            self.addCoins(-self.SingleRollPrice)
            return True
        else:
            return False

    def guessReward(self, ans, calc):
        self.addCoins((1 + ans) * self.db.getBonus(calc), calc)

    def getCoins(self):
        return self.db.getCoinValue()



    def getPlayerStatsStr(self):
        stats = self.db.getStatusInfo()
        stri = f"""name: {stats['name']}
coins: {stats['coins']}
level: {stats['level']}
exp:{stats['exp']}/{self.expNeeded}
bonus: \n"""
        for k in stats["bonus"]:
            stri += f"-{k}: {stats['bonus'][k][0]} ({stats['bonus'][k][1]})\n"
        return stri

g = Game()
# for i in range(100):
#     print(g.getRandomID())
print(g.expNeeded)
