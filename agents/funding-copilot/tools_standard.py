from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field
import json
import os

# Mock Database of Funding Opportunities
FUNDING_DB = [
    {
        "id": "GRANT-001",
        "title": "AI Innovation Grant",
        "provider": "TechFuture Foundation",
        "amount": "$50,000",
        "description": "Grants for startups developing innovative AI solutions.",
        "criteria": "Must be an SME, < 5 years old, focused on AI/ML."
    },
    {
        "id": "GRANT-002",
        "title": "Green Energy Subsidy",
        "provider": "EcoWorld Alliance",
        "amount": "$100,000",
        "description": "Subsidies for companies transitioning to renewable energy.",
        "criteria": "Must be in the energy sector, reducing carbon footprint."
    },
    {
        "id": "GRANT-003",
        "title": "Small Business Digitalization",
        "provider": "GovTech",
        "amount": "$10,000",
        "description": "Support for small businesses to upgrade their digital infrastructure.",
        "criteria": "Any SME with < 50 employees."
    }
]

class SearchInput(BaseModel):
    query: str = Field(description="Keywords to search for (e.g., 'AI startup', 'green energy').")

@tool(name="find_funding_opportunities", description="Search for funding opportunities based on a query.")
def find_funding_opportunities(input: SearchInput) -> str:
    """
    Search for funding opportunities based on a query.
    Returns a JSON string of matching opportunities.
    """
    query = input.query.lower()
    results = []
    for item in FUNDING_DB:
        if query in item["title"].lower() or query in item["description"].lower():
            results.append(item)
    
    # If no specific match, return all for demo purposes if query is generic like "funding"
    if not results and "funding" in query:
        return json.dumps(FUNDING_DB, indent=2)
        
    return json.dumps(results, indent=2)

class EligibilityInput(BaseModel):
    opportunity_id: str = Field(description="The ID of the funding opportunity.")
    company_profile: str = Field(description="Description of the company.")

@tool(name="check_eligibility", description="Check if a company is eligible for a specific funding opportunity.")
def check_eligibility(input: EligibilityInput) -> str:
    """
    Check if a company is eligible for a specific funding opportunity.
    Returns a string assessment.
    """
    opportunity = next((item for item in FUNDING_DB if item["id"] == input.opportunity_id), None)
    if not opportunity:
        return "Opportunity not found."
    
    # Simple mock logic
    company_profile = input.company_profile.lower()
    criteria = opportunity["criteria"].lower()
    
    # Mock logic for demo
    if "ai" in criteria and "ai" not in company_profile:
        return f"Likely Ineligible. Criteria requires: {opportunity['criteria']}"
    
    return f"Likely Eligible. The company profile seems to match the criteria: {opportunity['criteria']}"

class DraftInput(BaseModel):
    application_content: str = Field(description="The full text of the application.")
    filename: str = Field(description="The name of the file to save (e.g., 'draft_application.txt').")

@tool(name="save_draft", description="Save a drafted funding application to a file.")
def save_draft(input: DraftInput) -> str:
    """
    Save a drafted funding application to a file.
    """
    try:
        # Ensure directory exists
        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", input.filename)
        
        with open(filepath, "w") as f:
            f.write(input.application_content)
        return f"Successfully saved draft to {filepath}"
    except Exception as e:
        return f"Error saving draft: {str(e)}"
