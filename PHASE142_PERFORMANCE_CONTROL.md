# Phase 142 — localized home mobile hero

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

## Evidencia previa

Se revisó el artefacto exacto de producción de la Fase 141 (`10321335103`, SHA256 `630c21138a76d31247a5fa831b86705e4548412cd62a30bf803b3adb2e96ee75`). La Home inglesa ya utiliza `<picture>` con `/assets/images/hero-mobile.jpg` para pantallas de hasta 700 px y `/assets/images/hero-desktop.jpg` como fallback. Las Home localizadas `/fr/`, `/de/`, `/ar/` y `/es/` seguían cargando directamente el JPEG de escritorio como imagen prioritaria.

Tamaños medidos en el artefacto: `hero-desktop.jpg` = 402,379 bytes; `hero-mobile.jpg` = 179,951 bytes. Para un navegador que elija la fuente móvil, reutilizar el asset ya existente evita aproximadamente 222,428 bytes del payload de esa imagen (55.3%). Esto es una reducción de bytes de imagen, no una medición de Core Web Vitals ni una garantía de mejora de ranking o conversión.

## Cambio preparado

`phase142_enhance.py` envuelve únicamente la imagen `fetchpriority="high"` de las cuatro Home localizadas con el mismo patrón `<picture>` ya usado por Home inglesa. No crea un asset, URL, preload o tracker nuevo y no cambia copy, H1, canonical, hreflang, schema, sitemap, formularios, WhatsApp, precios ni políticas.

`phase142_audit.py` exige una sola imagen prioritaria responsive por Home localizada, confirma que el asset móvil es más liviano que el de escritorio y conserva el inventario de 156 URLs. El gate se encadena a la auditoría final ya ejecutada por Fase 141.

## Validación local sobre producción congelada

El audit falla antes del cambio, como se espera. Después de aplicar el enhancer, las cuatro Home contienen exactamente una fuente móvil `(max-width:700px)` apuntando a `/assets/images/hero-mobile.jpg`, con `/assets/images/hero-desktop.jpg` y `fetchpriority="high"` preservados como fallback. La segunda ejecución cambia 0 páginas (idempotencia) y el audit pasa. El sitemap sigue en 156 URLs.

Estado: **PREPARADO / VALIDADO LOCALMENTE**. Falta CI de PR, revisión exacta del diff, merge y deployment antes de denominarlo publicado.
