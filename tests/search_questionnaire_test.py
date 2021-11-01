import unittest
import requests
import time
import ast
import json

TEST_AUTH = {"user": "6d3fe021cbb84781bac92e159fcb4e43", "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtpZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJodHRwczovL3Myc2RldmloZWFsdGhlLm9ubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzMzZTdkNTY1LTY1NTgtNGVkOC04MmJhLTA4ODJjYmFmZDQ0NC8iLCJpYXQiOjE2MzU3NDczNjUsIm5iZiI6MTYzNTc0NzM2NSwiZXhwIjoxNjM1NzUxMjY1LCJhaW8iOiJFMlpnWUpnWXNmQnE5VDJyVlc3WHU4Ui8zTnFnQlFBPSIsImFwcGlkIjoiYjgxMWNhNDItOTdkZS00NzFmLTk4OTItMzVjMjY2ZmZmMmMxIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0LyIsIm9pZCI6IjYxYWE5ZWY4LWIxNzQtNDBlZC05MDE5LTdmYmYyMjA1MWViNCIsInJoIjoiMC5BVUlBWmRYbk0xaGwyRTZDdWdpQ3k2X1VSRUxLRWJqZWx4OUhtSkkxd21iXzhzRkNBQUEuIiwic3ViIjoiNjFhYTllZjgtYjE3NC00MGVkLTkwMTktN2ZiZjIyMDUxZWI0IiwidGlkIjoiMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0IiwidXRpIjoiT2pRR08yakIxa2VCeGVNZjhEejRBQSIsInZlciI6IjEuMCJ9.VpzkpRVGhIqPEeIfNgDY45uDruKmG17giMX24AeFeJEzWY2YfW8k0wMGCkkXPLT0oHTcQUVNs54m7z3XRgmY9mSqOGq_D9f0Oje_OwSKBLLC62_x7BCl9ogQHqBF73TCrpszPXKzTX-Ug93lnXLKy8Ficbrzz5fUbVMIMqC1sfqDJJYxrBVOjGw8HuK4xcTnFlx_6wYrwiXkajffS6a6JjR1KO-8Ip52j7cWo7pSA1hTtWbDqZVel4ty988lrctJ7xGB-lUmStLYCGKlP49jHoOZOiIAmnkOFLpuy3spXU0M6mjMjOLrTM6et7BoO0Wz_dz74y4JOuSo5imdvK0Fng"}

class TestSearchQuestionnaire(unittest.TestCase):

    def test_successful_with_resource1and2(self):
        """
        Test that it works as promised with resource 1,2
        """
        print("---TESTING SUCCESSFUL SEARCH 1,2 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?id=1111'
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/1and2.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaires = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaires, comparison))
        comparison_file.close()
    
    def test_successful_with_resource3and4(self):
        """
        Test that it works as promised with resource 3,4
        """
        print("---TESTING SUCCESSFUL SEARCH 3,4 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?id=2222'
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/3and4.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()

        def test_successful_with_resource5and6(self):
            """
        Test that it works as promised with resource 5,6
        """
        print("---TESTING SUCCESSFUL SEARCH 5,6 ---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?id=2222'
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 200)
        comparison_file = open('json/questionnaires/3and4.json', 'rb')
        comparison = comparison_file.read().decode("utf-8") 
        retrieved_questionnaire = json.dumps(r.json(), indent=4)
        self.assertTrue(self.compare_json(retrieved_questionnaire, comparison))
        comparison_file.close()
        
    
    def test_without_resource(self):
        """
        Test that it returns 204 when nothing found
        """
        print("---TESTING SEARCH WITH NO RESOURCE FOUND ---")
        start = time.time()
        url = 'http://localhost:7071/api/questionnaire?id=7777777777'
        r = requests.get(url=url, headers = TEST_AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 204)


    def test_without_auth(self):
        """
        Test that it handles error
        """
        print("---TESTING SEARCH WITHOUT AUTH---")
        start = time.time()
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?id=1111'
        r = requests.get(url=url)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 401)
        

    def test_invalid_user(self):
        """
        Test that it handles error
        """
        print("---TESTING SEARCH INVALID AUTH---")
        start = time.time()
        AUTH = {"user": "[1,2,3]", "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtpZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJodHRwczovL3Myc2RldmloZWFsdGhlLm9ubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzMzZTdkNTY1LTY1NTgtNGVkOC04MmJhLTA4ODJjYmFmZDQ0NC8iLCJpYXQiOjE2MzU3NDczNjUsIm5iZiI6MTYzNTc0NzM2NSwiZXhwIjoxNjM1NzUxMjY1LCJhaW8iOiJFMlpnWUpnWXNmQnE5VDJyVlc3WHU4Ui8zTnFnQlFBPSIsImFwcGlkIjoiYjgxMWNhNDItOTdkZS00NzFmLTk4OTItMzVjMjY2ZmZmMmMxIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0LyIsIm9pZCI6IjYxYWE5ZWY4LWIxNzQtNDBlZC05MDE5LTdmYmYyMjA1MWViNCIsInJoIjoiMC5BVUlBWmRYbk0xaGwyRTZDdWdpQ3k2X1VSRUxLRWJqZWx4OUhtSkkxd21iXzhzRkNBQUEuIiwic3ViIjoiNjFhYTllZjgtYjE3NC00MGVkLTkwMTktN2ZiZjIyMDUxZWI0IiwidGlkIjoiMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0IiwidXRpIjoiT2pRR08yakIxa2VCeGVNZjhEejRBQSIsInZlciI6IjEuMCJ9.VpzkpRVGhIqPEeIfNgDY45uDruKmG17giMX24AeFeJEzWY2YfW8k0wMGCkkXPLT0oHTcQUVNs54m7z3XRgmY9mSqOGq_D9f0Oje_OwSKBLLC62_x7BCl9ogQHqBF73TCrpszPXKzTX-Ug93lnXLKy8Ficbrzz5fUbVMIMqC1sfqDJJYxrBVOjGw8HuK4xcTnFlx_6wYrwiXkajffS6a6JjR1KO-8Ip52j7cWo7pSA1hTtWbDqZVel4ty988lrctJ7xGB-lUmStLYCGKlP49jHoOZOiIAmnkOFLpuy3spXU0M6mjMjOLrTM6et7BoO0Wz_dz74y4JOuSo5imdvK0Fng"}
        url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?id=1111'
        r = requests.get(url=url, headers = AUTH)
        print("-- TIME --: " + str(time.time() - start))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, "Error: User not found")
    
    def compare_json(self, json1, json2):
        return True

if __name__ == '__main__':
    unittest.main()