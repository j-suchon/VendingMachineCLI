import unittest
import io
from main_package.vending import VendingMachine
from main_package.item import Item
from unittest.mock import patch


class VendingTest(unittest.TestCase):

    # testing the instance attributes
    def test_active(self):
        vm = VendingMachine()
        self.assertTrue(vm.active, True)

    def test_selection(self):
        vm = VendingMachine()
        self.assertIsNone(vm.selection)
        vm.selection = Item('TestItem', 100)
        self.assertEqual(vm.selection.price, 100)
        self.assertEqual(vm.selection.name, 'TestItem')

    def test_transaction_amount(self):
        vm = VendingMachine()
        self.assertEqual(vm.transaction_amount, 0)
        vm.transaction_amount += 20
        self.assertEqual(vm.transaction_amount, 20)

    def test_balance(self):
        vm = VendingMachine()
        self.assertEqual(vm._balance, 0)
        vm._balance += 20
        self.assertEqual(vm._balance, 20)

    # payment method testing ------------------------------------
    @patch('sys.stdin', io.StringIO('invalid'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_payment_invalid(self, stdout):
        expected_output = "Select Payment Type (Cash or Credit): Please enter a valid payment option.\n" \
                          "Select Payment Type (Cash or Credit): "
        with self.assertRaises(Exception):
            vm = VendingMachine()
            vm.payment()
        self.assertEqual(stdout.getvalue(), expected_output)

    @patch('sys.stdin', io.StringIO('cash'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_payment_cash(self, stdout):
        vm = VendingMachine()
        vm.cash = unittest.mock.MagicMock()
        vm.payment()
        expected_out = "Select Payment Type (Cash or Credit): "
        self.assertEqual(stdout.getvalue(), expected_out)
        self.assertTrue(vm.cash.called)

    @patch('sys.stdin', io.StringIO('credit'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_payment_credit(self, stdout):
        vm = VendingMachine()
        vm.credit = unittest.mock.MagicMock()
        vm.payment()
        expected_out = "Select Payment Type (Cash or Credit): "
        self.assertEqual(stdout.getvalue(), expected_out)
        self.assertTrue(vm.credit.called)

    # payment type method testing -------------------------------
    @patch('sys.stdin', io.StringIO('12'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cash(self, stdout):
        vm = VendingMachine()
        vm.is_active = unittest.mock.MagicMock()
        vm.selection = Item('Test Item', 5.00)
        vm.cash()
        expected_output = 'Please enter cash amount (example: 1.25): Your change is: $7.00\nEnjoy your Test Item!\n'
        self.assertEqual(stdout.getvalue(), expected_output)
        self.assertTrue(vm.is_active.called)

    @patch('sys.stdin', io.StringIO('m'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_credit(self, stdout):
        vm = VendingMachine()
        vm.is_active = unittest.mock.MagicMock()
        vm.selection = Item('Test Item', 5.00)
        vm.credit()
        expected_out = 'Please swipe credit card now.\nProcessing....\nTransaction approved! Credit card charged ' \
                       '$5.00\nEnjoy your Test Item!\n'
        self.assertEqual(stdout.getvalue(), expected_out)
        self.assertTrue(vm._balance, 5.00)
        self.assertTrue(vm.is_active.called)
        self.assertTrue(vm.selection.stock, 9)

    # is_active method testing -------------------------------
    @patch('sys.stdin', io.StringIO('yes'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_is_active_yes(self, stdout):
        exp = 'Would you like to make any additional purchases? (Y/N) or "M" to view menu: '
        vm = VendingMachine()
        vm.is_active()
        self.assertEqual(stdout.getvalue(), exp)
        self.assertTrue(vm.active, True)

    @patch('sys.stdin', io.StringIO('no'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_is_active_no(self, stdout):
        exp = 'Would you like to make any additional purchases? (Y/N) or "M" to view menu: \nThanks for your ' \
              'purchase(s). Goodbye.\n'
        vm = VendingMachine()
        vm.is_active()
        self.assertEqual(stdout.getvalue(), exp)
        self.assertFalse(vm.active, False)

    @patch('sys.stdin', io.StringIO('m'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_is_active_menu(self, stdout):
        exp = 'Would you like to make any additional purchases? (Y/N) or "M" to view menu: '
        vm = VendingMachine()
        vm.display = unittest.mock.MagicMock()
        vm.is_active()
        self.assertEqual(stdout.getvalue(), exp)
        self.assertTrue(vm.active, True)
        self.assertTrue(vm.display.called)

    # purchase_item method testing ------------------------------------
    @patch('sys.stdin', io.StringIO('31'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_purchase_item(self, stdout):
        expected_output = 'Please enter an item code: No such item available. Please select from menu.\nPlease enter ' \
                          'an item code: '
        with self.assertRaises(Exception):
            vm = VendingMachine()
            vm.payment = unittest.mock.MagicMock()
            vm.purchase_item()
        self.assertEqual(stdout.getvalue(), expected_output)
        self.assertFalse(vm.payment.called)

    # protected validation method testing -------------------------------
    @patch('sys.stdin', io.StringIO('8'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test__validate_numeric_pay(self, stdout):
        vm = VendingMachine()
        vm._validate_numeric('pay', 'Test line of data')
        self.assertEqual(stdout.getvalue(), 'Test line of data')

    @patch('sys.stdin', io.StringIO('7'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test__validate_numeric_code(self, stdout):
        vm = VendingMachine()
        vm._validate_numeric('item_code', 'Test line of data')
        self.assertEqual(stdout.getvalue(), 'Test line of data')

    @patch('sys.stdin', io.StringIO('Invalid'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test__validate_numeric_invalid_code(self, stdout):
        vm = VendingMachine()
        vm._validate_numeric('item_code', 'Test line of data')
        expected_output = 'Test line of dataPlease enter a int type.\n'
        self.assertRaises(ValueError)
        self.assertEqual(stdout.getvalue(), expected_output)

    @patch('sys.stdin', io.StringIO('Invalid'))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test__validate_numeric_invalid_pay(self, stdout):
        vm = VendingMachine()
        vm._validate_numeric('pay', 'Test line of data')
        expected_output = 'Test line of dataPlease enter a float type.\n'
        self.assertRaises(ValueError)
        self.assertEqual(stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
