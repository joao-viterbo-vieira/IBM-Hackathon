from tools_standard import find_funding_opportunities, check_eligibility
from pydantic import BaseModel
import json

class SearchInput(BaseModel):
    query: str

print("Testing find_funding_opportunities...")
print("\n1. Testing 'AI startup' query:")
result1 = find_funding_opportunities(SearchInput(query="AI startup"))
data1 = json.loads(result1)
print(f"Found {len(data1)} results")
print(f"First result: {data1[0]['title']}")

print("\n2. Testing 'healthcare' query:")
result2 = find_funding_opportunities(SearchInput(query="healthcare"))
data2 = json.loads(result2)
print(f"Found {len(data2)} results")

print("\n3. Testing 'machine learning' query:")
result3 = find_funding_opportunities(SearchInput(query="machine learning"))
data3 = json.loads(result3)
print(f"Found {len(data3)} results")

print("\n4. Testing generic 'funding' query:")
result4 = find_funding_opportunities(SearchInput(query="funding"))
data4 = json.loads(result4)
print(f"Found {len(data4)} results")

print("\n✅ All tests passed!")
