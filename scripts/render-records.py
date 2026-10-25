from pathlib import Path
import json,html,math,re
from urllib.parse import quote
p=Path(__file__).resolve().parent.parent;trips=json.loads((p/'travel-records.json').read_text());E=html.escape
base=(p/'index.html').read_text();header=base[base.index('<header>'):base.index('<main')].replace('href="#','href="index.html#')
def private_link(t,path='journey.md'):
 return 'https://github.com/login?return_to='+quote('/ksangki/family-travel-private/blob/main/albums/'+t['folder']+'/'+path,safe='')
def route_map(t):
 if t.get('mapMode')=='sequence':
  labels=t['route'];count=len(labels);nodes='';buttons=''
  for i,label in enumerate(labels):
   x=70+i*(600/(count-1));y=160 if i%2==0 else 220
   nodes+=f'<g data-map-node="{i}" class="map-node'+(' active' if i==0 else '')+f'"><circle cx="{x}" cy="{y}" r="15"/><text x="{x}" y="{y+5}" class="map-number">{i+1}</text><text x="{x}" y="{y+40}" class="map-label">{E(label)}</text></g>'
   buttons+=f'<button type="button" data-map-point="{i}" aria-pressed="'+('true' if i==0 else 'false')+f'">{i+1}. {E(label)}</button>'
  return f'<div class="route-map sequence-map"><p class="note">위치를 나타내는 지도가 아닌 날짜별 장면 순서도입니다.</p><svg viewBox="0 0 740 340" role="img" aria-label="제주 여행 날짜별 장면 순서도"><rect width="740" height="340" rx="12" class="map-bg"/>{nodes}</svg><div class="map-buttons">{buttons}</div><p id="map-selection" aria-live="polite">1. {E(labels[0])} · 기록에서 선택한 장면</p></div>'
 pts=t['map'][:]
 if t['id']=='osaka-2025':pts=[pts[0],pts[1],['교토·우메코지',34.987,135.747]]
 minx=min(q[2] for q in pts);maxx=max(q[2] for q in pts);miny=min(q[1] for q in pts);maxy=max(q[1] for q in pts);coords=[]
 for i,(label,lat,lon) in enumerate(pts):
  x=100+(lon-minx)/max(.001,maxx-minx)*540;y=310-(lat-miny)/max(.001,maxy-miny)*230;coords.append((x,y,label))
 lines=''.join(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>' for a,b in zip(coords,coords[1:]))
 nodes=''.join(f'<g data-map-node="{i}" class="map-node'+(' active' if i==0 else '')+f'"><circle cx="{x:.1f}" cy="{y:.1f}" r="15"/><text x="{x:.1f}" y="{y+5:.1f}" class="map-number">{i+1}</text><text x="{x:.1f}" y="{y+34:.1f}" class="map-label">{E(label)}</text></g>' for i,(x,y,label) in enumerate(coords))
 buttons=''.join(f'<button type="button" data-map-point="{i}" aria-pressed="'+('true' if i==0 else 'false')+f'">{i+1}. {E(label)}</button>' for i,(_,_,label) in enumerate(coords))
 return f'<div class="route-map"><svg viewBox="0 0 740 390" role="img" aria-label="{E(t["title"])} 공개 장소 대표점 개략도"><rect width="740" height="390" rx="12" class="map-bg"/><path d="M35 55V25m0 0-7 12m7-12 7 12" class="north-arrow"/><text x="26" y="76" class="map-label">북</text><g class="map-lines">{lines}</g>{nodes}</svg><div class="map-buttons" aria-label="지도 대표 장소 선택">{buttons}</div><p id="map-selection" aria-live="polite">1. {E(coords[0][2])} · 지도에서 선택한 대표 장소</p></div>'
for t in trips:
 hero=(f'<img src="{t["hero"]}" alt="{E(t["heroAlt"])}" fetchpriority="high"><div class="shade"></div>' if t['hero'] else f'<div class="hong-kong-background" aria-hidden="true"><span>{E(t.get('heroWord','홍콩'))}</span><i>가족과 함께 남긴 장면</i></div>')
 days=''
 for i,d in enumerate(t['days']):
  evidence='이번 원본' if '기존 여행기' not in d['evidence'] else ('기존 기록 보완' if '이번' in d['evidence'] else '기존 여행기')
  trail=''.join(f'<li>{E(s)}</li>' for s in d['route'])
  scene=next((photo for photo in t.get('representatives',[]) if photo['date']==d['date']),None)
  scene_html=(f'<figure class="day-scene"><button class="gallery-photo" data-src="{scene["src"]}" data-caption="{E(scene["caption"])}" aria-label="{E(scene["caption"])} 사진 크게 보기"><img src="{scene["src"]}" alt="{E(scene["caption"])}" loading="lazy"></button><figcaption>{E(scene["caption"])}</figcaption></figure>' if scene else '')
  days+=f'<article class="day-card" id="day-{d["date"]}" data-record-day="{d["date"]}"><div class="day-side"><span class="day-index">{i+1:02}</span><time datetime="{d["date"]}">{d["date"].replace("-", ". ")}</time><span class="evidence-badge">{evidence}</span></div><div class="day-body"><p class="eyebrow">{E(d["category"])}</p><h3>{E(d["title"])}</h3><ol class="stop-list">{trail}</ol><p>{E(d["story"])}</p><p class="evidence-detail">근거: {E(d["evidence"])} · 이번 폴더 사진 {d["photos"]}장 / 동영상 {d["videos"]}개</p>'+(f'<details><summary>확인이 필요한 내용</summary><p>{E(d["missing"])}</p></details>' if d['missing'] else '')+scene_html+f'<a class="text-link" href="{private_link(t,"date-"+d["date"]+".md") if d["photos"] or d["videos"] else private_link(t)}">가족 전용 기록 보기 ↗</a></div></article>'
  
 day_buttons='<button type="button" data-day-filter="all" aria-pressed="true">전체 일정</button>'+''.join(f'<button type="button" data-day-filter="{d["date"]}" aria-pressed="false">{d["date"][5:].replace("-","/")}</button>' for d in t['days'])
 cats=list(dict.fromkeys(s['category'] for s in t['spots']));options='<option value="all">모든 활동</option>'+''.join(f'<option value="{E(c)}">{E(c)}</option>' for c in cats)
 spots=''.join(f'<article class="place-card" data-place-category="{E(s["category"])}"><span class="eyebrow">{E(s["category"])}</span><h3>{E(s["name"])}</h3><p>{E(s["description"])}</p><span class="place-evidence">{E(s["evidence"])}</span></article>' for s in t['spots'])
 summary=''.join(f'<li>{E(s)}</li>' for s in t['summary']);stats=t['stats'];sources=''.join(f'<li><a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(title)} ↗</a></li>' for title,url in t['sources'])
 photo_section=''
 if t.get('representatives'):
  for photo in t['representatives']:
   photo_section+=f'<figure class="photo"><button class="gallery-photo" data-src="{photo["src"]}" data-caption="{E(photo["caption"])}" aria-label="{E(photo["caption"])} 크게 보기"><img src="{photo["src"]}" alt="{E(photo["caption"])}" loading="lazy"><span>크게 보기 ＋</span></button><figcaption>{E(photo["caption"])}<small>{photo["date"]}</small></figcaption></figure>'
 elif t['id']=='osaka-2025':
  for f,title in [('city-view','창밖으로 펼쳐진 공원'),('sunset','오사카의 저녁 하늘'),('night-gate','불빛이 켜진 입구')]:photo_section+=f'<figure class="photo"><button class="gallery-photo" data-src="assets/osaka-2025/{f}.jpg" data-caption="{title}" aria-label="{title} 크게 보기"><img src="assets/osaka-2025/{f}.jpg" alt="{title}" loading="lazy"><span>사진 크게 보기 ＋</span></button><figcaption>{title}</figcaption></figure>'
 elif t['hero']:photo_section=f'<figure class="photo"><img class="record-cover-photo" src="{t["hero"]}" alt="{E(t["heroAlt"])}" loading="lazy"><figcaption>시드니 항구 대표 풍경 · Kgbo · <a href="https://commons.wikimedia.org/wiki/File:Sydney_Harbour_Bridge_and_Sydney_Opera_House_panorama.jpg">위키미디어 공용</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ko">저작자표시-동일조건변경허락 4.0</a></figcaption></figure>'
 else:photo_section=f'<div class="locked-photo-panel"><span aria-hidden="true">⌑</span><h3>사진은 가족 앨범에서 이어집니다.</h3><p>{E(t["title"])} 사진 {stats["photos"]}장은 로그인한 가족만 볼 수 있습니다.</p></div>'
 original=f'<a class="button outline" href="https://ksangki.github.io/australia-family-2026/">기존 호주 여행기 전체 보기 ↗</a>' if t['id']=='australia-2026' else ''
 doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(t['intro'])}"><meta name="theme-color" content="#234c43"><title>{E(t['title'])} | 우리 가족 여행 기록</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="travel.css"><script src="app.js" defer></script><script src="travel.js" defer></script></head><body><a class="skip" href="#main">본문으로 바로가기</a>{header}<main id="main"><section class="hero record-hero">{hero}<div class="hero-copy"><p class="eyebrow">사진으로 다시 잇는 우리 여행</p><h1>{E(t['title'])}</h1><p>{E(t['subtitle'])}</p><span class="period">{E(t['period'])}</span></div></section><nav class="record-nav" aria-label="여행기 목차"><a href="#overview">여행 한눈에</a><a href="#route">우리의 동선</a><a href="#days">날짜별 이야기</a><a href="#places">방문 장소</a><a href="#album">사진첩</a></nav><section id="overview" class="wrap section record-overview"><div><p class="eyebrow">기억을 이어 주는 사진들</p><h2>{E(t['subtitle'])}</h2><p class="lead">{E(t['intro'])}</p><ul class="summary-list">{summary}</ul>{original}</div><aside class="record-facts"><p class="eyebrow">이번 원본 폴더</p><div class="stats-row"><strong>{stats['photos']}<small>사진</small></strong><strong>{stats['videos']}<small>동영상</small></strong><strong>{stats['gpsPhotos']}<small>위치가 남은 사진</small></strong></div><p>{E(t['scope'])}</p><a class="text-link" href="{private_link(t)}">가족 전용 상세 여행기 ↗</a></aside></section><section id="route" class="story-section"><div class="wrap section"><div class="section-title"><div><p class="eyebrow">장소와 시간을 연결하다</p><h2>우리의 동선</h2></div></div><ol class="route-ribbon">{''.join('<li>'+E(s)+'</li>' for s in t['route'])}</ol>{route_map(t)}<p class="note">공개 장소의 대표점을 연결한 개략도입니다. 실제 도로·철도·항공 경로나 이동거리를 뜻하지 않습니다. 번호를 누르면 장소를 선택할 수 있습니다. 세부 GPS·사적 주소는 표시하지 않습니다.</p></div></section><section id="days" class="wrap section"><div class="section-title"><div><p class="eyebrow">날짜별로 펼쳐 보는 기억</p><h2>날짜별 여행 이야기</h2></div></div><div class="day-filters" aria-label="여행 날짜 선택">{day_buttons}</div><p id="day-filter-status" class="note" aria-live="polite">전체 {len(t['days'])}개 날짜를 보고 있습니다.</p><div class="days-list">{days}</div></section><section id="places" class="story-section"><div class="wrap section"><div class="section-title"><div><p class="eyebrow">우리가 머문 장소들</p><h2>방문 장소 모아보기</h2></div><label class="category-control">활동 분류 <select id="category-filter">{options}</select></label></div><p id="place-filter-status" class="note" aria-live="polite">전체 {len(t['spots'])}곳</p><div class="places-grid">{spots}</div></div></section><section id="album" class="wrap section"><div class="section-title"><div><p class="eyebrow">풍경은 공개로, 가족의 순간은 우리끼리</p><h2>여행 사진첩</h2></div></div><div class="record-photos">{photo_section}</div><div class="private-album-banner"><div><h3>가족 사진과 상세 분류는 비공개 앨범에</h3><p>날짜·장소·활동별 사진, 원본과 동영상을 함께 볼 수 있습니다.</p></div><a class="button light" href="{private_link(t)}">GitHub 로그인 후 보기 ↗</a></div></section><section class="wrap section evidence-section"><h2>기록의 근거와 남은 빈칸</h2><p>{E(t['extra'])}</p><p>촬영된 장면과 촬영 시각·위치가 함께 맞는 구간을 우선 정리했습니다. 날짜만 있는 사진이나 기존 여행기로 보완한 부분은 별도로 표시했습니다. 사진 없는 시간을 채워 전체 이동을 추정하지 않습니다.</p><details><summary>시간·위치 정보를 해석한 방법</summary><p>사진은 원촬영 시각과 시간대, 동영상은 원촬영 날짜 정보를 우선했습니다. 공유·내보내기 날짜는 여행 날짜로 사용하지 않았습니다. 기내 GPS는 출발지에 남을 수 있습니다. 가까운 장소는 사진 속 간판·풍경과 함께 확인했고, 교통수단·탑승 완료·정확한 숙소명은 증거가 있을 때만 기록합니다.</p><p>사진의 개수는 현재 백업 폴더 기준입니다. 사진 기록일은 전체 여행 기간과 같지 않을 수 있습니다.</p></details><h3>장소·기록 참고자료</h3><p class="note">공식 안내는 장소 이름과 위치 맥락 확인용이며 가족의 실제 방문은 사진·메타데이터 또는 명시한 기존 여행기 근거로 판단했습니다.</p><ul>{sources}</ul></section><div class="wrap"><a class="button outline" href="index.html#places">← 우리 가족 여행 목록</a></div></main><footer class="wrap"><div><a class="brand" href="index.html">우리 가족 여행 기록</a><p>함께한 시간을, 오래도록.</p></div><p>가족 사진 원본과 정확한 위치는 비공개로 보관합니다.</p></footer><dialog id="viewer" aria-labelledby="caption"><button id="close-photo" class="close">닫기 ×</button><img src="assets/sydney-harbour.jpg" alt="여행 풍경 확대 사진"><p id="caption">공개 대표 풍경 사진</p></dialog></body></html>'''
 if t.get('representatives'):
  doc=doc.replace('href="travel.css"','href="travel.css?v=selected-photos-1"').replace('hero record-hero','hero record-hero selected-photo-hero').replace('class="record-photos"','class="record-photos selected-photos"').replace('풍경은 공개로, 가족의 순간은 우리끼리','선별한 대표 장면만 함께 나눕니다').replace('가족 사진과 상세 분류는 비공개 앨범에','나머지 사진과 원본은 가족 앨범에').replace('날짜·장소·활동별 사진, 원본과 동영상을 함께 볼 수 있습니다.','선별한 대표 사진만 공개하고, 나머지 사진·원본·동영상은 로그인한 가족만 볼 수 있습니다.')
 if t.get('mapMode')=='sequence':doc=doc.replace('공개 장소의 대표점을 연결한 개략도입니다. 실제 도로·철도·항공 경로나 이동거리를 뜻하지 않습니다. 번호를 누르면 장소를 선택할 수 있습니다. 세부 GPS·사적 주소는 표시하지 않습니다.','유효 GPS가 없어 지리적 경로를 그리지 않았습니다. 사진 촬영일과 장면을 순서로 정리했으며, 장소 간 거리나 방향을 뜻하지 않습니다.')
 if t['id']=='osaka-2025':doc=doc.replace('<section id="album" class="wrap section">','<section id="album" class="wrap section"><span id="osaka-photos"></span>')
 (p/(t['id']+'.html')).write_text(doc)
