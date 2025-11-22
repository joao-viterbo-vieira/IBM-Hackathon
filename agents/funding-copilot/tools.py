from mcp.server.fastmcp import FastMCP
import json
import os

# Create the MCP server instance
mcp = FastMCP("funding-copilot-tools")

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

@mcp.tool("find_funding_opportunities")
def find_funding_opportunities(query: str) -> str:
    """
    Search for funding opportunities based on a query.
    Returns a JSON string of matching opportunities.
    """
    query = query.lower()
    results = []
    for item in FUNDING_DB:
        if query in item["title"].lower() or query in item["description"].lower():
            results.append(item)
    
    # If no specific match, return all for demo purposes if query is generic like "funding"
    if not results and "funding" in query:
        return json.dumps(FUNDING_DB, indent=2)
        
    return json.dumps(results, indent=2)

@mcp.tool("check_eligibility")
def check_eligibility(opportunity_id: str, company_profile: str) -> str:
    """
    Check if a company is eligible for a specific funding opportunity.
    Returns a string assessment.
    """
    opportunity = next((item for item in FUNDING_DB if item["id"] == opportunity_id), None)
    if not opportunity:
        return "Opportunity not found."
    
    # Simple mock logic: assume eligibility if keywords match, else ask for manual review
    # In a real app, this would use an LLM or complex rule engine
    company_profile = company_profile.lower()
    criteria = opportunity["criteria"].lower()
    
    # Mock logic for demo
    if "ai" in criteria and "ai" not in company_profile:
        return f"Likely Ineligible. Criteria requires: {opportunity['criteria']}"
    
    return f"Likely Eligible. The company profile seems to match the criteria: {opportunity['criteria']}"

@mcp.tool("save_draft")
def save_draft(application_content: str, filename: str) -> str:
    """
    Save a drafted funding application to a file.
    """
    try:
        # Ensure directory exists
        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", filename)
        
        with open(filepath, "w") as f:
            f.write(application_content)
        return f"Successfully saved draft to {filepath}"
    except Exception as e:
        return f"Error saving draft: {str(e)}"

if __name__ == "__main__":
    mcp.run()
