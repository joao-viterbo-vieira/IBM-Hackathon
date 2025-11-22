from mcp.server.fastmcp import FastMCP
import json
import os
from duckduckgo_search import DDGS

# Create the MCP server instance
mcp = FastMCP("funding-copilot-tools")

@mcp.tool("find_funding_opportunities")
def find_funding_opportunities(query: str) -> str:
    """
    Search for funding opportunities based on a query using DuckDuckGo.
    Returns a JSON string of matching opportunities.
    """
    print(f"Searching for: {query}")
    results = []
    try:
        with DDGS() as ddgs:
            # Search for the query + "funding grant" to make it more specific
            search_query = f"{query} funding grant"
            ddgs_results = list(ddgs.text(search_query, max_results=5))
            
            for r in ddgs_results:
                results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
                
    except Exception as e:
        return json.dumps({"error": str(e)})
        
    return json.dumps(results, indent=2)

@mcp.tool("check_eligibility")
def check_eligibility(opportunity_description: str, company_profile: str) -> str:
    """
    Check if a company is eligible for a specific funding opportunity.
    Returns a string assessment.
    """
    # Simple mock logic: assume eligibility if keywords match, else ask for manual review
    # In a real app, this would use an LLM or complex rule engine
    company_profile = company_profile.lower()
    opportunity_description = opportunity_description.lower()
    
    # Mock logic for demo - just checking for some overlap or keywords
    if "ai" in opportunity_description and "ai" not in company_profile:
         return f"Likely Ineligible. Opportunity seems to be about AI, but company profile does not mention it."

    return f"Likely Eligible. Based on the description, it seems worth applying."

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
