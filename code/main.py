import asyncio
from code.mcp import BrowserMCP
from code.workflows.items import items_workflow


async def test_connection():
    """Util function to test the connection to a web page using the Playwright MCP."""

    PAGE_URL = "https://www.zapimoveis.com.br/venda/imoveis/sp+presidente-prudente/?transacao=venda"
    SCREENSHOT_FILENAME = "zapimoveis.png"

    browser_mcp = BrowserMCP(base_url="http://localhost:8931")
    await browser_mcp.take_screenshot(
        page_url=PAGE_URL,
        filename=SCREENSHOT_FILENAME,
    )


if __name__ == "__main__":
    asyncio.run(test_connection())
