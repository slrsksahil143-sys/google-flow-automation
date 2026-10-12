import os
import sys
import json
import base64
import asyncio
import traceback

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

async def main():
    print("=" * 60, flush=True)
    print("🚀 GOOGLE FLOW AUTOMATED DEMO GENERATION RUNNER", flush=True)
    print("=" * 60, flush=True)

    prompt = os.environ.get("INPUT_PROMPT", "3D Pixar animated vegetable character running happily through market, full temporal motion, high framerate 3D CGI")
    print(f"Target Prompt: {prompt}", flush=True)

    os.makedirs("output_clips", exist_ok=True)

    try:
        from browser_use import Browser

        state_b64 = os.environ.get("GOOGLE_STORAGE_STATE", "")
        storage_state_dict = None
        if state_b64:
            try:
                state_json = base64.b64decode(state_b64).decode("utf-8")
                storage_state_dict = json.loads(state_json)
                print(f"Decoded storage state ({len(storage_state_dict.get('cookies', []))} cookies).", flush=True)
            except Exception as e:
                print(f"Warning: could not decode state: {e}", flush=True)

        print("Launching browser with xvfb virtual display...", flush=True)
        b = Browser(headless=True, storage_state=storage_state_dict)
        await asyncio.wait_for(b.start(), timeout=45)

        print("Navigating to https://flow.google.com/about ...", flush=True)
        await asyncio.wait_for(b.navigate_to("https://flow.google.com/about"), timeout=40)
        await asyncio.sleep(4)

        title = await b.get_current_page_title()
        url = await b.get_current_page_url()
        print(f"Page Title: {title}", flush=True)
        print(f"Page URL: {url}", flush=True)

        state = await b.get_state_as_text()
        print("\n--- PAGE STATE SUMMARY ---", flush=True)
        print(state[:1500], flush=True)
        print("--- END SUMMARY ---\n", flush=True)

        # Look for 'Create with Google Flow' button
        target_idx = None
        for line in state.split("\n"):
            if "Create with Google Flow" in line and "[" in line and "]" in line:
                try:
                    target_idx = int(line.split("[")[1].split("]")[0])
                    break
                except Exception:
                    pass

        if target_idx is not None:
            print(f"Found 'Create with Google Flow' at index {target_idx}. Clicking...", flush=True)
            elem = await b.get_element_by_index(target_idx)
            if elem:
                try:
                    await elem.click()
                except Exception as click_err:
                    print(f"Click notice: {click_err}", flush=True)
        else:
            print("Direct navigation to https://flow.google.com ...", flush=True)
            await b.navigate_to("https://flow.google.com")

        await asyncio.sleep(8)
        current_url = await b.get_current_page_url()
        current_title = await b.get_current_page_title()
        print("=" * 60, flush=True)
        print(f"AFTER NAVIGATION URL: {current_url}", flush=True)
        print(f"AFTER NAVIGATION TITLE: {current_title}", flush=True)
        print("=" * 60, flush=True)

        # Save screenshot
        try:
            await b.take_screenshot("studio_snapshot.png")
            print("Saved snapshot: studio_snapshot.png", flush=True)
        except Exception as ss_err:
            print(f"Screenshot notice: {ss_err}", flush=True)

        new_state = await b.get_state_as_text()
        print("\n--- NEW PAGE STATE ---", flush=True)
        print(new_state[:2500], flush=True)
        print("--- END NEW PAGE STATE ---\n", flush=True)

        try:
            await asyncio.wait_for(b.kill(), timeout=10)
        except Exception:
            pass

        print("Runner finished step execution cleanly.", flush=True)
        sys.exit(0)

    except Exception as e:
        print("Fatal error in runner:", flush=True)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())