import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
export async function serve(rootDir='dist',port=4330){
 const root=path.resolve(rootDir),mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.json':'application/json','.jpeg':'image/jpeg','.jpg':'image/jpeg','.png':'image/png','.woff2':'font/woff2'};
 const server=http.createServer((req,res)=>{let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/kleines-schaeferrad\//,'');if(!p||p.endsWith('/'))p+='index.html';const f=path.resolve(root,p);if(!f.startsWith(root+path.sep)||!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);return res.end()}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');fs.createReadStream(f).pipe(res)});
 await new Promise(r=>server.listen(port,'127.0.0.1',r));return {base:`http://127.0.0.1:${port}/kleines-schaeferrad/`,close:()=>new Promise(r=>server.close(r))};
}
