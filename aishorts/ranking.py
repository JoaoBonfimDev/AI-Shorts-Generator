"""Transparent signal-based alternative; not semantic understanding or virality prediction."""
import json,math,re
from .media import save
LIMITS={'visual':25,'reacoes':25,'entretenimento':20,'narrativa':15,'qualidade':10,'originalidade':5}
REACTIONS=('caramba','nossa','consegui','não acredito','caralho','meu deus','que lindo','que fofo','engraçado','haha','ufa','morri')
EVENTS=('chefe','boss','vitória','venci','ganhei','derrotei','finalmente','consegui','morreu','salvei')

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def overlap(a,b):return any(max(x,u)<min(y,v) for x,y in a for u,v in b)

def validate(data,duration):
    for c in data['clips']:
        if set(c['scores'])!=set(LIMITS):raise ValueError('Ranking deve conter os seis critérios.')
        if any(not math.isfinite(v) or not 0<=v<=LIMITS[k] for k,v in c['scores'].items()):raise ValueError('Nota fora dos limites.')
        if c['score']!=sum(c['scores'].values()):raise ValueError('Total não corresponde aos critérios.')
        previous=-1
        for a,b in c['parts']:
            if not (math.isfinite(a) and math.isfinite(b) and 0<=a<b<=duration and a>=previous):raise ValueError('Intervalo inválido ou fora de ordem.')
            previous=b
        if not 30<=sum(b-a for a,b in c['parts'])<=60:raise ValueError('Corte deve durar de 30 a 60 segundos.')
    return data

def generate(folder,cfg,duration):
    segments=read(folder/'transcript.json');visual=read(folder/'visual.json');energy=read(folder/'energy.json')
    length=min(cfg['duration_seconds'],duration);candidates=[]
    if length<30:return {'method':'heuristic','clips':[],'selected':[]}
    # Every part of the recording is eligible, including the final window.
    starts=sorted(set(list(range(0,max(1,int(duration-length)+1),15))+[max(0,duration-length)]))
    for start in starts:
        end=start+length
        ss=[s for s in segments if s['start']<end and s['end']>start and s.get('avg_logprob',0)>-1 and s.get('no_speech_prob',0)<.6]
        text=' '.join(s['text'] for s in ss).lower();reaction=[x for x in REACTIONS if x in text];events=[x for x in EVENTS if x in text]
        vv=[v for v in visual if start<=v['seconds_approx']<end];ee=energy[int(start):math.ceil(end)]
        movement=sum(v['difference'] for v in vv)/max(1,len(vv));brightness=sum(v['brightness'] for v in vv)/max(1,len(vv))
        sound=sum(ee)/max(1,len(ee));speech=min(1,sum(min(end,s['end'])-max(start,s['start']) for s in ss)/length)
        # Never nominate solely because audio is loud. Visual-only clips need sound and changing imagery.
        if not reaction and not events and not (movement>=8 and sound>.004 and brightness>12):continue
        scores={'visual':min(25,round(min(1,movement/25)*18+min(7,len(events)*3))),
                'reacoes':min(25,len(reaction)*6+round(speech*3)),
                'entretenimento':min(20,round(min(1,movement/25)*6+min(8,len(reaction)*3)+min(6,len(events)*3))),
                'narrativa':min(15,round(speech*5)+(5 if events else 1)+(2 if ss and ss[-1]['text'].rstrip().endswith(('.', '!', '?')) else 0)),
                'qualidade':(4 if brightness>20 else 1)+(4 if .004<sound<.3 else 1),
                'originalidade':3}
        score=sum(scores.values());title='Reação: '+reaction[0] if reaction else ('Possível acontecimento: '+events[0] if events else 'Sequência de ação — conferir contexto')
        candidates.append({'start':start,'end':end,'parts':[[start,end]],'score':score,'scores':scores,'title':title,'hook':title,'evidence':{'reaction_cues':reaction,'event_cues':events,'movement_mean':round(movement,2),'audio_rms':round(sound,4),'speech_fraction':round(speech,2)},'tokens':sorted(set(re.findall(r'\w{4,}',text)))})
    candidates.sort(key=lambda c:(c['score'],c['scores']['narrativa'],c['scores']['reacoes'],c['scores']['entretenimento']),reverse=True)
    selected=[]
    for i,c in enumerate(candidates,1):
        c['rank']=i;c['slug']=f"{c['score']}pts_candidato_{i:03}"
        c['selected']=False
        if c['score']<cfg['minimum_score'] or len(selected)>=4:continue
        if any(overlap(c['parts'],s['parts']) or abs(c['start']-s['start'])<60 for s in selected):continue
        tokens=set(c['tokens'])
        if tokens and any(len(tokens&set(s['tokens']))/max(1,len(tokens|set(s['tokens'])))>.7 for s in selected):continue
        c['selected']=True;selected.append(c)
    return {'method':'heuristic_v1_not_editorial','warning':'Notas são proxies de sinais; não reconhecem bosses, humor, identidade do falante nem garantem contexto ou originalidade. Rever antes de publicar.','clips':candidates,'selected':[c['rank'] for c in selected]}

def selected(data):return [c for c in data['clips'] if c['rank'] in data['selected']]
