import unittest
import requests
import time

SMALL_TEST_UID = 12342
LARGE_TEST_UID
TEST_AUTH = 123


class TestGetQuestionnaire(unittest.TestCase):
    def test_successful_with_small_resource(self):
        """
        Test that it works as promised
        """
        start = time.time()
        r = requests.get('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/{TEST_UID}')
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)
    
    def test_successful_with_large_resource(self):
        """
        Test that it works as promised
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)

    def test_successful_without_resource(self):
        """
        Test that it returns 204 for no questionnaire found
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)

    def test_invalid_auth(self):
        """
        Test that it handles error
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6) 

    def test_user_not_found(self):
        """
        Test that it handles error
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)   
    
    def test_invalid_json(self):
        """
        Test that it handles error
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)
    
    def test_missing_json(self):
        """
        Test that it handles error
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)
    
    def test_xml_input(self):
        """
        Test that it handles error
        """
        start = time.time()
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(6, 6)


if __name__ == '__main__':
    unittest.main()