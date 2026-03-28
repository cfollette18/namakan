from typing import Dict, Any, List, Optional
from datetime import datetime
import structlog
import markdown
from jinja2 import Template
import json

logger = structlog.get_logger()

class DocumentWriter:
    """
    Document generation tool for agents
    Supports multiple output formats
    """
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load document templates"""
        return {
            "research_report": """
# Research Report: {{ title }}

**Date:** {{ date }}
**Prepared by:** {{ author }}

## Executive Summary
{{ summary }}

## Key Findings
{% for finding in findings %}
### {{ finding.title }}
{{ finding.content }}

**Source:** {{ finding.source }}
**Confidence:** {{ finding.confidence }}
{% endfor %}

## Methodology
{{ methodology }}

## Recommendations
{% for rec in recommendations %}
- {{ rec }}
{% endfor %}

## Appendix
{{ appendix }}
""",
            
            "strategy_document": """
# Strategic Plan: {{ title }}

**Date:** {{ date }}
**Status:** {{ status }}

## Vision
{{ vision }}

## Strategic Objectives
{% for objective in objectives %}
### {{ objective.title }}
{{ objective.description }}

**Key Results:**
{% for kr in objective.key_results %}
- {{ kr }}
{% endfor %}
{% endfor %}

## Market Analysis
{{ market_analysis }}

## Competitive Positioning
{{ competitive_positioning }}

## Implementation Roadmap
{% for phase in roadmap %}
### Phase {{ loop.index }}: {{ phase.name }}
**Timeline:** {{ phase.timeline }}
{{ phase.description }}
{% endfor %}

## Success Metrics
{% for metric in metrics %}
- **{{ metric.name }}:** {{ metric.target }}
{% endfor %}
""",
            
            "marketing_copy": """
# {{ title }}

{{ content }}

---

**Target Audience:** {{ audience }}
**Tone:** {{ tone }}
**Key Message:** {{ key_message }}
""",
            
            "generic": """
# {{ title }}

{{ content }}
"""
        }
    
    async def create_document(
        self,
        template_type: str,
        data: Dict[str, Any],
        output_format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Create a document from template and data
        
        Args:
            template_type: Type of document (research_report, strategy_document, etc.)
            data: Data to fill template
            output_format: Output format (markdown, html, json)
        
        Returns:
            Document content and metadata
        """
        try:
            # Add timestamp if not provided
            if "date" not in data:
                data["date"] = datetime.utcnow().strftime("%Y-%m-%d")
            
            # Get template
            template_str = self.templates.get(
                template_type,
                self.templates["generic"]
            )
            
            # Render template
            template = Template(template_str)
            content = template.render(**data)
            
            # Convert format if needed
            if output_format == "html":
                content = markdown.markdown(content)
            elif output_format == "json":
                content = json.dumps({
                    "type": template_type,
                    "data": data,
                    "rendered": content
                }, indent=2)
            
            logger.info(
                "Document created",
                template_type=template_type,
                output_format=output_format
            )
            
            return {
                "content": content,
                "format": output_format,
                "template": template_type,
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "word_count": len(content.split())
                }
            }
        
        except Exception as e:
            logger.error("Error creating document", error=str(e))
            raise
    
    async def create_research_report(
        self,
        title: str,
        author: str,
        summary: str,
        findings: List[Dict[str, Any]],
        methodology: str = "",
        recommendations: List[str] = None,
        appendix: str = ""
    ) -> Dict[str, Any]:
        """Create a research report"""
        data = {
            "title": title,
            "author": author,
            "summary": summary,
            "findings": findings,
            "methodology": methodology,
            "recommendations": recommendations or [],
            "appendix": appendix
        }
        
        return await self.create_document("research_report", data)
    
    async def create_strategy_document(
        self,
        title: str,
        vision: str,
        objectives: List[Dict[str, Any]],
        market_analysis: str = "",
        competitive_positioning: str = "",
        roadmap: List[Dict[str, Any]] = None,
        metrics: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a strategy document"""
        data = {
            "title": title,
            "status": "Draft",
            "vision": vision,
            "objectives": objectives,
            "market_analysis": market_analysis,
            "competitive_positioning": competitive_positioning,
            "roadmap": roadmap or [],
            "metrics": metrics or []
        }
        
        return await self.create_document("strategy_document", data)
    
    async def create_marketing_copy(
        self,
        title: str,
        content: str,
        audience: str,
        tone: str,
        key_message: str
    ) -> Dict[str, Any]:
        """Create marketing copy"""
        data = {
            "title": title,
            "content": content,
            "audience": audience,
            "tone": tone,
            "key_message": key_message
        }
        
        return await self.create_document("marketing_copy", data)
    
    async def save_to_file(
        self,
        content: str,
        filename: str,
        directory: str = "./outputs"
    ) -> str:
        """
        Save document to file
        
        Args:
            content: Document content
            filename: File name
            directory: Output directory
        
        Returns:
            Full path to saved file
        """
        import os
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
            
            # Full path
            filepath = os.path.join(directory, filename)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("Document saved", filepath=filepath)
            
            return filepath
        
        except Exception as e:
            logger.error("Error saving document", error=str(e))
            raise


# Convenience functions for agents
async def write_research_report(
    title: str,
    findings: List[Dict[str, Any]],
    **kwargs
) -> Dict[str, Any]:
    """Write a research report"""
    writer = DocumentWriter()
    return await writer.create_research_report(title, **kwargs, findings=findings)

async def write_strategy_doc(
    title: str,
    vision: str,
    objectives: List[Dict[str, Any]],
    **kwargs
) -> Dict[str, Any]:
    """Write a strategy document"""
    writer = DocumentWriter()
    return await writer.create_strategy_document(title, vision, objectives, **kwargs)

async def write_copy(
    title: str,
    content: str,
    audience: str,
    tone: str,
    key_message: str
) -> Dict[str, Any]:
    """Write marketing copy"""
    writer = DocumentWriter()
    return await writer.create_marketing_copy(
        title, content, audience, tone, key_message
    )
