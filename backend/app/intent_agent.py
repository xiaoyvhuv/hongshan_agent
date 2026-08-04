import re
from .bailian_client import BailianClient
from .schemas import Preferences

class IntentAgent:
    """Qwen extracts intent; local validation prevents the model from inventing POI ids."""
    ALLOWED={'panda','native','primate','rest','africa','food','north_gate','south_gate'}

    def parse(self,text:str,base:Preferences)->Preferences:
        data=base.model_dump()
        if not text:return base
        if m:=re.search(r'(\d+)\s*(小时|h)',text,re.I):data['duration_minutes']=int(m.group(1))*60
        if '半天' in text:data['duration_minutes']=240
        if '全天' in text:data['duration_minutes']=480
        data['avoid_climbing']=data['avoid_climbing'] or any(x in text for x in ['不爬山','不想爬','怕累','省力','爬坡'])
        data['avoid_sun']=data['avoid_sun'] or any(x in text for x in ['怕晒','不想晒','避开太阳','树荫'])
        data['with_child']=data['with_child'] or any(x in text for x in ['孩子','宝宝','亲子','儿童'])
        if '熊猫' in text:data['preferred_animals']=list(dict.fromkeys(data['preferred_animals']+['大熊猫']));data['must_visit']=list(dict.fromkeys(data['must_visit']+['panda']))
        if '灵长' in text:data['preferred_animals']=list(dict.fromkeys(data['preferred_animals']+['灵长类']));data['must_visit']=list(dict.fromkeys(data['must_visit']+['primate']))
        if '貉' in text or '本土' in text:data['preferred_animals']=list(dict.fromkeys(data['preferred_animals']+['貉']));data['must_visit']=list(dict.fromkeys(data['must_visit']+['native']))
        if '休息' in text or '累' in text:data['must_visit']=list(dict.fromkeys(data['must_visit']+['rest']))
        return Preferences(**data)

    def parse_with_qwen(self,text:str,base:Preferences)->tuple[Preferences,str]:
        if not text:return base,'empty'
        client=BailianClient()
        try:
            content=client.chat([
                {'role':'system','content':'你是红山动物园路线需求解析器。只输出JSON，不要解释。字段：duration_minutes, pace, avoid_climbing, avoid_sun, with_child, preferred_animals, must_visit, avoid_pois。must_visit和avoid_pois只能使用POI id：panda,native,primate,rest,africa,food,north_gate,south_gate。'},
                {'role':'user','content':f'已有偏好：{base.model_dump()}\n游客需求：{text}'}
            ],temperature=0)
            raw=client.parse_json(content)
            if raw:
                merged=base.model_dump()
                for key in ('duration_minutes','pace','avoid_climbing','avoid_sun','with_child','preferred_animals','must_visit','avoid_pois'):
                    if key in raw:merged[key]=raw[key]
                merged['must_visit']=[x for x in merged['must_visit'] if x in self.ALLOWED]
                merged['avoid_pois']=[x for x in merged['avoid_pois'] if x in self.ALLOWED]
                return Preferences(**merged),'qwen'
        except Exception:
            pass
        return self.parse(text,base),'rule_fallback'
