from okane.entity.moneyregister import MoneyRegister
from okane.entity.category import Category
from okane.entity.account import Account


class EntityFactory:
    def createMoneyRegister(self,args):
        return MoneyRegister(args)
    def createCategory(self, name):
        return Category(name)
    def createAccount(self, name):
        return Account(name)

