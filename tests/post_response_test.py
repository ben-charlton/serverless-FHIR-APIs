import unittest
import requests
import time
import ast
import json

TEST_AUTH = {"authorisation": "6d3fe021cbb84781bac92e159fcb4e43"}

class TestPostQuestionnaireResponse(unittest.TestCase):

    def test_successful_with_resource1(self):
        """
        Test that it works as promised with resource 1
        """
        print("---TESTING SUCCESSFUL WITH RESOURCE 1 ---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + uid
        retrieved_response = json.dumps((requests.get(url=url, headers = TEST_AUTH)).json(), indent=4)
        z = requests.delete(url=url, headers = TEST_AUTH)
        self.assertTrue(self.compare_json(retrieved_response, response))
        response_file.close()
        
    
    def test_successful_with_resource2(self):
        """
        Test that it works as promised with resource 2
        """
        print("---TESTING SUCCESSFUL WITH RESOURCE 2 ---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + uid
        retrieved_response = json.dumps((requests.get(url=url, headers = TEST_AUTH)).json(), indent=4)
        z = requests.delete(url=url, headers = TEST_AUTH)
        self.assertTrue(self.compare_json(retrieved_response, response))
        response_file.close()
    
    def test_successful_with_resource3(self):
        """
        Test that it works as promised with resource 3
        """
        print("---TESTING SUCCESSFUL WITH RESOURCE 3 ---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + uid
        retrieved_response = json.dumps((requests.get(url=url, headers = TEST_AUTH)).json(), indent=4)
        z = requests.delete(url=url, headers = TEST_AUTH)
        self.assertTrue(self.compare_json(retrieved_response, response))
        response_file.close()
    
    def test_successful_with_resource4(self):
        """
        Test that it works as promised with resource 4
        """
        print("---TESTING SUCCESSFUL WITH RESOURCE 4 ---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.text, str)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + uid
        retrieved_response = json.dumps((requests.get(url=url, headers = TEST_AUTH)).json(), indent=4)
        z = requests.delete(url=url, headers = TEST_AUTH)
        self.assertTrue(self.compare_json(retrieved_response, response))
        response_file.close()

    def test_successful_without_resource(self):
        """
        Test that it returns 400 for no response found
        """
        print("---TESTING NO RESOURCE ---")
        start = time.time()
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Invalid JSON supplied")


    def test_without_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING WITHOUT AUTH---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertIsInstance(r.text, str)
        response_file.close()
    
    def test_invalid_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID AUTH---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        AUTH = {"authorisation": "[1,2,3]"}
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertIsInstance(r.text, str)
        response_file.close()

    def test_user_not_found(self):
        """
        Test that it handles error
        """
        print("---TESTING USER NOT FOUND---")
        start = time.time()
        response_file = open('json/responses/test1.json', 'rb')
        response = response_file.read().decode("utf-8") 
        AUTH = {"authorisation": "12234567"}
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: User not found")
        response_file.close()
    
    def test_invalid_json(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID RESOURCE ---")
        start = time.time()
        response_file = open('json/responses/bad.json', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: JSON object must be a QuestionnaireResponse resource")
        response_file.close()
    
    def test_xml_input(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID RESOURCE ---")
        start = time.time()
        response_file = open('json/responses/xml.xml', 'rb')
        response = response_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse', headers = TEST_AUTH, data=response)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Invalid JSON supplied")
        response_file.close()

    def compare_json(self, json1, json2):
        try:
            for attr, val in json.loads(json1).items():
                if ((attr in json.loads(json2).keys())):# and (val in ast.literal_eval(json2).values())):
                    continue
                else:
                    return False
        except Exception as e:
            print("EXCEPTION:" + str(e))
        return True

if __name__ == '__main__':
    unittest.main()