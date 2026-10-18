"""CLI independente: python main.py --help."""
import argparse,json,sys
from pathlib import Path
from aishorts.config import ROOT,load,run_directory,lock
from aishorts.media import save

def main():
    parser=argparse.ArgumentParser(description='AI Shorts Generator — local, sem APIs de inferência.')
    parser.add_argument('stage',choices=['init','doctor','prepare-model','inspect','scan','rank','render','verify','export','run'])
    parser.add_argument('--config',type=Path,default=ROOT/'config.local.json')
    parser.add_argument('--input',help='Vídeo original; não será copiado nem alterado.')
    parser.add_argument('--output',help='Diretório de exportação dos MP4.')
    parser.add_argument('--model-path',help='Pasta local contendo model.bin do faster-whisper.')
    parser.add_argument('--ranking',type=Path,help='Ranking revisado com source_id da execução.')
    parser.add_argument('--allow-download',action='store_true',help='Permite somente baixar modelo gratuito; não envia vídeos.')
    args=parser.parse_args()
    if args.stage=='init':
        cfg=load(args.config)
        for key,value in [('input',args.input),('export_directory',args.output),('model_path',args.model_path)]:
            if value:cfg[key]=str(Path(value).resolve())
        save(args.config,cfg);print(f'Configuração local salva: {args.config}');return
    cfg=load(args.config)
    if args.input:cfg['input']=str(Path(args.input).resolve())
    if args.output:cfg['export_directory']=str(Path(args.output).resolve())
    if args.model_path:cfg['model_path']=str(Path(args.model_path).resolve())
    if args.stage=='doctor':
        import importlib.metadata as m
        from aishorts.media import ffmpeg
        from aishorts.pipeline import choose_encoder
        from aishorts.scan import model_location
        print('Python:',sys.version.split()[0])
        for name in ['faster-whisper','imageio-ffmpeg','numpy','av','opencv-python-headless','ctranslate2']:print(name,m.version(name))
        print('FFmpeg:',ffmpeg());print('Encoder:',choose_encoder(cfg))
        try:print('Modelo local:',model_location(cfg))
        except FileNotFoundError:print('Modelo pendente: configure model_path ou use prepare-model --allow-download.')
        print('Nenhum serviço Work ou chave de API necessário para executar. Ranking automático é heurístico.');return
    if args.stage=='prepare-model':
        if not args.allow_download:parser.error('Confirme download gratuito com --allow-download, ou configure --model-path existente.')
        from faster_whisper.utils import download_model
        dest=Path(cfg['data_directory'])/'models'/cfg['model'];dest.parent.mkdir(parents=True,exist_ok=True)
        download_model(cfg['model'],output_dir=str(dest));print(dest);return
    folder=run_directory(cfg)
    print(f'Execução: {folder.name}\nIntermediários: {folder}',flush=True)
    if args.stage=='inspect':
        from aishorts.media import inspect
        print(json.dumps(inspect(Path(cfg['input'])),ensure_ascii=False,indent=2));return
    from aishorts.pipeline import execute
    with lock(folder):execute(cfg,folder,args.stage,args.ranking)

if __name__=='__main__':
    try:main()
    except (ValueError,FileNotFoundError,RuntimeError,PermissionError) as e:
        print(f'Erro: {e}',file=sys.stderr);sys.exit(1)
