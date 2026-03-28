from typing import Dict, Callable, Any, List
from app.tools.web_browser import web_search, scrape_url, extract_from_page
from app.tools.document_writer import write_research_report, write_strategy_doc, write_copy
from app.tools.data_analyzer import analyze_data, find_data_trends, get_data_insights
import structlog

logger = structlog.get_logger()

class ToolRegistry:
    """
    Central registry for agent tools
    Maps tool names to callable functions
    """
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all default tools"""
        
        # Web browsing tools
        self.register_tool("web_search", web_search)
        self.register_tool("scrape_url", scrape_url)
        self.register_tool("extract_from_page", extract_from_page)
        
        # Document writing tools
        self.register_tool("write_research_report", write_research_report)
        self.register_tool("write_strategy_doc", write_strategy_doc)
        self.register_tool("write_copy", write_copy)
        
        # Data analysis tools
        self.register_tool("analyze_data", analyze_data)
        self.register_tool("find_data_trends", find_data_trends)
        self.register_tool("get_data_insights", get_data_insights)
        
        logger.info("Default tools registered", count=len(self.tools))
    
    def register_tool(self, name: str, func: Callable):
        """
        Register a tool
        
        Args:
            name: Tool name
            func: Callable function
        """
        self.tools[name] = func
        logger.debug("Tool registered", name=name)
    
    def get_tool(self, name: str) -> Callable:
        """
        Get a tool by name
        
        Args:
            name: Tool name
        
        Returns:
            Callable function
        
        Raises:
            ValueError: If tool not found
        """
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")
        
        return self.tools[name]
    
    def get_tools_for_agent(self, agent_role: str) -> List[str]:
        """
        Get allowed tools for an agent role
        
        Args:
            agent_role: Agent role
        
        Returns:
            List of tool names
        """
        # Define tool constraints per agent type
        tool_permissions = {
            "Research Agent": [
                "web_search",
                "scrape_url",
                "extract_from_page",
                "analyze_data",
                "get_data_insights",
                "write_research_report"
            ],
            "Strategy Agent": [
                "analyze_data",
                "find_data_trends",
                "get_data_insights",
                "write_strategy_doc"
            ],
            "Copywriter Agent": [
                "write_copy",
                "analyze_data"
            ],
            "Email Marketing Agent": [
                "write_copy",
                "analyze_data"
            ],
            "Technical Agent": [
                "web_search",
                "scrape_url",
                "analyze_data"
            ]
        }
        
        return tool_permissions.get(agent_role, [])
    
    async def execute_tool(
        self,
        tool_name: str,
        **kwargs
    ) -> Any:
        """
        Execute a tool with arguments
        
        Args:
            tool_name: Tool name
            **kwargs: Tool arguments
        
        Returns:
            Tool execution result
        """
        try:
            tool = self.get_tool(tool_name)
            result = await tool(**kwargs)
            
            logger.info(
                "Tool executed",
                tool=tool_name,
                success=True
            )
            
            return result
        
        except Exception as e:
            logger.error(
                "Tool execution failed",
                tool=tool_name,
                error=str(e)
            )
            raise
    
    def list_tools(self) -> List[str]:
        """List all registered tools"""
        return list(self.tools.keys())
    
    def get_tool_description(self, tool_name: str) -> str:
        """Get description of a tool"""
        descriptions = {
            "web_search": "Search the web for information on a topic",
            "scrape_url": "Extract content from a specific URL",
            "extract_from_page": "Extract specific data from a page using CSS selector",
            "write_research_report": "Create a formatted research report",
            "write_strategy_doc": "Create a strategic planning document",
            "write_copy": "Write marketing copy with specific tone and audience",
            "analyze_data": "Perform statistical analysis on data",
            "find_data_trends": "Identify trends in time series data",
            "get_data_insights": "Generate insights from data analysis"
        }
        
        return descriptions.get(tool_name, "No description available")


# Global tool registry
tool_registry = ToolRegistry()
