from code.config.logs import logger
from code.gpt_model import gpt_model
from code.prompts.items import get_pagination_prompt
from code.schemas.pagination import PageItem, Pagination, PaginationOutput
from code.utils.prompt import concat_prompt_n_snapshot


def handle_pagination(page_snapshot: str) -> Pagination:
    """Extracts pagination information from the current page and returns it in a
    structured format.

    Returns:
        Pagination: Object containing the total number of pages and the list of
        page items, each with its page number and URL.
    """

    pagination_model = gpt_model.with_structured_output(PaginationOutput)

    full_prompt = concat_prompt_n_snapshot(
        initial_prompt=get_pagination_prompt,
        snapshot=page_snapshot,
    )
    response = pagination_model.invoke(full_prompt)
    pagination_output: PaginationOutput = response

    # logger.info(pagination_output.model_dump())

    url_pattern = pagination_output.page_url_pattern
    start = pagination_output.first_page_number
    end = pagination_output.last_page_number

    total = end - start + 1

    pagination = Pagination(total=total)

    for page_number in range(start, end + 1):

        page_url = url_pattern.replace("PAGE_NUMBER", str(page_number))
        page_item = PageItem(page_number=page_number, page_url=page_url)
        pagination.pages.append(page_item)

    return pagination
