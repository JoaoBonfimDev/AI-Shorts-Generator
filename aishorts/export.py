"""Export local MP4s without recompression or overwriting previous exports."""
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def export_files(files, source, destination, count=4, manifest=None):
    if os.name != 'nt':
        raise RuntimeError('Exportação exige Windows local; não usar armazenamento de nuvem.')
    destination = Path(destination)
    if not destination.is_absolute() or not Path(destination.anchor).is_dir():
        raise RuntimeError(f'Disco local indisponível: {destination.anchor}')
    files = [Path(p) for p in files][:count]
    if len(files) != count or any(not p.is_file() or p.suffix.lower() != '.mp4' for p in files):
        raise ValueError(f'São necessários {count} MP4 prontos antes de exportar.')
    destination.mkdir(parents=True, exist_ok=True)
    prefix = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', Path(source).stem).strip(' .')[:100]
    results = []
    for src in files:
        expected = digest(src)
        base = f'{prefix} - {src.stem}'
        suffix = 1
        while True:
            name = base if suffix == 1 else f'{base} ({suffix})'
            target = destination / f'{name}.mp4'
            try:
                output = target.open('xb')  # Atomic exclusive creation: never overwrite.
                break
            except FileExistsError:
                suffix += 1
        try:
            with output, src.open('rb') as original:
                shutil.copyfileobj(original, output, length=1024 * 1024)
                output.flush()
                os.fsync(output.fileno())
            if digest(target) != expected:
                raise IOError(f'Falha ao verificar cópia: {target}')
        except BaseException:
            target.unlink(missing_ok=True)  # Only the new file exclusively created above.
            raise
        results.append({'file': str(target), 'bytes': target.stat().st_size, 'sha256': expected})
        print(f'Confirmado: {target}', flush=True)
    if manifest:
        from .media import save
        save(Path(manifest), {'source':str(source),'files':results})
    return results
