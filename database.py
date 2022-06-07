import sqlite3
from datetime import date


class DataBase():
    def __init__(self, database) -> None:
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute("PRAGMA foreign_keys = ON;")
        self.maxID = self.getMaxIDDB()
        self.getPlayerStats()

    def getPlayerStats(self):
        with self.conn:
            self.c.execute("select dailyCoins from dailyCoinsAndBonus where playerID=1")
            cnb = self.c.fetchall()
            self.c.execute("select name,level,exp,coins from playerStats where playerID=1")
            ps = self.c.fetchall()
        self.playerStats = {"player":ps,"coinsNbonus":cnb}

    def getMaxID(self):
        return self.maxID

    def getMaxIDDB(self):
        with self.conn:
            self.c.execute("SELECT max(bid) FROM signs")
        return int(self.c.fetchall()[0][0])

    def getsignsValues(self, bid):
        try:
            with self.conn:
                self.c.execute(
                    "select bName,bsymb,bImg,hasType.gid from signs,hasType where signs.bid = hasType.bid and signs.bid=:bid",
                    {"bid": bid})
            return self.c.fetchall()[0]
        except:
            return False

    def getValuesForNameGuesser(self, bid):
        try:
            with self.conn:
                self.c.execute("select bName,bsymb,bImg from signs where signs.bid=:bid and bImg!='noImg.png'",
                               {"bid": bid})
            return self.c.fetchall()[0]
        except:
            return False

    def getGestures(self, bid):
        with self.conn:
            self.c.execute("select gid from hasType where bid=:bid", {"bid": bid})
        return self.c.fetchall()

    def getGeneralBehaviorData(self, bid):
        with self.conn:
            self.c.execute("select bName,bsymb,bImg,bDescription from signs where signs.bid=:bid", {"bid": bid})
        return self.c.fetchall()[0]

    def getCoinValue(self):
        with self.conn:
            self.c.execute("select coins from playerStats where playerID=1")
        return int(self.c.fetchall()[0][0])

    def getDailyCoins(self, quizID):
        with self.conn:
            self.c.execute("select dailyCoins from dailyCoinsAndBonus where playerID=1 and quizID=:quizID",
                           {"quizID": quizID})
        return int(self.c.fetchall()[0][0])

    def updateDailyCoins(self, dailyCoins, quizID):
        with self.conn:
            self.c.execute("update dailyCoinsAndBonus set dailyCoins = :dailyCoins where playerID=1 and quizID=:quizID",
                           {"dailyCoins": dailyCoins, "quizID": quizID})

    def resetDailyCoins(self):
        with self.conn:
            self.c.execute("update dailyCoinsAndBonus set dailyCoins = 0 where playerID=1")

    def getExpValue(self):
        with self.conn:
            self.c.execute("select exp from playerStats where playerID=1")
        return int(self.c.fetchall()[0][0])

    def updateCoinValue(self, coins):
        with self.conn:
            self.c.execute("update playerStats set coins = :coins where playerID=1", {"coins": coins})

    def updateExpValue(self, exp):
        with self.conn:
            self.c.execute("update playerStats set exp = :exp where playerID=1", {"exp": exp})

    def addToCoins(self, num):
        coins = self.getCoinValue()
        coins += num
        self.updateCoinValue(coins)

    def addToExp(self, num,expCap):
        exp = self.getExpValue()
        exp += num
        levelUp = False
        if exp > expCap:
            exp -= expCap
            self.updateLevel(self.getLevel() + 1)
            levelUp = True
        self.updateExpValue(exp)
        return levelUp

    def getStatusInfo(self):
        with self.conn:
            self.c.execute("select name,level,exp,coins from playerStats where playerID=1")
            s = self.c.fetchall()[0]
            self.c.execute("select quizName,dailyBonus,dailyCoins from dailyCoinsAndBonus where playerID=1")
            f = self.c.fetchall()
            k = [x[0] for x in f]
            v = [[x[1],x[2]] for x in f]
            dic = dict(zip(k, v))
            stats = {"name": s[0], "level": s[1], "exp": s[2], "coins": s[3], "bonus": dic}
        return stats

    def getBonus(self, quizID):
        with self.conn:
            self.c.execute("select dailyBonus from dailyCoinsAndBonus where playerID=1 and quizID=:quizID",
                           {"quizID": quizID})
        return int(self.c.fetchall()[0][0])

    def updateBonus(self, dailyBonus, quizID):
        with self.conn:
            self.c.execute("update dailyCoinsAndBonus set dailyBonus = :dailyBonus where playerID=1 and quizID=:quizID",
                           {"dailyBonus": dailyBonus, "quizID": quizID})

    def resetBonusCoins(self):
        maxBonus = 4
        with self.conn:
            self.c.execute("update dailyCoinsAndBonus set dailyBonus = :maxBonus where playerID=1",
                           {"maxBonus": maxBonus})

    def getLevel(self):
        with self.conn:
            self.c.execute("select level from playerStats where playerID=1")
        return int(self.c.fetchall()[0][0])

    def updateLevel(self, level):
        with self.conn:
            self.c.execute("update playerStats set level = :level where playerID=1", {"level": level})

    def sameDay(self):
        with self.conn:
            self.c.execute("select date from playerStats where playerID=1")
        return self.c.fetchall()[0][0] == str(date.today())

    def updateDate(self):
        with self.conn:
            self.c.execute("update playerStats set date = :date where playerID=1", {"date": str(date.today())})


d = DataBase('app.db')
# for i in range(1,123):
#     print(d.getGeneralBehaviorData(i))
