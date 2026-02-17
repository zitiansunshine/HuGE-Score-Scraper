# scraper.py
import asyncio
import sys
from playwright.async_api import async_playwright
import os
import re

async def fetch_result(gene: str, phenotype: str) -> str:
    """Fetch single gene-trait score from HUGE calculator."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        try:
            page = await browser.new_page()
            url = f"https://hugeamp.org/hugecalculator.html?gene={gene}&phenotype={phenotype}"
            
            await page.goto(url, timeout=120_000)
            
            # Wait for gene symbol validation
            await page.wait_for_selector(f"text='{gene}'", timeout=90_000)
            
            # Attempt to fetch the primary result element
            try:
                result_div = await page.wait_for_selector(
                    "div.col-md-6[style='text-align: right; white-space: nowrap;']",
                    timeout=90_000
                )
            except Exception:
                # Fallback to secondary result element if primary fails
                result_div = await page.wait_for_selector(
                    "div.col-md-6[style='text-align: right;']",
                    timeout=90_000
                )
            
            # Extract and process result text
            result_text = (await result_div.text_content()).strip()
            match = re.search(r'([\d.]+)', result_text)
            if match:
                return match.group(1)
            else:
                return f"ERROR: No numeric score found in: {result_text}"
            
        except Exception as e:
            return f"ERROR: {str(e)}"
        
        finally:
            await browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scraper.py <gene> <phenotype>", file=sys.stderr)
        sys.exit(1)
    
    gene = sys.argv[1]
    phenotype = sys.argv[2]
    
    result = asyncio.run(fetch_result(gene, phenotype))
    print(f"{gene}\t{phenotype}\t{result}")
