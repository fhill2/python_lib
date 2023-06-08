# 1 instance only
# class Farm():
#     def __init__():
#         pass

# data["data"]["repositories"]["nodes"]
# {
#     "name": "github.com/voldikss/vim-floaterm",
#     "description": ":star2: Terminal manager for (neo)vim",
#     "url": "/github.com/voldikss/vim-floaterm",
#     "keyValuePairs": [
#         {"key": "asd12345678", "value": null},
#         {"key": "asd123", "value": null},
#     ],
# }
#

class Repo():
    def __init__(self):
        self.in_stars = False
        # self.in_sourcegraph = False
        # self.in_config = False

        self.config_tags = []
        self.sourcegraph_tags = []
        self.sourcegraph_id = 0



# repos = get_sg_repos()
# print(repos["voldikss/vim-floaterm"])
# set_tag()

# variables = {"countryCode": "CA"}
# variables = {"repoID": "123456"}

# Synchronous request


# OLD
# client = GraphqlClient(endpoint="https://countries.trevorblades.com")
# Create the query string and variables required for the request.
# query = """
#     query countryQuery($countryCode: String) {
#         country(code:$countryCode) {
#             code
#             name
#         }
#     }
# """
# Asynchronous request
# import asyncio

# data = asyncio.run(client.execute_async(query=query, variables=variables))
# print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}
