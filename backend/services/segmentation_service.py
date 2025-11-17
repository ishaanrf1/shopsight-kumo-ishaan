"""
Customer segmentation service.
NOTE: This is MOCKED data for demo purposes.
In a real system, this would use customer data and ML clustering.
"""
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SegmentationService:
    """
    Service for customer segmentation analysis.
    Provides buyer personas and characteristics (mocked for demo).
    """
    
    def get_customer_segments(self, article_id: str, product_info: Dict) -> Dict:
        """
        Get customer segmentation for a product.
        Returns realistic buyer personas based on product type.
        
        Args:
            article_id: Product article ID
            product_info: Product details for context
            
        Returns:
            Dictionary with customer segments
        """
        # Determine product category
        product_type = product_info.get('product_type_name', '').lower() if product_info else ''
        department = product_info.get('department_name', '').lower() if product_info else ''
        
        # Generate segments based on product type
        segments = self._generate_segments_for_product(product_type, department)
        
        return {
            'article_id': article_id,
            'segments': segments
        }
    
    def _generate_segments_for_product(self, product_type: str, department: str) -> List[Dict]:
        """
        Generate realistic customer segments based on product characteristics.
        
        Args:
            product_type: Type of product
            department: Department/category
            
        Returns:
            List of customer segments
        """
        # Default segments for general products
        if 'sport' in department or 'shoe' in product_type or 'activewear' in product_type:
            return [
                {
                    'name': 'Active Athletes',
                    'percentage': 35.0,
                    'age_range': '25-34',
                    'characteristics': [
                        'High purchase frequency',
                        'Brand conscious',
                        'Values performance features',
                        'Willing to pay premium'
                    ],
                    'purchase_likelihood': 0.85
                },
                {
                    'name': 'Fitness Enthusiasts',
                    'percentage': 28.0,
                    'age_range': '35-44',
                    'characteristics': [
                        'Regular gym-goers',
                        'Quality focused',
                        'Moderate spending',
                        'Loyal to brands'
                    ],
                    'purchase_likelihood': 0.72
                },
                {
                    'name': 'Casual Buyers',
                    'percentage': 37.0,
                    'age_range': '18-24',
                    'characteristics': [
                        'Price sensitive',
                        'Trend followers',
                        'Occasional purchases',
                        'Social media influenced'
                    ],
                    'purchase_likelihood': 0.58
                }
            ]
        
        elif 'ladies' in department or 'women' in department:
            return [
                {
                    'name': 'Fashion Forward',
                    'percentage': 32.0,
                    'age_range': '25-34',
                    'characteristics': [
                        'Trend conscious',
                        'Frequent shoppers',
                        'Social media active',
                        'Medium to high spending'
                    ],
                    'purchase_likelihood': 0.78
                },
                {
                    'name': 'Classic Professionals',
                    'percentage': 28.0,
                    'age_range': '35-50',
                    'characteristics': [
                        'Quality over quantity',
                        'Timeless style preference',
                        'Higher price tolerance',
                        'Brand loyal'
                    ],
                    'purchase_likelihood': 0.81
                },
                {
                    'name': 'Value Seekers',
                    'percentage': 40.0,
                    'age_range': '18-30',
                    'characteristics': [
                        'Budget conscious',
                        'Sale shoppers',
                        'Mix and match style',
                        'Online shoppers'
                    ],
                    'purchase_likelihood': 0.65
                }
            ]
        
        elif 'men' in department or 'male' in department:
            return [
                {
                    'name': 'Modern Professionals',
                    'percentage': 38.0,
                    'age_range': '30-45',
                    'characteristics': [
                        'Work wardrobe focused',
                        'Quality conscious',
                        'Efficient shoppers',
                        'Brand preference'
                    ],
                    'purchase_likelihood': 0.76
                },
                {
                    'name': 'Casual Comfort',
                    'percentage': 35.0,
                    'age_range': '25-40',
                    'characteristics': [
                        'Comfort prioritized',
                        'Practical choices',
                        'Moderate spending',
                        'Infrequent shopping'
                    ],
                    'purchase_likelihood': 0.68
                },
                {
                    'name': 'Young Trendsetters',
                    'percentage': 27.0,
                    'age_range': '18-28',
                    'characteristics': [
                        'Style conscious',
                        'Social media influenced',
                        'Price sensitive',
                        'Frequent browsers'
                    ],
                    'purchase_likelihood': 0.62
                }
            ]
        
        else:
            # Generic segments for accessories or other categories
            return [
                {
                    'name': 'Frequent Shoppers',
                    'percentage': 30.0,
                    'age_range': '25-40',
                    'characteristics': [
                        'Regular purchases',
                        'Brand aware',
                        'Medium spending',
                        'Quality focused'
                    ],
                    'purchase_likelihood': 0.75
                },
                {
                    'name': 'Occasional Buyers',
                    'percentage': 45.0,
                    'age_range': '30-50',
                    'characteristics': [
                        'Need-based shopping',
                        'Value conscious',
                        'Research before buying',
                        'Moderate loyalty'
                    ],
                    'purchase_likelihood': 0.65
                },
                {
                    'name': 'Bargain Hunters',
                    'percentage': 25.0,
                    'age_range': '18-35',
                    'characteristics': [
                        'Price driven',
                        'Sale focused',
                        'Impulse buyers',
                        'Low brand loyalty'
                    ],
                    'purchase_likelihood': 0.52
                }
            ]


# Global instance
_segmentation_service = None


def get_segmentation_service() -> SegmentationService:
    """Get or create the global segmentation service instance."""
    global _segmentation_service
    if _segmentation_service is None:
        _segmentation_service = SegmentationService()
    return _segmentation_service

