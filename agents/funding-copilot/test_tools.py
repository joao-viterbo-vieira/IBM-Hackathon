from tools import find_funding_opportunities, check_eligibility, save_draft
import json
import os

def test_tools():
    print("Testing find_funding_opportunities...")
    # Test 1: Search for AI
    result = find_funding_opportunities("AI")
    data = json.loads(result)
    assert len(data) > 0, "Should find AI opportunities"
    print("Find AI: PASS")

    # Test 2: Search for generic funding
    result = find_funding_opportunities("funding")
    data = json.loads(result)
    assert len(data) > 0, "Should find all opportunities for generic query"
    print("Find Generic: PASS")

    print("\nTesting check_eligibility...")
    # Test 3: Check eligibility (Eligible)
    opp_id = data[0]['id']
    result = check_eligibility(opp_id, "We are an AI startup")
    assert "Likely Eligible" in result, "Should be eligible"
    print("Check Eligible: PASS")

    # Test 4: Check eligibility (Ineligible)
    result = check_eligibility(opp_id, "We are a bakery")
    assert "Likely Ineligible" in result, "Should be ineligible"
    print("Check Ineligible: PASS")

    print("\nTesting save_draft...")
    # Test 5: Save draft
    content = "This is a test application."
    filename = "test_app.txt"
    result = save_draft(content, filename)
    assert "Successfully saved" in result, "Should save successfully"
    assert os.path.exists(os.path.join("output", filename)), "File should exist"
    print("Save Draft: PASS")
    
    # Cleanup
    if os.path.exists(os.path.join("output", filename)):
        os.remove(os.path.join("output", filename))

if __name__ == "__main__":
    test_tools()
