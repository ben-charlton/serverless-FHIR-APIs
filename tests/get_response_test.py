import unittest
import requests
import time
import ast
import json

TEST_AUTH = {"authorisation": "6d3fe021cbb84781bac92e159fcb4e43"}
TEST_1 = '604b216a72b44cbc9271e101f1110ade'
TEST_2 = 'ea829835c74141189a7805f21273c053'
TEST_3 = '8a04b0314789451eb47a3c1afdd46008'
TEST_4 = 'a1e0b56dbea342388152354a18813ed2'

class TestGetQuestionnaireResponse(unittest.TestCase):

    def test_successful_with_resource1(self):
        """
        Test that it works as promised with resource 1
        """
        print("---TESTING SUCCESSFUL GET 1 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + TEST_1
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/responses/test1.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_response = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_response, comparison))
        comparison_file.close()


    def test_successful_with_resource2(self):
        """
        Test that it works as promised with resource 2
        """
        print("---TESTING SUCCESSFUL GET 2 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + TEST_2
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/responses/test2.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_response = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_response, comparison))
        comparison_file.close()
    
    def test_successful_with_resource3(self):
        """
        Test that it works as promised with resource 3
        """
        print("---TESTING SUCCESSFUL GET 3 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + TEST_3
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/responses/test3.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_response = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_response, comparison))
        comparison_file.close()
    
    
    def test_successful_with_resource4(self):
        """
        Test that it works as promised with resource 4
        """
        print("---TESTING SUCCESSFUL GET 4 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + TEST_4
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/responses/test4.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_response = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_response, comparison))
        comparison_file.close()
    
        
    
    def test_successful_without_resource(self):
        """
        Test that it returns 204 when nothing found
        """
        print("---TESTING GET WITH NO RESOURCE FOUND ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + '77777777'
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 204)


    def test_without_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING WITHOUT AUTH---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + TEST_1
        r = requests.get(url=url)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: User not found")
        

    def test_invalid_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID AUTH---")
        start = time.time()
        AUTH = {"authorisation": "[1,2,3]"}
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + TEST_1
        r = requests.get(url=url, headers = AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: User not found")

    
    def compare_json(self, json1, json2):
        for attr, val in json.loads(json1).items():
            if ((attr in json.loads(json2).keys())):
                continue
            else:
                return False
        return True

if __name__ == '__main__':
    unittest.main()