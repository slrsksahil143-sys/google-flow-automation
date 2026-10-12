import os, sys, asyncio, base64, json
sys.stdout.reconfigure(encoding='utf-8')
from browser_use import Browser

async def main():
    print('Starting Cloud Browser with virtual display...')
    state_b64 = os.environ.get('GOOGLE_STORAGE_STATE', '')
    storage_state_dict = None
    if state_b64:
        try:
            state_json = base64.b64decode(state_b64).decode('utf-8')
            storage_state_dict = json.loads(state_json)
            print('Successfully loaded Google Storage State secret!')
        except Exception as e:
            print('Warning: Failed to decode GOOGLE_STORAGE_STATE:', e)

    b = Browser(
        headless=True,
        storage_state=storage_state_dict
    )
    try:
        await b.start()
        print('Navigating to Google Flow...')
        await b.navigate_to('https://flow.google.com/about')
        await asyncio.sleep(4)
        title = await b.get_current_page_title()
        url = await b.get_current_page_url()
        print(f'Google Flow Connected successfully!\nTitle: {title}\nURL: {url}')
    finally:
        await b.stop()
        print('Cloud session completed cleanly.')

if __name__ == '__main__':
    asyncio.run(main())
