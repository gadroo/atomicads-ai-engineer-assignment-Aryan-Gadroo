# 🚀 AtomicAds: AI-Powered Campaign Generator

> **TL;DR**: Feed me a simple campaign brief, I'll build you a killer Meta ad campaign using the power of AI. No marketing degree required! 🧠✨

Hello there, fellow digital marketer (or marketing-curious developer)! Tired of staring at the Meta Ads Manager wondering what buttons to press? Wish you had a marketing expert whispering sweet campaign strategies in your ear? **AtomicAds** is your new best friend.

This Python-powered marketing wizard uses Retrieval-Augmented Generation (RAG) to turn your simple campaign brief into professional-grade Meta ad campaigns that actually work. Just describe your product, audience, and goals—we'll handle the rest!

## 📸 CLI Interface

![CLI Screenshot 1](./cli%20images/CLI%20images.jpeg)
![CLI Screenshot 2](./cli%20images/CLI%20images%202.jpeg)

## 🏗️ Architecture Decisions: The Method Behind Our Madness

### 1. Modular Design: Lego Blocks, But for Code
I've built AtomicAds with a highly modular architecture that separates concerns into distinct components—think of it like a well-organized kitchen where everything has its place.

**Why you'll love it:**
- 🔧 Easy to maintain and update individual components
- 🧪 Better testability with clear boundaries
- 🚀 Simpler for new devs to jump in and contribute
- 🔄 Ready for future expansion to other ad platforms

**The slight downsides:**
- A bit more initial code to write (but worth it!)
- Small performance trade-offs from cross-module communication
- Slightly more complex initial setup

### 2. RAG over Fine-tuning: Teaching vs. Training
Instead of fine-tuning a custom LLM (expensive and rigid), we went with Retrieval-Augmented Generation (RAG). It's like giving our AI a library of marketing books to reference instead of forcing it to memorize everything.

**Why this rocks:**
- 📚 Can update knowledge without retraining the entire model
- 💰 Much lower development cost and time
- 🔍 Transparency in decision-making (you can see what influenced the output)
- 📈 Easily adaptable as Meta Ads changes policies and features

**The trade-offs:**
- Slightly higher latency (that retrieval step takes time)
- Potentially higher per-request costs
- Quality depends on our knowledge base
- Less specialized behavior than a fine-tuned model

### 3. Vector Database Choice: Pinecone FTW
For our vector database needs, we chose Pinecone. It's like having a lightning-fast librarian who can find exactly what you need in milliseconds.

**The upsides:**
- ☁️ Managed service with minimal ops headaches
- ⚡ Blazing fast performance
- 🔌 Dead simple API to integrate with
- 🔍 Great filtering capabilities for metadata

**The downsides:**
- Vendor lock-in (but worth it for the convenience)
- Costs scale with usage
- Limited control over the underlying infrastructure
- Internet connectivity required

### 4. CLI-First Interface: Command Line Magic
We prioritized a command-line interface over a flashy GUI. Think of it as choosing a sports car over a luxury sedan—more powerful, even if it takes a bit more skill to drive.

**Why CLI rules:**
- ⌨️ Faster development cycle
- 🤖 Easier automation and scripting
- 💻 Lower resource requirements
- 🧰 Integrates better with developer workflows

**The compromises:**
- Less intuitive for non-technical users
- Limited visual feedback
- Requires terminal access

## 🤖 LLM Selection: Choosing Our AI Brain

### Model Choice: OpenAI GPT-4o-mini
We selected OpenAI's GPT-4o-mini model as our AI workhorse for generating high-quality ad campaigns while keeping costs reasonable. This model offers an excellent balance between performance and affordability.

**Why this model won our hearts:**
- 💰 Most cost-effective of the GPT-4 class models
- 🧠 Strong reasoning capabilities for ad campaign creation
- 📊 Good understanding of advertising concepts and best practices
- 🧩 Reliable JSON output formatting with the response_format parameter
- 🎯 Effective reasoning for ad creative and targeting choices
- ⚡ Faster inference speeds than larger models

**The alternatives we considered:**

1. **GPT-4o-mini vs. Other GPT-4 Variants:**
   - While full GPT-4 models offer slightly better reasoning, the cost difference wasn't justified
   - GPT-4o-mini delivers excellent quality at a fraction of the cost of GPT-4 Turbo
   - The cost savings can be redirected to campaign spending or other business needs

