# from python_graphql_client import GraphqlClient
#
# # Instantiate the client with an endpoint.
# client = GraphqlClient(endpoint="https://countries.trevorblades.com")
#
# # Create the query string and variables required for the request.
# query = """
#     query countryQuery($countryCode: String) {
#         country(code:$countryCode) {
#             code
#             name
#         }
#     }
# """
# variables = {"countryCode": "CA"}
#
# # Synchronous request
# data = client.execute(query=query, variables=variables)
# print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}
#
#
# # Asynchronous request
# import asyncio
#
# data = asyncio.run(client.execute_async(query=query, variables=variables))
# print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}

# ===============

import requests

# url = 'https://api.github.com/graphql'
url = "http://127.0.0.1:7080/.api/graphql"
# json = { 'query' : """
# mutation AddSecurityOwner($repoID: ID!) {
#   addRepoKeyValuePair(repo: $repoID, key: "owning-team", value: "security") {
#     alwaysNil
#   }
# }
# """}

json = { "query" : "query { currentUser { username } }"}
api_token = "325001d495562b097b03c698bceded4a0ddff72e"
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)
print (r.text)
