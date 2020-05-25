"""Assignment 3: Classes and objects

You will implement a set of classes that model a restaurant menu.

Feel free to add data, methods, and constructors to these classes as
needed, what I provide here is just a skeleton which also describes
the API you need to implement. As long as the API is implemented I
don't care if you add things to the classes to support the API. Just
make sure you actually need what you add.

NOTE: `raise NotImplementedError()` is a standard way to mark methods
that still need to be implemented. Remove it along with the TODOs
when you have implemented the methods.

"""

class Menu(object):
    """A menu of available items and some associated information.

    This class must have 2 class attributes drink_tax and food_tax
    that are used for the tax amount on drink and food. The value
    should be 0.18 (18%) for drink, and 0.10 (10%) for food.

    """
    drink_tax = 0.18
    food_tax = 0.10

    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    
    def add_item(self, item):
        """Add an item to this menu and set it's menu attribute to this menu.

        Items should not be allowed to be added to more than one menu
        so check if the item is already in another menu.

        Return: True if the item was added, and False it was not (because it had already been assigned a menu).
        """
        assert hasattr(item, "menu")
        if item.menu is None:
            item.menu = self
            self._items.append(item)
            return True
        else:
            return False
        

    # TODO: Add a read-only property named items that returns a COPY
    # of the set of items in this menu
    @property
    def items(self):
        return self._items.copy()



class Order(object):
    """A list of items that will be purchased together.

    This provides properties that compute prices with tax and tip for
    the whole order.

    """
    def __init__(self):
        self.lst = []
    
    def add_item(self, item):
        """Add an item to this order.

        Items are required to all be part of one menu. You will need
        to check for this.

        Return True if the item was added, False otherwise (mainly if
        it was not part of the same menu as previous items).

        """
        if len(self.lst) == 0:
            self.lst.append(item)
        else:
            if item.menu is self.lst[0].menu:
                self.lst.append(item)
            else:
                return False
        return True
        
        

    def price_plus_tax(self):
        """A function that returns the sum of all the item prices
        including their tax.

        """
        total = 0
        total = sum([i.price_plus_tax() for i in self.lst])
        return total
    
    def price_plus_tax_and_tip(self, amount):
        """A method returns the sum of all the item prices with
        tax and a specified tip.

        amount is given as a proportion of the cost including tax.

        """
        return self.price_plus_tax() * (1 + amount)

    
class GroupOrder(Order):
    """An order than is made by a large ground and forces the tip to be at least
    20% (0.20).

    If a price with a tip less than 20% is requested return a price with a 20%
    tip instead.
    """
    
    # TODO: Override price_plus_tax_and_tip to force a tip of at least
    # 20% (0.20). Do not duplicate any code (incl. the implementation of
    # price_plus_tax_and_tip from Order)
    def price_plus_tax_and_tip(self, amount):
        return super().price_plus_tax_and_tip( amount if amount > 0.2 else 0.2)

    
class Item(object):
    """An item that can be bought.

    It has a name and a price attribute, and can compute its price with
    tax. This also has a menu property that stores the menu this has
    been added to.

    """
 

    def __init__(self, name, price):
        # TODO: Implement
        self.name = name
        self.price = price
        self._inMenu = None
    

    # TODO: Add a property (not just an attribute) called "menu" that
    # returns the menu this item is part of. It should only be
    # possible to set it once.
    @property
    def menu(self):
        return self._inMenu
    
    @menu.setter
    def menu(self, obj):
        if self._inMenu is None:
            self._inMenu = obj
        

    def price_plus_tax(self):
        """Return the price of this item with tax added.

        Make sure you could support additional Item types, other than
        what you have in this file (meaning isinstance checks will not
        work). Imagine that I might have a Dessert class that derives
        from Item in another file.

        """
        # TODO: Implement
        return self.price * (1 + self._applicable_tax())
        

    def _applicable_tax(self):
        """Return the amount of tax applicable to this item as a proportion
        (eg. 0.2 if the tax is 20%).
        """
        # This is an abstract method. It should not be implemented in
        # this class.
        raise NotImplementedError()


# DO NOT change the classes below. Your code in Item should work with
# these implementations or others in other files.
     
class Food(Item):
    """An Item subclass which uses the food tax rate."""
    def _applicable_tax(self):
        return self.menu.food_tax

class Drink(Item):
    """An Item subclass which uses the drink tax rate."""
    def _applicable_tax(self):
        return self.menu.drink_tax
