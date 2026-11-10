const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
const html='file://'+path.resolve(process.argv[2]);const out=process.argv[3];fs.mkdirSync(out,{recursive:true});
const T=[2,4.9,5.1,9.9,10.1,14,17,19.9,20.1,24.9,25.1,28].concat(process.argv.slice(4).map(Number));
const F=(t)=>{setTime(t);const r=[];const vis=[...document.querySelectorAll('.scene')].map(s=>[s.id,+getComputedStyle(s).opacity]);
const on=vis.filter(v=>v[1]>0.01);
for(const [id,op] of on){const sc=document.getElementById(id);
 const els=[...sc.querySelectorAll('h1,.sub,.bub,.chip,.badge,.row,.ok,.tag,.cta,.contact,.photo,.car,img.logo,.phone>div:not(.bub):not(.car):not(.ok)')].filter(e=>+getComputedStyle(e).opacity>0.05||!e.classList.contains('it'));
 const B=els.map(e=>{const b=e.getBoundingClientRect();return {n:(e.className||e.tagName)+':'+(e.innerText||'').slice(0,25),x:b.left,y:b.top,r:b.right,b:b.bottom,e}});
 for(const b of B){ if(b.x<0||b.r>1080||b.y<0||b.b>1920) r.push(['HORS_CADRE',id,b.n,[b.x,b.y,b.r,b.b].map(Math.round)]);
   if(b.y<150||b.b>1920-200) r.push(['ZONE_SECU',id,b.n,[b.y,b.b].map(Math.round)]);
   const e=b.e; if(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2) r.push(['TEXTE_COUPE',id,b.n]);}
 for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const a=B[i],c=B[j];
   if(a.e.contains(c.e)||c.e.contains(a.e))continue;
   const ox=Math.min(a.r,c.r)-Math.max(a.x,c.x), oy=Math.min(a.b,c.b)-Math.max(a.y,c.y);
   if(ox>1&&oy>1) r.push(['CHEVAUCHEMENT',id,a.n,c.n,Math.round(oy)]);}
 if(sc.scrollHeight>1921) r.push(['SCENE_DEBORDE',id,sc.scrollHeight]);
 r.push(['visibles',id,op.toFixed(2),B.length]);}
if(on.length>1) r.push(['DEUX_SCENES',on]); if(on.length==0) r.push(['ECRAN_VIDE']);
return r;};
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto(html);await pg.waitForTimeout(800);
for(const t of T){const r=await pg.evaluate(F,t);await pg.screenshot({path:`${out}/t${t.toFixed(2).padStart(5,'0')}.png`});console.log('t='+t,JSON.stringify(r));}
await b.close();})();