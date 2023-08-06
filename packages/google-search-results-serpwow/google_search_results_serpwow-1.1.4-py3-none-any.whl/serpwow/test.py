from google_search_results import GoogleSearchResults
import json

# create the serpwow object, passing in our API key
serpwow = GoogleSearchResults("4BCC1B8B")



# set the batch id
batchId = "500CB8A6"

# list all batches
result = serpwow.list_batches()

# pretty-print the result
print(json.dumps(result, indent=2, sort_keys=True))