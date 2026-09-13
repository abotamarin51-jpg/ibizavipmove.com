# Phase 142 — localized home mobile hero

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

## Evidencia previa

Se revisó el artefacto exacto de producción de la Fase 141 (`10321335103`, SHA256 `630c21138a76d31247a5fa831b86705e4548412cd62a30bf803b3adb2e96ee75`). La Home inglesa ya utiliza `<picture>` con `/assets/images/hero-mobile.jpg` para pantallas de hasta 700 px y `/assets/images/hero-desktop.jpg` como fallback. Las Home localizadas `/fr/`, `/de/`, `/ar/` y `/es/` seguían cargando directamente el JPEG de escritorio como imagen prioritaria.

Tamaños medidos en el artefacto: `hero-desktop.jpg` = 402,379 bytes; `hero-mobile.jpg` = 179,951 bytes. Para un navegador que elija la fuente móvil, reutilizar el asset ya existente evita aproximadamente 222,428 bytes del payload de esa imagen (55.3%). Esto es una reducción de bytes de imagen, no una medición de Core Web Vitals ni una garantía de mejora de ranking o conversión.

## Cambio

`phase142_enhance.py` envuelve únicamente la imagen `fetchpriority="high"` de las cuatro Home localizadas con el mismo patrón `<picture>` ya usado por Home inglesa. No crea un asset, URL, preload o tracker nuevo y no cambia copy, H1, canonical, hreflang, schema, sitemap, formularios, WhatsApp, precios ni políticas.

`phase142_audit.py` exige una sola imagen prioritaria responsive por Home localizada, confirma que el asset móvil es más liviano que el de escritorio y conserva el inventario de 156 URLs. El gate queda encadenado a la auditoría final ya ejecutada por Fase 141.

## Validación local y CI

El audit falla antes del cambio, como se espera. Después de aplicar el enhancer, las cuatro Home contienen exactamente una fuente móvil `(max-width:700px)` apuntando a `/assets/images/hero-mobile.jpg`, con `/assets/images/hero-desktop.jpg` y `fetchpriority="high"` preservados como fallback. La segunda ejecución cambia 0 páginas (idempotencia) y el audit pasa. El sitemap sigue en 156 URLs.

PR #72 pasó CI completo `34769932349`, fue revisado como mergeable y el diff contenía únicamente `PHASE142_PERFORMANCE_CONTROL.md`, `phase141_enhance.py`, `phase141_audit.py`, `phase142_enhance.py` y `phase142_audit.py`. Se fusionó como `ac727ab4320a81e265a5be7850a6b9287a9153f7`.

## Producción verificada

El deployment de producción `34769985509` terminó en `success`, incluyendo GitHub Pages e IndexNow. El artefacto exacto es `10321916618`, digest `sha256:288a646a89a5032d83f08485799339ec455b8a8f0e2595be143106c0cd830a93`.

La inspección del artefacto confirma en `/fr/`, `/de/`, `/ar/` y `/es/` una única fuente móvil `(max-width:700px)` hacia `/assets/images/hero-mobile.jpg`, con `/assets/images/hero-desktop.jpg` como fallback prioritario. El sitemap conserva 156 URLs. Frente a Fase 141 cambian los cuatro HTML previstos más la variación ya conocida de clean-build en `assets/images/villa.jpg`; no se modificó código fuente de esa imagen en esta fase.

Estado final: **PUBLICADO Y VALIDADO EN EL ARTEFACTO DE PRODUCCIÓN**. La mejora técnica demostrada es la reducción potencial de 222,428 bytes (55.3%) del hero cuando el navegador selecciona la fuente móvil. No se infiere por ello mejora medida de Core Web Vitals, ranking, indexación, visibilidad en IA, leads o ventas.
