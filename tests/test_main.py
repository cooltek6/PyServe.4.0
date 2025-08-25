import unittest

class TestMain(unittest.TestCase):
    pass
    # def test_print_form(self):
    #     from main import ServiceOrder
    #     custy_info = {
    #         'name': 'John Doe',
    #         'address': '123 Main St',
    #         'city': 'Anytown',
    #         'zipcode': '12345',
    #         'phone': '555-1234',
    #         'email': 'Don't look here'
    #     }
    #     form = ServiceOrder(custy_info)
    #     expected_output = """
    #     Service Order Form
    #     -------------------
    #     Customer Name: John Doe
    #     Address: 123 Main St
    #     City: Anytown
    #     Zipcode: 12345
    #     Phone: 555-1234
    #     Email: Don't look here
    #     -------------------
    #     Description of Work:
    #
    #     ______________________
    #
    #     Service Performed:
    #
    #
    #
    #
    #     ______________________
    #
    #     Parts Used:
    #
    #
    #
    #
    #     ______________________
    #
    #     Technician Notes: --- IGNORE ---
    #
    #     ______________________
    #     """
    #     self.assertEqual(form.print_form().strip(), expected_output.strip())
    
if __name__ == '__main__':
    import unittest
    unittest.main()
