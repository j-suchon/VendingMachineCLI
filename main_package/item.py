class Item:
    """
    A class to represent an Item object

    ...

    Attributes
    ----------
    name : str
        name of item
    price : float
        price of item
    stock : int
        number of item in stock

    Methods
    -------
    __str__()
        custom string print of item and listed price for use in VendingMachine class
    """

    def __init__(self, name: str, price: float, stock: int = 10) -> None:
        """
        Constructs all the necessary attributes for the Item object.

        Parameters
        ----------
            name : str
                name of item
            price : float
                price of item
            stock : int
                number of item in stock
        """
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"Item(name={self.name}, price={self.price}, stock={self.stock})"

    def __str__(self):
        return f"{self.name} ${self.price:.2f}"
