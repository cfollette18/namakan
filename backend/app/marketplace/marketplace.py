from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import structlog

logger = structlog.get_logger()

class AgentCategory(str, Enum):
    RESEARCH = "research"
    STRATEGY = "strategy"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    OPERATIONS = "operations"
    ANALYTICS = "analytics"

class TemplateType(str, Enum):
    AGENT_TEAM = "agent_team"
    WORKFLOW = "workflow"
    PROMPT_TEMPLATE = "prompt_template"
    TOOL_INTEGRATION = "tool_integration"

class AgentTemplate(BaseModel):
    """Template for creating specialized agents"""
    template_id: str
    name: str
    description: str
    category: AgentCategory
    created_by: str
    
    # Agent configuration
    system_prompt: str
    tools: List[str]
    quality_criteria: Dict[str, Any]
    
    # Performance metrics
    usage_count: int = 0
    avg_rating: float = 0.0
    success_rate: float = 0.0
    
    # Pricing
    is_free: bool = True
    price: float = 0.0
    
    # Metadata
    tags: List[str] = []
    version: str = "1.0.0"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class WorkflowTemplate(BaseModel):
    """Template for multi-agent workflows"""
    template_id: str
    name: str
    description: str
    template_type: TemplateType
    
    # Workflow configuration
    phases: List[Dict[str, Any]]
    required_agents: List[str]
    estimated_duration: str
    
    # Use cases
    use_cases: List[str]
    industries: List[str]
    
    # Performance metrics
    usage_count: int = 0
    avg_completion_time: float = 0.0
    success_rate: float = 0.0
    
    # Metadata
    created_by: str
    is_verified: bool = False
    tags: List[str] = []
    created_at: datetime = datetime.utcnow()

class MarketplaceReview(BaseModel):
    """User review of template"""
    review_id: str
    template_id: str
    user_id: str
    rating: int  # 1-5
    comment: str
    verified_purchase: bool = False
    created_at: datetime = datetime.utcnow()

class AgentMarketplace:
    """
    Marketplace for agent templates and workflows
    Users can share, discover, and monetize agent configurations
    """
    
    def __init__(self):
        self.templates: Dict[str, AgentTemplate] = {}
        self.workflows: Dict[str, WorkflowTemplate] = {}
        self.reviews: Dict[str, List[MarketplaceReview]] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize marketplace with default templates"""
        
        # Research Agent Template
        self.templates["research-master"] = AgentTemplate(
            template_id="research-master",
            name="Research Master",
            description="Deep dive research agent for market analysis, competitor research, and trend identification",
            category=AgentCategory.RESEARCH,
            created_by="namakan",
            system_prompt="""You are an expert research agent specialized in gathering and analyzing information.
Your goal is to provide comprehensive, well-sourced research with actionable insights.

Key Capabilities:
- Web search and content extraction
- Source verification and credibility assessment
- Trend identification and pattern recognition
- Competitive analysis
- Market sizing and opportunity assessment

Always cite your sources and provide confidence levels for your findings.""",
            tools=["web_search", "scrape_url", "extract_data", "analyze_trends"],
            quality_criteria={
                "has_sources": True,
                "min_sources": 5,
                "confidence_above": 0.7,
                "has_insights": True
            },
            usage_count=1247,
            avg_rating=4.8,
            success_rate=0.92,
            tags=["research", "analysis", "market-intelligence"]
        )
        
        # Strategy Agent Template
        self.templates["strategy-architect"] = AgentTemplate(
            template_id="strategy-architect",
            name="Strategy Architect",
            description="Strategic planning agent for positioning, go-to-market, and business strategy",
            category=AgentCategory.STRATEGY,
            created_by="namakan",
            system_prompt="""You are a strategic planning expert who develops winning strategies.

Key Capabilities:
- Market positioning and differentiation
- Go-to-market strategy development
- Competitive strategy formulation
- OKR and roadmap creation
- Risk assessment and mitigation

Develop strategies that are specific, measurable, and actionable.""",
            tools=["analyze_data", "generate_insights", "write_strategy_doc"],
            quality_criteria={
                "has_positioning": True,
                "has_tactics": True,
                "confidence_above": 0.75
            },
            usage_count=892,
            avg_rating=4.7,
            success_rate=0.89,
            tags=["strategy", "planning", "positioning"]
        )
        
        # Creative Copywriter Template
        self.templates["creative-genius"] = AgentTemplate(
            template_id="creative-genius",
            name="Creative Genius",
            description="High-converting copywriting agent for emails, landing pages, and ads",
            category=AgentCategory.CREATIVE,
            created_by="namakan",
            system_prompt="""You are a world-class copywriter who creates compelling, conversion-focused content.

Key Capabilities:
- Persuasive copywriting
- Headline and hook creation
- Email sequences
- Landing page copy
- Ad creative

