"""
Search API routes for product search functionality.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from services.search_service import get_search_service

router = APIRouter()


class SearchRequest(BaseModel):
    """Request model for product search"""
    query: str
    limit: Optional[int] = 10


class ProductResult(BaseModel):
    """Product search result model"""
    article_id: str
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


class SearchResponse(BaseModel):
    """Response model for search results"""
    query: str
    results: List[ProductResult]
    count: int


@router.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    """
    Search for products using natural language query.
    Uses LLM to understand the query and match against product database.
    This is a REAL implementation using the H&M dataset + OpenAI.
    
    Args:
        request: SearchRequest containing the search query
        
    Returns:
        SearchResponse with matching products
    """
    search_service = get_search_service()
    results = search_service.search(request.query, request.limit)
    return results

