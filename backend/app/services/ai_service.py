import httpx
import json
from typing import Dict, Any, Optional, List
from app.core.config import settings
import structlog

logger = structlog.get_logger()

class AIService:
    """Service for AI model interactions"""

    def __init__(self):
        self.anthropic_key = settings.ANTHROPIC_API_KEY
        self.openai_key = settings.OPENAI_API_KEY
        self.deepseek_key = settings.DEEPSEEK_API_KEY

    async def call_anthropic(self, prompt: str, model: str = "claude-3-sonnet-20240229", **kwargs) -> Dict[str, Any]:
        """Call Anthropic Claude API"""
        if not self.anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not configured")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        data = {
            "model": model,
            "max_tokens": kwargs.get("max_tokens", 1000),
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

    async def call_openai(self, prompt: str, model: str = "gpt-4", **kwargs) -> Dict[str, Any]:
        """Call OpenAI API"""
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not configured")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1000)
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

    async def call_deepseek(self, prompt: str, model: str = "deepseek-chat", **kwargs) -> Dict[str, Any]:
        """Call DeepSeek API"""
        if not self.deepseek_key:
            raise ValueError("DEEPSEEK_API_KEY not configured")

        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.deepseek_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7)
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

    async def generate_response(self, prompt: str, provider: str = "deepseek", model: str = None, **kwargs) -> str:
        """Generate AI response with fallback logic"""
        providers = [
            ("deepseek", self.call_deepseek, model or "deepseek-chat"),
            ("anthropic", self.call_anthropic, model or settings.DEFAULT_AGENT_MODEL),
            ("openai", self.call_openai, model or settings.FALLBACK_MODEL)
        ]

        # Start with requested provider, then fallback
        start_idx = next((i for i, (name, _, _) in enumerate(providers) if name == provider), 0)

        for i in range(len(providers)):
            provider_name, call_method, model_name = providers[(start_idx + i) % len(providers)]

            try:
                logger.info(f"Calling {provider_name} with model {model_name}")
                response = await call_method(prompt, model_name, **kwargs)

                # Extract text from different response formats
                if provider_name == "anthropic":
                    return response["content"][0]["text"]
                elif provider_name in ["openai", "deepseek"]:
                    return response["choices"][0]["message"]["content"]

            except Exception as e:
                logger.warning(f"{provider_name} call failed", error=str(e))
                continue

        raise Exception("All AI providers failed")

    async def analyze_domain(self, task_description: str) -> str:
        """Analyze what domain a task belongs to"""
        prompt = f"""
        Analyze this task description and determine the primary domain/industry it belongs to.
        Return only the domain name (e.g., marketing, product_development, research, finance, etc.).

        Task: {task_description}
        """

        response = await self.generate_response(prompt, provider="deepseek", temperature=0.3)
        return response.strip().lower()

    async def decompose_task(self, task_description: str, domain: str) -> Dict[str, Any]:
        """Break down a complex task into manageable components"""
        prompt = f"""
        You are an expert project manager in {domain}. Break down this complex task into specific, actionable components.

        Task: {task_description}

        Return a JSON object with:
        - phases: array of phase objects with {{name, description, deliverables, estimated_hours}}
        - required_expertise: array of required skill sets
        - dependencies: array of phase dependencies
        - risks: array of potential risks

        Format: JSON only, no additional text.
        """

        response = await self.generate_response(prompt, provider="deepseek", temperature=0.2)
        try:
            return json.loads(response)
        except:
            # Fallback parsing
            return {
                "phases": [{"name": "Main Task", "description": task_description, "deliverables": ["Complete task"], "estimated_hours": 8}],
                "required_expertise": ["General"],
                "dependencies": [],
                "risks": []
            }

    async def design_agent_team(self, expertise_needed: List[str], domain: str) -> List[Dict[str, Any]]:
        """Design an optimal agent team for the required expertise"""
        expertise_str = ", ".join(expertise_needed)

        prompt = f"""
        Design a team of AI agents for a {domain} project requiring: {expertise_str}

        For each required expertise, create an agent specification with:
        - role: specific agent title
        - responsibilities: array of 3-5 key responsibilities
        - tools: array of required tools/capabilities
        - personality: brief personality description
        - constraints: array of important constraints

        Return as JSON array of agent objects.
        """

        response = await self.generate_response(prompt, provider="deepseek", temperature=0.4)
        try:
            return json.loads(response)
        except:
            # Fallback
            return [
                {
                    "role": "General Assistant",
                    "responsibilities": ["Handle tasks", "Provide support"],
                    "tools": ["web_browser", "document_writer"],
                    "personality": "helpful",
                    "constraints": ["Stay focused"]
                }
            ]

# Global AI service instance
ai_service = AIService()