"""Adaptado de editorial_export.py: legenda ASS e composição originais."""
import json,subprocess,textwrap
from . import media as shorts

def encoder_args(name):
    if name == "h264_nvenc": return ["-c:v","h264_nvenc","-preset","p4","-rc","vbr","-cq","20","-b:v","0"]
    return ["-c:v","libx264","-preset","fast","-crf","20"]

def ass_time(t):
    cs=max(0,round(t*100))
    return f'{cs//360000:01}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'


def ass_text(text,width=30):
    return r'\N'.join(textwrap.wrap(text.replace('{','').replace('}','').replace('\\',''),width))


def caption_groups(rows):
    for s in rows:
        group=[]
        for w in s['words']:
            if group and (len(group)>=5 or len(' '.join(x['text'].strip() for x in group+[w]))>32 or w['start']-group[-1]['end']>.7):
                yield group
                group=[]
            group.append(w)
        if group:
            yield group


def make_ass(c, OUT, tag):
    duration=sum(b-a for a,b in c['parts'])
    rows=json.loads((OUT/f"{c['rank']:02}_transcript.json").read_text(encoding='utf-8'))
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,58,&H00FFFFFF,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,65,65,400,1
Style: Title,Arial,66,&H00FFFFFF,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,5,70,70,0,1
Style: Tag,Arial,28,&H00FFC77A,&H00FFFFFF,&H00202020,&H80000000,-1,0,0,0,100,100,3,0,1,1,0,5,50,50,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events=[f"Dialogue: 0,0:00:00.00,{ass_time(duration)},Tag,,0,0,0,,{{\\pos(540,270)}}{ass_text(tag)}",
            f"Dialogue: 0,0:00:00.00,{ass_time(duration)},Title,,0,0,0,,{{\\pos(540,420)}}{ass_text(c['hook'],26)}"]
    srt=[]
    groups = list(caption_groups(rows))
    for index, g in enumerate(groups):
        a,b=max(0,g[0]['start']),min(duration,g[-1]['end'])
        next_start = groups[index+1][0]['start'] if index+1<len(groups) else duration
        b = min(duration, next_start, max(b, a+0.65))
        if b<=a:
            continue
        text=' '.join(w['text'].strip() for w in g)
        events.append(f'Dialogue: 1,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,{ass_text(text)}')
        srt.append(f'{len(srt)+1}\n{shorts.stamp(a)} --> {shorts.stamp(b)}\n{text}\n')
    stem=f"{c['rank']:02}_{c['slug']}"
    (OUT/f'{stem}.ass').write_text(header+'\n'.join(events)+'\n',encoding='utf-8-sig')
    (OUT/f'{stem}.srt').write_text('\n'.join(srt),encoding='utf-8')
    return stem


def render(CFG, OUT, clips):
    import av
    with av.open(CFG['input']) as container:
        rate = container.streams.video[0].average_rate or 30
        fps = str(round(float(rate))) if abs(float(rate)-round(float(rate)))<.001 else str(rate)
    for c in clips:
        stem=make_ass(c, OUT, CFG.get("label", "GAMEPLAY"))
        if (OUT/f'{stem}.mp4').exists():
            print(f'Existing: {stem}',flush=True)
            continue
        print(f'Rendering rank {c["rank"]}: {c["title"]}',flush=True)
        prep=[]
        inputs=[]
        for i,(a,b) in enumerate(c['parts']):
            inputs.extend(['-ss',str(a),'-t',str(b-a),'-i',CFG['input']])
            prep.append(f'[{i}:v]setpts=PTS-STARTPTS,fps={fps}[v{i}];[{i}:a:{CFG['render_audio_track']}]asetpts=PTS-STARTPTS[a{i}];')
        concat=''.join(f'[v{i}][a{i}]' for i in range(len(c['parts'])))
        filt=(''.join(prep)+concat+f"concat=n={len(c['parts'])}:v=1:a=1[main][audio];[main]split=2[bg0][fg0];"
              "[bg0]scale=304:540:force_original_aspect_ratio=increase,crop=304:540,"
              "gblur=sigma=18,eq=brightness=-0.16:saturation=0.7,scale=1080:1920[bg];"
              "[fg0]scale=1080:608:force_original_aspect_ratio=decrease,pad=1080:608:(ow-iw)/2:(oh-ih)/2[fg];[bg][fg]overlay=0:650,setsar=1,"
              f"ass={stem}.ass[v]")
        command=[shorts.ffmpeg(),'-hide_banner','-loglevel','error','-nostdin','-n',
                 *inputs,'-t',str(sum(b-a for a,b in c['parts'])),'-filter_complex',filt,'-map','[v]','-map','[audio]',
                 *encoder_args(CFG["encoder"]),
                 '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',f'{stem}.partial.mp4']
        partial = OUT/f"{stem}.partial.mp4"
        if partial.exists(): partial.unlink()
        subprocess.run(command,cwd=OUT,check=True)
        partial.rename(OUT/f"{stem}.mp4")
