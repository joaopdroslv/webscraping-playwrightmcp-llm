import os
from typing import Optional

from dotenv import load_dotenv
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

load_dotenv()

PLAYWRIGHT_MCP_URL = os.getenv("PLAYWRIGHT_MCP_URL")


class BrowserMCP:
    def __init__(self, base_url: str = PLAYWRIGHT_MCP_URL):
        self.transport = StreamableHttpTransport(base_url)
        self.client: Optional[Client] = None

    async def __aenter__(self):
        self.client = Client(self.transport)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc, tb)

    async def navigate(self, url: str):
        await self.client.call_tool("browser_navigate", {"url": url})

    async def wait(self, seconds: int = 5):
        await self.client.call_tool("browser_wait_for", {"time": seconds})

    async def extract_snapshot(self, url: str) -> str:
        await self.navigate(url)
        await self.wait(10)
        snapshot = await self.client.call_tool("browser_snapshot", {})
        return snapshot.content

    async def query_product(self, url: str, input_ref: str, query: str) -> str:
        await self.navigate(url)
        await self.wait()
        await self.client.call_tool(
            "browser_click",
            {
                "ref": input_ref,
                "element": "search input",
            },
        )
        await self.client.call_tool(
            "browser_type",
            {
                "ref": input_ref,
                "element": "search input",
                "text": query,
            },
        )
        await self.client.call_tool("browser_press_key", {"key": "Enter"})
        await self.client.call_tool("browser_wait_for", {"time": 5})
        snapshot = await self.client.call_tool("browser_snapshot", {})

        return snapshot.content
