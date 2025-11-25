import base64
import logging
import os

from dotenv import load_dotenv
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

logger = logging.getLogger(__name__)

load_dotenv()

PLAYWRIGHT_MCP_URL = os.getenv("PLAYWRIGHT_MCP_URL")


async def simple_mcp(page_url: str) -> str:

    transport = StreamableHttpTransport(PLAYWRIGHT_MCP_URL)

    async with Client(transport) as client:

        logger.info("[STEP_1] Navigating to the web page")
        await client.call_tool(
            "browser_navigate",
            {"url": page_url},
        )

        logger.info("[STEP_2] Waiting the page to load")
        await client.call_tool("browser_wait_for", {"time": 10})

        logger.info("[STEP_3] Taking a full page screenshot")
        result = await client.call_tool(
            "browser_take_screenshot", {"fullPage": True, "type": "png"}
        )

        logger.info("[STEP_4] Saving the screenshot to a .png file")
        for item in result.content:
            if getattr(item, "type", None) == "image":
                raw_bytes = base64.b64decode(item.data)
                with open("screenshot.png", "wb") as f:
                    f.write(raw_bytes)
