import os, sqlite3, time, json, threading, queue, shutil, sys, glob
from pathlib import Path

ROOT = Path(os.environ.get('ULTRA_MEGA_DB', Path.home() / 'AppData' / 'Local' / 'UltraMegaTextSearchTool'))
SOURCE = Path(os.environ.get('ULTRA_MEGA_SOURCE', '.'))
DB = ROOT/'search.sqlite3'
STATUS = ROOT/'build-status.json'
STOP = ROOT/'stop-build.flag'
MIN_FREE = 20 * 1024**3

def status(**data):
    temp=ROOT/('build-status-%s.tmp' % os.getpid())
    temp.write_text(json.dumps(data),encoding='utf-8')
    for attempt in range(20):
        try:
            os.replace(temp,STATUS); return
        except PermissionError:
            time.sleep(0.1)
    try: temp.unlink()
    except OSError: pass  # A transient display update must not stop indexing.

def connect():
    c=sqlite3.connect(str(DB),timeout=30)
    c.execute('PRAGMA busy_timeout=30000')
    return c

def build():
    ROOT.mkdir(parents=True,exist_ok=True)
    c=connect(); c.execute('PRAGMA journal_mode=WAL'); c.execute('PRAGMA synchronous=NORMAL'); c.execute('PRAGMA cache_size=-%d' % (int(os.environ.get('BREACH_CACHE_MB','256')) * 1024))
    c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS records USING fts5(text, tokenize='trigram')")
    c.execute('CREATE TABLE IF NOT EXISTS completed (path TEXT PRIMARY KEY, size INTEGER, modified INTEGER, rows INTEGER)')
    c.commit(); files=([SOURCE] if SOURCE.is_file() else sorted(p for p in SOURCE.rglob('*') if p.is_file() and not p.is_symlink())); started=time.time(); count=0
    total_bytes=sum(p.stat().st_size for p in files); done_bytes=0
    try:
        for i,p in enumerate(files):
            if STOP.exists(): status(state='Stopped',file=i,total=len(files),rows=count,seconds=round(time.time()-started)); break
            st=p.stat(); old=c.execute('SELECT size,modified FROM completed WHERE path=?',(str(p),)).fetchone()
            if old:
                if old != (st.st_size,st.st_mtime_ns):
                    status(state='Error: a previously indexed source file changed. Rebuild required.',file=i,total=len(files),rows=count); return
                done_bytes+=st.st_size
                continue
            if shutil.disk_usage(ROOT).free < MIN_FREE:
                status(state='Paused: less than 20 GiB free on the database drive. Free space and restart.',file=i,total=len(files),rows=count); break
            status(state='Indexing',file=i+1,total=len(files),current=(p.name if SOURCE.is_file() else str(p.relative_to(SOURCE))),rows=count,seconds=round(time.time()-started),done_bytes=done_bytes,total_bytes=total_bytes)
            n=0
            try:
                c.execute('BEGIN')
                with p.open('r',encoding='utf-8',errors='replace',newline=None) as f:
                    batch=[]
                    for line in f:
                        batch.append((line.rstrip('\r\n'),)); n+=1
                        if len(batch)>=10000:
                            c.executemany('INSERT INTO records(text) VALUES (?)',batch); batch.clear()
                            if STOP.exists() or shutil.disk_usage(ROOT).free < MIN_FREE: raise InterruptedError('Stopped or low disk space')
                    if batch: c.executemany('INSERT INTO records(text) VALUES (?)',batch)
                if (p.stat().st_size,p.stat().st_mtime_ns)!=(st.st_size,st.st_mtime_ns): raise RuntimeError('Source file changed during indexing')
                c.execute('INSERT INTO completed VALUES (?,?,?,?)',(str(p),st.st_size,st.st_mtime_ns,n)); c.commit(); count+=n; done_bytes+=st.st_size
            except Exception as e:
                c.rollback(); status(state='Paused: '+str(e),file=i,total=len(files),current=str(p),rows=count); return
        else: status(state='Complete',file=len(files),total=len(files),rows=count,seconds=round(time.time()-started),done_bytes=total_bytes,total_bytes=total_bytes)
    except Exception as e: status(state='Error: '+str(e),rows=count)
    finally:
        c.close()
        try: STOP.unlink()
        except FileNotFoundError: pass

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--build': build()
    elif len(sys.argv)>1 and sys.argv[1]=='--search':
        try:
            request=json.loads(sys.stdin.readline()); text=request['text']; sensitive=request.get('case',False); maximum=request.get('limit',500)
            c=sqlite3.connect('file:'+str(DB).replace('\\','/')+'?mode=ro',uri=True,timeout=30)
            q='"'+text.replace('"','""')+'"'; start=time.monotonic(); count=0
            for (line,) in c.execute('SELECT text FROM records WHERE records MATCH ?', (q,)):
                if (text in line) if sensitive else (text.lower() in line.lower()):
                    print(json.dumps({'line':line}),flush=True); count+=1
                    if count>=maximum: break
            print(json.dumps({'done':count,'seconds':round(time.monotonic()-start,2),'capped':count>=maximum}),flush=True); c.close()
        except Exception as e: print(json.dumps({'error':str(e)}),flush=True)
    else: print('Run Ultra Mega Text Search Tool.exe to open the application.')

