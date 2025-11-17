# Setup Guide - ShopSight Analytics

Complete instructions for setting up and running the ShopSight demo locally.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher**
- **Node.js 18 or higher**
- **OpenAI API key** (for LLM features)
- **No AWS credentials needed** (S3 bucket is public)
- **~100MB free disk space** for data files

## 🏗️ Tech Stack

### Backend (Python + FastAPI)
- FastAPI for REST API
- OpenAI GPT-4 for natural language processing and insights
- pandas + pyarrow for data processing
- boto3 for S3 data access
- uvicorn as ASGI server

### Frontend (React + Vite)
- React 18 with Vite for fast development
- Tailwind CSS for styling
- Recharts for data visualization
- Axios for API communication

---

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd shopsight-kumo-ishaan
```

---

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Create `.env` file:**

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

> **Note:** If you don't have an OpenAI API key, the demo will still work with fallback templates (search uses keyword matching, insights use templates).

---

### Step 3: Download and Process Data

This step downloads real H&M transaction data from S3:

```bash
# Make sure you're in the backend directory and venv is activated
python scripts/download_data.py
```

**What this does:**

1. Downloads H&M articles catalog from S3 (~3 MB)
2. Downloads transaction parquet files (~50-100 MB total)
3. **Intelligently samples ~150 products** using diverse category sampling
4. Processes and aggregates sales data by product and date
5. Saves optimized parquet files: `data/products.parquet` and `data/sales.parquet`

**Expected output:**

```
INFO: Looking for articles and transaction files in S3...
INFO: ✓ Found articles file: hm_with_images/articles/articles.parquet
INFO: ✓ Found transaction file: hm_with_images/transactions/part-00001.parquet
INFO: ✓ Found transaction file: hm_with_images/transactions/part-00002.parquet
...
INFO: Successfully downloaded 10 transaction files
INFO: Loaded 1,000,000 transactions for diverse category sampling
INFO: Sampled 150 products across 20 categories
INFO: Created 44,513 aggregated sales records
INFO: Filtered product catalog to 150 products with sales data
INFO: Successfully downloaded and processed S3 data!
```

**Sampling Strategy:**

The script samples the **top 10 products from EACH category** (shoes, bags, blazers, etc.) to ensure:
- ✅ Diverse product types for better demo coverage
- ✅ Natural language search works across categories
- ✅ More realistic analytics showcase
- ✅ Manageable dataset size (~20K sales records)

**Time:** ~2-3 minutes depending on your internet connection

---

### Step 4: Start the Backend Server

```bash
# Make sure you're in the backend directory and venv is activated
uvicorn main:app --reload --port 8000
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ Backend is now running at `http://localhost:8000`

**API Documentation:** Visit `http://localhost:8000/docs` for interactive API docs

---

### Step 5: Frontend Setup

Open a **new terminal window** (keep backend running):

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected output:**

```
  VITE v4.x.x  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ Frontend is now running at `http://localhost:5173`

---

## ✅ Verify Installation

1. Open your browser to `http://localhost:5173`
2. You should see the ShopSight Analytics dashboard
3. Try searching for "belt" or "bag"
4. Select a product to see sales charts and AI insights

---

## 🧪 Testing the Application

### Manual Testing Flow

1. **Search for a product**: Try queries like:
   - "belt" (basic search)
   - "I need a comfortable bag" (natural language - shows LLM!)
   - "boots"
   - "blazer"

2. **Select a product** from the dropdown

3. **Observe the dashboard panels**:
   - ✅ Sales chart shows 90 days of historical data
   - ✅ Forecast chart shows 30-day prediction
   - ✅ AI insights panel generates analysis (with GPT) or templates (without)
   - ✅ Customer segments display buyer personas

### Sample Queries to Try

**Basic Searches:**
- `belt` - accessories
- `bag` - handbags
- `boots` - footwear
- `blazer` - formal wear
- `bra` - intimates

**Natural Language Searches (Shows LLM!):**
- `I need a comfortable bag for everyday use`
- `stylish belt for jeans`
- `warm winter accessories`
- `comfortable shoes for walking`

> The natural language queries demonstrate the LLM's ability to understand context and extract relevant search terms beyond simple keyword matching.

---

## 📊 System Architecture

```
┌─────────────────┐
│   React Frontend │
│   (Vite + Tailwind)│
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│  FastAPI Backend │
│  (Python 3.10+)  │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────────┐
    ↓         ↓          ↓            ↓
┌────────┐ ┌──────┐ ┌────────┐ ┌──────────┐
│Analytics│ │Search│ │Forecast│ │Segments  │
│Service │ │Service│ │Service │ │Service   │
└────┬───┘ └───┬──┘ └────────┘ └──────────┘
     │         │
     ↓         ↓
┌─────────────────┐      ┌──────────────┐
│  H&M Dataset    │      │  OpenAI API  │
│  (Parquet files)│      │  (GPT-4)     │
└─────────────────┘      └──────────────┘
```

---

## 🎯 Next Steps

Once everything is running:

1. **Try the sample queries** to see LLM search in action
2. **Select different products** to see varying sales patterns
3. **Check the API docs** at `http://localhost:8000/docs`
4. **Look at the code** in `backend/services/` to understand the architecture

---

## 📝 Environment Variables

### Backend `.env` file:

```bash
# Required for LLM features (search term extraction, insights generation)
OPENAI_API_KEY=your_openai_api_key_here

# Optional - defaults shown
AWS_REGION=us-east-1
S3_BUCKET_NAME=kumo-public-datasets
S3_PREFIX=hm_with_images/
```

### Frontend (no env vars needed)

All configuration is in `frontend/src/config.js` if you need to change the API URL.

---

## ✅ Quick Start Summary

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev

# Open browser to http://localhost:5173
```

That's it! Your ShopSight demo should be running. 🚀

