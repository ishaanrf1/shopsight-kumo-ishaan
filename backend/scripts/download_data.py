"""
Script to download and process H&M dataset from S3.
Run this script once to set up the data for the application.

Usage:
    python scripts/download_data.py
"""
import sys
from pathlib import Path

# Add parent directory to path to import from utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import DataLoader
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_sales_for_products(products_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate sample sales data for real products.
    Used when we have product catalog but no transaction data.
    
    Args:
        products_df: DataFrame with product information
        
    Returns:
        Sales aggregation DataFrame
    """
    logger.info(f"Generating sample sales for {len(products_df)} products...")
    
    sales_records = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)
    
    # Use first 200 products to ensure we have coverage for searches
    # This gives us enough variety while keeping data size manageable
    sample_products = products_df.head(200) if len(products_df) > 200 else products_df
    
    for _, product in sample_products.iterrows():
        article_id = str(product['article_id'])  # Convert to string for consistency
        
        # Generate daily sales with some randomness
        base_sales = np.random.randint(5, 30)
        base_price = np.random.uniform(20, 150)
        
        current_date = start_date
        while current_date <= end_date:
            day_of_week = current_date.weekday()
            weekend_boost = 1.3 if day_of_week in [5, 6] else 1.0
            
            days_since_start = (current_date - start_date).days
            trend_factor = 1 + (np.random.uniform(-0.002, 0.003) * days_since_start)
            
            units = int(base_sales * weekend_boost * trend_factor * np.random.uniform(0.7, 1.3))
            price = base_price * np.random.uniform(0.95, 1.05)
            
            if units > 0:
                sales_records.append({
                    'article_id': str(article_id),
                    't_dat': current_date.strftime('%Y-%m-%d'),
                    'price': round(price, 2),
                    'units': units
                })
            
            current_date += timedelta(days=1)
    
    sales_df = pd.DataFrame(sales_records)
    
    # Aggregate
    sales_agg = sales_df.groupby(['article_id', 't_dat']).agg({
        'price': ['mean', lambda x: (x * sales_df.loc[x.index, 'units']).sum()],
        'units': 'sum'
    }).reset_index()
    
    sales_agg.columns = ['article_id', 'date', 'avg_price', 'total_revenue', 'units_sold']
    
    logger.info(f"Generated {len(sales_agg)} sales records for {len(sample_products)} products")
    return sales_agg


def create_sample_data():
    """
    Create sample data for demo purposes.
    This is used if S3 download fails completely or for quick testing.
    """
    logger.info("Creating sample data for demo...")
    
    # Sample products (fashion items)
    products_data = {
        'article_id': [
            '0108775001', '0108775002', '0108775003', '0108775004', '0108775005',
            '0108775006', '0108775007', '0108775008', '0108775009', '0108775010'
        ],
        'prod_name': [
            'Running Shoes', 'Winter Jacket', 'Casual Sneakers', 'Sports T-Shirt',
            'Yoga Pants', 'Denim Jeans', 'Summer Dress', 'Hoodie', 'Backpack', 'Baseball Cap'
        ],
        'product_type_name': [
            'Shoes', 'Jacket', 'Shoes', 'T-shirt', 'Pants',
            'Jeans', 'Dress', 'Sweater', 'Bag', 'Hat'
        ],
        'product_group_name': [
            'Footwear', 'Outerwear', 'Footwear', 'Activewear', 'Activewear',
            'Bottoms', 'Dresses', 'Tops', 'Accessories', 'Accessories'
        ],
        'colour_group_name': [
            'Black', 'Navy Blue', 'White', 'Red', 'Black',
            'Blue', 'Floral', 'Grey', 'Black', 'Navy'
        ],
        'department_name': [
            'Sport', 'Menswear', 'Sport', 'Sport', 'Sport',
            'Menswear', 'Ladieswear', 'Menswear', 'Accessories', 'Accessories'
        ]
    }
    
    products_df = pd.DataFrame(products_data)
    
    # Generate sample sales data (last 120 days)
    sales_records = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)
    
    for article_id in products_df['article_id']:
        # Generate daily sales with some randomness and trends
        base_sales = np.random.randint(5, 30)
        base_price = np.random.uniform(20, 150)
        
        current_date = start_date
        while current_date <= end_date:
            # Add some weekly seasonality and random variation
            day_of_week = current_date.weekday()
            weekend_boost = 1.3 if day_of_week in [5, 6] else 1.0
            
            # Add some trend (some products growing, some declining)
            days_since_start = (current_date - start_date).days
            trend_factor = 1 + (np.random.uniform(-0.002, 0.003) * days_since_start)
            
            units = int(base_sales * weekend_boost * trend_factor * np.random.uniform(0.7, 1.3))
            price = base_price * np.random.uniform(0.95, 1.05)  # Small price variations
            
            if units > 0:  # Only add if there were sales
                sales_records.append({
                    'article_id': article_id,
                    't_dat': current_date.strftime('%Y-%m-%d'),
                    'price': round(price, 2),
                    'units': units
                })
            
            current_date += timedelta(days=1)
    
    sales_df = pd.DataFrame(sales_records)
    
    # Aggregate sales by product and date
    sales_agg = sales_df.groupby(['article_id', 't_dat']).agg({
        'price': ['mean', lambda x: (x * sales_df.loc[x.index, 'units']).sum()],
        'units': 'sum'
    }).reset_index()
    
    sales_agg.columns = ['article_id', 'date', 'avg_price', 'total_revenue', 'units_sold']
    
    return products_df, sales_agg


def try_download_from_s3():
    """
    Attempt to download data from S3.
    Returns True if successful, False otherwise.
    """
    try:
        loader = DataLoader()
        
        logger.info("Looking for articles and transaction files in S3...")
        
        # Look specifically for articles files
        logger.info("Checking articles directory...")
        articles_files = loader.list_s3_files(max_files=10, prefix_override='hm_with_images/articles/')
        articles_file = None
        for f in articles_files:
            if f.endswith('.parquet'):
                articles_file = f
                logger.info(f"✓ Found articles file: {f}")
                break
        
        # Look specifically for transaction files
        logger.info("Checking transactions directory...")
        transaction_files_response = loader.list_s3_files(max_files=100, prefix_override='hm_with_images/transactions/')
        transaction_files = []
        for f in transaction_files_response:
            if f.endswith('.parquet'):
                transaction_files.append(f)
                logger.info(f"✓ Found transaction file: {f}")
        
        if not articles_file:
            logger.warning("Could not find articles parquet file")
            return False
        
        if not transaction_files:
            logger.warning("Could not find transaction parquet files - using sample data for sales")
            # Download articles and generate sample data
            articles_path = loader.download_file(articles_file, 'articles.parquet')
            if not articles_path:
                return False
            articles_df = pd.read_parquet(articles_path)
            products_df = loader.create_product_index(articles_df)
            sales_agg = generate_sample_sales_for_products(products_df)
            loader.save_processed_data(products_df, 'products')
            loader.save_processed_data(sales_agg, 'sales')
            return True
        
        logger.info(f"✓ Found {len(transaction_files)} transaction parquet files")
        
        # Download articles file
        logger.info("Downloading articles parquet file...")
        articles_path = loader.download_file(articles_file, 'articles.parquet')
        
        if not articles_path:
            logger.error("Failed to download articles file")
            return False
        
        # Process articles data
        logger.info("Processing articles...")
        articles_df = pd.read_parquet(articles_path)
        products_df = loader.create_product_index(articles_df)
        
        # Download all transaction files to a directory
        logger.info(f"Downloading {len(transaction_files)} transaction files...")
        transactions_dir = loader.data_dir / "transactions"
        transactions_dir.mkdir(exist_ok=True)
        
        downloaded_count = 0
        for trans_file in transaction_files:
            filename = trans_file.split('/')[-1]  # Get just the filename
            local_path = loader.download_file(trans_file, f'transactions/{filename}')
            if local_path:
                downloaded_count += 1
                logger.info(f"  Downloaded {downloaded_count}/{len(transaction_files)}: {filename}")
        
        if downloaded_count == 0:
            logger.warning("Failed to download any transaction files, generating sample data")
            sales_agg = generate_sample_sales_for_products(products_df)
        else:
            logger.info(f"Successfully downloaded {downloaded_count} transaction files")
            
            # Use pyarrow.dataset to efficiently read all parquet files
            try:
                import pyarrow.dataset as ds
                from collections import defaultdict
                
                logger.info("Reading transaction data using pyarrow dataset...")
                dataset = ds.dataset(str(transactions_dir), format="parquet")
                
                # STEP 1: First pass - Calculate revenue per product to identify top sellers
                logger.info("Analyzing product performance across categories...")
                product_revenue = defaultdict(float)
                
                for batch in dataset.to_batches(
                    columns=['article_id', 'price'], 
                    batch_size=100_000
                ):
                    df = batch.to_pandas()
                    grouped = df.groupby('article_id')['price'].sum()
                    for article_id, revenue in grouped.items():
                        product_revenue[int(article_id)] += float(revenue)
                
                logger.info(f"Analyzed {len(product_revenue):,} unique products")
                
                # STEP 2: Merge with product metadata to enable category-based sampling
                revenue_df = pd.DataFrame([
                    {'article_id': k, 'revenue': v} 
                    for k, v in product_revenue.items()
                ])
                products_with_revenue = products_df.merge(
                    revenue_df, 
                    on='article_id', 
                    how='inner'
                )
                
                # STEP 3: Sample diverse products across categories
                # Strategy: Take top sellers from EACH product type for variety
                logger.info("Selecting diverse products across categories...")
                selected_products = []
                products_per_category = 10  # Top 10 from each category
                
                # Group by product type and take top sellers from each
                for product_type, group in products_with_revenue.groupby('product_type_name'):
                    top_in_category = group.nlargest(products_per_category, 'revenue')
                    selected_products.extend(top_in_category['article_id'].tolist())
                    logger.info(f"  Selected {len(top_in_category)} {product_type} products")
                
                # Ensure we have a good number of products (aim for ~150)
                target_count = 150
                if len(selected_products) < target_count:
                    # Add more top sellers to reach target
                    remaining = target_count - len(selected_products)
                    all_top = products_with_revenue.nlargest(target_count + 50, 'revenue')
                    additional = all_top[~all_top['article_id'].isin(selected_products)]
                    selected_products.extend(additional['article_id'].head(remaining).tolist())
                    logger.info(f"  Added {remaining} additional top sellers")
                
                selected_products = selected_products[:target_count]
                logger.info(f"Final selection: {len(selected_products)} products across "
                          f"{products_with_revenue['product_type_name'].nunique()} categories")
                
                # STEP 4: Second pass - Process transactions for selected products only
                logger.info("Processing transactions for selected products...")
                all_transactions = []
                target_set = set(selected_products)
                batch_count = 0
                
                for batch in dataset.to_batches(
                    columns=['article_id', 't_dat', 'price'], 
                    batch_size=100_000
                ):
                    df = batch.to_pandas()
                    # Filter to only selected products
                    df = df[df['article_id'].isin(target_set)]
                    
                    if not df.empty:
                        all_transactions.append(df)
                        batch_count += 1
                        logger.info(f"  Processed batch {batch_count} ({len(df)} relevant transactions)")
                
                # Combine all batches
                transactions_df = pd.concat(all_transactions, ignore_index=True)
                logger.info(f"Loaded {len(transactions_df):,} transactions for {len(selected_products)} products")
                
                # Aggregate sales by product and date
                sales_agg = loader.aggregate_sales_by_product(transactions_df)
                logger.info(f"Created {len(sales_agg):,} aggregated sales records")
                
                # IMPORTANT: Filter products to only those with sales data
                # This prevents 404 errors when users select products without sales
                products_with_sales = sales_agg['article_id'].unique()
                products_df = products_df[products_df['article_id'].isin(products_with_sales)]
                logger.info(f"Filtered product catalog to {len(products_df)} products with sales data")
                
            except ImportError:
                logger.warning("pyarrow not available, falling back to pandas...")
                # Fallback: read first file only
                first_file = transactions_dir / transaction_files[0].split('/')[-1]
                transactions_df = pd.read_parquet(first_file)
                logger.info(f"Loaded {len(transactions_df):,} transactions from first file")
                sales_agg = loader.aggregate_sales_by_product(transactions_df)
        
        # Save processed data
        loader.save_processed_data(products_df, 'products')
        loader.save_processed_data(sales_agg, 'sales')
        
        logger.info("Successfully downloaded and processed S3 data!")
        return True
        
    except Exception as e:
        logger.error(f"Error downloading from S3: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def main():
    """Main function to download and process data."""
    logger.info("Starting data download and processing...")
    
    # Try to download from S3 first
    success = try_download_from_s3()
    
    if not success:
        logger.info("Falling back to sample data generation...")
        products_df, sales_agg = create_sample_data()
        
        # Save sample data
        loader = DataLoader()
        loader.save_processed_data(products_df, 'products')
        loader.save_processed_data(sales_agg, 'sales')
        
        logger.info("Sample data created successfully!")
    
    # Verify the data
    loader = DataLoader()
    products_path = loader.data_dir / "products.parquet"
    sales_path = loader.data_dir / "sales.parquet"
    
    if products_path.exists() and sales_path.exists():
        products = pd.read_parquet(products_path)
        sales = pd.read_parquet(sales_path)
        
        logger.info(f"\n{'='*60}")
        logger.info("✅ DATA SETUP COMPLETE!")
        logger.info(f"{'='*60}")
        logger.info(f"Products: {len(products)} items")
        logger.info(f"Sales records: {len(sales)} entries")
        logger.info(f"Date range: {sales['date'].min()} to {sales['date'].max()}")
        logger.info(f"Unique products with sales: {sales['article_id'].nunique()}")
        logger.info(f"{'='*60}\n")
        
        # Show sample products with key fields
        logger.info("📦 Sample Products (first 5):")
        logger.info("-" * 60)
        display_cols = [col for col in ['article_id', 'prod_name', 'product_type_name', 
                                         'product_group_name', 'department_name'] 
                        if col in products.columns]
        if display_cols:
            print(products[display_cols].head().to_string(index=False))
        else:
            print(products.head())
        
        # Show sample sales
        logger.info("\n💰 Sample Sales Data (first 5):")
        logger.info("-" * 60)
        print(sales.head().to_string(index=False))
        
        # Show some statistics
        logger.info("\n📊 Sales Statistics:")
        logger.info("-" * 60)
        logger.info(f"Total revenue: ${sales['total_revenue'].sum():,.2f}")
        logger.info(f"Total units sold: {sales['units_sold'].sum():,}")
        logger.info(f"Average daily revenue per product: ${sales['total_revenue'].mean():,.2f}")
        logger.info(f"{'='*60}\n")
        
        logger.info("🚀 Ready to go! Start the FastAPI server:")
        logger.info("   cd backend")
        logger.info("   uvicorn main:app --reload --port 8000")
        logger.info("")
    else:
        logger.error("Data files not found after processing!")
        sys.exit(1)


if __name__ == "__main__":
    main()

