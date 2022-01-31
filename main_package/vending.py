import pyfiglet
import time
from main_package.item import Item


class VendingMachine:
    """
       A class to represent a VendingMachine object.

       ...

        Attributes
        ----------
        inventory : dict
            dictionary of inventory menu - {item code: Item object}
        transaction_amount : float default=0
            cash being deposited into machine before change returned
        balance : float default=0
            amount of money in VendingMachine instance after purchases
        active : bool default=True
            Boolean flag set to True if customer is purchasing items
        selection : Item default=None
            active selected item chosen by user input

       Methods
       -------
        display()
            Prints the current VendingMachine instance inventory divided up by category

        purchase item()
            Creates the initial purchase loop that accepts and validates user input.
            Then calls payment method or re-calls purchase_item method to request new input.

        payment()
            Accepts string input for payment type, validates and calls corresponding method from response.

        cash()
            Accepts float input for cash amount.
            Prints change if amount > item price
            or
            Requests more if amount < item price until > or ==
            Adds item price paid to balance and decrements item stock

        credit()
            'Processes' credit card
            Adds item price paid to balance and decrements item stock

        is_active()
            Sets the active attribute by user input and either continues loop or ends application.

        * private static method
        _validate_numeric (category, msg)
            Validates user input as int for item_code or float for cash.

            Parameters
            ----------
            category : str
                item_code or pay to determine function call on input
            msg : str
                message passed along for user input directions

            Returns
            ----------
            int or float
                depending upon parameters passed

            Raises
            ------
            ValueError, IndexError, KeyError, TypeError
                If incorrect data type is passed in as input.
       """

    def __init__(self):
        """
        Constructs all the necessary attributes for the VendingMachine object.
        In this case - pre-built hardcoded Items.

        Parameters
        ----------
        None
        """
        self.beverages = [Item(*i) for i in [("Water", 1.00),
                                             ("Iced Coffee", 1.50),
                                             ("Iced Tea", 1.50),
                                             ("Root Beer", 1.75)]]
        self.candy = [Item(*i) for i in [("Snickers", 1.50),
                                         ("M&M's", 1.50),
                                         ("Sour Patch Kids", 2.00),
                                         ("Haribo Gummy Bears", 2.25)]]
        self.chips = [Item(*i) for i in [("Lay's Potato Chips", 1.50),
                                         ("Doritos", 1.50),
                                         ("Pretzels", 1.25),
                                         ("Sun Chips", 1.25)]]
        self.gum = [Item(*i) for i in [('Trident', 1.25),
                                       ('Hubba Bubba', 1.00),
                                       ('Orbit', 1.25),
                                       ('Big Red', .75)]]
        self.inventory = {n: item for n, item in enumerate(self.beverages +
                                                           self.candy +
                                                           self.chips +
                                                           self.gum)}

        self.transaction_amount = 0
        self.selection = None
        self._balance = 0
        self.active = True

    def display(self):
        """
        Prints the current VendingMachine instance inventory divided up by category and calls purchase_item method
        """
        # pretty print vending machine for some added flares
        print(pyfiglet.figlet_format("Vending Machine", width=50))

        # reset selection to none whenever display is called to cancel transaction
        self.selection = None

        # pretty print each item and corresponding item code to command line
        for n, item in self.inventory.items():

            if item == self.beverages[0]:
                print('\n*********** Beverages ***********')

            if item == self.candy[0]:
                print('\n*********** Candy ***********')

            if item == self.chips[0]:
                print('\n*********** Chips ***********')

            if item == self.gum[0]:
                print('\n*********** Gum ***********')

            print(f"[{n}] - {item}")

        # call purchase method to select item from display
        self.purchase_item()

    def purchase_item(self):
        """
        Creates the initial purchase loop that accepts and validates user input.

        Then calls payment method or re-calls purchase_item method to request new input.
        """
        # loop to run while user is purchasing items
        while self.active:

            # validates input as int within inventory keys
            valid_code = self._validate_numeric('item_code', 'Please enter an item code: ')

            if valid_code in self.inventory:
                self.selection = self.inventory[valid_code]

                # if selected item stock is below 1, restart the purchase process
                if self.selection.stock < 1:
                    print(f"Sorry! {self.selection.name} out of stock. Please select another item.")

                # print selection and call payment method
                else:
                    print(f'Selection: {self.selection}')
                    self.payment()

            # if entered code is not in inventory keys, restart the purchase process
            else:
                print('No such item available. Please select from menu.')
                self.purchase_item()

    def payment(self):
        """
        Accepts string input for payment type, validates and calls corresponding method from response.
        """

        # take input as string 'cash' or 'credit'
        payment_type = input('Select Payment Type (Cash or Credit): ').lower()

        # dictionary to store input types and return corresponding method
        pay_dict = {'cash': self.cash, 'credit': self.credit}

        # call method from dict specified by input or retry
        if payment_type in pay_dict:
            pay_dict[payment_type]()
        else:
            print('Please enter a valid payment option.')
            self.payment()

    def cash(self):
        """
        Accepts float input for cash amount.

        Prints change if amount > item price
        or
        Requests more if amount < item price until > or ==

        Adds price paid to balance and decrements item stock
        """

        # validate cash input as float
        self.transaction_amount = self._validate_numeric('pay', 'Please enter cash amount (example: 1.25): ')

        if self.transaction_amount:

            # if amount entered by user is less than item price we ask for more until > or =
            while self.transaction_amount < self.selection.price:
                remainder = self.selection.price - self.transaction_amount

                print(f'Total cash inserted: ${self.transaction_amount:.2f}')
                print(f'Amount due: ${remainder:.2f}')

                additional = self._validate_numeric('pay', f'Please enter remaining sum of ${remainder:.2f}: ')

                if additional is not None:
                    self.transaction_amount += additional

            # once amount entered is > or = price, add to balance, decrement item stock
            if self.transaction_amount >= self.selection.price:
                change = self.transaction_amount - self.selection.price

                print(f'Your change is: ${change:.2f}')
                print(f'Enjoy your {self.selection.name}!')

                self._balance += self.selection.price
                self.selection.stock -= 1

            # call is_active to continue purchase loop or end app
            self.is_active()

        else:
            self.cash()

    def credit(self):
        """
        'Processes' credit card
        Adds item price paid to balance and decrements item stock
        """

        # Fake process a credit card and pass time
        print("Please swipe credit card now.")
        time.sleep(.5)
        print('Processing', end='')

        for _ in range(4):
            time.sleep(1)
            print('.', end='')

        print(f'\nTransaction approved! Credit card charged ${self.selection.price:.2f}')

        # add price to balance and decrement stock
        self._balance += self.selection.price
        self.selection.stock -= 1

        print(f'Enjoy your {self.selection.name}!')
        self.is_active()

    def is_active(self):
        """
        Sets the active attribute by user input and either continues loop or ends application.
        """
        # user input to determine continuation of loop
        choice = input('Would you like to make any additional purchases? (Y/N) or "M" to view menu: ').lower()

        # if/else cases for continuation
        if choice not in ['n', 'no', 'y', 'yes', 'm']:
            print('Please limit your response to Yes or No (Y/N/M).')
            self.is_active()
        elif choice in ['n', 'no']:
            self.active = False
            print('\nThanks for your purchase(s). Goodbye.')
        elif choice == 'm':
            self.display()

    @staticmethod
    def _validate_numeric(category: str, msg: str) -> int or float:
        """
        Validates user input as int for item_code or float for cash.

        Parameters
        ----------
        category : str
            item_code or pay to determine function call on input
        msg : str
            message passed along for user input directions

        Returns
        ----------
        int or float
            depending upon parameters passed

        Raises
        ------
        ValueError, IndexError, KeyError, TypeError
            If incorrect data type is passed in as input.
        """

        var = input(msg)
        category_dict = {'item_code': int, 'pay': float}

        # check if input can be cast to int or float, if not request an input of that type and return to function
        try:
            var = category_dict[category](var)
            return var
        except (ValueError, IndexError, KeyError, TypeError):
            print(f'Please enter a {category_dict[category].__name__} type.')
