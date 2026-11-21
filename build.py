#!/usr/bin/env python3
"""Static generator. Python standard library only. Run: python3 build.py."""
import csv
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

SELLER_WHATSAPP = ""
ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
KITS = ROOT.parent / "kits" / "brand_kits"
LEADS = ROOT.parent / "leads.csv"


def e(value):
    return html.escape(str(value), quote=True)


def icon(name="arrow"):
    paths = {"arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2"/>', "check": '<path d="m5 12 4 4L19 6"/>', "star": '<path d="m12 2 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1Z"/>', "chat": '<path d="M21 11a9 9 0 0 1-13 8l-6 2 2-6a9 9 0 1 1 17-4Z"/><path d="M8 9h8M8 13h5"/>', "spark": '<path d="m12 2 2 8 8 2-8 2-2 8-2-8-8-2 8-2Z"/>'}
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'+paths[name]+'</svg>'


def wordmark(name, kind):
    marks = {"restaurant": '<path d="M17 46V25a15 15 0 0 1 30 0v21M10 46h44M26 46V27h12v19"/>', "fashion": '<path d="M15 45 32 12l17 33M22 33h20"/>', "accounting": '<path d="M13 45V30h9v15M27 45V22h9v23M41 45V12h9v33M10 49h44"/>', "barber": '<path d="m20 18 25 28M44 18 19 46M26 25l12 13"/><circle cx="18" cy="15" r="6"/><circle cx="46" cy="15" r="6"/>', "gym": '<path d="M8 25v14M15 19v26M49 19v26M56 25v14M15 32h34"/>', "icecream": '<path d="m21 32 11 24 11-24M18 32h28a9 9 0 0 0-5-16 10 10 0 0 0-19 0 9 9 0 0 0-4 16Z"/>'}
    return f'<svg class="wordmark" viewBox="0 0 64 64" role="img" aria-label="{e(name)}"><g fill="none" stroke="currentColor" stroke-width="2">{marks.get(kind, marks["fashion"])}</g></svg>'


def photo(pair):
    return "https://images.unsplash.com/" + pair[0] + "?w=1600&q=80&auto=format&fit=crop"


def image_tag(pair, cls="", eager=False):
    return f'<img class="{cls}" src="{photo(pair)}" alt="{e(pair[1])}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def head(title, fonts, css="../site.css"):
    families = "&".join("family="+quote(f)+":wght@"+('400' if f in ['Bebas Neue','Anton','Archivo Black'] else '400;500;600;700') for f in fonts)
    return f'<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#161b25"><meta name="description" content="{e(title)} · Cartagena. Conoce nuestros servicios y contáctanos directamente."><title>{e(title)} · Cartagena</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?{families}&display=swap" rel="stylesheet"><link rel="stylesheet" href="{css}"></head>'


def offer(name):
    msg = quote(f"Hola, quiero reservar mi página web para {name} por $200.000")
    url = f'https://wa.me/{SELLER_WHATSAPP}?text={msg}'
    return f'''<div class="proposal-ribbon"><span>PROPUESTA WEB</span><button data-offer>¿Te gusta? Ten tu página web — Reserva por $200.000 COP {icon()}</button></div>
<button class="offer-float" data-offer>{icon('spark')}<span>¿Te gusta? Ten tu página web<br><b>Reserva por $200.000 COP</b></span></button>
<dialog id="offer-dialog" aria-labelledby="offer-title"><button class="close" aria-label="Cerrar propuesta">×</button><p class="overline">UNA PROPUESTA PARA TU NEGOCIO</p><h2 id="offer-title">Tu marca merece su propio lugar.</h2><p>Esta es una propuesta de página web para <strong>{e(name)}</strong>.</p><ul class="included">{''.join('<li>'+icon('check')+x+'</li>' for x in ['Diseño completo con tu marca','Adaptada a celular','Botón de WhatsApp','Ubicación en Google Maps','Entrega rápida'])}</ul><p class="offer-price">$200.000 <small>COP</small></p><a class="seller-cta" href="{url}" target="_blank" rel="noopener">Reservar mi página web {icon()}</a><a class="seller-email" href="mailto:ablanquicet@agapai.com.co?subject={quote('Propuesta web para '+name)}">Prefiero escribir por correo</a><p class="fine">Propuesta comercial independiente del negocio. Las imágenes son referenciales. Servicios y disponibilidad sujetos a confirmación.</p></dialog>'''


def render(row, content, kit, index, photos):
    name, kind = content['name'], content['kind']
    slug = kit.name
    target = DIST / slug
    target.mkdir(parents=True, exist_ok=True)
    brand = json.loads((kit/'brand.json').read_text())
    style = (kit/'DESIGN_STYLE.md').read_text()
    colors = re.findall(r'--color-[\w-]+:\s*(#[\da-fA-F]{6})', style)
    fonts = re.search(r'Sugerida: títulos \*\*(.*?)\*\*, texto \*\*(.*?)\*\*', style).groups()
    palette = colors + ['#a58a65'] * 4
    cssvars = ';'.join(f'--color-{key}:{value}' for key,value in zip(['primary','secondary','accent','accent-2'],palette))
    logos = list(kit.glob('logo.*'))
    if logos:
        shutil.copy2(logos[0], target/logos[0].name)
        logo = f'<img class="logo" src="{logos[0].name}" alt="Logo {e(name)}">'
        gallery_logo = f'<img src="{slug}/{logos[0].name}" alt="Logo {e(name)}">'
    else:
        logo = gallery_logo = wordmark(name,kind)
    wa = row['WhatsApp'] or 'https://wa.me/'+re.sub(r'\D','',row['Teléfono'])
    wa += ('&' if '?' in wa else '?') + 'text=' + quote(f'Hola, quiero información de {name}.')
    button = f'<a class="button primary" href="{e(wa)}" target="_blank" rel="noopener">{e(content["cta"])} {icon("arrow")}</a>'
    rating, count = re.match(r'([\d.]+)\s*\((\d+)\)',row['Rating Google']).groups()
    stars = f'<a class="rating" href="{e(row["Google Maps"])}" target="_blank" rel="noopener"><span class="stars">★★★★★</span><strong>{rating}★</strong> ({count} reseñas) <span>en Google ↗</span></a>'
    p = photos[kind][:]
    if index in (4,7,8,11,12,17,18):
        p = p[1:] + p[:1]
    hero_img = image_tag(p[0],'hero-photo',True)
    hero = f'''<section class="hero variant-{index%3}"><div class="hero-visual">{hero_img}<span class="image-note">Imagen de inspiración</span><div class="orbit">{icon('spark')}<span>HECHO PARA<br>DISFRUTARLO</span></div></div><div class="hero-copy"><p class="overline">{e(content['eyebrow'])}</p><h1>{e(content['title'])}</h1><p class="intro">{e(content['intro'])}</p><div class="hero-actions">{button}<a class="text-link" href="#descubre">Descubre más ↓</a></div>{stars}</div><a class="scroll-cue" href="#descubre">01 / EXPLORA <span>↓</span></a></section>'''
    booking = ''
    if kind == 'hotel':
        booking = f'<form class="booking" data-wa="{e(row["WhatsApp"])}"><div><label for="arrival">Llegada</label><input id="arrival" name="arrival" type="date" required></div><div><label for="departure">Salida</label><input id="departure" name="departure" type="date" required></div><div><label for="guests">Huéspedes</label><select id="guests" name="guests">'+''.join(f'<option>{i}</option>' for i in range(1,9))+f'</select></div><button class="button primary" type="submit">Consultar fechas {icon()}</button><p class="fine">Consulta sin pago · Reserva sujeta a confirmación</p></form>'
    service_titles = {'jewelry':'Encuentra tu próxima historia.','wellness':'No tienes que resolverlo a solas.','restaurant':'El gusto de elegir.','fashion':'Tu próximo look empieza aquí.','accounting':'Orden para cada etapa.','hotel':'Un lugar para tu próxima pausa.','nutrition':'Comienza por cuidarte.','barber':'Elige tu próximo acabado.','skin':'Cuidado que empieza contigo.','medical':'Una mirada profesional a tu piel.','hardware':'Lo que tu proyecto necesita.','gym':'Tu objetivo. Tu siguiente paso.','icecream':'¿De qué tienes antojo?'}
    service_photos = [p[2],p[3],p[1]] if kind == 'jewelry' else [p[1],p[2],p[3]]
    services = ''.join(f'<article class="service reveal"><span class="service-num">0{i+1}</span>{image_tag(service_photos[i]) if i<3 else ""}<div><h3>{e(s[0])}</h3><p>{e(s[1])}</p><a href="{e(wa)}" class="text-link">Consultar {icon()}</a></div></article>' for i,s in enumerate(content['services']))
    gallery = ''.join(f'<figure class="reveal">{image_tag(pair)}<figcaption>0{i+1} / {e(pair[1])}</figcaption></figure>' for i,pair in enumerate(p))
    channels = ''.join(f'<a href="{e(row[key])}" target="_blank" rel="noopener">{key} ↗</a>' for key in ['Instagram','Facebook'] if row[key])
    email = f'<a href="mailto:{e(row["Email"])}">{e(row["Email"])}</a>' if row['Email'] else ''
    mapurl = 'https://maps.google.com/maps?q='+quote(name+' '+row['Dirección']+' Cartagena Colombia')+'&output=embed'
    sections = f'''{booking}<div class="ticker" aria-hidden="true"><div>{('CARTAGENA  ✦  '+e(content['name'])+'  ✦  ')*6}</div></div>
<section id="descubre" class="about section reveal"><div><p class="overline">01 / NUESTRA ESENCIA</p><h2>Un lugar para<br><em>{'ser tú.' if kind in ['wellness','fashion','gym'] else 'lo que importa.'}</em></h2>{icon('spark')}</div><div><p class="large-copy">{e(content['about'])}</p><a class="text-link" href="#servicios">Conoce nuestra propuesta {icon()}</a></div></section>
<section id="servicios" class="services section"><header class="section-heading reveal"><div><p class="overline">02 / {'SABORES Y MOMENTOS' if kind=='icecream' else 'DESCUBRE LA PROPUESTA'}</p><h2>{service_titles[kind]}</h2></div><a class="text-link" href="{e(wa)}">Hablemos {icon()}</a></header><div class="service-grid">{services}</div><p class="fine">Consulta disponibilidad, precios y condiciones directamente con el negocio.</p></section>
<section class="feature section"><div class="feature-image reveal">{image_tag(p[3])}<svg class="decor" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="80"/><path d="M100 0v200M0 100h200M29 29l142 142M29 171 171 29"/></svg></div><div class="feature-copy reveal"><p class="overline">03 / EL VALOR ESTÁ EN LOS DETALLES</p><h2>{e(content['feature'])}</h2><p>{e(content['feature_text'])}</p>{button}</div></section>
<section class="gallery section" id="galeria"><header class="section-heading reveal"><div><p class="overline">04 / INSPÍRATE</p><h2>{'Un poco de nuestro universo.' if kind not in ['medical','accounting'] else 'Una nueva perspectiva.'}</h2></div><p>Imágenes editoriales de referencia.<br>No representan instalaciones, inventario ni equipo real.</p></header><div class="photo-grid">{gallery}</div></section>
<section class="social-proof section reveal"><p class="overline">LA CONFIANZA DE QUIENES NOS ENCUENTRAN</p><div class="rating-large">{rating}<span>★</span></div><h2>Tu experiencia importa.</h2><p>{count} {'reseña' if count=='1' else 'reseñas'} en Google. Consulta las opiniones originales y conoce más del negocio.</p>{stars}</section>
<section class="faq section reveal"><div><p class="overline">05 / ANTES DE VISITARNOS</p><h2>Hablemos claro.</h2><p>¿Te quedó una pregunta?<br>Estamos a un mensaje.</p></div><div>{''.join(f'<details><summary>{e(q)}<span>+</span></summary><p>{e(a)}</p></details>' for q,a in content['faq'])}</div></section>
<section class="contact section" id="contacto"><div class="reveal"><p class="overline">06 / ENCUÉNTRANOS EN CARTAGENA</p><h2>{'Nos vemos pronto.' if kind not in ['medical','accounting'] else 'Demos el siguiente paso.'}</h2><p class="address">{icon('pin')}{e(row['Dirección'])}</p>{button}<div class="contact-links"><a href="tel:{e(row['Teléfono'])}">{e(row['Teléfono'])}</a>{email}{channels}</div><p class="fine">Horarios: consulta la atención del día por WhatsApp.</p></div><iframe title="Ubicación de {e(name)} en Google Maps" src="{mapurl}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></section>'''
    nav = f'<header class="nav"><a class="brand" href="#">{logo}<span>{e(name)}<small>CARTAGENA · COLOMBIA</small></span></a><nav aria-label="Navegación principal"><a href="#descubre">Nosotros</a><a href="#servicios">{ "Colecciones" if kind in ["fashion","jewelry"] else "Descubre"}</a><a href="#contacto">Encuéntranos</a></nav><a class="nav-cta" href="{e(wa)}">Hablemos {icon("chat")}</a><button class="menu-toggle" aria-label="Abrir menú" aria-expanded="false">☰</button></header>'
    page = head(name, fonts) + f'<body class="site {kind} variation-{index%3}" style="{cssvars};--heading:\'{fonts[0]}\';--body:\'{fonts[1]}\'">'+offer(name)+nav+'<main>'+hero+sections+f'</main><footer><a class="brand" href="#">{logo}<span>{e(name)}</span></a><p>Cartagena se vive con lo nuestro.</p><a href="../">Ver todas las propuestas ↗</a><p class="fine">Propuesta MVP · Fotos de referencia de Unsplash · Información comercial por confirmar.</p></footer><script src="../site.js"></script></body></html>'
    (target/'index.html').write_text(page)
    return f'<a class="gallery-card" href="{slug}/" style="--card-color:{colors[0]}"><div class="gallery-cover">{image_tag(p[0])}<span>EXPLORAR PROPUESTA {icon()}</span></div><div class="gallery-card-info">{gallery_logo}<div><p class="overline">{e(row["Rubro"])}</p><h2>{e(name)}</h2><p>{e(content["eyebrow"])}</p></div>{icon()}</div></a>'


def main():
    DIST.mkdir(exist_ok=True)
    with LEADS.open(encoding='utf-8-sig') as source:
        rows = list(csv.DictReader(source))[60:80]
    kits = {json.loads(p.read_text())['negocio']: p.parent for p in KITS.glob('*/brand.json')}
    copy = json.loads((ROOT/'content/copy.json').read_text())
    photos = json.loads((ROOT/'content/photos.json').read_text())
    if len(rows) != 20 or len(copy) != 20:
        raise ValueError('Expected exactly 20 leads and 20 copy entries')
    cards = [render(row,c,kits[row['Negocio']],i,photos) for i,(row,c) in enumerate(zip(rows,copy))]
    for asset in ['site.css','site.js']:
        shutil.copy2(ROOT/'assets'/asset,DIST/asset)
    page = head('Cartagena · Veinte marcas, nuevas posibilidades',['Syne','Inter'],'site.css')+f'''<body class="portfolio"><header class="portfolio-nav"><a href="./">CARTAGENA<span> / EN DIGITAL</span></a><span>SELECCIÓN 061—080</span><a href="#coleccion">Las propuestas ↓</a></header><main><section class="portfolio-hero"><p class="overline">NEGOCIOS LOCALES. NUEVAS POSIBILIDADES.</p><h1>La ciudad tiene historias.<br><em>Démosles una web.</em></h1><div><p>20 marcas de Cartagena, 20 formas de conectar.<br>Explora una colección de propuestas hechas para<br>que lo nuestro llegue más lejos.</p><a href="#coleccion" class="round-link">↓</a><span>20 <small>NEGOCIOS<br>CON IDENTIDAD</small></span></div><svg viewBox="0 0 240 240" aria-hidden="true"><path d="M120 0v240M0 120h240M35 35l170 170M35 205 205 35M73 9l94 222M9 73l222 94M9 167 231 73M73 231 167 9" stroke="currentColor" stroke-width="2"/></svg></section><section id="coleccion" class="portfolio-collection"><div class="collection-heading"><h2>El talento está aquí.</h2><span>20 propuestas · Cartagena, Colombia</span></div><div class="portfolio-grid">{''.join(cards)}</div></section></main><footer><strong>CARTAGENA / EN DIGITAL</strong><p>Diseño con identidad. Hecho para conectar.</p><a href="mailto:ablanquicet@agapai.com.co">Hablemos de tu marca ↗</a></footer></body></html>'''
    (DIST/'index.html').write_text(page)
    print('Built 20 business sites + gallery in',DIST)


if __name__ == '__main__':
    main()
