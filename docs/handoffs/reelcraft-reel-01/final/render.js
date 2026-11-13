// Rendu déterministe image par image de reel_final.html -> ffmpeg (H.264, 1080x1920, 30 fps)
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
const [html,audio,out]=process.argv.slice(2);const FPS=30,N=30*FPS;
(async()=>{
 const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-','-i',audio,
  '-map','0:v','-map','1:a','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r',String(FPS),
  '-c:a','aac','-b:a','192k','-t','30','-movflags','+faststart',out],{stdio:['pipe','ignore','inherit']});
 const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('file://'+path.resolve(html));await pg.waitForTimeout(1000);
if(process.env.PHONE) await pg.evaluate(p=>{document.getElementById('phone').textContent=p},process.env.PHONE);
 for(let i=0;i<N;i++){await pg.evaluate(t=>setTimeAsync(t),i/FPS);const buf=await pg.screenshot({type:'png'});
  if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); if(i%150==0) console.log('frame',i);}
 await b.close();ff.stdin.end();ff.on('close',c=>console.log('ffmpeg exit',c));
})();
