"""Local paths and source/config-specific caches; no Work dependency."""
import hashlib,json
from pathlib import Path
from contextlib import contextmanager
from .media import save

ROOT=Path(__file__).resolve().parents[1]

def load(path=None):
    path=Path(path or ROOT/'config.local.json').resolve()
    cfg=json.loads((ROOT/'config.example.json').read_text(encoding='utf-8'))
    if path.exists(): cfg.update(json.loads(path.read_text(encoding='utf-8-sig')))
    if cfg['paid_api_enabled']: raise ValueError('APIs externas não implementadas; mantenha paid_api_enabled=false.')
    if not 30<=cfg['duration_seconds']<=60: raise ValueError('duration_seconds deve estar entre 30 e 60.')
    if cfg['shorts']!=4: raise ValueError('Esta versão seleciona até quatro cortes.')
    if any(not isinstance(cfg[k],int) or cfg[k]<0 for k in ('audio_track','render_audio_track')):raise ValueError('Faixas de áudio devem ser inteiros não negativos.')
    if cfg['sample_seconds']<=0 or cfg['chunk_seconds']<10: raise ValueError('Intervalos de análise inválidos.')
    if cfg['encoder'] not in ('auto','libx264','h264_nvenc'): raise ValueError('Encoder inválido.')
    for key in ('input','export_directory','data_directory','model_path'):
        if cfg.get(key):
            p=Path(cfg[key]).expanduser();cfg[key]=str(p.resolve() if p.is_absolute() else (path.parent/p).resolve())
    return cfg

def identity(cfg):
    p=Path(cfg['input'])
    if not p.is_file(): raise FileNotFoundError('Configure input com o caminho de um vídeo existente.')
    analysis={k:cfg[k] for k in ('model','model_path','language','audio_track','sample_seconds','chunk_seconds')}
    value=[str(p.resolve()),p.stat().st_size,p.stat().st_mtime_ns,analysis,1]
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()[:20]

def run_directory(cfg):
    p=Path(cfg['data_directory'])/'runs'/identity(cfg);p.mkdir(parents=True,exist_ok=True);return p

@contextmanager
def lock(folder):
    p=folder/'running.lock'
    try: f=p.open('x')
    except FileExistsError: raise RuntimeError(f'Execução em andamento ou interrompida. Confira processos antes de remover {p}')
    try:
        import os
        with f:f.write(str(os.getpid()))
        yield
    finally:p.unlink(missing_ok=True)
