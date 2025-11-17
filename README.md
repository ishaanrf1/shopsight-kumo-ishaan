# ShopSight Analytics

An AI-powered e-commerce analytics dashboard that provides intelligent product search, historical sales analysis, demand forecasting, and customer segmentation insights.

## 📋 Table of Contents

- [Thought Process & Approach](#thought-process--approach)
- [Assumptions Made](#assumptions-made)
- [Quick Start](#quick-start)
- [Features](#features)
- [What's Real vs. Mocked](#whats-real-vs-mocked)
- [Testing the Application](#testing-the-application)
- [Gaps & Future Work](#gaps--future-work)
- [Screenshots](#screenshots)
- [Setup Guide](./SETUP.md) - Detailed installation instructions

---

## 💭 Thought Process & Approach

### What Was Prioritized

**Core Flow: Search → Sales Analysis → AI Insights**

The focus was on delivering one end-to-end flow that's fully functional with real data:
1. **Natural language product search** using LLM
2. **Historical sales visualization** from real H&M transactions
3. **AI-generated insights** analyzing sales patterns

**Why This Flow?**
- Demonstrates both data processing AND LLM capabilities
- Most valuable for a customer demo (shows immediate business value)
- Allows me to showcase modern architecture (FastAPI + React)

### Key Decisions

**1. Diverse Category Sampling Strategy**
- Sample the top 10 products from EACH category (shoes, bags, blazers, etc.)
- **Why:** Ensures users can search for different product types and find results
- **Result:** Better demo experience, shows LLM search works across categories

**2. FastAPI + React Architecture**
- Separated backend and frontend for clean architecture
- **Why:** Production-ready approach with clear separation of concerns
- **Trade-off:** Takes longer to set up but demonstrates better engineering practices

**3. Real Transaction Data**
- Downloads and processes actual H&M transaction data from S3
- **Why:** Provides authentic insights and realistic sales patterns
- **Trade-off:** Larger initial download, but ensures high data quality

**4. Mocked Forecasting & Segmentation**
- Used algorithms and templates instead of ML models
- **Why:** Time constraints - shows the UX without building complex ML pipeline
- **Clearly documented:** What's real vs mocked

---

## 📝 Assumptions Made

1. **Dataset Access**
   - H&M dataset in `s3://kumo-public-datasets/hm_with_images/` is publicly accessible
   - No AWS credentials needed (confirmed - bucket allows unsigned requests)

2. **Data Sampling**
   - 150 products is sufficient for demo purposes
   - Diverse category sampling provides good product variety
   - Users will search for different product types, not just one category

3. **LLM Integration**
   - OpenAI API access is available (user provides API key)
   - GPT-4 or GPT-3.5-turbo is sufficient for search term extraction and insights
   - **Graceful fallbacks:** If API fails, system falls back to keyword extraction for search and template-based insights (demo still works without API key)

4. **Time Period**
   - 90 days of historical sales is sufficient for trend analysis
   - 30-day forecast horizon is reasonable for retail planning

5. **User Behavior**
   - Users will search using natural language (e.g., "comfortable bags")
   - Single-product analysis is the core use case for MVP
   - Users want quick insights and actionable recommendations

6. **Technical Environment**
   - Local development setup (Python 3.10+, Node.js 18+)
   - Modern browsers (Chrome, Firefox, Safari)
   - Reasonable internet connection for S3 downloads (~100MB)

7. **Business Context**
   - This is a seller/merchant-facing tool (not end-customer facing)
   - Focus on actionable insights (trends, performance) over vanity metrics
   - Mocked forecasts and segments are acceptable if clearly labeled

---

## 🚀 Quick Start

> **Full setup instructions:** See [SETUP.md](./SETUP.md) for detailed installation and troubleshooting guide.

**Prerequisites:** Python 3.10+, Node.js 18+, OpenAI API key (optional)

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py  # Downloads real H&M data (~2-3 min)
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm install && npm run dev

# Open http://localhost:5173
```

### Tech Stack

- **Backend:** FastAPI, Python 3.10+, pandas, OpenAI GPT-4, boto3
- **Frontend:** React 18, Vite, Tailwind CSS, Recharts
- **Data:** Real H&M transactions from S3 (public bucket)

## ✨ Features

### 1. Natural Language Product Search ✅ REAL
- Type queries like "running shoes" or "winter jacket"
- LLM extracts search intent and product attributes
- Returns matching products from H&M dataset

### 2. Historical Sales Visualization ✅ REAL
- Line charts showing revenue and units sold
- 90-day historical data from actual transactions
- Interactive tooltips with daily breakdowns

### 3. AI-Powered Insights ✅ REAL
- GPT-4 analyzes sales patterns and generates human-readable insights
- Identifies trends, anomalies, and opportunities
- Confidence scores for each insight

### 4. Demand Forecasting ⚠️ MOCKED
- 30-day ahead predictions with confidence intervals
- Based on historical patterns using moving averages
- Would use ML models (ARIMA, Prophet, etc.) in production

### 5. Customer Segmentation ⚠️ MOCKED
- Buyer personas with characteristics and purchase likelihood
- Generated based on product category
- Would use actual customer data and clustering in production


## 📊 What's Real vs. Mocked

### ✅ Real (End-to-End Working)

| Feature | Implementation | Data Source |
|---------|---------------|-------------|
| Product Search | LLM-powered query understanding | H&M dataset + OpenAI GPT-4 |
| Sales History | Actual transaction aggregation | Real H&M transaction data from S3 |
| AI Insights | Natural language generation | OpenAI GPT-4 analyzing real sales patterns |
| API Integration | Full REST API | FastAPI with proper error handling |

### ⚠️ Mocked (Realistic but Simulated)

| Feature | Current Implementation | Production Approach |
|---------|----------------------|---------------------|
| Demand Forecast | Moving average with trend | ML models (ARIMA, Prophet, LSTM) |
| Customer Segments | Template-based personas | K-means clustering on customer data |
| Confidence Intervals | Simple percentage-based | Statistical models (bootstrap, etc.) |

## 🎨 Key Design Decisions

### 1. Diverse Category Sampling Strategy
- **Why**: Better demo experience than just "top N by revenue"
- **How**: Sample top 10 products from EACH category (shoes, jackets, dresses, etc.)
- **Benefit**: 
  - Users can search for different product types and find results
  - Shows analytics across diverse categories
  - More realistic than 150 similar products
  - Reduces data from 725K to ~20K records while maintaining quality

### 2. LLM as Search Orchestrator with Fallbacks
- **Why**: Makes search more natural and forgiving
- **How**: GPT-4 extracts product attributes from queries
- **Fallback Strategy**: 
  - If API key missing: Uses keyword extraction (splits query into words)
  - If API call fails: Catches exception and falls back to keyword extraction
  - For insights: Falls back to template-based insights with trend analysis
  - **Result:** Demo works even without OpenAI API key (just less sophisticated)

### 3. Pandas for Data Processing
- **Why**: Fast, efficient, and familiar for data work
- **How**: Parquet files for optimized storage and loading
- **Benefit**: Can handle millions of rows easily

### 4. FastAPI for Backend
- **Why**: Modern, fast, async-capable, great docs
- **How**: Service layer pattern for clean separation
- **Benefit**: Easy to test and extend

### 5. Mocked Forecasting
- **Why**: Time constraint + no ML infrastructure needed for demo
- **How**: Simple algorithms that produce realistic outputs
- **Benefit**: Shows the UX without complex ML setup

### 6. Component-Based Frontend
- **Why**: Reusable, testable, easy to understand
- **How**: Each panel is independent with clear props
- **Benefit**: Can be explained and modified easily

## 📁 Project Structure

```
shopsight-kumo-ishaan/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Python dependencies
│   ├── data/                      # Processed data files
│   │   ├── products.parquet
│   │   └── sales.parquet
│   ├── services/                  # Business logic
│   │   ├── analytics_service.py   # Sales data processing
│   │   ├── llm_service.py         # OpenAI integration
│   │   ├── search_service.py      # Product search
│   │   ├── forecast_service.py    # Demand forecasting (mocked)
│   │   └── segmentation_service.py # Customer segments (mocked)
│   ├── routes/                    # API endpoints
│   │   ├── search.py              # POST /api/search
│   │   ├── products.py            # GET /api/products/{id}/*
│   │   └── insights.py            # POST /api/insights
│   ├── utils/
│   │   └── data_loader.py         # S3 and data processing
│   └── scripts/
│       └── download_data.py       # Data setup script
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main dashboard
│   │   ├── components/
│   │   │   ├── SearchBar.jsx      # Natural language search
│   │   │   ├── SalesChart.jsx     # Historical sales chart
│   │   │   ├── ForecastChart.jsx  # Demand forecast chart
│   │   │   ├── InsightsPanel.jsx  # AI insights display
│   │   │   └── SegmentsPanel.jsx  # Customer segments
│   │   └── services/
│   │       └── api.js             # API client
│   ├── package.json
│   └── vite.config.js
├── PLAN.md                        # Implementation plan
└── README.md                      # This file
```

## 🔧 API Endpoints

### Search
```
POST /api/search
Body: { "query": "running shoes", "limit": 10 }
Response: { "query": "...", "results": [...], "count": 10 }
```

### Product Sales
```
GET /api/products/{article_id}/sales?days=90
Response: { "article_id": "...", "data": [...], "total_revenue": 1234.56 }
```

### Demand Forecast
```
GET /api/products/{article_id}/forecast?days=30
Response: { "article_id": "...", "forecast": [...], "method": "..." }
```

### Customer Segments
```
GET /api/products/{article_id}/segments
Response: { "article_id": "...", "segments": [...] }
```

### AI Insights
```
POST /api/insights
Body: { "article_id": "..." }
Response: { "article_id": "...", "summary": "...", "insights": [...] }
```

## 🧪 Testing the Application

### Manual Testing Flow

1. **Start both servers** (backend on :8000, frontend on :5173)
2. **Search for a product**: Try "shoes" or "jacket"
3. **Select a product** from the dropdown
4. **Observe the dashboard**:
   - Sales chart should show 90 days of data
   - Forecast chart shows 30-day prediction
   - AI insights panel generates analysis
   - Customer segments display buyer personas

### Sample Queries to Try

**Basic Searches:**
- "belt" - accessories
- "bag" - handbags
- "boots" - footwear
- "blazer" - formal wear
- "bra" - intimates

**Natural Language Searches (Shows LLM!):**
- "I need a comfortable bag for everyday use"
- "stylish belt for jeans"
- "warm winter accessories"
- "comfortable shoes for walking"

> The natural language queries demonstrate the LLM's ability to understand context and extract relevant search terms beyond simple keyword matching.

---

## 🔧 Gaps & Future Work

### What's Missing (Intentionally Scoped Out)

**Note:** These features were consciously deprioritized to focus on delivering a working end-to-end flow with real data and LLM integration.

1. **Conversational Chat Assistant**
   - **What it would do:** Allow users to ask follow-up questions like "Why are sales declining?" or "What products pair well with this?"
   - **Why not included:** The core value is in the analytics dashboard. A chat interface would be a nice-to-have but doesn't demonstrate additional technical capability beyond the existing LLM integration for search and insights
   - **How to implement:** Add chat component with message history, use LLM as an orchestrator to parse questions and route to appropriate APIs (search, sales, forecast), return conversational responses

2. **Product Comparison View**
   - **What it would do:** Compare 2-3 products side-by-side with overlaid charts and diff metrics
   - **Why not included:** Single-product deep-dive provides more value for merchants than surface-level comparisons. Most use cases focus on understanding one product's performance deeply
   - **How to implement:** Add multi-select to search results, create grid layout with synchronized time-series charts, add delta calculations for key metrics

3. **Agent-Based Query Orchestrator**
   - **What it would do:** Allow complex queries like "Show me my top 5 products with declining sales" or "Which accessories are underperforming?" where the LLM determines which data to fetch and how to filter
   - **Why not included:** The current LLM integration focuses on search term extraction and insight generation. An agent pattern requires defining available tools/functions and prompt engineering for reliable orchestration
   - **How to implement (simpler than it sounds):**
     - Define "tools" the agent can use: `get_sales_data(category, time_range)`, `get_trend(article_id)`, `search_products(filters)`
     - Use OpenAI function calling to let LLM choose which tools to invoke
     - LLM sees query "declining accessories" → decides to call `search_products(category='accessories')` then `get_trend()` for results
     - Execute the function calls, pass results back to LLM for synthesis
     - **Key insight:** With a database, these "tools" are just SQL queries. The agent doesn't need to call APIs for each product—it can request "all products where trend='declining' AND category='accessories'" in one query
     - Example flow: User asks "underperforming belts" → LLM calls `analyze_category_performance('belt')` → SQL aggregates data → LLM explains findings

4. **RFM Customer Segmentation**
   - **What it would do:** Cluster customers by Recency, Frequency, Monetary value and show actual buying patterns per segment
   - **Why not included:** The H&M dataset doesn't include customer IDs in the transaction data, so real segmentation isn't possible. Template personas show the UX without requiring additional data
   - **How to implement:** Add customer_id to transactions, calculate RFM scores, apply K-means clustering, profile each segment with demographics and behavior patterns

5. **Multi-User Authentication**
   - **What it would do:** User login, role-based permissions, saved searches/dashboards
   - **Why not included:** Demo is single-user focused. Authentication adds complexity without demonstrating analytics or LLM capabilities
   - **How to implement:** JWT-based auth with refresh tokens, role-based access control (RBAC), session management with Redis

### Performance & Scalability Improvements

If building for production, these would be added:

1. **Caching Layer**
   - Redis for frequently accessed products
   - Cache LLM responses for common queries
   - API response caching with TTL

2. **Database Migration**
   - Move from Parquet to PostgreSQL
   - Add proper indexes on article_id, date
   - Implement connection pooling

3. **Testing**
   - Unit tests for all services (pytest)
   - Integration tests for API endpoints
   - Frontend tests (Jest, React Testing Library)

4. **Monitoring & Observability**
   - Structured logging (structlog)
   - Error tracking (Sentry)
   - Performance monitoring (New Relic, DataDog)
   - API analytics

5. **Advanced LLM & Agent Features**
   - **Natural language to SQL:** User asks "What are my best-selling products this month?" → LLM generates SQL query → returns results with natural language explanation
   - **Smart recommendations:** LLM analyzes aggregate transaction patterns (via SQL) to suggest "products often bought together"
   - **Anomaly detection agent:** Automatically runs periodic SQL queries to detect unusual patterns, then uses LLM to explain and investigate causes
   - **Action recommendations:** Agent queries multiple data sources (sales trends, inventory levels, seasonal patterns) and suggests specific actions with reasoning
   - **Cross-category insights:** Single query compares performance across categories, LLM synthesizes findings into executive summary
   - **What-if scenarios:** "What if I increase price by 10%?" → agent adjusts forecast parameters and explains impact
   - **Streaming responses:** Real-time insight generation with progressive rendering for better UX

---

## 📸 Screenshots

### Search Interface
![Search Interface](./screenshots/search.png)
*Natural language product search with LLM-powered query understanding*

### Sales Analytics Dashboard
![Dashboard](./screenshots/dashboard.png)
*Historical sales visualization with 90-day trends*

### AI-Generated Insights
![AI Insights](./screenshots/insights.png)
*GPT-4 analyzing sales patterns and generating actionable insights*

### Forecast & Segments
![Forecast](./screenshots/forecast.png)
*30-day demand forecast and customer segmentation*

> **Note:** Screenshots to be added. For now, run the demo locally to see the interface.

---

## 📝 License

MIT

## 👤 Author

Built as a take-home exercise for Kumo AI
