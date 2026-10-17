import {chromium} from '../apps/web/node_modules/playwright/index.mjs';
import {mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const artifacts=fileURLToPath(new URL('../artifacts/',import.meta.url));await mkdir(artifacts,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true,slowMo:200});
const context=await browser.newContext({viewport:{width:1440,height:1000},recordVideo:{dir:artifacts,size:{width:1440,height:1000}}});
const page=await context.newPage();const video=page.video();let sourceChanged=false;
const pause=()=>page.waitForTimeout(1800);
try{
 await page.goto('http://127.0.0.1:3000/investigate');
 await page.getByRole('combobox',{name:'Workspace role'}).selectOption('Lead');
 await page.getByText('200 accessible records',{exact:true}).waitFor();await pause();
 const pending=page.waitForResponse(r=>r.url().endsWith('/api/v1/investigations')&&r.request().method()==='POST');
 await page.getByRole('button',{name:'Find launch risks'}).click();
 const run=(await (await pending).json()).run_id;
 await page.getByRole('heading',{name:'1 known blocker and an ownership conflict'}).waitFor();
 await page.locator('.answerSummary').scrollIntoViewIfNeeded();await pause();
 await page.getByRole('button',{name:'Open evidence 1',exact:true}).first().click();await page.locator('blockquote').waitFor();await pause();
 await page.keyboard.press('Escape');await page.getByRole('button',{name:'Graph',exact:true}).click();await pause();
 await page.getByRole('button',{name:'Prepare review task'}).click();
 await page.getByRole('button',{name:'Preview review'}).click();await pause();
 await page.getByRole('button',{name:'Create review task'}).click();await page.getByText('Created',{exact:true}).waitFor();await pause();
 await page.getByRole('button',{name:'Close dialog'}).click();
 await page.goto('http://127.0.0.1:3000/sources');await page.getByRole('heading',{name:'Sources',exact:true}).waitFor();await pause();
 await page.getByRole('button',{name:'Update ticket status',exact:true}).click();
 await page.getByRole('combobox',{name:'Ticket to update'}).selectOption('ticket:T-101');
 await page.getByRole('combobox',{name:'New ticket status'}).selectOption('done');
 await page.getByRole('button',{name:'Save status',exact:true}).click();sourceChanged=true;
 await page.getByRole('status').filter({hasText:'Indexed'}).waitFor();await pause();
 await page.goto('http://127.0.0.1:3000/investigate?run='+run);
 await page.getByText('Sources changed since this answer. Rerun to use current evidence.').waitFor();
 await page.getByRole('button',{name:'Rerun',exact:true}).click();
 await page.getByRole('heading',{name:'No confirmed blockers and an ownership conflict'}).waitFor();
 await page.getByRole('heading',{name:'What changed'}).scrollIntoViewIfNeeded();await pause();
 await page.screenshot({path:artifacts+'updated-investigation.png',fullPage:true});
}finally{
 if(sourceChanged){
  const source=(await (await page.request.get('http://127.0.0.1:3000/api/v1/sources?limit=100&q=T-101')).json()).items.find(s=>s.id==='ticket:T-101');
  const envelope={schema_version:'1.0',source_id:'ticket:T-101',kind:'ticket',title:'T-101 · Payment confirmation check',source_updated_at:'2026-10-17T03:30:00Z',acl_groups:['engineering'],body:'',expected_revision_id:source.active_revision_id,records:{entity_id:'ticket:T-101',status:'blocked',blocks:['service:payments']}};
  await page.request.post('http://127.0.0.1:3000/api/v1/imports',{headers:{origin:'http://localhost:3000','x-brain-csrf':'1'},multipart:{files:{name:'ticket.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(envelope))}}});
 }
 await context.close();await video.saveAs(artifacts+'demo.webm');await video.delete();await browser.close();
}
console.log('Recorded artifacts/demo.webm. Automated walkthrough, synthetic data, no narration; scenario restored.');
