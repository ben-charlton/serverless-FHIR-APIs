import unittest
import requests
import time
import ast
import json

TEST_USER = {"user": "6d3fe021cbb84781bac92e159fcb4e43"}

class TestStressQuestionnaire(unittest.TestCase):

    def get_bearer_token(self):
        token = 1
        return token

    def test_stress_questionnaire(self):
        """
        Test response time with hundreds of resources
        """
        print("---STRESS TESTING POST QUESTIONNAIRE ---")
        uids = []
        questionnaire_file = open('json/questionnaires/stress.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        headers = {"authorisation": "6d3fe021cbb84781bac92e159fcb4e43", "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtpZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJodHRwczovL3Myc2RldmloZWFsdGhlLm9ubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzMzZTdkNTY1LTY1NTgtNGVkOC04MmJhLTA4ODJjYmFmZDQ0NC8iLCJpYXQiOjE2MzUxMTM4ODksIm5iZiI6MTYzNTExMzg4OSwiZXhwIjoxNjM1MTE3Nzg5LCJhaW8iOiJFMlpnWU1oNHNycjVpZENVcGZzejFhWVZNbjg3QmdBPSIsImFwcGlkIjoiYjgxMWNhNDItOTdkZS00NzFmLTk4OTItMzVjMjY2ZmZmMmMxIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0LyIsIm9pZCI6IjYxYWE5ZWY4LWIxNzQtNDBlZC05MDE5LTdmYmYyMjA1MWViNCIsInJoIjoiMC5BVUlBWmRYbk0xaGwyRTZDdWdpQ3k2X1VSRUxLRWJqZWx4OUhtSkkxd21iXzhzRkNBQUEuIiwic3ViIjoiNjFhYTllZjgtYjE3NC00MGVkLTkwMTktN2ZiZjIyMDUxZWI0IiwidGlkIjoiMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0IiwidXRpIjoiZ1NqQVlDMk92MDJMQTRfekhHYjFBQSIsInZlciI6IjEuMCJ9.GbqNkyUVrXMzK83R-cXynjxyAFxupglVmxz8eUUUKT0hvg80okxoEpOxpG0hENRAQy8pPyRozjVglzo5-m-JNICAfW4OJQuAmOhlOilnpTSfYv7HFNaG4p9WrRNfyP5EOlhBrQa8AMgSIbNX7R7kGJGDI30EMaIf9q8JBV2C2Ze9wUqlqFaaYIDbEVkbKsw7TLcQCShNn7VLrPr1ZxLLHqJZRix82Tk1GJoNc1ScAONwHbomhftGekY7rziibyD_h4pQ9u5Fxhy5uGm2B0fyXq7dgDpzFvK1Ek_AgevGYzI-4D3lcH1Kr8KWHS5alG-jRMieuxM3zKdfBfqmG2GrQQ"}
        for i in range(401,501):
            start = time.time()
            r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers=headers, data=questionnaire)
            print("posting" + str(time.time() - start))
            self.assertEqual(r.status_code, 200)
            self.assertIsInstance(r.text, str)
            uid = str(r.text)
            uids.append(uid)
            
        print("-- STRESS TESTING GET QUESTIONNAIRE --")
        for uid in uids:
            url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
            start = time.time()
            z = requests.get(url=url, headers = headers)
            print(str(time.time() - start))
            r = requests.delete(url=url, headers = headers)
            
        
        questionnaire_file.close()
        
if __name__ == '__main__':
    unittest.main()