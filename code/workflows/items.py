import uuid
from code.config.general import ITEMS_WORKFLOW_SITES
from code.config.logs import logger
from code.gpt_model import gpt_model
from code.mcp import BrowserMCP
from code.prompts.items import found_items_prompt, get_item_details_prompt
from code.schemas.items import (
    ItemDetails,
    ItemDetailsOutput,
    ItemsWorkflowSite,
    PageItemsOutput,
)
from code.utils.file import make_dir, write_dataframe_into_file
from code.utils.pagination import handle_pagination
from code.utils.prompt import concat_prompt_n_snapshot

"""
The correct workflow would be to access the homepage,
search by city/region, and extract a snapshot of the first page
after the search to retrieve the pagination.

For now, we are accessing the first page directly and extracting
its pagination, which in practice has the same effect;
we just skip the step of searching by city/region.
"""

stop_page = 3


async def items_workflow() -> None:

    browser_mcp = BrowserMCP()
    run_id = "runId=" + str(uuid.uuid4())
    run_dir_path = make_dir(dir_name=run_id)

    page_items_model = gpt_model.with_structured_output(schema=PageItemsOutput)
    item_details_model = gpt_model.with_structured_output(schema=ItemDetailsOutput)

    logger.info(f'>>> Run ID "{run_id}"')
    logger.info(f'>>> Run DIR path "{run_dir_path}"')

    items_details_list = []

    site: ItemsWorkflowSite
    for site in ITEMS_WORKFLOW_SITES:

        logger.info(f'>>> Processing site "{site.name}"')

        post_search_page_snapshot = await browser_mcp.extract_snapshot(
            page_url=site.url
        )

        pagination = handle_pagination(page_snapshot=post_search_page_snapshot)

        for page in pagination.pages:

            logger.info(f">>> Processing page [ {page.page_number} ]")

            items_listing_page_snapshot = await browser_mcp.extract_snapshot(
                page_url=site.url
            )

            full_prompt = concat_prompt_n_snapshot(
                initial_prompt=found_items_prompt, snapshot=items_listing_page_snapshot
            )
            page_items_output: PageItemsOutput = page_items_model.invoke(full_prompt)

            for i, item_url in enumerate(page_items_output.items_urls):

                item_number = i + 1

                logger.info(
                    f">>> Acessing item [ {item_number} ] details, from page [ {page.page_number} ]"
                )

                item_details_page_snapshot = await browser_mcp.extract_snapshot(
                    page_url=item_url
                )

                full_prompt = concat_prompt_n_snapshot(
                    initial_prompt=get_item_details_prompt,
                    snapshot=item_details_page_snapshot,
                )
                item_details_output: ItemDetailsOutput = item_details_model.invoke(
                    full_prompt
                )
                item_details = item_details_output.model_copy(
                    update={"site": site.name}
                )
                items_details_list.append(item_details.model_dump())

                scheenshot_filename = (
                    run_dir_path + f"/id={str(uuid.uuid4())}_ref={item_details.ref}.png"
                )
                await browser_mcp.take_screenshot(
                    page_url=item_url, filename=scheenshot_filename
                )

            # ---------- codeblock start ----------
            # NOTE: Remove this code later, only for testing
            if page.page_number == stop_page:
                break
            # ---------- codeblock end ----------

        final_output_filename = run_dir_path + f"/{run_id}_output"
        write_dataframe_into_file(
            output=items_details_list,
            filename=final_output_filename,
            extension="xlsx",
        )
