# Data Setup Scripts

## download_data.py

This script downloads and processes the H&M dataset from S3.

### Usage

```bash
cd backend
python scripts/download_data.py
```

### What it does

1. **Attempts to download from S3**: Tries to connect to `s3://kumo-public-datasets/hm_with_images/`
2. **Falls back to sample data**: If S3 is unavailable, generates realistic sample data
3. **Processes and saves**: Creates optimized parquet files in `backend/data/`
   - `products.parquet`: Product catalog with searchable fields
   - `sales.parquet`: Aggregated sales data by product and date

### Sample Data

If S3 download fails, the script generates:
- 10 sample products (shoes, clothing, accessories)
- 120 days of sales history
- Realistic patterns (weekend boosts, trends, seasonality)

This is sufficient for demo purposes and testing the application.

### Requirements

- boto3 (for S3 access)
- pandas
- pyarrow

All included in `requirements.txt`.

