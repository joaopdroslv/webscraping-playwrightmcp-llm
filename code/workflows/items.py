from code.config.general import ITEMS_WORKFLOW_SITES
from code.config.logs import logger
from code.gpt_model import gpt_model
from code.mcp import BrowserMCP
from code.prompts.items import found_items_prompt, get_item_details_prompt
from code.schemas.items import ItemDetails, ItemsOutput, ItemsWorkflowSite
from code.utils.file import make_dir, write_dataframe_into_file
from datetime import datetime


def concat_prompt_n_snapshot(initial_prompt: str, snapshot: str) -> str:
    """Helper function to concat partial prompts with it's relevant snapshot."""

    return (
        initial_prompt
        + f"""
    \nHere is the snapshot:
    {snapshot}
    """
    )


async def items_workflow() -> None:

    browser_mcp = BrowserMCP()
    run_id = "runId_" + str(int(datetime.now().timestamp()))
    run_dir_path = make_dir(dir_name=run_id)

    logger.info(f'>>> Run ID "{run_id}"')
    logger.info(f'>>> Run DIR path "{run_dir_path}"')

    site: ItemsWorkflowSite
    for site in ITEMS_WORKFLOW_SITES:

        logger.info(f'>>> Processing site "{site.name}"')

        items_listing_page_snapshot = await browser_mcp.extract_snapshot(
            page_url=site.url
        )

        items_model = gpt_model.with_structured_output(schema=ItemsOutput)

        full_prompt = concat_prompt_n_snapshot(
            initial_prompt=found_items_prompt, snapshot=items_listing_page_snapshot
        )
        response = items_model.invoke(full_prompt)
        items_ouput: ItemsOutput = response

        item_details_model = gpt_model.with_structured_output(ItemDetails)

        items_details_list = []
        for i, item_url in enumerate(items_ouput.items_urls):

            logger.info(f'>>> Acessing item "{i}" details')

            item_details_page_snapshot = await browser_mcp.extract_snapshot(
                page_url=item_url
            )

            full_prompt = concat_prompt_n_snapshot(
                initial_prompt=get_item_details_prompt,
                snapshot=item_details_page_snapshot,
            )
            response = item_details_model.invoke(full_prompt)
            item_details: ItemDetails = response

            scheenshot_filename = run_dir_path + f"/{run_id}_{i}_{item_details.ref}.png"
            await browser_mcp.take_screenshot(
                page_url=item_url, filename=scheenshot_filename
            )

            items_details_list.append(response.model_dump())

        final_output_filename = run_dir_path + f"/{run_id}_output"
        write_dataframe_into_file(
            output=items_details_list,
            filename=final_output_filename,
            extension="xlsx",
        )