# Update home cards and connect the original Australia guide through the new summary.
h=base.replace('두 편의 여행 기록','세 편의 여행 기록').replace('2025 오사카 가족여행','2025 오사카·교토 가족여행')
h=h.replace('href="https://ksangki.github.io/australia-family-2026/"','href="australia-2026.html"')
h=h.replace('2025 · 일본 오사카','2025. 6. 1. — 6. 6. · 일본 사진 기록').replace('창밖으로 펼쳐진 공원의 풍경, 붉게 물든 저녁 하늘, 불빛이 켜진 입구까지. 사진으로 남긴 오사카의 하루를 펼쳐봅니다.','유니버설시티와 USJ를 거쳐 교토 철도박물관까지. 촬영 날짜와 위치를 따라 오사카·교토의 여정을 다시 펼칩니다.').replace('오사카 여행 기록 보기','오사카·교토 여행 기록 보기')
card='''<article class="trip osaka-card"><a class="trip-image hong-kong-card" href="hong-kong-2024.html" aria-label="2024 홍콩 가족여행 기록 보기"><span class="badge">홍콩 · 2024</span><strong>정원을 걷고,<br>디즈니 성 앞까지.</strong><span class="hk-card-year">2024</span></a><div class="trip-copy"><p class="eyebrow">사진 기록 · 2024. 5. 26. — 5. 27.</p><h3>2024 홍콩 가족여행</h3><p class="cities">디즈니 리조트 · 디즈니랜드</p><p>리조트 정원과 해안 산책에서 다음 날 아침 디즈니랜드 입구까지. 사진에 남은 이틀의 동선을 이어 봅니다.</p><div class="tags"><span>정원 산책</span><span>테마파크</span><span>가족 여행</span></div><a class="text-link" href="hong-kong-2024.html">홍콩 여행 기록 보기 <span>↗</span></a></div></article>'''
hong_kong_seen=False
def unique_hong_kong_card(match):
 global hong_kong_seen
 block=match.group(0)
 if 'href="hong-kong-2024.html"' not in block:return block
 if hong_kong_seen:return ''
 hong_kong_seen=True
 return block
