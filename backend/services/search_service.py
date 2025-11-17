"""
Search service combining analytics and LLM for intelligent product search.
"""
from typing import List, Dict
import logging

from services.analytics_service import get_analytics_service
from services.llm_service import get_llm_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for intelligent product search.
    Combines LLM query understanding with product data search.
    """
    
    def __init__(self):
        """Initialize search service with dependencies."""
        self.analytics = get_analytics_service()
        self.llm = get_llm_service()
    
    def search(self, query: str, limit: int = 10) -> Dict:
        """
        Search for products using natural language query.
        
        Process:
        1. Use LLM to extract search terms from natural language
        2. Search product database with extracted terms
        3. Return formatted results
        
        Args:
            query: Natural language search query
            limit: Maximum number of results
            
        Returns:
            Dictionary with search results
        """
        logger.info(f"Searching for: {query}")
        
        # Extract search terms using LLM
        search_terms = self.llm.extract_search_terms(query)
        
        # Search products with each term and combine results
        all_results = []
        seen_ids = set()
        
        for term in search_terms:
            products = self.analytics.search_products(term, limit=limit)
            for product in products:
                article_id = product.get('article_id')
                if article_id and article_id not in seen_ids:
                    all_results.append(product)
                    seen_ids.add(article_id)
                    
                    if len(all_results) >= limit:
                        break
            
            if len(all_results) >= limit:
                break
        
        # If no results from extracted terms, try original query
        if not all_results:
            all_results = self.analytics.search_products(query, limit=limit)
        
        # Format results
        formatted_results = []
        for product in all_results[:limit]:
            formatted_results.append({
                'article_id': str(product.get('article_id', '')),  # Convert to string
                'name': product.get('prod_name', 'Unknown Product'),
                'category': product.get('product_type_name', None),
                'price': None,  # Price not in product catalog, comes from sales
                'description': self._create_description(product)
            })
        
        return {
            'query': query,
            'results': formatted_results,
            'count': len(formatted_results)
        }
    
    def _create_description(self, product: Dict) -> str:
        """
        Create a product description from available attributes.
        
        Args:
            product: Product dictionary
            
        Returns:
            Description string
        """
        parts = []
        
        if product.get('colour_group_name'):
            parts.append(product['colour_group_name'])
        
        if product.get('product_group_name'):
            parts.append(product['product_group_name'])
        
        if product.get('department_name'):
            parts.append(f"from {product['department_name']}")
        
        return ' '.join(parts) if parts else None


# Global instance
_search_service = None


def get_search_service() -> SearchService:
    """Get or create the global search service instance."""
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service

