import unittest

from sitools2.clients.sdo_client_medoc import media_search, media_get, media_get_selection, media_metadata_search,\
    metadata_info


class MyTestCase(unittest.TestCase):

    def test_media_search(self):
        try:
            # self.assertRaises(ValueError("Nothing to download"), sdo_client_medoc.media_get())

            media_search()
            self.fail("No exception raised")
        except ValueError:
            pass
        except AssertionError:
            self.fail("exception")

    def test_media_get(self):
        try:
            # self.assertRaises(ValueError("Nothing to download"), sdo_client_medoc.media_get())

            media_get()
            self.fail("No exception raised")
        except ValueError:
            pass
        except AssertionError:
            self.fail("exception")

    def test_media_get_selection(self):
        try:
            media_get_selection()
        except IOError:
            pass
        except ValueError:
            pass
        except AssertionError:
            self.fail("AssertionError")
        except Exception:
            pass

    def test_metadata_search(self):
        try:
            media_metadata_search()

        except ValueError:
            pass
        except AssertionError:
            self.fail("Exception")

    def test_metada_info(self):
        try:
            metadata_info()
        except AssertionError:
            self.fail("Exception")
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()
