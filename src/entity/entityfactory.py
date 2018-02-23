from moneyregister import MoneyRegister
from category import Category
from account import Account

class EntityFactory:
    def createMoneyRegister(self,args):
        return MoneyRegister(args)
    def createCategory(self, name):
        return Category(name)
    def createAccount(self, name):
        return Account(name)

