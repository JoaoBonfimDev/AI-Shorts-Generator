"""Create source-only ZIP using an explicit allowlist. Never package local media/configs."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
TOP=['main.py','package_project.py','README.md','requirements.txt','.gitignore','config.example.json','Instalar.cmd','Executar.cmd']
ALLOWED={'aishorts':{'.py'},'tests':{'.py'},'docs':{'.md','.json','.txt'},'.vscode':{'.json'}}

def source_files():
    files=[ROOT/n for n in TOP]
    for directory,suffixes in ALLOWED.items():
        files.extend(p for p in (ROOT/directory).glob('*') if p.is_file() and p.suffix in suffixes)
    return sorted(files)

if __name__=='__main__':
    tree=['AI-Shorts-Generator/']
    for p in source_files():tree.append('  '+p.relative_to(ROOT).as_posix())
    tree+=['','Arquivos locais não incluídos no ZIP:','  config.local.json (entrada/saída/modelo pessoais)','  .venv/ (instalada pelo usuário)','  .local/ (modelos, intermediários, testes e resultados privados)']
    (ROOT/'docs/ESTRUTURA.txt').write_text('\n'.join(tree),encoding='utf-8')
    files=source_files()
    # Include structure itself in its inventory on first packaging.
    names=[p.relative_to(ROOT).as_posix() for p in files]
    tree=['AI-Shorts-Generator/']+['  '+n for n in names]+tree[tree.index(''):]
    (ROOT/'docs/ESTRUTURA.txt').write_text('\n'.join(tree),encoding='utf-8')
    target=ROOT.parent/(ROOT.name+'.zip')
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert all(not n.endswith(('.mp4','.mkv','.wav','.srt','.ass')) and 'config.local.json' not in n and '/.local/' not in n for n in z.namelist())
    print(json.dumps({'zip':str(target),'source_files':len(files),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
