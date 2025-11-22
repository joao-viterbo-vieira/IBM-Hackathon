from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, Field
import json
import os

# Comprehensive AI Funding Database
AI_FUNDING_DATABASE = [
    {
        "title": "AI Innovation Grant 2025",
        "provider": "TechFuture Foundation",
        "amount": "$50,000 - $100,000",
        "link": "https://techfuture.org/ai-innovation-grant",
        "snippet": "Grants for startups developing innovative AI solutions in healthcare, education, or sustainability. Must be an SME, less than 5 years old, focused on AI/ML technologies. Deadline: March 31, 2025."
    },
    {
        "title": "AI for Good Challenge",
        "provider": "Global AI Initiative",
        "amount": "$75,000",
        "link": "https://globalai.org/ai-for-good",
        "snippet": "Funding for AI projects that address social challenges. Open to SMEs working on AI applications for education, healthcare, climate change, or accessibility. Rolling applications accepted."
    },
    {
        "title": "Machine Learning Research Grant",
        "provider": "National Science Foundation",
        "amount": "$100,000 - $250,000",
        "link": "https://nsf.gov/ml-research-grant",
        "snippet": "Support for companies conducting cutting-edge machine learning research. Focus areas include natural language processing, computer vision, and reinforcement learning. Must demonstrate commercial viability."
    },
    {
        "title": "AI Startup Accelerator Fund",
        "provider": "Venture Capital Partners",
        "amount": "$150,000 + mentorship",
        "link": "https://vcpartners.com/ai-accelerator",
        "snippet": "Equity-free funding for early-stage AI startups. Includes 6-month accelerator program with industry mentors. Looking for AI companies in fintech, healthtech, or enterprise software."
    },
    {
        "title": "Deep Learning Innovation Prize",
        "provider": "AI Research Institute",
        "amount": "$200,000",
        "link": "https://airesearch.org/deep-learning-prize",
        "snippet": "Annual prize for breakthrough deep learning applications. Open to SMEs with novel approaches to computer vision, speech recognition, or generative AI. Application deadline: June 15, 2025."
    },
    {
        "title": "AI Ethics and Safety Grant",
        "provider": "Responsible AI Foundation",
        "amount": "$60,000",
        "link": "https://responsibleai.org/ethics-grant",
        "snippet": "Funding for companies developing AI safety tools, bias detection systems, or ethical AI frameworks. Priority given to diverse founding teams and underrepresented communities."
    },
    {
        "title": "Enterprise AI Solutions Fund",
        "provider": "Corporate Innovation Lab",
        "amount": "$120,000",
        "link": "https://corporatelab.com/enterprise-ai",
        "snippet": "Grants for B2B AI solutions targeting enterprise customers. Focus on AI for automation, predictive analytics, or decision support systems. Must have at least one pilot customer."
    },
    {
        "title": "AI in Healthcare Grant",
        "provider": "Medical Innovation Fund",
        "amount": "$180,000",
        "link": "https://medinnovation.org/ai-healthcare",
        "snippet": "Support for AI applications in medical diagnosis, drug discovery, or patient care. Requires collaboration with healthcare institutions. FDA approval pathway preferred."
    },
    {
        "title": "Generative AI Creator Fund",
        "provider": "Creative Tech Alliance",
        "amount": "$40,000 - $80,000",
        "link": "https://creativetech.org/generative-ai",
        "snippet": "Funding for startups building generative AI tools for content creation, design, or media production. Open to companies working with text, image, video, or audio generation."
    },
    {
        "title": "AI Climate Solutions Grant",
        "provider": "Green Technology Initiative",
        "amount": "$90,000",
        "link": "https://greentech.org/ai-climate",
        "snippet": "Grants for AI solutions addressing climate change, renewable energy optimization, or environmental monitoring. Must demonstrate measurable environmental impact."
    }
]

class SearchInput(BaseModel):
    query: str = Field(description="Keywords to search for (e.g., 'AI startup', 'healthcare AI', 'machine learning').")

@tool(name="find_funding_opportunities", description="Search for AI funding opportunities based on a query from a curated database.")
def find_funding_opportunities(input: SearchInput) -> str:
    """
    Search for AI funding opportunities based on a query.
    Returns a JSON string of matching opportunities from a curated database.
    """
    print(f"Searching for: {input.query}")
    query_lower = input.query.lower()
    results = []
    
    # Search through the database for matching opportunities
    for opportunity in AI_FUNDING_DATABASE:
        # Check if query matches title, provider, or snippet
        if (query_lower in opportunity["title"].lower() or 
            query_lower in opportunity["provider"].lower() or 
            query_lower in opportunity["snippet"].lower()):
            results.append(opportunity)
    
    # If no specific matches, return all AI-related opportunities
    if not results:
        # Check for general AI-related terms
        ai_terms = ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "neural", "startup", "funding", "grant"]
        if any(term in query_lower for term in ai_terms):
            results = AI_FUNDING_DATABASE[:5]  # Return top 5 opportunities
        else:
            results = AI_FUNDING_DATABASE[:3]  # Return top 3 for non-AI queries
    
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
