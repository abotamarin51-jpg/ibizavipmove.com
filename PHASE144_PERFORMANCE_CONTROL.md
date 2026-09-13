# Phase 144 — priority villa hero modern formats

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

## Evidencia previa

Se revisó el artefacto exacto de producción de la Fase 143 (`10322447559`, digest `sha256:96ebcf35c196ffbb8e7bc430d2cf277d5d5a1eaaf97bd13983dd16f216d87e61`). El asset compartido `/assets/images/villa.jpg` pesa 705.320 bytes y mide 2000×1334 píxeles.

Catorce páginas lo usan como imagen `fetchpriority="high"`: cinco páginas de villas en EN/FR/DE/AR/ES; cuatro páginas localizadas de Private Concierge en FR/DE/AR/ES; y cinco páginas Villa Arrival Planning en EN/FR/DE/AR/ES. Nueve de esas páginas además precargan directamente el JPEG. Las tarjetas de Services que usan la misma imagen con `loading="lazy"` quedan fuera de esta fase.

La prueba local sobre el mismo JPEG produjo AVIF de 348.484 bytes (quality 60; ~50,6 % menos que el JPEG) y WebP de 501.690 bytes (quality 80; ~28,9 % menos). Ambos conservan 2000×1334. El error absoluto medio frente al JPEG decodificado fue 3,609/255 para AVIF y 2,879/255 para WebP; la comparación visual de una muestra central no mostró cambio de encuadre ni un artefacto evidente que justifique conservar el JPEG como formato preferido.

## Cambio preparado

`phase144_enhance.py` genera ambos formatos a partir del JPEG del build y envuelve únicamente las 14 imágenes prioritarias revisadas con `<picture>` en orden AVIF → WebP → JPEG. El `<img src>` original sigue siendo el JPEG y conserva alt, dimensiones, `fetchpriority` y demás atributos. Las nueve precargas JPEG existentes pasan a una única precarga AVIF con `type="image/avif"`; no se añaden precargas a las otras cinco páginas.

`phase144_audit.py` exige inventario exacto de las 14 páginas, dimensiones idénticas, presupuestos de tamaño, AVIF/WebP + JPEG fallback, precargas coherentes, un H1, self-canonical y permanencia en el sitemap de 156 URLs. El enhancer se encadena desde la Fase 139 porque ese paso ya se ejecuta con Pillow 12.3.0; el audit se encadena en el mismo entorno. No se rebaja ningún gate existente.

No se crean URLs, servicios, copy, schema, trackers ni cambios de política. No se modifica Google Business Profile, Analytics, precios, formularios ni WhatsApp.

## Validación local

Sobre el artefacto congelado de Fase 143, el gate falla antes del cambio por ausencia de los nuevos assets. Tras aplicar el enhancer, pasan las 14 páginas, los dos formatos modernos y las nueve precargas; una segunda ejecución no vuelve a modificar HTML (idempotencia). La comparación de salida cambia exactamente 14 HTML y añade dos assets; sitemap y resto del artefacto permanecen iguales.

## Referencias primarias verificadas

- Google Search Central, Image SEO: `picture` puede ofrecer formatos modernos manteniendo un `img src` fallback; Google Search admite JPEG, WebP y AVIF. https://developers.google.com/search/docs/appearance/google-images
- Google Search Central, AVIF: AVIF es compatible con Google Search e Images; Google desaconseja cambios masivos ciegos y recomienda evaluar el formato por necesidad. https://developers.google.com/search/blog/2024/08/happy-avifriday
- web.dev, imágenes: para fotografía, AVIF puede ser el formato preferido, WebP un fallback moderno y JPEG el fallback más compatible. https://web.dev/learn/images/automating/

Estado en este archivo: **PREPARADO Y VALIDADO LOCALMENTE; pendiente de CI/PR/publicación**. No se atribuye mejora de Core Web Vitals de campo, ranking, indexación, visibilidad en IA, tráfico, leads o ventas sin medición posterior.
