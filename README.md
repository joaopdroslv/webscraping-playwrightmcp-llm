# Simple Playwright MCP Integration (Python)

This project demonstrates a minimal integration with Microsoft’s **Playwright MCP** using the `fastmcp` client.
It provides a thin abstraction layer for browser automation and snapshot extraction, and it includes an example flow where an LLM analyzes the page to locate UI elements and extract product data from an e-commerce website.

## Overview

The core of the project is the `BrowserMCP` class, a small helper that wraps MCP tools such as:
- Navigating to a URL
- Waiting for elements or timeouts
- Clicking and typing into elements
- Taking snapshots
- Triggering basic browser interactions via MCP

It uses the `StreamableHttpTransport` to communicate with a locally running (`Dockerized`) Playwright MCP instance (`http://localhost:8931` by default).

The repository also includes a simple demonstration (`main.py`) where:
1. The browser navigates to Kabum.
2. A snapshot of the page is sent to an LLM so it can identify the search input reference (ref).
3. The code types a product query into the search bar.
4. A new snapshot is sent to the LLM to extract structured product data (name + price).
5. The products are printed to the console.

## Output Example

```bash
Found a total of [ 6 ] products
[ 1 ] Processador AMD Ryzen 7 5800X3D - R$ 1.799,90
[ 2 ] Processador AMD Ryzen 7 5800X3D 100-100000651WOF - R$ 1.749,00
[ 3 ] AMD Ryzen 7 5800X3D 8-Core, 16-Thread - R$ 1.789,99
[ 4 ] Processador Gamer AMD Ryzen 7 5800X3D - R$ 1.829,90
[ 5 ] Ryzen 7 5800X3D 3.4GHz (4.5GHz Max Turbo) - R$ 1.759,00
[ 6 ] AMD Ryzen 7 5800X3D 8 núcleos / 16 threads - R$ 1.769,90
```

## How to Run

Follow the steps below to set up the environment and run the example.

1. Start the local Playwright MCP server
Make sure the MCP instance is running before executing any Python code:
```bash
docker compose up --build -d
```

2. Create a Python virtual environment
```bash
python -m venv .venv
```

3. Activate the virtual environment (Windows)
```bash
.venv\Scripts\activate
```

On Linux/macOS, use:

```bash
source .venv/bin/activate
```

4. Install the project dependencies
```bash
pip install -r requirements.txt
```

5. Run the main script
```bash
python -m code.main
```
