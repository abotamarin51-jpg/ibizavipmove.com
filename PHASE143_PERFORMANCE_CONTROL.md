# Phase 143 — Partners hero WebP reuse

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

## Evidencia

Se revisó el artefacto exacto de producción de la Fase 142 (`10321916618`, digest `sha256:288a646a89a5032d83f08485799339ec455b8a8f0e2595be143106c0cd830a93`). Las cinco páginas Partners existentes (`/partners/`, `/fr/partners/`, `/de/partners/`, `/ar/partners/`, `/es/partners/`) usan como imagen prioritaria `/assets/images/private-office.jpg` de 727.490 bytes sin una fuente alternativa moderna. El WebP ya existente y validado por Fase 139, `/assets/images/private-office-hero.webp`, pesa 357.986 bytes y representa la misma imagen a la misma resolución; reutilizarlo evita aproximadamente 369.504 bytes (50,8 %) del payload de esa imagen cuando el navegador admite WebP.

La página inglesa también precarga el JPEG. Para evitar una descarga redundante, el cambio sustituye únicamente esa precarga por el WebP con `type="image/webp"`; el `<img>` original conserva el JPEG como fallback.

## Cambio

`phase143_enhance.py` envuelve únicamente la imagen `fetchpriority="high"` de las cinco páginas Partners con un `<picture>` que ofrece primero el WebP existente. No crea assets, URLs, servicios, trackers ni contenido nuevo. No cambia H1, copy, canonical, hreflang, schema, sitemap, formularios, WhatsApp, precios ni políticas.

`phase143_audit.py` exige la fuente WebP y el JPEG fallback en el mismo `<picture>`, valida el preload inglés, conserva un H1 y self-canonical por página y exige que el sitemap siga teniendo 156 URLs únicas.

## Validación local sobre producción congelada

El gate falla antes del cambio como se espera. Después de aplicar el enhancer, las cinco páginas contienen exactamente un `picture` marcado para Fase 143; la inglesa precarga el WebP y ya no precarga el JPEG. La segunda ejecución es idempotente. La comparación del artefacto congelado cambia únicamente los cinco HTML de Partners y no modifica el sitemap.

Estado en este registro: **PREPARADO / VALIDADO LOCALMENTE**. Falta CI de PR, revisión exacta del diff, merge y deployment antes de denominarlo publicado. La mejora demostrada es una reducción potencial del payload de imagen; no demuestra mejora medida de Core Web Vitals, ranking, indexación, visibilidad en IA, tráfico, leads o ventas.
