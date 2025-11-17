"""
Analytics service for processing sales data and generating metrics.
Uses pandas for efficient data manipulation and aggregation.
"""
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for sales analytics and data processing.
    Loads data from parquet files and provides methods for querying and aggregating.
    """
    
    def __init__(self):
        """Initialize the analytics service and load data."""
        self.data_dir = Path(__file__).parent.parent / "data"
        self.products_df = None
        self.sales_df = None
        self.load_data()
    
    def load_data(self):
        """Load processed data from parquet files."""
        try:
            products_path = self.data_dir / "products.parquet"
            sales_path = self.data_dir / "sales.parquet"
            
            if products_path.exists() and sales_path.exists():
                self.products_df = pd.read_parquet(products_path)
                self.sales_df = pd.read_parquet(sales_path)
                
                # Ensure date column is datetime
                if 'date' in self.sales_df.columns:
                    self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
                
                logger.info(f"Loaded {len(self.products_df)} products and {len(self.sales_df)} sales records")
            else:
                logger.warning("Data files not found. Run scripts/download_data.py first.")
                self.products_df = pd.DataFrame()
                self.sales_df = pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.products_df = pd.DataFrame()
            self.sales_df = pd.DataFrame()
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search products by name, category, or other attributes.
        This is a simple text-based search; LLM enhancement happens in search_service.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching products
        """
        if self.products_df.empty:
            return []
        
        query_lower = query.lower()
        
        # Search across multiple columns
        search_columns = ['prod_name', 'product_type_name', 'product_group_name', 
                         'colour_group_name', 'department_name']
        
        # Filter columns that exist in the dataframe
        existing_columns = [col for col in search_columns if col in self.products_df.columns]
        
        # Create a combined search field
        if existing_columns:
            search_text = self.products_df[existing_columns].fillna('').astype(str).agg(' '.join, axis=1).str.lower()
            mask = search_text.str.contains(query_lower, na=False, regex=False)
            results = self.products_df[mask].head(limit)
        else:
            results = self.products_df.head(limit)
        
        return results.to_dict('records')
    
    def get_product_by_id(self, article_id: str) -> Optional[Dict]:
        """
        Get product details by article ID.
        
        Args:
            article_id: Product article ID
            
        Returns:
            Product dictionary or None if not found
        """
        if self.products_df.empty:
            return None
        
        # Try matching as string first, then as int if needed
        product = self.products_df[self.products_df['article_id'].astype(str) == str(article_id)]
        
        if product.empty:
            return None
        
        return product.iloc[0].to_dict()
    
    def get_sales_history(self, article_id: str, days: int = 90) -> Dict:
        """
        Get historical sales data for a product.
        
        Args:
            article_id: Product article ID
            days: Number of days of history to return
            
        Returns:
            Dictionary with sales data and metrics
        """
        if self.sales_df.empty:
            return {
                'article_id': article_id,
                'product_name': 'Unknown',
                'data': [],
                'total_revenue': 0,
                'total_units': 0
            }
        
        # Get product info
        product = self.get_product_by_id(article_id)
        product_name = product.get('prod_name', 'Unknown Product') if product else 'Unknown Product'
        
        # Filter sales for this product (handle both string and int article_ids)
        product_sales = self.sales_df[self.sales_df['article_id'].astype(str) == str(article_id)].copy()
        
        if product_sales.empty:
            return {
                'article_id': article_id,
                'product_name': product_name,
                'data': [],
                'total_revenue': 0,
                'total_units': 0
            }
        
        # Filter by date range
        end_date = product_sales['date'].max()
        start_date = end_date - timedelta(days=days)
        product_sales = product_sales[product_sales['date'] >= start_date]
        
        # Sort by date
        product_sales = product_sales.sort_values('date')
        
        # Prepare data points
        data_points = []
        for _, row in product_sales.iterrows():
            data_points.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'revenue': float(row['total_revenue']),
                'units_sold': int(row['units_sold'])
            })
        
        # Calculate totals
        total_revenue = float(product_sales['total_revenue'].sum())
        total_units = int(product_sales['units_sold'].sum())
        
        return {
            'article_id': article_id,
            'product_name': product_name,
            'data': data_points,
            'total_revenue': total_revenue,
            'total_units': total_units
        }
    
    def get_sales_summary(self, article_id: str) -> Dict:
        """
        Get summary statistics for a product's sales.
        Used for generating insights.
        
        Args:
            article_id: Product article ID
            
        Returns:
            Dictionary with summary statistics
        """
        sales_data = self.get_sales_history(article_id, days=90)
        
        if not sales_data['data']:
            return {
                'total_revenue': 0,
                'total_units': 0,
                'avg_daily_revenue': 0,
                'avg_daily_units': 0,
                'trend': 'unknown'
            }
        
        data_points = sales_data['data']
        
        # Calculate averages
        avg_daily_revenue = sales_data['total_revenue'] / len(data_points) if data_points else 0
        avg_daily_units = sales_data['total_units'] / len(data_points) if data_points else 0
        
        # Simple trend detection (compare first and last week)
        if len(data_points) >= 14:
            first_week_revenue = sum(d['revenue'] for d in data_points[:7])
            last_week_revenue = sum(d['revenue'] for d in data_points[-7:])
            
            if last_week_revenue > first_week_revenue * 1.1:
                trend = 'increasing'
            elif last_week_revenue < first_week_revenue * 0.9:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'total_revenue': sales_data['total_revenue'],
            'total_units': sales_data['total_units'],
            'avg_daily_revenue': avg_daily_revenue,
            'avg_daily_units': avg_daily_units,
            'trend': trend,
            'days_of_data': len(data_points)
        }


# Global instance
_analytics_service = None


def get_analytics_service() -> AnalyticsService:
    """
    Get or create the global analytics service instance.
    This ensures we only load data once.
    """
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service

