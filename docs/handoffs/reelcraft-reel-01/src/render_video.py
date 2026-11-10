import asyncio, subprocess
from playwright.async_api import async_playwright
html='file://'+__import__('os').path.abspath('docs/handoffs/reelcraft-reel-01/src/reel_v3.html')+''
FPS=30; N=30*FPS
async def main():
    ff=subprocess.Popen(['ffmpeg','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),'assets/reelcraft_reel_v3_silencieux.mp4'],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto(html); await pg.wait_for_timeout(500)
        for i in range(N):
            await pg.evaluate(f'setTime({i/FPS})')
            ff.stdin.write(await pg.screenshot(type='jpeg',quality=94))
        await b.close()
    ff.stdin.close(); ff.wait()
asyncio.run(main())