Write with clarity, emotion, and a clear call-to-action.""",
            tools=["write_copy", "analyze_sentiment", "test_readability"],
            quality_criteria={
                "has_headline": True,
                "has_cta": True,
                "readability_score_above": 70
            },
            usage_count=2341,
            avg_rating=4.9,
            success_rate=0.94,
            tags=["copywriting", "marketing", "creative"]
        )
        
        # Default Workflows
        self.workflows["startup-launch"] = WorkflowTemplate(
            template_id="startup-launch",
            name="Startup Launch Campaign",
            description="Complete workflow for launching a startup product",
            template_type=TemplateType.WORKFLOW,
            phases=[
                {
                    "name": "Market Research",
                    "agents": ["research-master"],
                    "duration": "2-3 days"
                },
                {
                    "name": "Strategy Development",
                    "agents": ["strategy-architect"],
                    "duration": "1-2 days"
                },
                {
                    "name": "Creative Execution",
                    "agents": ["creative-genius"],
                    "duration": "2-3 days"
                }
            ],
            required_agents=["research-master", "strategy-architect", "creative-genius"],
            estimated_duration="5-8 days",
            use_cases=[
                "Product launch",
                "Market entry",
                "Go-to-market planning"
            ],
            industries=["SaaS", "Tech", "Startup"],
            created_by="namakan",
            is_verified=True,
            usage_count=456,
            avg_completion_time=6.2,
            success_rate=0.91,
            tags=["startup", "launch", "gtm"]
        )
    
    async def list_templates(
        self,
        category: Optional[AgentCategory] = None,
        tags: Optional[List[str]] = None,
        min_rating: float = 0.0,
        sort_by: str = "popularity"
    ) -> List[AgentTemplate]:
        """
        List available agent templates
        
        Args:
            category: Filter by category
            tags: Filter by tags
            min_rating: Minimum rating
            sort_by: Sort order (popularity, rating, recent)
        
        Returns:
            List of matching templates
        """
        templates = list(self.templates.values())
        
        # Apply filters
        if category:
            templates = [t for t in templates if t.category == category]
        
        if tags:
            templates = [
                t for t in templates
                if any(tag in t.tags for tag in tags)
            ]
        
        if min_rating > 0:
            templates = [t for t in templates if t.avg_rating >= min_rating]
        
        # Sort
        if sort_by == "popularity":
            templates.sort(key=lambda t: t.usage_count, reverse=True)
        elif sort_by == "rating":
            templates.sort(key=lambda t: t.avg_rating, reverse=True)
        elif sort_by == "recent":
            templates.sort(key=lambda t: t.created_at, reverse=True)
        
        logger.info("Templates listed", count=len(templates), category=category)
        
        return templates
    
    async def get_template(self, template_id: str) -> Optional[AgentTemplate]:
        """Get a specific template"""
        return self.templates.get(template_id)
    
    async def create_agent_from_template(
        self,
        template_id: str,
        agent_id: str,
        customizations: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an agent instance from template
        
        Args:
            template_id: Template to use
            agent_id: New agent ID
            customizations: Custom configurations
        
        Returns:
            Agent configuration
        """
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        # Build agent config from template
        config = {
            "agent_id": agent_id,
            "name": template.name,
            "system_prompt": template.system_prompt,
            "tools": template.tools,
            "quality_criteria": template.quality_criteria,
            "template_id": template_id
        }
        
        # Apply customizations
        if customizations:
            config.update(customizations)
        
        # Increment usage count
        template.usage_count += 1
        
        logger.info(
            "Agent created from template",
            template_id=template_id,
            agent_id=agent_id
        )
        
        return config
    
    async def publish_template(
        self,
        user_id: str,
        template: AgentTemplate
    ) -> str:
        """
        Publish a new template to marketplace
        
        Args:
            user_id: User publishing the template
            template: Template to publish
        
        Returns:
            Template ID
        """
        import uuid
        
        template_id = str(uuid.uuid4())
        template.template_id = template_id
        template.created_by = user_id
        template.created_at = datetime.utcnow()
        
        self.templates[template_id] = template
        
        logger.info(
            "Template published",
            template_id=template_id,
            user_id=user_id
        )
        
        return template_id
    
    async def add_review(
        self,
        template_id: str,
        user_id: str,
        rating: int,
        comment: str
    ) -> MarketplaceReview:
        """
        Add a review for a template
        
        Args:
            template_id: Template being reviewed
            user_id: User submitting review
            rating: Rating (1-5)
            comment: Review comment
        
        Returns:
            MarketplaceReview
        """
        import uuid
        
        review = MarketplaceReview(
            review_id=str(uuid.uuid4()),
            template_id=template_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
            verified_purchase=True,
            created_at=datetime.utcnow()
        )
        
        # Store review
        if template_id not in self.reviews:
            self.reviews[template_id] = []
        self.reviews[template_id].append(review)
        
        # Update template rating
        template = self.templates.get(template_id)
        if template:
            all_ratings = [r.rating for r in self.reviews[template_id]]
            template.avg_rating = sum(all_ratings) / len(all_ratings)
            template.updated_at = datetime.utcnow()
        
        logger.info(
            "Review added",
            template_id=template_id,
            rating=rating
        )
        
        return review
    
    async def get_reviews(
        self,
        template_id: str,
        limit: int = 10
    ) -> List[MarketplaceReview]:
        """Get reviews for a template"""
        reviews = self.reviews.get(template_id, [])
        return reviews[:limit]
    
    async def search_templates(
        self,
        query: str,
        limit: int = 20
    ) -> List[AgentTemplate]:
        """
        Search templates by keyword
        
        Args:
            query: Search query
            limit: Maximum results
        
        Returns:
            Matching templates
        """
        query_lower = query.lower()
        matches = []
        
        for template in self.templates.values():
            # Search in name, description, and tags
            if (query_lower in template.name.lower() or
                query_lower in template.description.lower() or
                any(query_lower in tag.lower() for tag in template.tags)):
                matches.append(template)
        
        # Sort by relevance (simple: by usage count)
        matches.sort(key=lambda t: t.usage_count, reverse=True)
        
        logger.info("Template search", query=query, results=len(matches))
        
        return matches[:limit]
    
    async def get_trending_templates(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[AgentTemplate]:
        """Get trending templates"""
        # For simplicity, return top-rated recently updated templates
        templates = [
            t for t in self.templates.values()
            if (datetime.utcnow() - t.updated_at).days <= days
        ]
        
        templates.sort(key=lambda t: (t.avg_rating, t.usage_count), reverse=True)
        
        return templates[:limit]


# Global marketplace instance
marketplace = AgentMarketplace()
