import base64
import os

from dotenv import load_dotenv
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

load_dotenv()

PLAYWRIGHT_MCP_URL = os.getenv("PLAYWRIGHT_MCP_URL")


class BrowserMCP:
    def __init__(self, base_url: str = PLAYWRIGHT_MCP_URL):
        self.transport = StreamableHttpTransport(base_url)

    async def extract_snapshot(self, url: str) -> str:
        async with Client(self.transport) as client:
            await client.call_tool("browser_navigate", {"url": url})
            await client.call_tool("browser_wait_for", {"time": 5})
            snapshot = await client.call_tool("browser_snapshot", {})
        return snapshot.content

    async def take_screenshot(self, url: str, filename: str) -> None:
        async with Client(self.transport) as client:
            await client.call_tool("browser_navigate", {"url": url})
            await client.call_tool("browser_wait_for", {"time": 5})
            result = await client.call_tool(
                "browser_take_screenshot", {"fullPage": True, "type": "png"}
            )
            for item in result.content:
                if getattr(item, "type", None) == "image":
                    raw_bytes = base64.b64decode(item.data)
                    with open(filename, "wb") as f:
                        f.write(raw_bytes)

    async def query_product(self, url: str, input_ref: str, query: str) -> str:
        async with Client(self.transport) as client:
            await client.call_tool("browser_navigate", {"url": url})
            await client.call_tool("browser_wait_for", {"time": 5})
            await client.call_tool(
                "browser_click",
                {
                    "ref": input_ref,
                    "element": "search input",
                },
            )
            await client.call_tool(
                "browser_type",
                {
                    "ref": input_ref,
                    "element": "search input",
                    "text": query,
                },
            )
            await client.call_tool("browser_press_key", {"key": "Enter"})
            await client.call_tool("browser_wait_for", {"time": 5})
            snapshot = await client.call_tool("browser_snapshot", {})
        return snapshot.content
