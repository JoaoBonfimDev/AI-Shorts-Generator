"""Análise integral em blocos, adaptada de editorial_scan.py e review_current.py."""
import json,math,subprocess,wave
from pathlib import Path
import numpy as np
from . import media

def model_location(cfg):
    path=Path(cfg['model_path']) if cfg['model_path'] else Path(cfg['data_directory'])/'models'/cfg['model']
    if not (path/'model.bin').is_file():
        raise FileNotFoundError('Modelo local ausente. Configure model_path ou execute prepare-model --allow-download.')
    return path

def audio(cfg,folder):
    complete=folder/'coverage_audio.json'
    if complete.exists():return
    from faster_whisper import WhisperModel
    model=WhisperModel(str(model_location(cfg)),device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
    duration=media.inspect(Path(cfg['input']))['duration'];wav=folder/'audio.wav'
    if not wav.exists():
        part=folder/'audio.partial.wav'
        media.run(['-y','-i',cfg['input'],'-map',f"0:a:{cfg['audio_track']}",'-ac','1','-ar','16000','-c:a','pcm_s16le',str(part)])
        part.rename(wav)
    rows=[];energy=[];chunk=cfg['chunk_seconds']
    with wave.open(str(wav)) as w:
        for index,start in enumerate(range(0,math.ceil(duration),chunk)):
            end=min(duration,start+chunk);cached=folder/f'transcript_{index:04}.json'
            if cached.exists():data=json.loads(cached.read_text(encoding='utf-8'))
            else:
                w.setpos(start*16000)
                signal=np.frombuffer(w.readframes(round((end-start)*16000)),np.int16).astype(np.float32)/32768
                energy_chunk=[float(np.sqrt(np.mean(signal[i:i+16000]**2))) for i in range(0,len(signal),16000)]
                # Short local windows reduce forced translation of mixed game/creator speech.
                segments=[]
                for offset in range(0,len(signal),30*16000):
                    segs,info=model.transcribe(signal[offset:offset+30*16000],language=cfg['language'],beam_size=3,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,repetition_penalty=1.1,no_repeat_ngram_size=4)
                    base=start+offset/16000
                    for s in segs:
                        segments.append({'start':s.start+base,'end':s.end+base,'text':s.text,'language':info.language,'language_probability':info.language_probability,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob,'words':[{'start':t.start+base,'end':t.end+base,'text':t.word} for t in s.words or []]})
                data={'segments':segments,'energy':energy_chunk};media.save(cached,data)
            rows.extend(data['segments']);energy.extend(data['energy']);print(f'Áudio: {end/duration:.0%}',flush=True)
    media.save(folder/'transcript.json',rows);media.save(folder/'energy.json',energy)
    media.save(complete,{'completed':True,'seconds':duration,'api_cost_brl':0})

def visuals(cfg,folder):
    if (folder/'coverage_visual.json').exists():return
    import cv2
    step=cfg['sample_seconds'];frames=folder/'frames';frames.mkdir(exist_ok=True)
    cmd=[media.ffmpeg(),'-hide_banner','-loglevel','error','-nostdin','-i',cfg['input'],'-an','-vf',f'fps=1/{step},scale=384:216','-pix_fmt','bgr24','-f','rawvideo','pipe:1']
    rows=[];previous=None
    with subprocess.Popen(cmd,stdout=subprocess.PIPE) as proc:
        while True:
            raw=proc.stdout.read(384*216*3)
            if not raw:break
            if len(raw)!=384*216*3:raise RuntimeError('Quadro incompleto.')
            frame=np.frombuffer(raw,np.uint8).reshape(216,384,3);gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY).astype(float)
            index=len(rows);difference=float(np.abs(gray-previous).mean()) if previous is not None else 0
            rows.append({'seconds_approx':index*step,'difference':difference,'brightness':float(gray.mean()),'detail':float(cv2.Laplacian(gray,cv2.CV_64F).var())})
            cv2.imwrite(str(frames/f'{index:05}.jpg'),frame);previous=gray
        if proc.wait():raise RuntimeError('Falha no FFmpeg durante análise visual.')
    media.save(folder/'visual.json',rows)
    for page in range(math.ceil(len(rows)/24)):
        canvas=np.zeros((6*244,4*384,3),np.uint8)
        for j,row in enumerate(rows[page*24:(page+1)*24]):
            index=page*24+j;y,x=j//4*244,j%4*384
            canvas[y:y+216,x:x+384]=cv2.imread(str(frames/f'{index:05}.jpg'))
            t=int(row['seconds_approx']);cv2.putText(canvas,f'~{t//60}:{t%60:02}',(x+5,y+236),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),1)
        cv2.imwrite(str(folder/f'contact_{page:04}.jpg'),canvas)
    media.save(folder/'coverage_visual.json',{'completed':True,'samples':len(rows),'sample_seconds':step,'timestamps':'approximate'})
