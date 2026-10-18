import json,tempfile,unittest
from pathlib import Path
from aishorts.config import load,identity,lock
from aishorts.media import save
from aishorts.ranking import generate,validate,LIMITS,selected,overlap
from aishorts.pipeline import captions
from aishorts.export import export_files,digest

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_root=Path(__file__).resolve().parents[1]/'.local/tests'
        self.temp_root.mkdir(parents=True,exist_ok=True)
    def test_cache_tracks_source_and_analysis_not_destination(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            p=Path(tmp)/'source.mp4';p.write_bytes(b'first');cfg=load();cfg['input']=str(p)
            first=identity(cfg);cfg['export_directory']=tmp;self.assertEqual(first,identity(cfg))
            cfg['audio_track']=1;self.assertNotEqual(first,identity(cfg));cfg['audio_track']=0
            p.write_bytes(b'changed');self.assertNotEqual(first,identity(cfg))

    def test_lock_prevents_parallel_runs(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            with lock(Path(tmp)):
                with self.assertRaises(RuntimeError):
                    with lock(Path(tmp)):pass
            self.assertFalse((Path(tmp)/'running.lock').exists())

    def test_no_candidates_for_silence_and_static_frames(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            f=Path(tmp);save(f/'transcript.json',[]);save(f/'energy.json',[0]*180)
            save(f/'visual.json',[{'seconds_approx':t,'difference':0,'brightness':0} for t in range(0,180,10)])
            self.assertEqual(generate(f,load(),180)['selected'],[])

    def test_whole_recording_and_limits(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            f=Path(tmp);save(f/'transcript.json',[{'start':170,'end':178,'text':'Nossa, consegui! Finalmente, caramba!', 'avg_logprob':-.1}])
            save(f/'energy.json',[.05]*180);save(f/'visual.json',[{'seconds_approx':t,'difference':20 if t>=140 else 0,'brightness':80} for t in range(0,180,10)])
            result=validate(generate(f,load(),180),180)
            self.assertTrue(selected(result));self.assertGreaterEqual(selected(result)[0]['start'],130)
            for c in result['clips']:
                self.assertEqual(c['score'],sum(c['scores'].values()))
                self.assertTrue(all(0<=v<=LIMITS[k] for k,v in c['scores'].items()))

    def test_caption_remap_and_low_confidence_exclusion(self):
        rows=[{'start':10,'end':11,'text':'Olá','language':'pt','avg_logprob':-.1,'no_speech_prob':0,'words':[{'start':10,'end':11,'text':'Olá'}]}, {'language':'en','words':[]}, {'language':'pt','avg_logprob':-2,'words':[]}]
        out=captions(rows,{'parts':[[0,2],[10,12]]})
        self.assertEqual(len(out),1);self.assertEqual(out[0]['words'][0]['start'],2)

    def test_export_no_overwrite_and_hash(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as tmp:
            f=Path(tmp);sources=[]
            for i in range(4):p=f/f'{i}.mp4';p.write_bytes(bytes([i])*1024);sources.append(p)
            a=export_files(sources,'Live.mkv',f/'dest');b=export_files(sources,'Live.mkv',f/'dest')
            self.assertEqual(len(list((f/'dest').glob('*.mp4'))),8)
            for src,x,y in zip(sources,a,b):
                self.assertNotEqual(x['file'],y['file']);self.assertEqual(digest(src),digest(Path(y['file'])))
            with self.assertRaises(ValueError):export_files(sources[:2],'Live.mkv',f/'missing')
            self.assertFalse((f/'missing').exists())

if __name__=='__main__':unittest.main()
