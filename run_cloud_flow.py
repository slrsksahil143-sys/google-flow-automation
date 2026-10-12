import os, sys, traceback, asyncio, base64, json
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

async def main():
    print('Starting Cloud Script execution...', flush=True)
    try:
        from browser_use import Browser
        state_b64 = os.environ.get('GOOGLE_STORAGE_STATE', '')
        print(f'GOOGLE_STORAGE_STATE present: {bool(state_b64)} (length: {len(state_b64)})', flush=True)
        
        storage_state_dict = None
        if state_b64:
            try:
                state_json = base64.b64decode(state_b64).decode('utf-8')
                storage_state_dict = json.loads(state_json)
                print(f'Decoded storage state keys: {list(storage_state_dict.keys())}', flush=True)
            except Exception as e:
                print('Error decoding state:', e, flush=True)

        print('Initializing Browser...', flush=True)
        b = Browser(headless=True, storage_state=storage_state_dict)
        print('Starting Browser...', flush=True)
        await asyncio.wait_for(b.start(), timeout=30)
        print('Navigating to Google Flow...', flush=True)
        await asyncio.wait_for(b.navigate_to('https://flow.google.com/about'), timeout=30)
        await asyncio.sleep(4)
        title = await b.get_current_page_title()
        url = await b.get_current_page_url()
        print('====================================', flush=True)
        print(f'SUCCESS! Google Flow Connected!', flush=True)
        print(f'Title: {title}', flush=True)
        print(f'URL: {url}', flush=True)
        print('====================================', flush=True)
        try:
            await asyncio.wait_for(b.kill(), timeout=10)
        except Exception:
            pass
        print('Automation finished cleanly. Exiting.', flush=True)
        os._exit(0)
    except Exception as e:
        print('FATAL ERROR IN RUN_CLOUD_FLOW:', flush=True)
        traceback.print_exc()
        os._exit(1)

if __name__ == '__main__':
    asyncio.run(main())
