from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field
import json
import os
from duckduckgo_search import DDGS

class SearchInput(BaseModel):
    query: str = Field(description="Keywords to search for (e.g., 'AI startup', 'green energy').")

@tool(name="find_funding_opportunities", description="Search for funding opportunities based on a query using DuckDuckGo.")
def find_funding_opportunities(input: SearchInput) -> str:
    """
    Search for funding opportunities based on a query using DuckDuckGo.
    Returns a JSON string of matching opportunities.
    """
    print(f"Searching for: {input.query}")
    results = []
    try:
        with DDGS() as ddgs:
            # Search for the query + "funding grant" to make it more specific
            search_query = f"{input.query} funding grant"
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

class EligibilityInput(BaseModel):
    opportunity_description: str = Field(description="The description of the funding opportunity.")
    company_profile: str = Field(description="Description of the company.")

@tool(name="check_eligibility", description="Check if a company is eligible for a specific funding opportunity.")
def check_eligibility(input: EligibilityInput) -> str:
    """
    Check if a company is eligible for a specific funding opportunity.
    Returns a string assessment.
    """
    # Simple mock logic: assume eligibility if keywords match, else ask for manual review
    # In a real app, this would use an LLM or complex rule engine
    company_profile = input.company_profile.lower()
    opportunity_description = input.opportunity_description.lower()
    
    # Mock logic for demo - just checking for some overlap or keywords
    if "ai" in opportunity_description and "ai" not in company_profile:
         return f"Likely Ineligible. Opportunity seems to be about AI, but company profile does not mention it."

    return f"Likely Eligible. Based on the description, it seems worth applying."

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
