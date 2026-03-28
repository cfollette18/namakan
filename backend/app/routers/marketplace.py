from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.marketplace.marketplace import marketplace, AgentCategory

router = APIRouter()

@router.get("/templates")
async def list_templates(
    category: Optional[AgentCategory] = None,
    min_rating: float = 0.0,
    sort_by: str = "popularity"
):
    """List all available agent templates"""
    templates = await marketplace.list_templates(
        category=category,
        min_rating=min_rating,
        sort_by=sort_by
    )
    return {"templates": templates}

@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """Get details of a specific template"""
    template = await marketplace.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.get("/templates/{template_id}/reviews")
async def get_template_reviews(template_id: str, limit: int = 10):
    """Get reviews for a template"""
    reviews = await marketplace.get_reviews(template_id, limit)
    return {"reviews": reviews}

@router.post("/templates/{template_id}/reviews")
async def add_review(
    template_id: str,
    user_id: str,
    rating: int,
    comment: str
):
    """Add a review for a template"""
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    review = await marketplace.add_review(template_id, user_id, rating, comment)
    return review

@router.get("/search")
async def search_templates(query: str, limit: int = 20):
    """Search templates by keyword"""
    templates = await marketplace.search_templates(query, limit)
    return {"results": templates}

@router.get("/trending")
async def get_trending(days: int = 7, limit: int = 10):
    """Get trending templates"""
    templates = await marketplace.get_trending_templates(days, limit)
    return {"trending": templates}

@router.post("/agents/create")
async def create_agent_from_template(
    template_id: str,
    agent_id: str,
    customizations: Optional[dict] = None
):
    """Create an agent instance from a template"""
    try:
        config = await marketplace.create_agent_from_template(
            template_id,
            agent_id,
            customizations
        )
        return config
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
