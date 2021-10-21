import unittest
import requests
import time
import ast
import json

TEST_AUTH = {"authorisation": "6d3fe021cbb84781bac92e159fcb4e43"}
TEST_1 = '974bf28525024f169687c679f2358b82'

class TestDeleteQuestionnaire(unittest.TestCase):

    def test_successful_with_resource1(self):
        """
        Test that it works as promised with resource 1
        """ 
        print("---TESTING SUCCESSFUL RESOURCE 1 ---")
        questionnaire_file = open('json/questionnaires/test1.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
        start = time.time()
        z = requests.delete(url=url, headers = TEST_AUTH)   
        print("-- TIME --: " + str(time.time() - start))
        res_ques = (requests.get(url=url, headers = TEST_AUTH))
        self.assertEqual(res_ques.status_code, 204)
        questionnaire_file.close()

    def test_successful_with_resource2(self):
        """
        Test that it works as promised with resource 2
        """ 
        print("---TESTING SUCCESSFUL RESOURCE 2 ---")
        questionnaire_file = open('json/questionnaires/test2.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
        start = time.time()
        z = requests.delete(url=url, headers = TEST_AUTH)   
        print("-- TIME --: " + str(time.time() - start))
        res_ques = (requests.get(url=url, headers = TEST_AUTH))
        self.assertEqual(res_ques.status_code, 204)
        questionnaire_file.close()


    def test_successful_with_resource3(self):
        """
        Test that it works as promised with resource 3
        """ 
        print("---TESTING SUCCESSFUL RESOURCE 3 ---")
        questionnaire_file = open('json/questionnaires/test3.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
        start = time.time()
        z = requests.delete(url=url, headers = TEST_AUTH)   
        print("-- TIME --: " + str(time.time() - start))
        res_ques = (requests.get(url=url, headers = TEST_AUTH))
        self.assertEqual(res_ques.status_code, 204)
        questionnaire_file.close()
    
    def test_successful_with_resource4(self):
        """
        Test that it works as promised with resource 4
        """ 
        print("---TESTING SUCCESSFUL RESOURCE 4 ---")
        questionnaire_file = open('json/questionnaires/small.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers = TEST_AUTH, data=questionnaire)
        uid = str(r.text)
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
        start = time.time()
        z = requests.delete(url=url, headers = TEST_AUTH)   
        print("-- TIME --: " + str(time.time() - start))
        res_ques = (requests.get(url=url, headers = TEST_AUTH))
        self.assertEqual(res_ques.status_code, 204)
        questionnaire_file.close()


    def test_without_resource(self):
        """
        Test that it returns 400 when no resource to delete 
        """
        print("---TESTING GET WITH NO RESOURCE FOUND ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/' + '77777777'
        r = requests.delete(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "No resource with matching uid found")

    def test_without_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING WITHOUT AUTH---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_1
        r = requests.delete(url=url)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "User not found")
        

    def test_invalid_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING INVALID AUTH---")
        start = time.time()
        AUTH = {"authorisation": "[1,2,3]"}
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + TEST_1
        r = requests.delete(url=url, headers = AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "User not found")

if __name__ == '__main__':
    unittest.main()