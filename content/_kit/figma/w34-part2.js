// use_figma, file 1FNqlhxDdZgP6twmzb94oU — memes, contest stories, countdown stories for 12–25.10 + fill zubr:* layers from «Ассеты зубра»
const page=figma.root.children.find(p=>p.id==='8:2');await figma.setCurrentPageAsync(page);
const BASE=8200,TAG='[12–25.10] ';
const NEW=['Ср 14.10 · Мем «Родительский чат»','Пт 16.10 · Мем «Нет / Да»','Вс 18.10 · Какой ты зубр сегодня?','Вт 20.10 · Мем «Ожидание / реальность»','Чт 22.10 · Мем «Уровни владельца»','Конкурс имени — сторис','Сторис-отсчёт 32 → 19'];
for(const c of [...page.children]) if(NEW.some(n=>c.name===TAG+n)) c.remove();
const C={ink:'#0D0F13',paper:'#F3F0E8',raised:'#FAF8F3',amber:'#F0B90B',deep:'#8A6B06',card:'#16181D',soft:'#C9CBD1',lineDark:'#2B2E35'};
const rgb=h=>({r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255});
const solid=(h,o=1)=>({type:'SOLID',color:rgb(h),opacity:o});
const F={dx:{family:'Unbounded',style:'ExtraBold'},ub:{family:'Unbounded',style:'Bold'},ms:{family:'Montserrat',style:'SemiBold'},mb:{family:'Montserrat',style:'Bold'},mx:{family:'Montserrat',style:'ExtraBold'}};
for(const f of Object.values(F)) await figma.loadFontAsync(f);
const TH={ink:{bg:C.ink,fg:C.raised,acc:C.amber,logo:'8:3'},paper:{bg:C.paper,fg:C.ink,acc:C.deep,logo:'8:8'},amber:{bg:C.amber,fg:C.ink,acc:C.ink,logo:'8:13'}};
const LOGO={};for(const id of ['8:3','8:8','8:13']) LOGO[id]=await figma.getNodeByIdAsync(id);
const ASP={"aplodiruet":0.463,"dumaet":0.648,"facepalm":0.446,"flipchart":0.806,"klass":0.505,"networking":0.726,"podmigivaet":0.484,"priglashaet":0.677,"smeetsya-2":0.467,"smeetsya":0.505,"spit":0.96,"ustal":0.727,"v-shoke":0.462,"zakatyvaet-glaza":0.441,"zlitsya":0.51};
function txt(ch,font,size,color,o={}){const t=figma.createText();t.fontName=font;t.fontSize=size;t.characters=ch;t.fills=[solid(color,o.o??1)];if(o.upper)t.textCase='UPPER';if(o.lh)t.lineHeight={unit:'PERCENT',value:o.lh};t.name=o.name||ch.slice(0,30);return t;}
function al(name,dir='VERTICAL',gap=0){const f=figma.createFrame();f.name=name;f.layoutMode=dir;f.itemSpacing=gap;f.fills=[];f.primaryAxisSizingMode='AUTO';f.counterAxisSizingMode='AUTO';f.clipsContent=false;return f;}
function rich(t,html,bold,bc){const s=html.replace(/<br\s*\/?>/g,'\n');let pl='',r=[],last=0,m;const re=/<b>(.*?)<\/b>/g;while((m=re.exec(s))){pl+=s.slice(last,m.index);const a=pl.length;pl+=m[1];r.push([a,pl.length]);last=re.lastIndex;}pl+=s.slice(last);t.characters=pl;for(const [a,b] of r){t.setRangeFontName(a,b,bold);if(bc)t.setRangeFills(a,b,[solid(bc)]);}}
function fillW(n){n.layoutSizingHorizontal='FILL';if(n.type==='TEXT')n.textAutoResize='HEIGHT';}
function sp(col,h){const g=figma.createFrame();g.name='Отступ';g.fills=[];g.resize(10,h);col.appendChild(g);}
function zubr(par,pose,h,x,y){const w=Math.round(h*ASP[pose]);const r=figma.createRectangle();r.name='zubr:'+pose;r.resize(w,Math.round(h));r.fills=[solid('#888888',.25)];par.appendChild(r);r.x=Math.round(x);r.y=Math.round(y);return r;}
function glow(fr,x,y,d){const e=figma.createEllipse();e.name='Свечение';e.resize(d,d);e.fills=[solid(C.amber,.35)];e.effects=[{type:'LAYER_BLUR',radius:120,visible:true}];fr.appendChild(e);e.x=x;e.y=y;}
function story(s,name){const th=TH[s.t],tm=s.t,W=1080,H=1920,mT=360,cw=900,by=H-280-32;
 const fr=figma.createFrame();fr.name=name;fr.resize(W,H);fr.fills=[solid(th.bg)];fr.clipsContent=true;
 if(s.m){const [p,h,r,b,gl]=s.m;const w=h*ASP[p];if(gl)glow(fr,W-(r+h*.05)-h*.7,H-(b+h*.15)-h*.7,h*.7);zubr(fr,p,h,W-r-w,H-b-h);}
 const lg=LOGO[th.logo].createInstance();fr.appendChild(lg);lg.x=90;lg.y=230;lg.name='Логотип';
 const col=al('Контент');col.counterAxisSizingMode='FIXED';col.resize(cw,10);col.primaryAxisSizingMode='AUTO';col.counterAxisAlignItems='MIN';fr.appendChild(col);
 for(const b of s.bl){const k=b[0];
  if(k==='gap'){sp(col,{s:24,m:50,l:80}[b[1]]);continue;}
  if(k==='tag'){const p=al('Тег','HORIZONTAL');p.paddingTop=p.paddingBottom=14;p.paddingLeft=p.paddingRight=30;p.cornerRadius=999;p.fills=[tm==='ink'?solid(C.amber):solid(C.ink)];p.appendChild(txt(b[1],F.ub,30,tm==='ink'?C.ink:C.amber,{upper:true,name:'Тег'}));col.appendChild(p);continue;}
  if(k==='d'){const box=al('Заголовок');const ls=b[2].map(l=>l[0]==='*'?{t:l.slice(1),c:1}:{t:l});let mw=0;
   const ns=ls.map(l=>{const t=txt(l.t,F.dx,100,th.fg,{upper:true,lh:102});t.textAutoResize='WIDTH_AND_HEIGHT';mw=Math.max(mw,t.width+((tm==='amber'&&l.c)?20:0));return t;});
   const size=Math.floor(Math.min(b[1],100*cw/mw));
   ns.forEach((t,i)=>{t.fontSize=size;if(ls[i].c){if(tm==='amber'){t.fills=[solid(C.amber)];const w=al('Акцент','HORIZONTAL');w.fills=[solid(C.ink)];w.cornerRadius=Math.round(size*.08);w.paddingLeft=w.paddingRight=Math.round(size*.1);w.appendChild(t);box.appendChild(w);return;}t.fills=[solid(th.acc)];}box.appendChild(t);});
   box.itemSpacing=Math.round(size*.04);col.appendChild(box);continue;}
  if(k==='p'){const t=txt('x',F.ms,b[2]||36,tm==='ink'?C.soft:C.ink,{lh:140,name:'Текст'});rich(t,b[1],F.mb,tm==='ink'?C.raised:null);col.appendChild(t);fillW(t);continue;}
  if(k==='slot'){const r=al(b[1],'HORIZONTAL');r.primaryAxisAlignItems='CENTER';r.counterAxisAlignItems='CENTER';r.cornerRadius=26;r.strokes=[solid(th.fg,.45)];r.strokeWeight=3;r.dashPattern=[16,12];r.appendChild(txt(b[1],F.mb,28,th.fg,{o:.45,name:'Подсказка'}));col.appendChild(r);fillW(r);r.layoutSizingVertical='FIXED';r.resize(cw,b[2]);continue;}
 }
 col.x=90;col.y=mT;
 const l=txt(s.bt,F.ms,26,th.fg,{o:.6,name:'Низ — подпись'});fr.appendChild(l);l.x=90;l.y=by+32-l.height/2;return fr;}
