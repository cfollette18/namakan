from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Browser, Page
import structlog
import asyncio

logger = structlog.get_logger()

class WebBrowser:
    """
    Web browsing tool for agents
    Uses Playwright for JavaScript-rendered content
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def initialize(self):
        """Initialize browser"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            logger.info("Web browser initialized")
        except Exception as e:
            logger.error("Error initializing browser", error=str(e))
            raise
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Web browser closed")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search the web for a query
        
        Args:
            query: Search query
            max_results: Maximum number of results
        
        Returns:
            List of search results with title, url, snippet
        """
        try:
            page = await self.browser.new_page()
            
            # Use DuckDuckGo for privacy-friendly search
            search_url = f"https://duckduckgo.com/?q={query}"
            await page.goto(search_url, wait_until='networkidle')
            
            # Wait for results to load
            await page.wait_for_selector('article[data-testid="result"]', timeout=10000)
            
            # Extract results
            results = await page.evaluate('''() => {
                const articles = document.querySelectorAll('article[data-testid="result"]');
                return Array.from(articles).slice(0, 10).map(article => {
                    const titleEl = article.querySelector('h2');
                    const linkEl = article.querySelector('a[href]');
                    const snippetEl = article.querySelector('[data-result="snippet"]');
                    
                    return {
                        title: titleEl ? titleEl.textContent : '',
                        url: linkEl ? linkEl.href : '',
                        snippet: snippetEl ? snippetEl.textContent : ''
                    };
                });
            }''')
            
            await page.close()
            
            logger.info("Search completed", query=query, results=len(results))
            
            return results[:max_results]
        
        except Exception as e:
            logger.error("Error searching", error=str(e))
            return []
    
    async def scrape_page(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a web page
        
        Args:
            url: URL to scrape
        
        Returns:
            Dictionary with title, content, metadata
        """
        try:
            page = await self.browser.new_page()
            
            # Navigate to page
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Extract content
            content = await page.evaluate('''() => {
                // Remove scripts, styles, and other non-content elements
                const elementsToRemove = document.querySelectorAll('script, style, nav, header, footer, iframe, noscript');
                elementsToRemove.forEach(el => el.remove());
                
                return {
                    title: document.title,
                    headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h => h.textContent.trim()),
                    paragraphs: Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim()),
                    links: Array.from(document.querySelectorAll('a[href]')).map(a => ({
                        text: a.textContent.trim(),
                        href: a.href
                    })),
                    images: Array.from(document.querySelectorAll('img[src]')).map(img => ({
                        alt: img.alt,
                        src: img.src
                    }))
                };
            }''')
            
            await page.close()
            
            logger.info("Page scraped", url=url)
            
            return {
                "url": url,
                "title": content["title"],
                "headings": content["headings"],
                "text": " ".join(content["paragraphs"]),
                "links": content["links"][:20],  # Limit links
                "images": content["images"][:10]  # Limit images
            }
        
        except Exception as e:
            logger.error("Error scraping page", url=url, error=str(e))
            return {
                "url": url,
                "error": str(e)
            }
    
    async def extract_data(self, url: str, selector: str) -> List[str]:
        """
        Extract specific data using CSS selector
        
        Args:
            url: URL to extract from
            selector: CSS selector
        
        Returns:
            List of extracted text content
        """
        try:
            page = await self.browser.new_page()
            await page.goto(url, wait_until='networkidle')
            
            # Extract using selector
            elements = await page.query_selector_all(selector)
            data = []
            
            for element in elements:
                text = await element.text_content()
                if text:
                    data.append(text.strip())
            
            await page.close()
            
            logger.info("Data extracted", url=url, selector=selector, count=len(data))
            
            return data
        
        except Exception as e:
            logger.error("Error extracting data", error=str(e))
            return []
    
    async def screenshot(self, url: str, output_path: str, full_page: bool = False) -> bool:
        """
        Take a screenshot of a page
        
        Args:
            url: URL to screenshot
            output_path: Path to save screenshot
            full_page: Capture full page or just viewport
        
        Returns:
            True if successful
        """
        try:
            page = await self.browser.new_page()
            await page.goto(url, wait_until='networkidle')
            
            await page.screenshot(path=output_path, full_page=full_page)
            await page.close()
            
            logger.info("Screenshot captured", url=url, path=output_path)
            
            return True
        
        except Exception as e:
            logger.error("Error taking screenshot", error=str(e))
            return False


# Convenience functions for agents
async def web_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Perform web search"""
    async with WebBrowser() as browser:
        return await browser.search(query, max_results)

async def scrape_url(url: str) -> Dict[str, Any]:
    """Scrape content from URL"""
    async with WebBrowser() as browser:
        return await browser.scrape_page(url)

async def extract_from_page(url: str, selector: str) -> List[str]:
    """Extract data from page using selector"""
    async with WebBrowser() as browser:
        return await browser.extract_data(url, selector)
