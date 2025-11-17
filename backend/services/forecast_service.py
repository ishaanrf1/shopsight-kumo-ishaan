"""
Forecast service for demand prediction.
NOTE: This is MOCKED data for demo purposes.
In a real system, this would use ML models or statistical forecasting.
"""
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ForecastService:
    """
    Service for generating demand forecasts.
    Uses simple algorithms based on historical patterns (mocked for demo).
    """
    
    def generate_forecast(self, article_id: str, historical_data: List[Dict], days: int = 30) -> Dict:
        """
        Generate demand forecast for a product.
        This is mocked but uses historical data to create realistic predictions.
        
        Args:
            article_id: Product article ID
            historical_data: Historical sales data points
            days: Number of days to forecast
            
        Returns:
            Dictionary with forecast data
        """
        if not historical_data:
            # No historical data, return empty forecast
            return {
                'article_id': article_id,
                'forecast': [],
                'method': 'insufficient_data'
            }
        
        # Calculate average daily sales from historical data
        avg_units = np.mean([d['units_sold'] for d in historical_data])
        
        # Add some trend based on recent vs older data
        if len(historical_data) >= 14:
            recent_avg = np.mean([d['units_sold'] for d in historical_data[-7:]])
            older_avg = np.mean([d['units_sold'] for d in historical_data[:7]])
            trend = (recent_avg - older_avg) / 7  # Daily trend
        else:
            trend = 0
        
        # Generate forecast
        forecast_points = []
        last_date = datetime.strptime(historical_data[-1]['date'], '%Y-%m-%d')
        
        for i in range(1, days + 1):
            forecast_date = last_date + timedelta(days=i)
            
            # Base prediction with trend
            predicted = avg_units + (trend * i)
            
            # Add weekly seasonality (weekends higher)
            day_of_week = forecast_date.weekday()
            if day_of_week in [5, 6]:  # Saturday, Sunday
                predicted *= 1.2
            
            # Add some random variation
            predicted *= np.random.uniform(0.9, 1.1)
            
            # Ensure non-negative
            predicted = max(0, predicted)
            
            # Calculate confidence intervals (wider as we go further out)
            uncertainty = 0.1 + (0.01 * i)  # Increases with time
            confidence_lower = predicted * (1 - uncertainty)
            confidence_upper = predicted * (1 + uncertainty)
            
            forecast_points.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'predicted_units': round(predicted, 1),
                'confidence_lower': round(confidence_lower, 1),
                'confidence_upper': round(confidence_upper, 1)
            })
        
        return {
            'article_id': article_id,
            'forecast': forecast_points,
            'method': 'moving_average_with_trend'
        }


# Global instance
_forecast_service = None


def get_forecast_service() -> ForecastService:
    """Get or create the global forecast service instance."""
    global _forecast_service
    if _forecast_service is None:
        _forecast_service = ForecastService()
    return _forecast_service

