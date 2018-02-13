from moneyregister import MoneyRegister
from category import Category

class EntityFactory:
    def createMoneyRegister(self,args):
        return MoneyRegister(args)
    def createCategory(self):
        return Category()