function memeBase(theme,tag){const th=TH[theme];const fr=figma.createFrame();fr.resize(1080,1350);fr.fills=[solid(th.bg)];fr.clipsContent=true;
 const lg=LOGO[th.logo].createInstance();fr.appendChild(lg);lg.x=70;lg.y=70;lg.name='Логотип';
 const t=txt(tag,F.ub,20,th.fg,{upper:true,name:'Метка'});t.opacity=.55;fr.appendChild(t);t.x=1010-t.width;t.y=90;
 const a=txt('13–14 ноября · Москва',F.ms,24,th.fg,{o:.6,name:'Низ слева'});fr.appendChild(a);a.x=70;a.y=1350-55-a.height;
 const b=txt('reshenoforum.ru',F.ms,24,th.fg,{o:.6,name:'Низ справа'});fr.appendChild(b);b.x=1010-b.width;b.y=1350-55-b.height;return fr;}
const RC={no:['#E6E1D3',C.raised,C.ink],yes:[C.amber,C.ink,C.raised],b1:['#E6E1D3',C.raised,C.ink],b2:['#EADFB8',C.raised,C.ink],b3:['#F2CF5A',C.card,C.raised],b4:[C.amber,C.ink,C.amber]};
function memeRows(tag,rows){const fr=memeBase('paper',tag);const n=rows.length,gap=18,rh=(1060-gap*(n-1))/n;
 rows.forEach((r,i)=>{const [pc,tc,fc]=RC[r.cls];const row=figma.createFrame();row.name='Ряд '+(i+1);row.resize(940,rh);row.cornerRadius=28;row.clipsContent=true;row.fills=[solid(tc)];fr.appendChild(row);row.x=70;row.y=160+i*(rh+gap);
  const pic=figma.createFrame();pic.name='Картинка';pic.resize(357,rh);pic.fills=[solid(pc)];pic.clipsContent=true;row.appendChild(pic);pic.x=0;pic.y=0;
  const h=rh*1.18;zubr(pic,r.img,h,(357-h*ASP[r.img])/2,rh*.06);
  const box=al('Текст','VERTICAL',12);row.appendChild(box);box.counterAxisSizingMode='FIXED';box.resize(495,10);
  if(r.lbl){const lb=txt(r.lbl,F.dx,22,fc,{upper:true,name:'Подпись'});lb.opacity=.55;box.appendChild(lb);fillW(lb);}
  const t=txt(r.t,F.mb,r.size||44,fc,{lh:122,name:'Текст'});box.appendChild(t);fillW(t);box.x=357+44;box.y=(rh-box.height)/2;});return fr;}
