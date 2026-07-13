async function loadPartial(id,file){const el=document.getElementById(id);if(!el)return;try{const r=await fetch(file);el.innerHTML=await r.text()}catch(e){console.error(e)}}
Promise.all([loadPartial('site-header','header.html'),loadPartial('site-footer','footer.html')]).then(()=>{const h=document.querySelector('[data-header]'),btn=document.querySelector('.menu-toggle'),nav=document.querySelector('.primary-nav');window.addEventListener('scroll',()=>h?.classList.toggle('is-scrolled',scrollY>12));btn?.addEventListener('click',()=>{const open=nav.classList.toggle('open');btn.setAttribute('aria-expanded',String(open))});const page=location.pathname.split('/').pop()||'index.html';document.querySelectorAll('.primary-nav a').forEach(a=>{if(a.getAttribute('href')===page)a.setAttribute('aria-current','page')})});

const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;

document.querySelectorAll('[data-showcase]').forEach(box=>{
  const track=box.querySelector('.showcase-track');
  if(!track)return;
  const scope=box.closest('section')||box.parentElement;
  const prev=scope?.querySelector('[data-prev]');
  const next=scope?.querySelector('[data-next]');
  const interval=Math.max(4200,Number(box.dataset.interval||6500));
  const step=()=>{const card=track.querySelector(':scope > *');if(!card)return 320;const gap=parseFloat(getComputedStyle(track).columnGap||getComputedStyle(track).gap||'16')||16;return card.getBoundingClientRect().width+gap};
  const canMove=()=>track.scrollWidth>track.clientWidth+8;
  const go=d=>{if(!canMove())return;track.scrollBy({left:d*step(),behavior:reduced?'auto':'smooth'})};
  prev?.addEventListener('click',()=>go(-1));
  next?.addEventListener('click',()=>go(1));
  let visible=false;
  let timer=null;
  const stop=()=>{if(timer){clearInterval(timer);timer=null}};
  const start=()=>{stop();if(reduced||!visible||!canMove())return;timer=setInterval(()=>{if(box.matches(':hover,:focus-within'))return;const atEnd=track.scrollLeft+track.clientWidth>=track.scrollWidth-8;track.scrollTo({left:atEnd?0:track.scrollLeft+step(),behavior:'smooth'})},interval)};
  new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;start()},{threshold:.28}).observe(box);
  new MutationObserver(start).observe(track,{childList:true});
  box.addEventListener('mouseenter',stop);
  box.addEventListener('mouseleave',start);
  box.addEventListener('focusin',stop);
  box.addEventListener('focusout',start);
  window.addEventListener('resize',start);
});

document.querySelectorAll('[data-outcomes]').forEach(stack=>{const cards=[...stack.children];let i=0;cards[0]?.classList.add('active');if(!reduced)setInterval(()=>{cards[i].classList.remove('active');i=(i+1)%cards.length;cards[i].classList.add('active')},3000)});

const box=document.querySelector('[data-word-limit]'),count=document.querySelector('[data-word-count]');box?.addEventListener('input',()=>{let words=box.value.trim()?box.value.trim().split(/\s+/):[];if(words.length>300){box.value=words.slice(0,300).join(' ');words=words.slice(0,300)}if(count)count.textContent=`${words.length} / 300 words`});

document.querySelectorAll('[data-modal-open]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.modalOpen)?.classList.add('open')));document.querySelectorAll('[data-modal-close]').forEach(b=>b.addEventListener('click',()=>b.closest('.modal')?.classList.remove('open')));document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(m=>m.classList.remove('open'))});
