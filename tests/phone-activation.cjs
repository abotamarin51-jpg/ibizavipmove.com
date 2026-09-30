'use strict';
// Offline event-model regression test. No browser or external/network APIs.
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8');
const start=source.indexOf('let ivmLastPhoneTrack=0;');
const end=source.indexOf("const f=document.getElementById('conciergeForm');",start);
assert.ok(start>=0&&end>start,'Expected phone and delegated contact block');
const code=source.slice(start,end);
function harness(){
 let clock=10000;
 const listeners={}; const events=[];
 const context={Date:{now:()=>clock},document:{addEventListener(type,fn,options){(listeners[type]??=[]).push({fn,capture:!!options?.capture});}},ivmTrack:(type,detail)=>events.push({type,detail}),ivmPlacement:()=> 'hero',ivmContextLabel:()=> 'Private Concierge'};
 vm.runInNewContext(code,context,{timeout:1000});
 function anchor(href='tel:+34000000000'){
  return {textContent:'Call Concierge',getAttribute:k=>k==='href'?href:null,closest(s){return s==='a'||s==='a[href^="tel:"]'&&href.startsWith('tel:')?this:null;}};
 }
 function emit(type,target=anchor(),extra={}){
  const event={target,button:0,detail:1,defaultPrevented:false,preventDefault(){this.defaultPrevented=true;},...extra};
  const list=[...(listeners[type]||[])].sort((a,b)=>Number(b.capture)-Number(a.capture));
  for(const {fn} of list)fn(event);
  assert.equal(event.defaultPrevented,false,'Application must not cancel link activation');
  return event;
 }
 return {anchor,emit,events,advance:ms=>{clock+=ms;},phones:()=>events.filter(e=>e.type==='phone_click').length};
}
const cases=[
 ['pointerdown without activation',h=>{h.emit('pointerdown');assert.equal(h.phones(),0);}],
 ['scroll/pointercancel without click',h=>{const a=h.anchor();h.emit('pointerdown',a);h.emit('pointercancel',a);assert.equal(h.phones(),0);}],
 ['secondary button/context menu',h=>{const a=h.anchor();h.emit('pointerdown',a,{button:2});h.emit('contextmenu',a,{button:2});h.emit('pointerup',a,{button:2});assert.equal(h.phones(),0);}],
 ['completed tap counts once',h=>{const a=h.anchor();h.emit('pointerdown',a);h.emit('pointerup',a);h.emit('click',a);assert.equal(h.phones(),1);}],
 ['keyboard activation counts once',h=>{h.emit('click',h.anchor(),{detail:0});assert.equal(h.phones(),1);}],
 ['primary mouse click counts once',h=>{h.emit('click');assert.equal(h.phones(),1);}],
 ['two separated activations count twice',h=>{h.emit('click');h.advance(2000);h.emit('click');assert.equal(h.phones(),2);}],
 ['nested element activation',h=>{const a=h.anchor();h.emit('click',{closest:s=>a.closest(s)});assert.equal(h.phones(),1);}],
 ['WhatsApp remains unchanged',h=>{h.emit('click',h.anchor('https://wa.me/34600703303'));assert.equal(h.events[0]?.type,'whatsapp_click');assert.equal(h.events.length,1);}],
 ['email remains unchanged',h=>{h.emit('click',h.anchor('mailto:fixture@example.invalid'));assert.equal(h.events[0]?.type,'email_click');}],
 ['request remains unchanged',h=>{h.emit('click',h.anchor('/contact/'));assert.equal(h.events[0]?.type,'request_concierge_click');}],
 ['partner interest remains unchanged',h=>{h.emit('click',h.anchor('/partners/'));assert.equal(h.events[0]?.type,'partner_interest_click');}],
 ['non-link creates no event',h=>{h.emit('click',{closest:()=>null});assert.equal(h.events.length,0);}],
 ['secondary click is not a phone activation',h=>{h.emit('click',h.anchor(),{button:2});assert.equal(h.phones(),0);}]
];
let failed=0;
for(const [name,test] of cases){try{test(harness());console.log('PASS '+name);}catch(e){failed++;console.log('FAIL '+name+': '+e.message);}}
console.log(JSON.stringify({cases:cases.length,passed:cases.length-failed,failed}));
process.exitCode=failed?1:0;
