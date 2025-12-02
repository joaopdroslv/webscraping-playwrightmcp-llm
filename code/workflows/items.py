from code.gpt_model import gpt_model
from code.logs import logger
from code.mcp import BrowserMCP
from code.prompts.items import found_items_prompt, get_item_details_prompt
from code.schemas.items import ItemDetailed, ItemsOutput
from code.utils import make_dir, write_into_xlsx
from datetime import datetime


async def items_workflow() -> None:

    browser_mcp = BrowserMCP()

    PAGE_URL = "https://www.samburaimoveis.com.br/busca_avancada?finalidade=Venda"
    run_id = "runId_" + str(int(datetime.now().timestamp()))
    run_dir_path = make_dir(dir_name=run_id)

    logger.info(run_id)
    logger.info(run_dir_path)

    snapshot = await browser_mcp.extract_snapshot(url=PAGE_URL)

    items_model = gpt_model.with_structured_output(schema=ItemsOutput)

    full_prompt = (
        found_items_prompt
        + f"""
    \nHere is the snapshot:
    {snapshot}
    """
    )
    response = items_model.invoke(full_prompt)

    items_ouput: ItemsOutput = response
    items_list = items_ouput.items

    item_details_model = gpt_model.with_structured_output(ItemDetailed)

    items_detailed_list = []
    for item in items_list:
        logger.info(f"Processing URL: \n{item.url}")

        if not "/imovel" in item.url:
            logger.info("[ERROR] Item has no /imovel in its URL")
            continue

        snapshot = await browser_mcp.extract_snapshot(url=item.url)

        full_prompt = (
            get_item_details_prompt
            + f"""
        \nHere is the snapshot:
        {snapshot}
        """
        )
        response: ItemDetailed = item_details_model.invoke(full_prompt)

        item_ref = response.ref
        scheenshot_filename = run_dir_path + f"/{run_id}_{item_ref}.png"
        await browser_mcp.take_screenshot(url=item.url, filename=scheenshot_filename)

        items_detailed_list.append(response.model_dump())

    output_xlsx_filename = run_dir_path + f"/{run_id}_output.xlsx"
    write_into_xlsx(output=items_detailed_list, filename=output_xlsx_filename)
