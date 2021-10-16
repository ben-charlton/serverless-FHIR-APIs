import unittest
import requests
import time

TEST_AUTH = {"auth": "6d3fe021cbb84781bac92e159fcb4e43"}

class TestPostQuestionnaire(unittest.TestCase):
    def test_successful_with_small_resource(self):
        """
        Test that it works as promised
        """
        start = time.time()
        questionnaire = open('json/small_json.json', 'rb').read()
        
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        print("Execution time: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = r.text
        retrieved_questionnaire = (requests.get('https://fhir-questionnaire-api.azurewebsites.net/api/{uid}', headers = TEST_AUTH)).json()
        self.assertEqual(data, retrieved_questionnaire )
        requests.delete('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/{uid}', headers = TEST_AUTH)

    
    # def test_successful_with_large_resource(self):
    #     """
    #     Test that it works as promised
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6)

    # def test_successful_without_resource(self):
    #     """
    #     Test that it returns 204 for no questionnaire found
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6)

    # def test_invalid_auth(self):
    #     """
    #     Test that it handles error
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6)

    # def test_user_not_found(self):
    #     """
    #     Test that it handles error
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6) 
    
    # def test_invalid_json(self):
    #     """
    #     Test that it handles error
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6)
    
    # def test_missing_json(self):
    #     """
    #     Test that it handles error
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6)
    
    # def test_xml_input(self):
    #     """
    #     Test that it handles error
    #     """
    #     start = time.time()
    #     r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire')
    #     print("Execution time: " + str(time.time() - start))
    #     self.assertEqual(6, 6)


if __name__ == '__main__':
    unittest.main()