import unittest
import requests
import time
import ast
import json

TEST_AUTH = {"authorisation": "6d3fe021cbb84781bac92e159fcb4e43"}
TEST_UID = "c992d584bf4e4e7a8aa4ca46ffe093f1"
TEST_SMALL = 'b56b7eec10c542b083dcc5f4e71d11d8'

TEST_1 = '974bf28525024f169687c679f2358b82'
TEST_2 = '667f25969f8d4edeaa4cc5a4be6384ca'
TEST_3 = '70a9fd3757224cb79bdce7ed170e048f'

class TestGetQuestionnaire(unittest.TestCase):

    def test_successful_with_large_resource(self):
        """
        Test that it works as promised with a small questionnaire
        """
        print("---TESTING SUCCESSFUL GET LARGE ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_UID
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/large.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()

    def test_successful_with_small_resource(self):
        """
        Test that it works as promised with a small questionnaire
        """
        print("---TESTING SUCCESSFUL GET SMALL ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_SMALL
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/small.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()

    def test_successful_with_resource1(self):
        """
        Test that it works as promised with resource 1
        """
        print("---TESTING SUCCESSFUL GET 1 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_1
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/test1.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()
    
    def test_successful_with_resource2(self):
        """
        Test that it works as promised with resource 2
        """
        print("---TESTING SUCCESSFUL GET 2 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_2
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/test2.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()
    
    
    def test_successful_with_resource3(self):
        """
        Test that it works as promised with resource 3
        """
        print("---TESTING SUCCESSFUL GET 3 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_3
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/test3.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()
    
        
    
    def test_successful_without_resource(self):
        """
        Test that it returns 204 when nothing found
        """
        print("---TESTING GET WITH NO RESOURCE FOUND ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + '77777777'
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 204)


    def test_without_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING WITHOUT AUTH---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_SMALL
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
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_SMALL
        r = requests.get(url=url, headers = AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: User not found")

    
    def compare_json(self, json1, json2):
        for attr, val in json.loads(json1).items():
            if ((attr in json.loads(json2).keys())):# and (val in ast.literal_eval(json2).values())):
                continue
            else:
                return False
        return True

if __name__ == '__main__':
    unittest.main()