2. **GPT-4o-mini vs. GPT-3.5-Turbo:**
   - GPT-4o-mini offers better reasoning capabilities than GPT-3.5 models
   - The slight premium over GPT-3.5-Turbo is justified by better campaign performance
   - More consistent and reliable outputs for complex marketing tasks

3. **API vs. Local Models:**
   - Using OpenAI's API means no infrastructure headaches
   - API costs are predictable and scale with usage
   - Trade-off: dependency on external service vs. simplicity

4. **Other models we tested:**
   - Claude: Good capabilities but higher cost than GPT-4o-mini

### Embedding Model
For our vector embeddings, we use OpenAI's text-embedding-ada-002 model, which provides:
- 1536-dimensional vectors for accurate semantic search
- Great balance of performance and cost for embeddings
- Compatibility with our Pinecone vector database configuration

## 📝 Code Documentation: Our Love Letter to Future Developers

Documentation isn't just a necessity—it's an act of kindness to future developers (including future you!). Here's how we show the love:

### 1. Function and Class Documentation: The Map to Our Code
Every function, method, and class includes:
- ✨ Clear docstrings explaining purpose and functionality
- 📋 Parameter descriptions with types
- 🔙 Return value descriptions with types
- 🔍 Examples for complex functions

```python
def add_document(self, text: str, metadata: Dict[str, Any]) -> bool:
    """Add a document to the vector store.
    
    Args:
        text: The document text
        metadata: Metadata for the document
            
    Returns:
        bool: Success status
    """
```

### 2. Module-Level Documentation: The Big Picture
Each module includes:
- 🖼️ Description of the module's purpose
- 🧩 Overview of main classes/functions
- 🔍 Usage examples where appropriate

### 3. Inline Comments: The Secret Sauce
Strategic inline comments explain:
- 🧠 Complex algorithms or logic
- 📊 Non-obvious business rules
- ⚡ Performance considerations
- 🛡️ Error handling strategies

### 4. Type Annotations: Our Safety Net
Comprehensive type hints:
- 📌 All function parameters and return values
- 🧱 Complex data structures
- 🔧 Custom type definitions where needed

### 5. Code Structure: Our Zen Garden
- 🧹 Consistent style following PEP 8
- 🏗️ Logical organization of functionality
- 🧩 Clear separation of concerns
- 📝 Descriptive variable and function names

## 🌟 Features

- 🧠 RAG-enhanced LLM for campaign generation based on Meta Ads best practices
- 🔍 Query interface for retrieving marketing expertise from our knowledge base
- 🔗 Integration capability with Meta Ads API
- 💾 Pinecone vector database for lightning-fast knowledge retrieval
- 🧪 Error handling with retry mechanisms for API calls
- 📊 Campaign specification validation

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Pinecone API key (free tier works for testing)
- Meta Ads API credentials (for actual campaign creation)

## 🚀 Setup in 5 Minutes or Less

### 1. Clone this marketing magic

```bash
git clone <repository-url>
cd atomicads
```

### 2. Create a cozy virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the ingredients

```bash
pip install -r requirements.txt
```

### 4. Add your secret sauce (API keys)

Create a `.env` file in the project root:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here

# Pinecone settings
PINECONE_INDEX=ad-campaign-knowledge

# Meta Ads settings
META_APP_ID=your_meta_app_id
META_APP_SECRET=your_meta_app_secret
META_ACCESS_TOKEN=your_meta_access_token
META_AD_ACCOUNT_ID=your_ad_account_id
META_BUSINESS_ID=your_business_id

