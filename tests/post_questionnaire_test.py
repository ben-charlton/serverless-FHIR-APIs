import unittest
import requests
import time
import ast
import json

TEST_AUTH = {"authorisation": "6d3fe021cbb84781bac92e159fcb4e43"}

class TestPostQuestionnaire(unittest.TestCase):

    def test_successful_with_small_resource(self):
        """
        Test that it works as promised with a small questionnaire
        """
        print("---TESTING SMALL RESOURCE ---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/small.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
        retrieved_questionnaire = str((requests.get(url=url, headers = TEST_AUTH)).json())
        z = requests.delete(url=url, headers = TEST_AUTH)
        self.assertTrue(self.compare_json(retrieved_questionnaire, questionnaire))
        questionnaire_file.close()
        
    
    def test_successful_with_large_resource(self):
        """
        Test that it works as promised with a large questionnaire
        """
        print("---TESTING LARGE RESOURCE ---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/large.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
        retrieved_questionnaire = str((requests.get(url=url, headers = TEST_AUTH)).json())
        z = requests.delete(url=url, headers = TEST_AUTH)
        self.assertTrue(self.compare_json(retrieved_questionnaire, questionnaire))
        questionnaire_file.close()

    def test_successful_without_resource(self):
        """
        Test that it returns 400 for no questionnaire found
        """
        print("---TESTING NO RESOURCE ---")
        start = time.time()
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Invalid JSON supplied")


    def test_without_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING WITHOUT AUTH---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/small.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertIsInstance(r.text, str)
        questionnaire_file.close()
    
    def test_invalid_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID AUTH---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/small.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        AUTH = {"authorisation": "[1,2,3]"}
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = AUTH, data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertIsInstance(r.text, str)
        questionnaire_file.close()

    def test_user_not_found(self):
        """
        Test that it handles error
        """
        print("---TESTING USER NOT FOUND---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/small.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        AUTH = {"authorisation": "12234567"}
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = AUTH, data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: User not found")
        questionnaire_file.close()
    
    def test_invalid_json(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID RESOURCE ---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/bad.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: JSON object must be a Questionnaire resource")
        questionnaire_file.close()
    
    def test_xml_input(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID RESOURCE ---")
        start = time.time()
        questionnaire_file = open('json/questionnaire/xml.xml', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Invalid JSON supplied")
        questionnaire_file.close()

    def compare_json(self, json1, json2):
        for attr, val in ast.literal_eval(json1).items():
            if ((attr in ast.literal_eval(json2).keys())):# and (val in ast.literal_eval(json2).values())):
                continue
            else:
                return False
        return True

if __name__ == '__main__':
    unittest.main()