function memeChat(){const fr=memeBase('ink','Жиза владельца');glow(fr,1080-40-560,1350-120-560,560);zubr(fr,'zlitsya',680,1080-680*ASP.zlitsya,1350-100-680);
 const col=al('Текст','VERTICAL',26);col.counterAxisSizingMode='FIXED';col.resize(940,10);fr.appendChild(col);col.x=70;col.y=170;
 for(const [s,o] of [['Никто:',.45],['Абсолютно никто:',.45],['Родительский чат\nв 23:47:',1]]){const t=txt(s,F.mb,44,C.raised,{lh:120,o,name:'Строка'});col.appendChild(t);fillW(t);}
 const bub=al('Сообщение','VERTICAL',8);bub.paddingTop=bub.paddingBottom=28;bub.paddingLeft=bub.paddingRight=36;bub.fills=[solid(C.card)];bub.strokes=[solid(C.lineDark)];bub.strokeWeight=1.5;bub.topLeftRadius=30;bub.topRightRadius=30;bub.bottomRightRadius=30;bub.bottomLeftRadius=8;col.appendChild(bub);
 bub.counterAxisSizingMode='FIXED';bub.resize(600,10);const w=txt('Мама Артёма',F.mb,22,C.amber,{name:'Кто пишет'});bub.appendChild(w);fillW(w);const m=txt('А завтра тренировка точно будет? 🙂',F.ms,40,C.raised,{lh:125,name:'Сообщение'});bub.appendChild(m);fillW(m);return fr;}
function memeGrid(){const fr=memeBase('ink','Вопрос дня');const t=txt('Какой ты зубр сегодня?',F.dx,58,C.raised,{upper:true,lh:105,name:'Заголовок'});t.setRangeFills(13,22,[solid(C.amber)]);fr.appendChild(t);t.x=70;t.y=160;t.textAutoResize='HEIGHT';t.resize(940,t.height);
 const cells=['spit','zlitsya','ustal','v-shoke','smeetsya','klass'],cw=(940-32)/3,ch=(930-16)/2;
 cells.forEach((p,i)=>{const c=figma.createFrame();c.name='Зубр '+(i+1);c.resize(cw,ch);c.cornerRadius=24;c.clipsContent=true;c.fills=[solid(C.card)];fr.appendChild(c);c.x=70+(i%3)*(cw+16);c.y=300+Math.floor(i/3)*(ch+16);
  let h=ch*.88;if(h*ASP[p]>cw*.94)h=cw*.94/ASP[p];zubr(c,p,h,(cw-h*ASP[p])/2,ch-h);const n=txt(String(i+1),F.dx,52,C.amber,{name:'Номер'});c.appendChild(n);n.x=16;n.y=12;});return fr;}
