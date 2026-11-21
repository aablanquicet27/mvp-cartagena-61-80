# Cartagena / En digital

20 propuestas MVP en español para las filas de datos 61–80 del CSV (sin contar encabezado). Cada marca se une a su carpeta por el campo `negocio` de `brand.json`; los nombres visibles se limpian en el contenido editorial.

## Construir y servir

```sh
python3 build.py
python3 -m http.server 8080 --directory dist
```

El generador solo utiliza la biblioteca estándar de Python. Requiere los insumos originales en `../leads.csv` y `../kits/brand_kits/`. El resultado en `dist/` es independiente del generador: se puede alojar en cualquier servidor estático. Las fotos de Unsplash, Google Fonts y mapas requieren internet.

## Editar

- `content/copy.json`: redacción manual por negocio, en el orden de las 20 filas seleccionadas; títulos, introducción, historia, servicios, enfoque y preguntas frecuentes.
- `content/photos.json`: cuatro imágenes únicas por rubro y textos alternativos.
- `build.py`: extracción de paleta y tipografías de DESIGN_STYLE, contactos reales del CSV, SVG originales y páginas completas.
- `assets/site.css`: trece direcciones visuales, variaciones por marca, responsive, animaciones y reducción de movimiento.
- `assets/site.js`: entrada por scroll, menú móvil, propuesta comercial accesible y consultas de fechas.
- `SELLER_WHATSAPP` en `build.py`: vacío por defecto; abre el selector de WhatsApp con el mensaje comercial. Para configurar vendedor, usar solo dígitos con código de país y reconstruir.

La oferta de $200.000 COP se mantiene separada de los contactos del negocio. No se promete dominio ni hosting. El correo alterno es ablanquicet@agapai.com.co.

## Criterio editorial

Las fotos son reales, pero de referencia: no se presentan como habitaciones, inventario, empleados o casos clínicos reales. No se inventan testimonios, credenciales, resultados, horarios, precios de servicios, convenios ni disponibilidad. Se muestran las calificaciones y los conteos del CSV con enlace a Google. Las secciones con datos no suministrados invitan a verificarlos directamente. Los gimnasios usan un hero fotográfico animado en lugar de un video sin procedencia validada.

Referencias visuales revisadas: `_referencias/joyeria/dribbble-2.webp`, `_referencias/hotel-hostal/dribbble-3.webp`, `_referencias/gimnasio/dribbble-1.webp`.

## Verificación

```sh
python3 -m unittest -v test_build.py
python3 check_photos.py
python3 verify.py
```

`check_photos.py` usa curl y guarda el resultado por URL en `evidence/image-checks.json`. Reutiliza verificaciones 200 anteriores; borra ese registro si necesitas una comprobación nueva de todas. Las descargas están ignoradas en git. Las hojas de contacto documentan la revisión visual de pertinencia.

`verify.py` requiere Playwright únicamente como dependencia de desarrollo (`python3 -m pip install playwright`) y Chrome instalado. Prueba 20 sitios a 360, 768 y 1440 px, contactos, modales, menú, fechas de reserva y reducción de movimiento. Captura index y seis rubros a 1440 y 390 px, además del modal. Capturas y resultados en `evidence/`.
