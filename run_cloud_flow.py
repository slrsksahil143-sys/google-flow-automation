import os, sys, traceback, asyncio, base64, json
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

async def main():
    print('Starting Cloud Script execution...')
    try:
        from browser_use import Browser
        state_b64 = os.environ.get('GOOGLE_STORAGE_STATE', '')
        print(f'GOOGLE_STORAGE_STATE present: {bool(state_b64)} (length: {len(state_b64)})')
        
        storage_state_dict = None
        if state_b64:
            try:
                state_json = base64.b64decode(state_b64).decode('utf-8')
                storage_state_dict = json.loads(state_json)
                print(f'Decoded storage state keys: {list(storage_state_dict.keys())}')
            except Exception as e:
                print('Error decoding state:', e)

        print('Initializing Browser...')
        b = Browser(headless=True, storage_state=storage_state_dict)
        print('Starting Browser...')
        await b.start()
        print('Navigating to Google Flow...')
        await b.navigate_to('https://flow.google.com/about')
        await asyncio.sleep(4)
        title = await b.get_current_page_title()
        url = await b.get_current_page_url()
        print(f'SUCCESS! Page Title: {title} | URL: {url}')
        await b.stop()
        print('Clean stop complete.')
    except Exception as e:
        print('FATAL ERROR IN RUN_CLOUD_FLOW:')
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