h=re.sub(r'<article class="trip[^\"]*">.*?</article>',unique_hong_kong_card,h,flags=re.S)
if not hong_kong_seen:h=h.replace('<p class="next">',card+'<p class="next">',1)
h=h.replace('노을에서 야경까지, 오사카의 장면들','오사카에서 교토까지, 사진으로 잇는 코스').replace('공원의 전경과 저녁 풍경을 공개 대표 사진 세 장으로 모았습니다.','USJ와 교토 철도박물관, 사진 메타데이터로 정리한 날짜별 여행기입니다.')
h=h.replace('href="https://ksangki.github.io/australia-family-2026/#record"','href="australia-2026.html#days"').replace('href="https://ksangki.github.io/australia-family-2026/#journey"','href="australia-2026.html#route"')
def selected_home_card(match):
 block=match.group(0)
 trip=next((t for t in trips if t.get('representatives') and f'href="{t["id"]}.html"' in block),None)
 if not trip:return block
 if 'selected-trip-card' not in block:block=re.sub(r'<article class="([^"]+)"',lambda m:'<article class="'+m.group(1)+' selected-trip-card"',block,count=1)
 photo=f'<a class="trip-image" href="{trip["id"]}.html"><img src="{trip["hero"]}" alt="{E(trip["heroAlt"])}" loading="lazy"><span class="badge">{trip["period"].split("·")[0].strip()}</span></a>'
 return re.sub(r'<a class="trip-image[^"]*"[^>]*>.*?</a>',lambda m:photo,block,count=1,flags=re.S)
