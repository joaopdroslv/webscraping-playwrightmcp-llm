from code.config.logs import logger
from code.gpt_model import gpt_model
from code.mcp import BrowserMCP
from code.schemas.products import ProductsOutput


async def products_workflow() -> None:

    browser_mcp = BrowserMCP()

    PAGE_URL = "https://www.kabum.com.br/"

    snapshot = await browser_mcp.extract_snapshot(page_url=PAGE_URL)

    response = gpt_model.invoke(
        f"""
    Here is a page snapshot. Identify the search input bar
    (where the user types the product name) and return ONLY the "ref"
    value, nothing else.

    Respond only the ref ID (ex: e315). No explanation.

    Snapshot:
    ```yaml
        {snapshot}
    ```
    """
    )

    ref = response.content

    snapshot = await browser_mcp.query_product(
        page_url=PAGE_URL,
        input_ref=ref,
        query="AMD Ryzen 7 5800X3D",
    )

    products_model = gpt_model.with_structured_output(schema=ProductsOutput)

    response = products_model.invoke(
        f"""
    You will receive a page snapshot from an ecommerce website.
    Extract every product listed on the page.

    Return a JSON array where each item has:
    - name (string)
    - price (number)

    If the price is not present, omit the item.

    Respond ONLY with valid JSON, nothing else.

    Here's the snapshot:
    {snapshot}
    """
    )

    products_output: ProductsOutput = response
    product_list = products_output.products

    logger.info(f"Found a total of [ {len(product_list)} ] products")
    for i, p in enumerate(product_list):
        logger.info(f"[ {i + 1} ] {p.name.split(",")[0]} | {p.price}")
