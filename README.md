#Vending Machine

A standard vending machine CLI application. The app displays a menu of items
from which the user picks one associated code (key). 

Once an item is selected (and validated), payment is requested in the form of cash or card.

Once payment is received and added to the vending machine's balance, the item
is dispensed, it's inventory updated, and any change is returned. 

Finally, we ask the user if they'd like to continue with another purchase, if so, we re-run
the updated app again with our cached values, if not, we close our app.

###Outline:

    Objects:

        Item:
            name : str
            price : float
            stock : int (default=10)


         VendingMachine:
            __init__:
                instance attributes:
                    inventory : dict
                    transaction_amount : float
                    selection : Item
                    balance : float
                    active : bool

            display():
                displays all inventory and Item class details (code, name, price) for available items

            purchase_item():
                take input of code (validated)
                check if item in stock
                request payment method

            payment():
                take input of payment method
                call method of payment type entered

            cash():
                validate cash input
                register amount entered
                    if < selection price
                        recall method for additional money input
                    if >= selection price
                        item dispensed
                        return change if any
                        decrement item stock
                        add price to machine balance

            credit():
                credit card is 'processed'
                item dispensed
                decrement item stock
                add price to machine balance

            is_active():
                called after a purchase to continue or end operations
                sets active attribute bool flag
                    if TRUE - loop back to purchase method
                    if FALSE - end operations

            * private static method
            _validate_numeric (category: str, msg: str):
                takes in category(code or payment) and input message
                accepts input and casts to category type
                    loop through if unable to convert input