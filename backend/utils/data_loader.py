"""
Data loader utility for downloading and processing H&M dataset from S3.
This module handles the initial data pipeline from S3 to local storage.
"""
import os
import boto3
from typing import Optional, List
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Handles downloading and processing data from S3.
    
    This class provides methods to:
    - Download files from S3 bucket
    - Process raw CSV files into optimized parquet format
    - Create aggregated views for analytics
    """
    
    def __init__(self, bucket_name: str = "kumo-public-datasets", prefix: str = "hm_with_images/"):
        """
        Initialize DataLoader with S3 configuration.
        
        Args:
            bucket_name: S3 bucket name containing the dataset
            prefix: S3 key prefix for the dataset files
        """
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize S3 client for public bucket (no credentials needed)
        try:
            from botocore import UNSIGNED
            from botocore.config import Config
            # Configure for anonymous (unsigned) access to public bucket
            self.s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
            logger.info("S3 client initialized for public bucket access (no credentials required)")
        except Exception as e:
            logger.warning(f"Could not initialize S3 client: {e}")
            self.s3_client = None
    
    def list_s3_files(self, max_files: int = 10, prefix_override: str = None) -> List[str]:
        """
        List files available in the S3 bucket.
        
        Args:
            max_files: Maximum number of files to list
            prefix_override: Optional prefix to override the default
            
        Returns:
            List of S3 keys
        """
        if not self.s3_client:
            logger.error("S3 client not initialized")
            return []
        
        try:
            prefix = prefix_override if prefix_override else self.prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_files
            )
            
            files = [obj['Key'] for obj in response.get('Contents', [])]
            logger.info(f"Found {len(files)} files in S3 with prefix '{prefix}'")
            return files
        except Exception as e:
            logger.error(f"Error listing S3 files: {e}")
            return []
    
    def download_file(self, s3_key: str, local_filename: Optional[str] = None) -> Optional[Path]:
        """
        Download a single file from S3 to local storage.
        
        Args:
            s3_key: S3 object key
            local_filename: Optional local filename (defaults to basename of s3_key)
            
        Returns:
            Path to downloaded file or None if failed
        """
        if not self.s3_client:
            logger.error("S3 client not initialized")
            return None
        
        if not local_filename:
            local_filename = os.path.basename(s3_key)
        
        local_path = self.data_dir / local_filename
        
        try:
            logger.info(f"Downloading {s3_key} to {local_path}")
            self.s3_client.download_file(self.bucket_name, s3_key, str(local_path))
            logger.info(f"Successfully downloaded {local_filename}")
            return local_path
        except Exception as e:
            logger.error(f"Error downloading {s3_key}: {e}")
            return None
    
    def process_transactions(self, csv_path: Path) -> pd.DataFrame:
        """
        Process transaction data and create sales aggregations.
        
        Args:
            csv_path: Path to transactions CSV file
            
        Returns:
            Processed DataFrame with sales data
        """
        logger.info(f"Processing transactions from {csv_path}")
        
        # Read CSV with appropriate dtypes
        df = pd.read_csv(csv_path)
        
        # Convert date column if exists
        if 't_dat' in df.columns:
            df['t_dat'] = pd.to_datetime(df['t_dat'])
        
        logger.info(f"Loaded {len(df)} transactions")
        return df
    
    def create_product_index(self, articles_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a searchable product index from articles data.
        
        Args:
            articles_df: DataFrame containing product/article information
            
        Returns:
            Processed product index DataFrame
        """
        logger.info("Creating product index")
        
        # Select relevant columns for search
        # Typical H&M dataset has: article_id, product_code, prod_name, product_type_name, etc.
        product_cols = [col for col in articles_df.columns if col in [
            'article_id', 'prod_name', 'product_type_name', 'product_group_name',
            'colour_group_name', 'perceived_colour_value_name', 'department_name',
            'index_name', 'section_name', 'garment_group_name', 'detail_desc'
        ]]
        
        products = articles_df[product_cols].copy()
        logger.info(f"Created index with {len(products)} products")
        
        return products
    
    def aggregate_sales_by_product(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate sales data by product and date for time series analysis.
        
        Args:
            transactions_df: Raw transaction data
            
        Returns:
            Aggregated sales DataFrame
        """
        logger.info("Aggregating sales by product")
        
        # Group by product and date
        if 't_dat' in transactions_df.columns and 'article_id' in transactions_df.columns:
            sales_agg = transactions_df.groupby(['article_id', 't_dat']).agg({
                'price': ['sum', 'mean', 'count']
            }).reset_index()
            
            sales_agg.columns = ['article_id', 'date', 'total_revenue', 'avg_price', 'units_sold']
            
            logger.info(f"Created {len(sales_agg)} sales records")
            return sales_agg
        else:
            logger.warning("Required columns not found for aggregation")
            return pd.DataFrame()
    
    def save_processed_data(self, df: pd.DataFrame, filename: str):
        """
        Save processed DataFrame to parquet format for fast loading.
        
        Args:
            df: DataFrame to save
            filename: Output filename (without extension)
        """
        output_path = self.data_dir / f"{filename}.parquet"
        df.to_parquet(output_path, index=False)
        logger.info(f"Saved processed data to {output_path}")


def load_or_download_data():
    """
    Main function to load data from local storage or download from S3 if needed.
    This is called during application startup.
    """
    loader = DataLoader()
    
    # Check if processed data already exists
    products_path = loader.data_dir / "products.parquet"
    sales_path = loader.data_dir / "sales.parquet"
    
    if products_path.exists() and sales_path.exists():
        logger.info("Using existing processed data")
        return
    
    logger.info("Processed data not found, will need to download and process")
    # Note: Actual download will be triggered separately to avoid blocking startup

