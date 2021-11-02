import unittest
import requests
import time
import ast
import json

TEST_USER = {"user": "6d3fe021cbb84781bac92e159fcb4e43", "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCIsImtpZCI6Imwzc1EtNTBjQ0g0eEJWWkxIVEd3blNSNzY4MCJ9.eyJhdWQiOiJodHRwczovL3Myc2RldmloZWFsdGhlLm9ubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzMzZTdkNTY1LTY1NTgtNGVkOC04MmJhLTA4ODJjYmFmZDQ0NC8iLCJpYXQiOjE2MzU4MDYyNTMsIm5iZiI6MTYzNTgwNjI1MywiZXhwIjoxNjM1ODEwMTUzLCJhaW8iOiJFMlpnWUdETThURHArTnJDdUhNaGozSEswN29EQUE9PSIsImFwcGlkIjoiYjgxMWNhNDItOTdkZS00NzFmLTk4OTItMzVjMjY2ZmZmMmMxIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0LyIsIm9pZCI6IjYxYWE5ZWY4LWIxNzQtNDBlZC05MDE5LTdmYmYyMjA1MWViNCIsInJoIjoiMC5BVUlBWmRYbk0xaGwyRTZDdWdpQ3k2X1VSRUxLRWJqZWx4OUhtSkkxd21iXzhzRkNBQUEuIiwic3ViIjoiNjFhYTllZjgtYjE3NC00MGVkLTkwMTktN2ZiZjIyMDUxZWI0IiwidGlkIjoiMzNlN2Q1NjUtNjU1OC00ZWQ4LTgyYmEtMDg4MmNiYWZkNDQ0IiwidXRpIjoieDlySFF1bDVEa3V2SDVVdl9naXdBQSIsInZlciI6IjEuMCJ9.Oy4CW1f5TJyRZJ9uTHvCHlWoKsmXeIpKYUko4fWgcIYpOs2Ki9VlGqBqESIwl9Qdpf8ImCY4B9t5ouFfaVcDjczHvGuCPR3WuMXvrtoF5JCq3zT04kYt2TVLw4_pURGEOtUC7lb2m1ZUc7pVRfOva8REner6W3WKhtO0MG14bKTJspoiT0qGsr3cO2cjc6pSbsA4WIiyMXQxnIK0ZkpK7wdU9ONhvXrEGFKcEHFygJoqwAHfxohKUVRd5yjAJwKkGrbycevdunA0QphbO-6Qp2YRtbmgDQtz3CbIbBQfcQo7G96OAfI6xTY0oJBsgm3f4FH00xZpiaLOfTMinGHrTQ"}

class TestStressQuestionnaire(unittest.TestCase):


    def test_stress_questionnaire(self):
        """
        Test response time with hundreds of resources
        """
        print("---STRESS TESTING POST QUESTIONNAIRE ---")
        uids = []
        questionnaire_file = open('json/questionnaires/stress.json', 'rb')
        questionnaire = questionnaire_file.read().decode("utf-8") 
        for i in range(1,101):
            start = time.time()
            r = requests.post('https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire', headers=TEST_USER, data=questionnaire)
            print("posting" + str(time.time() - start))
            self.assertEqual(r.status_code, 200)
            self.assertIsInstance(r.text, str)
            uid = str(r.text)
            uids.append(uid)
            
        print("-- STRESS TESTING GET QUESTIONNAIRE --")
        for uid in uids:
            url = 'https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/' + uid
            start = time.time()
            z = requests.get(url=url, headers = TEST_USER)
            print(str(time.time() - start))
            r = requests.delete(url=url, headers = TEST_USER)
            
        questionnaire_file.close()
        
if __name__ == '__main__':
    unittest.main()