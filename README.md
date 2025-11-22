# Funding Copilot

An AI-powered agent built for IBM Watsonx Orchestrate that helps SMEs (Small and Medium Enterprises) discover funding opportunities, assess eligibility, and draft applications.

Important IBM documentation for setup: https://developer.ibm.com/tutorials/getting-started-with-watsonx-orchestrate/

## Overview

The Funding Copilot uses DuckDuckGo search to find real-time funding opportunities online, evaluates company eligibility, and assists in creating funding application drafts. It's designed to streamline the funding discovery process for small businesses.

## Features

- **🔍 Curated AI Funding Database**: Access to 10 comprehensive AI funding opportunities covering various sectors
- **✅ Eligibility Checking**: Evaluates whether your company qualifies for specific opportunities
- **📝 Draft Generation**: Creates professional funding application drafts
- **🤖 AI-Powered**: Leverages IBM Watsonx AI (Llama 3 405B) for intelligent assistance
- **🎯 Smart Search**: Robust keyword matching across titles, providers, and descriptions

## Project Structure

```
IBM_Hackaton/
├── agents/
│   └── funding-copilot/
│       ├── funding_agent.yaml          # Agent configuration
│       ├── tools.py                    # MCP-based tools (development)
│       ├── tools_standard.py           # SDK-based tools (deployment)
│       ├── requirements.txt            # MCP dependencies
│       └── requirements_standard.txt   # Deployment dependencies
├── script.html                         # Watsonx Orchestrate chat widget
├── test_script_page.html              # Test page for chat widget
├── deployment.md                       # Deployment guide
└── README.md                          # This file
```

## Tools

### 1. `find_funding_opportunities`
Searches for AI funding opportunities from a curated database of 10 comprehensive funding sources.

**Input**: Query string (e.g., "AI startup", "healthcare AI", "machine learning")

**Output**: JSON array of opportunities with title, provider, amount, link, and detailed description

**Database includes**:
- AI Innovation grants ($50K-$250K)
- Startup accelerator programs
- Research grants
- Healthcare AI funding
- Climate tech AI grants
- Generative AI creator funds
- And more...

### 2. `check_eligibility`
Evaluates if a company is eligible for a funding opportunity.

**Input**: 
- `opportunity_description`: Description of the funding opportunity
- `company_profile`: Description of your company

**Output**: Eligibility assessment

### 3. `save_draft`
Saves a funding application draft to a file.

**Input**:
- `application_content`: The application text
- `filename`: Name of the file to save

**Output**: Confirmation message with file path

## Setup

### Prerequisites

- Python 3.11+
- IBM Watsonx Orchestrate account
- Virtual environment

### Installation

1. **Clone the repository**:
   ```bash
   cd /Users/joaovieira/Desktop/IBM_Hackaton
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r agents/funding-copilot/requirements_standard.txt
   ```

## Deployment to IBM Watsonx Orchestrate

### 1. Activate Environment
```bash
orchestrate env activate env_test
```

### 2. Import Tools
```bash
./.venv/bin/orchestrate tools import --kind python \
  --file agents/funding-copilot/tools_standard.py \
  -r agents/funding-copilot/requirements_standard.txt
```

### 3. Import Agent
```bash
./.venv/bin/orchestrate agents import \
  --file agents/funding-copilot/funding_agent.yaml
```

### 4. Deploy Agent
```bash
./.venv/bin/orchestrate agents deploy --name Funding_Copilot
```

## Testing the Chat Widget

A test page is provided to verify the Watsonx Orchestrate chat widget integration:

1. Open `test_script_page.html` in your browser
2. The chat widget should load automatically
3. Interact with the Funding Copilot agent

## Development

### Two Tool Implementations

- **`tools.py`**: MCP (Model Context Protocol) based implementation for local development
- **`tools_standard.py`**: IBM Watsonx Orchestrate SDK implementation for deployment

Both implementations provide the same functionality but use different frameworks.

### Local Testing

For MCP-based tools:
```bash
pip install -r agents/funding-copilot/requirements.txt
python agents/funding-copilot/tools.py
```

## Configuration

The agent is configured in `funding_agent.yaml`:

- **LLM**: `watsonx/meta-llama/llama-3-405b-instruct`
- **Style**: `react` (ReAct prompting pattern)
- **Tools**: `find_funding_opportunities`, `check_eligibility`, `save_draft`

## Usage Example

1. **Start a conversation**: "I'm looking for AI startup funding in Australia"
2. **Agent searches**: Uses DuckDuckGo to find relevant opportunities
3. **Check eligibility**: Agent asks for your company profile and evaluates fit
4. **Draft application**: Agent helps create a tailored application draft
5. **Save draft**: Application is saved to the `output/` directory

## Troubleshooting

### Token Expired Error
```bash
orchestrate env activate env_test
```

### Module Not Found (MCP)
Make sure you're using `tools_standard.py` for deployment, not `tools.py`.

### Virtual Environment Issues
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r agents/funding-copilot/requirements_standard.txt
```

## Technologies Used

- **IBM Watsonx Orchestrate**: Agent orchestration platform
- **IBM Watsonx AI**: LLM inference (Llama 3 405B)
- **Python**: Implementation language
- **Pydantic**: Data validation

## License

This project was created for the IBM Watsonx Orchestrate Hackathon.

## Author

Built with ❤️ for the IBM Watsonx Orchestrate Hackathon
