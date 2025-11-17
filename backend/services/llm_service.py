"""
LLM service for natural language processing and insights generation.
Uses OpenAI API for understanding queries and generating human-readable insights.
"""
import os
from typing import List, Dict, Optional
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for LLM-powered features using OpenAI API.
    Handles natural language search and insights generation.
    """
    
    def __init__(self):
        """Initialize the LLM service with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            logger.warning("OpenAI API key not configured. LLM features will be limited.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
    
    def extract_search_terms(self, query: str) -> List[str]:
        """
        Extract key search terms from natural language query.
        Uses LLM to understand intent and extract relevant product attributes.
        
        Args:
            query: Natural language search query
            
        Returns:
            List of search terms
        """
        if not self.client:
            # Fallback: simple keyword extraction
            return [word.lower() for word in query.split() if len(word) > 2]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-5-nano",  # User's specified model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a search query analyzer for an e-commerce platform. "
                                 "Extract key product attributes from the user's query. "
                                 "Return a comma-separated list of search terms (product type, brand, color, style, etc.)."
                    },
                    {
                        "role": "user",
                        "content": f"Extract search terms from: {query}"
                    }
                ]
            )
            
            terms_str = response.choices[0].message.content.strip()
            terms = [t.strip().lower() for t in terms_str.split(',')]
            
            logger.info(f"Extracted terms from '{query}': {terms}")
            return terms
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            # Fallback to simple extraction
            return [word.lower() for word in query.split() if len(word) > 2]
    
    def generate_insights(self, article_id: str, sales_summary: Dict, product_info: Optional[Dict] = None) -> Dict:
        """
        Generate AI-powered insights about a product's sales performance.
        Creates human-readable analysis and recommendations.
        
        Args:
            article_id: Product article ID
            sales_summary: Summary statistics from analytics service
            product_info: Optional product details for context
            
        Returns:
            Dictionary with summary and detailed insights
        """
        if not self.client:
            # Fallback: template-based insights
            return self._generate_template_insights(article_id, sales_summary, product_info)
        
        try:
            # Prepare context for LLM
            product_name = product_info.get('prod_name', 'Unknown Product') if product_info else 'Unknown Product'
            
            context = f"""
Product: {product_name}
Total Revenue (90 days): ${sales_summary.get('total_revenue', 0):.2f}
Total Units Sold: {sales_summary.get('total_units', 0)}
Average Daily Revenue: ${sales_summary.get('avg_daily_revenue', 0):.2f}
Average Daily Units: {sales_summary.get('avg_daily_units', 0):.1f}
Trend: {sales_summary.get('trend', 'unknown')}
Days of Data: {sales_summary.get('days_of_data', 0)}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-5-nano",  # User's specified model
                messages=[
                    {
                        "role": "system",
                        "content": "You are an e-commerce analytics expert. Analyze sales data and provide "
                                 "clear, actionable insights. Be specific, mention numbers, and identify patterns. "
                                 "Format your response as: 1) A brief summary paragraph, 2) 3-4 specific insights."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this product's sales performance:\n{context}"
                    }
                ]
            )
            
            full_text = response.choices[0].message.content.strip()
            
            # Parse the response into summary and insights
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            summary = lines[0] if lines else "Sales data analyzed."
            
            # Extract insights (look for numbered or bulleted items)
            insights = []
            for line in lines[1:]:
                if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '-', '•']):
                    # Clean up numbering/bullets
                    clean_line = line.lstrip('1234567890.-•').strip()
                    if clean_line:
                        # Split into title (first sentence) and description (full text)
                        # Find first sentence ending with . ! or ?
                        first_sentence_end = min(
                            [clean_line.find('. ') if clean_line.find('. ') > 0 else len(clean_line),
                             clean_line.find('! ') if clean_line.find('! ') > 0 else len(clean_line),
                             clean_line.find('? ') if clean_line.find('? ') > 0 else len(clean_line)]
                        )
                        title = clean_line[:first_sentence_end + 1].strip() if first_sentence_end < len(clean_line) else clean_line[:60] + '...'
                        
                        insights.append({
                            'type': 'trend',
                            'title': title,
                            'description': clean_line,
                            'confidence': 0.8
                        })
            
            # If no structured insights found, create one from the full text
            if not insights:
                insights = [{
                    'type': 'analysis',
                    'title': 'Performance Analysis',
                    'description': full_text,
                    'confidence': 0.75
                }]
            
            return {
                'article_id': article_id,
                'summary': summary,
                'insights': insights[:4]  # Limit to 4 insights
            }
            
        except Exception as e:
            logger.error(f"Error generating insights with LLM: {e}")
            return self._generate_template_insights(article_id, sales_summary, product_info)
    
    def _generate_template_insights(self, article_id: str, sales_summary: Dict, product_info: Optional[Dict]) -> Dict:
        """
        Generate insights using templates (fallback when LLM unavailable).
        
        Args:
            article_id: Product article ID
            sales_summary: Summary statistics
            product_info: Optional product details
            
        Returns:
            Dictionary with insights
        """
        product_name = product_info.get('prod_name', 'this product') if product_info else 'this product'
        
        trend = sales_summary.get('trend', 'stable')
        total_revenue = sales_summary.get('total_revenue', 0)
        total_units = sales_summary.get('total_units', 0)
        avg_daily_units = sales_summary.get('avg_daily_units', 0)
        
        # Generate summary based on trend
        if trend == 'increasing':
            summary = f"{product_name} shows strong growth with ${total_revenue:.2f} in revenue over the past 90 days. Sales are trending upward, indicating increasing demand."
        elif trend == 'decreasing':
            summary = f"{product_name} has generated ${total_revenue:.2f} in revenue, but shows a declining trend. Consider promotional strategies to boost sales."
        else:
            summary = f"{product_name} maintains stable performance with ${total_revenue:.2f} in revenue and {total_units} units sold over the past 90 days."
        
        # Generate insights
        insights = [
            {
                'type': 'trend',
                'title': f'Sales Trend: {trend.title()}',
                'description': f'The product shows a {trend} sales pattern over the analyzed period.',
                'confidence': 0.85
            },
            {
                'type': 'metric',
                'title': f'Average Daily Sales: {avg_daily_units:.1f} units',
                'description': f'The product sells an average of {avg_daily_units:.1f} units per day.',
                'confidence': 0.9
            }
        ]
        
        # Add revenue insight
        if total_revenue > 1000:
            insights.append({
                'type': 'performance',
                'title': 'Strong Revenue Performance',
                'description': f'Generated ${total_revenue:.2f} in total revenue, indicating strong market demand.',
                'confidence': 0.8
            })
        
        return {
            'article_id': article_id,
            'summary': summary,
            'insights': insights
        }


# Global instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create the global LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

