"""
Product API routes for retrieving product details and analytics.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from services.analytics_service import get_analytics_service
from services.forecast_service import get_forecast_service
from services.segmentation_service import get_segmentation_service

router = APIRouter()


class SalesDataPoint(BaseModel):
    """Single data point in sales time series"""
    date: str
    revenue: float
    units_sold: int


class SalesResponse(BaseModel):
    """Historical sales data response"""
    article_id: str
    product_name: str
    data: List[SalesDataPoint]
    total_revenue: float
    total_units: int


class ForecastDataPoint(BaseModel):
    """Single data point in forecast"""
    date: str
    predicted_units: float
    confidence_lower: float
    confidence_upper: float


class ForecastResponse(BaseModel):
    """Demand forecast response"""
    article_id: str
    forecast: List[ForecastDataPoint]
    method: str  # e.g., "moving_average", "linear_regression"


class CustomerSegment(BaseModel):
    """Customer segment information"""
    name: str
    percentage: float
    age_range: str
    characteristics: List[str]
    purchase_likelihood: float


class SegmentsResponse(BaseModel):
    """Customer segments response"""
    article_id: str
    segments: List[CustomerSegment]


@router.get("/products/{article_id}/sales", response_model=SalesResponse)
async def get_product_sales(article_id: str, days: int = 90):
    """
    Get historical sales data for a product.
    This uses REAL data from the H&M dataset.
    
    Args:
        article_id: Product article ID
        days: Number of days of history to return
        
    Returns:
        SalesResponse with time series data
    """
    analytics = get_analytics_service()
    sales_data = analytics.get_sales_history(article_id, days)
    
    if not sales_data['data']:
        raise HTTPException(status_code=404, detail="Product not found or no sales data available")
    
    return sales_data


@router.get("/products/{article_id}/forecast", response_model=ForecastResponse)
async def get_product_forecast(article_id: str, days: int = 30):
    """
    Get demand forecast for a product.
    Note: This is MOCKED data based on historical patterns.
    
    Args:
        article_id: Product article ID
        days: Number of days to forecast
        
    Returns:
        ForecastResponse with predicted demand
    """
    # Get historical data first
    analytics = get_analytics_service()
    sales_data = analytics.get_sales_history(article_id, days=90)
    
    if not sales_data['data']:
        raise HTTPException(status_code=404, detail="Product not found or no sales data available")
    
    # Generate forecast based on historical data
    forecast_service = get_forecast_service()
    forecast = forecast_service.generate_forecast(article_id, sales_data['data'], days)
    
    return forecast


@router.get("/products/{article_id}/segments", response_model=SegmentsResponse)
async def get_customer_segments(article_id: str):
    """
    Get customer segmentation analysis for a product.
    Note: This is MOCKED data showing likely buyer personas.
    
    Args:
        article_id: Product article ID
        
    Returns:
        SegmentsResponse with customer segments
    """
    # Get product info for context
    analytics = get_analytics_service()
    product = analytics.get_product_by_id(article_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Generate segments
    segmentation = get_segmentation_service()
    segments = segmentation.get_customer_segments(article_id, product)
    
    return segments