# Python path settings
PYTHONPATH=.
```

### 5. Feed the AI brain

```bash
python scripts/ingest_knowledge_base.py --reset
```

This magical command:
- Creates a Pinecone index (if it doesn't exist) with 1536 dimensions for OpenAI embeddings
- Resets existing vectors (if using --reset)
- Processes and chunks our marketing knowledge from the data/knowledge_base directory
- Creates embeddings using OpenAI's text-embedding-ada-002
- Stores everything in Pinecone for lightning-fast retrieval

## 🎮 Usage: Let's Make Some Ads!

### Ask Marketing Questions

Curious about Meta ad best practices? Just ask:

```bash
./run_query.sh "What's the ideal image size for Meta carousel ads?"
```

This runs the `scripts/query_knowledge_base.py` script with proper PYTHONPATH settings.

### Create a Campaign from a Brief

Generate a campaign from our example brief (or create your own):

```bash
python src/main.py create-campaign --input examples/campaign_brief.json
```

### Send It Live to Meta

Ready to make it real? Add the execute flag:

```bash
python src/main.py create-campaign --input examples/campaign_brief.json --execute
```

### Save Your Campaign for Later

Want to review before publishing?

```bash
python src/main.py create-campaign --input examples/campaign_brief.json --output my_campaign.json
```

## 💻 Campaign Logic: How the Magic Happens

Here's how AtomicAds creates your campaigns:

1. **Knowledge Retrieval**: We search our vector database for relevant Meta Ads best practices based on your brief
2. **Context Formation**: We format these documents into a context the LLM can understand
3. **Campaign Generation**: The LLM (GPT-4o-mini) creates a campaign spec based on your brief and the retrieved context
4. **Validation**: We check the campaign against Meta Ads API requirements
5. **Execution**: If all looks good (and you gave the green light), we create it via the Meta Ads API

Your campaign follows Meta's structure:
- **Campaign**: Top-level container defining objective and budget
- **Ad Set**: Targeting, optimization goals, and budget details
- **Ad**: Creative content and call-to-action

## 📂 Project Structure: The Blueprint

```
atomicads/
├── data/                        # The knowledge vault
│   └── knowledge_base/         
│       └── meta_ads_best_practices.md
├── examples/                    # Example inputs
│   └── campaign_brief.json     
├── scripts/                     # Utility scripts
│   ├── ingest_knowledge_base.py # Process and embed knowledge
│   └── query_knowledge_base.py  # Query the knowledge base
├── screenshots/                 # Example query outputs
│   └── query_*.txt              # Sample query responses
├── src/                         # Core code
│   ├── api/                     # API integrations
│   │   └── meta_ads_api.py      # Meta Ads API client
│   ├── config/                  # Configuration
│   │   └── config.py            # App configuration
│   ├── core/                    # Business logic
│   │   └── rag_service.py       # RAG implementation
│   ├── database/                # Data storage
│   │   └── vector_store.py      # Pinecone interface
│   ├── models/                  # AI models
│   │   └── openai_service.py    # OpenAI API client
│   ├── ui/                      # User interfaces
│   │   └── cli.py               # Command-line interface
│   └── utils/                   # Utilities
│       └── validators.py        # Campaign validation
│   └── main.py                  # Entry point
├── run_query.sh                 # Helper script
├── requirements.txt             # Dependencies
└── README.md                    # You are here! 👋
```

## 📊 Limitations and Cost Considerations

### What to Watch Out For

1. **API Dependencies**: 
   - We rely on OpenAI, Pinecone, and Meta APIs
   - They can have rate limits, downtime, or spec changes

2. **Knowledge Constraints**:
   - Our AI is only as good as our knowledge base
   - Currently focused on basic Meta Ads best practices

3. **Creative Limitations**:
   - No image or video generation (yet!)
   - Text-based creative elements only

4. **Targeting Simplifications**:
   - Streamlined targeting model compared to full Meta capabilities
   - Limited support for custom audiences

5. **Error Handling**:
   - Basic error handling for API failures with retry mechanisms
   - May need human help for complex errors

### What It'll Cost You

1. **OpenAI API**:
   - Text embeddings (text-embedding-ada-002): ~$0.0001 per 1K tokens
   - GPT-4o-mini: ~$0.0015 per 1K input tokens, ~$0.0045 per 1K output tokens
   - Typical campaign generation: $0.03-$0.15
   - Knowledge base queries: ~$0.01-$0.05 per query

2. **Pinecone**:
   - Free tier works for testing (100K vectors)
   - Standard tier: ~$70/month if you scale up
   - Our implementation uses ~5-10MB of vector storage

3. **Meta Ads**:
   - API usage is free
   - Your ad spend is determined by your campaign budget
   - We suggest starting with $10-$30/day testing budgets

## 🛠️ Future Improvements: The Roadmap

Here's what's on our radar:

1. 📚 Expand the knowledge base with more Meta Ads documentation
2. 🌐 Add support for Google Ads, TikTok, and LinkedIn
3. 🖼️ Implement AI image generation for creative content
4. 🧪 Add A/B testing automation
5. 📊 Build performance monitoring and reporting

## 🙏 Acknowledgements

Huge thanks to:
- Meta for their comprehensive Ads API documentation
- OpenAI for their powerful GPT-4o-mini and embedding models
- Pinecone for making vector search a breeze
- Coffee for making this project possible ☕

---

Made with ❤️ and a healthy dose of AI magic. Have questions? Open an issue or reach out! # atomicads-ai-engineer-assignment-Aryan-Gadroo
