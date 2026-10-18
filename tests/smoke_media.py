"""Optional real FFmpeg/Whisper smoke test; creates only synthetic media in .local/tests."""
import argparse,sys,json,shutil,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from aishorts import media,scan
from aishorts.config import load,ROOT
from aishorts.render import render
from aishorts.pipeline import verify
from aishorts.export import export_files

parser=argparse.ArgumentParser();parser.add_argument('--model-path');args=parser.parse_args()
parent=ROOT/'.local/tests';parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(dir=parent) as tmp:
    f=Path(tmp);source=f/'synthetic.mp4'
    media.run(['-f','lavfi','-i','testsrc2=size=320x180:rate=30','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','4','-c:v','libx264','-c:a','aac',str(source)])
    cfg=load();cfg.update(input=str(source),sample_seconds=1,encoder='libx264',model_path=args.model_path or '',data_directory=str(f),label='TESTE SINTÉTICO')
    scan.visuals(cfg,f)
    if args.model_path:scan.audio(cfg,f)
    out=f/'renders';out.mkdir();clip={'rank':1,'slug':'smoke','title':'Teste local','hook':'Teste local','parts':[[0,2]]}
    media.save(out/'01_transcript.json',[{'words':[{'start':.3,'end':.5,'text':'Legenda de teste'}]}])
    render(cfg,out,[clip]);verified=verify([out/'01_smoke.mp4'],[clip],out)
    sources=[out/'01_smoke.mp4']
    for i in range(2,5):p=out/f'{i:02}_smoke.mp4';shutil.copyfile(sources[0],p);sources.append(p)
    exported=export_files(sources,source,f/'exports')
    result={'synthetic_only':True,'visual_scan':True,'local_whisper_executed':bool(args.model_path),'render_cpu':True,'full_decode':verified[0]['full_decode_passed'],'four_hash_verified_copies':len(exported)==4,'private_media_used':False,'network_calls':0}
    media.save(parent/'smoke_result.json',result);print(json.dumps(result,indent=2))
