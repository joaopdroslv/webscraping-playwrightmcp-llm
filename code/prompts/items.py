found_items_prompt = """
You will receive a page snapshot of a real-estate (imóveis) listing page.

Goal:
Extract every property (imóvel) shown in the snapshot and return a JSON
object matching the following schema:

{
    "items": [
        {
            "url": "<absolute URL to the property's detail page>",
            "name": "<visible title/name of the property>"
        }
    ]
}

Extraction rules and heuristics (follow in order):
    1. Consider a "property" an item/card in the listing that contains a visible
    title (e.g. "Apartamento 2 quartos", "Casa à venda") and at least one link
    that leads to that property's details page.
    2. Prefer the anchor (<a>) whose href appears inside the property card and
    points to a details page. Heuristics for a details URL:
    - href contains keywords like "imovel", "imóvel", "detalhe", "detalhes",
        "produto", "property", "listing", "id=" or a path segment that looks like an item id.
    - OR the href is the main clickable title image/title link inside the card.
    3. Ignore links that are clearly pagination ("1", "2", "Próximo", "Anterior"),
    share/contact buttons, phone links, mailto:, tel:, or links to agent profiles.
    4. If multiple candidate anchors exist inside a card, choose the one closest to
    the visible title text (or the anchor wrapping the title).
    5. If the extracted href is relative, convert it to an absolute URL using the
    page origin available in the snapshot (if an origin/host is not present,
    return the relative path as-is).
    6. Omit any property that does not have BOTH a visible name/title and a
    details URL.

Output rules:
    - Respond ONLY with valid JSON exactly matching the schema above.
    - Do NOT include any extra text, explanation, or HTML — only the JSON object.
    - If no properties are found, return: {"items": []}
"""


get_item_details_prompt = """
You will receive a snapshot of a real-estate property detail page (página de imóvel).

Your task is to extract structured information about the property and fill ALL fields of the ItemDetailed schema:
    - ref (string)
    - city (string)
    - neighborhood (string)
    - category (e.g., Casa, Terreno)
    - application (e.g., Residencial, Comercial)
    - value (float, without currency symbol)
    - bedroom_count (int)
    - bathroom_count (int)
    - commom_room_count (int)
    - kitchen_count (int)
    - has_service_area (bool)
    - total_area (float, m²)
    - built_area (float, m²)
    - material (e.g., Alvenaria, Madeira)

Extraction rules:
    1. All values must come ONLY from the provided snapshot.
    2. Consider “dormitório(s)” as bedrooms.
    3. Consider "sala(s)" as common rooms.
    4. Extract kitchen count from “cozinha”.
    5. Extract service area from “área de serviço”.
    6. “Área útil”, “Área construída”, “Área total”, and “Área do terreno” must be interpreted carefully:
    - built_area = área útil OR área construída
    - total_area = área total OR área do terreno
    7. Convert price such as "R$ 70.000,00" → 70000.00
    8. If a value is missing, infer _0_ for counts and "" for missing strings.
    9. has_service_area = true if any indication of “área de serviço” exists.

Respond ONLY with the JSON object matching the declared schema — no explanations, no extra text.
"""