function section(name,frames,y){const s=figma.createSection();s.name=TAG+name;page.appendChild(s);s.x=0;s.y=y;let x=80,h=0;for(const f of frames){s.appendChild(f);f.x=x;f.y=120;x+=f.width+60;h=Math.max(h,f.height);}s.resizeWithoutConstraints(Math.max(x+20,1400),h+240);return s.id;}
const out={};
const nm=(f,n)=>{f.name=n;return f;};
out.m1=section(NEW[0],[nm(memeChat(),'Мем')],BASE+2*1740);
out.m2=section(NEW[1],[nm(memeRows('Мем',[{cls:'no',img:'zakatyvaet-glaza',t:'Ещё один форум, где два дня вдохновляют и рассказывают про мечту'},{cls:'yes',img:'klass',t:'Два дня разбирать свои цифры с теми, кто уже прошёл этот путь'}]),'Мем')],BASE+4*1740);
out.m3=section(NEW[2],[nm(memeGrid(),'Картинка')],BASE+6*1740);
out.m4=section(NEW[3],[nm(memeRows('Мем',[{cls:'yes',img:'klass',lbl:'Ожидание',t:'Открою второй филиал — будет в два раза больше денег'},{cls:'no',img:'ustal',lbl:'Реальность',t:'В два раза больше чатов, тренеров и отчётов'}]),'Мем')],BASE+8*1740);
out.m5=section(NEW[4],[nm(memeRows('Мем',[{cls:'b1',img:'dumaet',t:'Привести больше учеников',size:40},{cls:'b2',img:'networking',t:'Удержать тех, кто уже пришёл',size:40},{cls:'b3',img:'flipchart',t:'Посчитать, сколько стоит каждый ушедший',size:40},{cls:'b4',img:'aplodiruet',t:'Разобрать это с теми, кто уже решил, — на РЕШЕНО',size:40}]),'Мем')],BASE+10*1740);
const K=[
 {t:'ink',m:['dumaet',740,150,330,1],bt:'Варианты — до 15 октября',bl:[['tag','Конкурс'],['gap','s'],['d',120,['Придумайте','имя зубру —','*выиграйте','*билет']]]},
 {t:'amber',bt:'Голосование до 17 октября, 23:59',bl:[['tag','Голосование'],['gap','s'],['d',120,['Выбираем','имя','*зубру']],['gap','m'],['slot','Сюда — стикер-опрос с вариантами имени',520]]},
 {t:'ink',m:['aplodiruet',820,140,330,1],bt:'До встречи на РЕШЕНО!',bl:[['tag','Имя выбрано'],['gap','s'],['d',120,['Знакомьтесь:','*[ИМЯ]']],['gap','s'],['p','Автор — <b>@[ник]</b>. Билет на РЕШЕНО — ваш!']]}];
out.k=section(NEW[5],K.map((s,i)=>story(s,['12.10 Старт','16.10 Голосование','18.10 Победитель'][i])),BASE+14*1740);
const poses=['priglashaet','v-shoke','zlitsya','klass','podmigivaet','aplodiruet','smeetsya','dumaet','ustal','facepalm','zakatyvaet-glaza','flipchart','smeetsya-2','spit'];
const days=n=>(n%10===1&&n%100!==11)?'день':([2,3,4].includes(n%10)&&![12,13,14].includes(n%100))?'дня':'дней';
const ST=poses.map((p,i)=>{const n=32-i,wide=['spit','flipchart','ustal'].includes(p);return story({t:i%2?'ink':'amber',m:[p,wide?640:840,wide?40:120,330,i%2],bt:'reshenoforum.ru',bl:[['tag','До форума'],['gap','s'],['d',360,[String(n)]],['d',130,[days(n)]],['gap','s'],['p','13–14 ноября · Москва',32]]},`${12+i}.10 — ${n}`);});
out.o=section(NEW[6],ST,BASE+14*1740+2400);
const assets={};for(const n of page.findAll(x=>x.name.startsWith('asset:')))assets[n.name.slice(6)]=n.fills;
let done=0,miss=[];for(const n of page.findAll(x=>x.type==='RECTANGLE'&&x.name.startsWith('zubr:'))){const f=assets[n.name.slice(5)];if(f&&f[0]&&f[0].type==='IMAGE'){n.fills=[{...f[0],scaleMode:'FILL'}];done++;}else miss.push(n.name);}
return {out,done,miss:miss.slice(0,5),missN:miss.length};
