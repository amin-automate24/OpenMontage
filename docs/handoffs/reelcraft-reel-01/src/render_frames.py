import sys, os, asyncio
from playwright.async_api import async_playwright
html='file://'+__import__('os').path.abspath('docs/handoffs/reelcraft-reel-01/src/reel_v3.html')+''
out=sys.argv[1]; times=[float(x) for x in sys.argv[2:]]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(html); await pg.wait_for_timeout(500)
        for t in times:
            await pg.evaluate(f'setTime({t})')
            await pg.screenshot(path=f'{out}/t{t:05.2f}.png')
        await b.close()
asyncio.run(main())
