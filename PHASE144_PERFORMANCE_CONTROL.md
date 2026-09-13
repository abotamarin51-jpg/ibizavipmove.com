# Phase 144 — priority villa hero modern formats

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

## Evidencia previa

Se revisó el artefacto exacto de producción de la Fase 143 (`10322447559`, digest `sha256:96ebcf35c196ffbb8e7bc430d2cf277d5d5a1eaaf97bd13983dd16f216d87e61`). El asset compartido `/assets/images/villa.jpg` pesaba 705.320 bytes y medía 2000×1334 píxeles en ese artefacto.

Catorce páginas lo usaban como imagen `fetchpriority="high"`: cinco páginas de villas en EN/FR/DE/AR/ES; cuatro páginas localizadas de Private Concierge en FR/DE/AR/ES; y cinco páginas Villa Arrival Planning en EN/FR/DE/AR/ES. Nueve de esas páginas además precargaban directamente el JPEG. Las tarjetas de Services que usan la misma imagen con `loading="lazy"` quedaron fuera de esta fase.

La prueba local sobre el mismo JPEG produjo AVIF de 348.484 bytes (quality 60; ~50,6 % menos que el JPEG) y WebP de 501.690 bytes (quality 80; ~28,9 % menos). Ambos conservaron 2000×1334. El error absoluto medio frente al JPEG decodificado fue 3,609/255 para AVIF y 2,879/255 para WebP; la comparación visual de una muestra central no mostró cambio de encuadre ni un artefacto evidente que justificara conservar el JPEG como formato preferido.

## Cambio

`phase144_enhance.py` genera ambos formatos a partir del JPEG del build y envuelve únicamente las 14 imágenes prioritarias revisadas con `<picture>` en orden AVIF → WebP → JPEG. El `<img src>` original sigue siendo el JPEG y conserva alt, dimensiones, `fetchpriority` y demás atributos. Las nueve precargas JPEG existentes pasan a una única precarga AVIF con `type="image/avif"`; no se añaden precargas a las otras cinco páginas.

`phase144_audit.py` exige inventario exacto de las 14 páginas, dimensiones idénticas, presupuestos de tamaño, AVIF/WebP + JPEG fallback, precargas coherentes, un H1, self-canonical y permanencia en el sitemap de 156 URLs. El enhancer se encadena desde la Fase 139 porque ese paso ya se ejecuta con Pillow 12.3.0; el audit se encadena en el mismo entorno. No se rebajó ningún gate existente.

No se crearon URLs, servicios, copy, schema, trackers ni cambios de política. No se modificó Google Business Profile, Analytics, precios, formularios ni WhatsApp.

## Validación local y CI

Sobre el artefacto congelado de Fase 143, el gate falló antes del cambio por ausencia de los nuevos assets. Tras aplicar el enhancer, pasaron las 14 páginas, los dos formatos modernos y las nueve precargas; una segunda ejecución no volvió a modificar HTML (idempotencia). La comparación de salida cambió exactamente 14 HTML y añadió dos assets; sitemap y resto del artefacto permanecieron iguales.

PR #76 pasó CI completo `34776398399`; el preview validado fue el artefacto `10323611618`, digest `sha256:7bafe7178cc0acb147d589c07b1d4f23757e97b4f057998e92d30018d1340ba4`. Antes del merge se confirmó que el PR era mergeable, que `main` no había avanzado y que los únicos archivos fuente modificados eran `PHASE144_PERFORMANCE_CONTROL.md`, `phase139_audit.py`, `phase139_enhance.py`, `phase144_audit.py` y `phase144_enhance.py`. PR #76 se fusionó como `c4f243eed1ce835168e1ffd6bd1bf18818e8b53d`.

## Producción verificada

El deployment `34776512394` terminó en `success`, incluyendo GitHub Pages e IndexNow. El artefacto exacto de producción es `10323841907`, digest `sha256:85ba295391be806207aefa0d34cde642b94f19fb680af52150c0eb3fb8cdf2ae`.

En ese build de producción, `villa.jpg` pesa 705.022 bytes; `villa-priority.avif` pesa 348.411 bytes y `villa-priority.webp` 501.768 bytes. Los tres conservan 2000×1334. Esto supone aproximadamente 356.611 bytes menos (50,6 %) para la fuente AVIF frente al JPEG de ese mismo build, y aproximadamente 203.254 bytes menos (28,8 %) para WebP.

La inspección del artefacto confirma exactamente 14 `<picture data-ivm144="villa-priority">`, nueve precargas AVIF y ninguna precarga JPEG en esas páginas. El sitemap conserva 156 URLs únicas. Frente al artefacto de Fase 143, la salida cambia los 14 HTML previstos, añade AVIF y WebP, y muestra únicamente la variación ya conocida de clean-build del propio `villa.jpg`; no cambió ninguna otra salida.

Las páginas públicas de Luxury Villas en inglés y francés continuaron resolviendo con sus H1, contenido y CTA existentes después del deployment. La verificación pública del HTML puede estar sujeta a caché, por lo que el artefacto exacto de producción es la evidencia primaria de la nueva selección de formatos.

## Referencias primarias verificadas

- Google Search Central, Image SEO: `picture` puede ofrecer formatos modernos manteniendo un `img src` fallback; Google Search admite JPEG, WebP y AVIF. https://developers.google.com/search/docs/appearance/google-images
- Google Search Central, AVIF: AVIF es compatible con Google Search e Images; Google desaconseja cambios masivos ciegos y recomienda evaluar el formato por necesidad. https://developers.google.com/search/blog/2024/08/happy-avifriday
- web.dev, imágenes: para fotografía, AVIF puede ser el formato preferido, WebP un fallback moderno y JPEG el fallback más compatible. https://web.dev/learn/images/automating/

Estado final: **PUBLICADO Y VALIDADO EN EL ARTEFACTO DE PRODUCCIÓN**. La mejora demostrada es de entrega/peso del recurso prioritario. No se atribuye por ello mejora medida de Core Web Vitals de campo, ranking, indexación, visibilidad en IA, tráfico, leads o ventas.
