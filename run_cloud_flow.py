import os, sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')
from browser_use import Browser

async def main():
    print('Starting Cloud Browser with virtual display...')
    # Running in GitHub Actions Ubuntu environment
    b = Browser(headless=True)
    try:
        await b.start()
        print('Navigating to Google Flow...')
        await b.navigate_to('https://flow.google.com/about')
        title = await b.get_current_page_title()
        url = await b.get_current_page_url()
        print(f'Google Flow Connected successfully!\nTitle: {title}\nURL: {url}')
    finally:
        await b.stop()
        print('Cloud session completed cleanly.')

if __name__ == '__main__':
    asyncio.run(main())
