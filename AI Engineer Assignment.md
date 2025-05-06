---

## 📅 Time Estimate
**12 hours** (split over 2 days)

---

## 🧠 LLM Automation MVP
### Project Brief
AI-Powered Campaign Creator for a Social Platform

### 🎯 Objective
Build a Python tool or script that takes a structured campaign brief and programmatically creates a campaign in one of the major social ad platforms (Meta, TikTok, LinkedIn, etc.) using their public APIs.
- Accepts user input for a task (necessary information required to build the campaign) through cli/UI
- Uses an LLM(open source or public api based LLM) to perform the task using prompt engineering (maybe finetune the LLM, for this use case)
- Finishes with a working prototype, that is able to generate a advertisement campaign on the social media with minimal imput.

### ✅ Tasks
1. Prompt Engineering & LLM Integration  
2. Model Tuning or Retrieval-Augmented Generation (RAG)
3. MVP creation for AI powered campaign generation for one or more major social ad platform.

### Submission
- GitHub repo with code + notes -> Create a public repo on your github and share access.
- (Optional) Loom/video walkthrough

### Notes
- Please make sure to highlight your architechture decisions. Clearly defining the pros and cons.
- Please explain your LLM choice and what trade offs you made.
- A clearly commented and documented code will give your subission an edge.

---

### ⚙️ Hints
- **Platform Choice**: Use Meta Ads API, or TikTok/LinkedIn Ads API
- **Authentication**: Use personal/test account credentials
- **LLM**: Use LLM API or any opensource LLM from HuggingFace or other platform
- **Campaign Flow**:
  - Create Campaign
  - Create Ad Set (or equivalent)
  - Create one Ad (placeholder creative/text)

---

### ✅ Deliverables
- Python script or Jupyter notebook
- `config.json` or `.env` for storing API tokens
- README with:
  - Setup instructions
  - Description of campaign logic
  - Notes on limitations as well as cost implications that might come with this solution
- Screenshots of campaign inside the ad platform

---
### Please make sure all the deliverables are included in your submission ###
### Please also, name your repository as atomicads-ai-engineer-assignment-{your_name} ###