h=re.sub(r'<article class="trip[^"]*">.*?</article>',selected_home_card,h,flags=re.S)
cards=list(re.finditer(r'<article class="trip[^"]*">.*?</article>',h,re.S))
if cards and all(not h[a.end():b.start()].strip() for a,b in zip(cards,cards[1:])):
 def trip_year(card):
  trip=next((t for t in trips if f'href="{t["id"]}.html"' in card.group(0)),None)
  return int(trip['folder'][:4]) if trip else 0
 h=h[:cards[0].start()]+''.join(m.group(0) for m in sorted(cards,key=trip_year,reverse=True))+h[cards[-1].end():]
h=h.replace('대표 풍경 사진:','시드니 항구 사진:')
if '그 외 대표 사진: 우리 가족' not in h:h=h.replace('<p>© 2026 우리 가족 여행 기록</p>','<p>그 외 대표 사진: 우리 가족</p><p>© 2026 우리 가족 여행 기록</p>')
h=re.sub(r'<link rel="stylesheet" href="travel\.css(?:\?[^"]*)?">','',h)
h=h.replace('<link rel="stylesheet" href="style.css">','<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="travel.css?v=selected-photos-1">');(p/'index.html').write_text(h)
print('Rendered',len(trips),'complete public travel records and home links')
