// Exercise the actual form runtime offline: no browser, Analytics or WhatsApp requests.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('_site/assets/phase107.js', 'utf8');

function submit({search='', lang='en', path='/contact/', service='Luxury Travel Concierge', valid=true}={}) {
  let handler;
  const notes=[];
  const elements={};
  for (const [id,value] of Object.entries({fName:'Example Guest',fPhone:'+1 212 555 0100',
    fArrival:'',fDeparture:'',fGuests:'2',fService:service,fBrief:'',
    fClientType:'travel_advisor',fArea:'ibiza_town'})) {
    elements[id]={value,addEventListener(){},setCustomValidity(message){this.validationMessage=message;}};
  }
  const form={addEventListener(type,fn){if(type==='submit')handler=fn;},
    before(note){notes.push(note);},reportValidity(){return valid&&Object.values(elements).every(el=>!el.validationMessage);}};
  const location={pathname:path,search,href:'unchanged'};
  const window={location,dispatchEvent(){}};
  vm.runInNewContext(code,{window,URLSearchParams,Intl,Date,Number,Boolean,
    document:{documentElement:{lang},getElementById(id){return id==='conciergeForm'?form:elements[id];},
      createElement(){return {style:{}};}},
    sessionStorage:{getItem(){return null;}},
    CustomEvent:class{constructor(type,init){this.type=type;this.detail=init.detail;}}});
  assert.equal(elements.fBrief.value,'');
  assert.equal(elements.fService.value,service);
  assert.equal(elements.fClientType.value,'travel_advisor');
  handler({preventDefault(){},stopImmediatePropagation(){}});
  if(!valid){assert.equal(location.href,'unchanged');assert.equal(window.dataLayer,undefined);return;}
  const target=new URL(location.href);
  assert.equal(target.origin+target.pathname,'https://wa.me/34600703303');
  const text=target.searchParams.get('text');
  assert.ok(text.includes(service));
  assert.ok(text.includes('Example Guest'));
  assert.equal(window.dataLayer.length,1);
  assert.equal(window.dataLayer[0].brief_present,false);
  assert.equal(window.dataLayer[0].service,service);
  assert.ok(!JSON.stringify(window.dataLayer).includes('Example Guest'));
  return {text,notes};
}

const plain=submit();
assert.equal(plain.notes.length,0);
assert.ok(!plain.text.includes('Enquiry page:'));
const origin=submit({search:'?service=travel-concierge&origin=new-york'});
assert.equal(origin.notes.length,1);
assert.equal(origin.notes[0].textContent,'Enquiry page: New York → Ibiza');
assert.equal(origin.text.replace('Enquiry page: New York → Ibiza\n',''),plain.text);
for(const search of ['?origin=miami','?origin=new-york&origin=new-york',
  '?origin=new-york&origin=miami','?origin=%3Cscript%3E','?origin=']) {
  const result=submit({search});
  assert.equal(result.notes.length,0);
  assert.equal(result.text,plain.text);
}
for(const lang of ['es','fr','de','ar']) {
  const result=submit({lang,search:'?origin=new-york'});
  assert.equal(result.notes.length,0);
  assert.ok(!result.text.includes('Enquiry page:'));
}
assert.equal(submit({path:'/other/',search:'?origin=new-york'}).notes.length,0);
assert.ok(submit({search:'?origin=new-york',service:'Full Concierge'}).text.includes('Service: Full Concierge'));
submit({search:'?origin=new-york',valid:false});
console.log('PASS: New York context reaches the WhatsApp draft; invalid contexts, editable service, empty brief, validation and other languages are preserved. No requests sent.');
