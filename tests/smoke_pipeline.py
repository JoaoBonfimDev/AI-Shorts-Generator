"""End-to-end orchestration with synthetic video and explicit ASR fixtures, no private live."""
import sys,tempfile,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from aishorts.config import ROOT,load,run_directory
from aishorts import media,scan
from aishorts.pipeline import execute
parent=ROOT/'.local/tests';parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(dir=parent) as tmp:
    f=Path(tmp);source=f/'synthetic32.mp4'
    media.run(['-f','lavfi','-i','testsrc2=size=320x180:rate=30','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','32','-c:v','libx264','-c:a','aac',str(source)])
    cfg=load();cfg.update(input=str(source),data_directory=str(f/'data'),export_directory=str(f/'export'),encoder='libx264',duration_seconds=30)
    folder=run_directory(cfg);scan.visuals(cfg,folder)
    media.save(folder/'transcript.json',[{'start':10,'end':14,'text':'Nossa, consegui! Finalmente, caramba!', 'language':'pt','avg_logprob':-.1,'no_speech_prob':0,'words':[{'start':10,'end':14,'text':'Legenda sintética'}]}])
    media.save(folder/'energy.json',[.05]*32);media.save(folder/'coverage_audio.json',{'completed':True,'test_fixture':True})
    execute(cfg,folder,'run');count=len(list((f/'export').glob('*.mp4')));assert count==1
    execute(cfg,folder,'export');assert len(list((f/'export').glob('*.mp4')))==count
    media.save(parent/'pipeline_result.json',{'synthetic_video':True,'asr_fixture':True,'run_rank_render_verify_export_passed':True,'resume_without_duplicate_export':True,'fewer_than_four_handled':True})
    print('Pipeline sintético e retomada: OK')
