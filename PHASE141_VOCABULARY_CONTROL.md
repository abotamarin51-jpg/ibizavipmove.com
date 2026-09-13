# Phase 141 — control de vocabulario no «concierge»

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

Fuente de vocabulario utilizada: **exclusivamente** `IBIZA_VIP_MOVE_REVISAR_ANTES_DE_AGREGAR.pdf`, por instrucción del usuario. La Fase 140 ya publicó A1–A8 y B25–B34 en Partners y Private Office; esta fase no los repite.

## Comprobación previa

Se revisó el artefacto exacto de producción de la Fase 140 (`10320468878`, SHA256 `90651df9065d24213e15dc316e54d1510fd212603492eb04697e12b24f4c2ed7`) en los cinco hubs de Services: `/services/`, `/fr/services/`, `/de/services/`, `/ar/services/` y `/es/servicios/`.

Los términos primarios seleccionados de B01, B02, B04, B06, B07, B23 y B24 no aparecían literalmente en ninguno de esos cinco hubs. La selección es deliberadamente pequeña: son formas de describir planificación, apoyo en destino y coordinación que ayudan a visitantes que no buscan la palabra «concierge». No se vuelcan B01–B24 como lista completa y no se crea ninguna URL por sinónimo.

| ID | EN | FR | DE | AR | ES | Estado previo | Acción final |
|---|---|---|---|---|---|---|---|
| B01 | Luxury travel planning | Organisation de voyages de luxe | Luxusreiseplanung | تخطيط السفر الفاخر | Planificación de viajes de lujo | No encontrado literalmente en los hubs revisados | Publicado en Services hub |
| B02 | Bespoke travel / Custom travel | Voyages sur mesure | Maßgeschneiderte Reisen / Suiza: Massgeschneiderte Reisen | رحلات مصممة حسب الطلب | Viajes a medida | No encontrado literalmente en los hubs revisados | Publicado con adaptación regional |
| B04 | Itinerary planning | Création d’itinéraires | Individuelle Reiseplanung | تخطيط برامج الرحلات | Planificación de itinerarios | No encontrado literalmente en los hubs revisados | Publicado en Services hub |
| B06 | Destination services | Services à destination | Services am Urlaubsort | خدمات الوجهة السياحية | Servicios en destino | No encontrado literalmente en los hubs revisados | Publicado en Services hub |
| B07 | On-the-ground support | Assistance sur place | Betreuung vor Ort | مساعدة أثناء الإقامة | Asistencia durante la estancia | No encontrado literalmente en los hubs revisados | Publicado en Services hub |
| B23 | Travel coordination | Coordination de voyages | Reisekoordination | تنسيق السفر | Coordinación de viajes | No encontrado literalmente en los hubs revisados | Publicado en Services hub |
| B24 | Luxury travel services | Services de voyage haut de gamme | Luxusreiseservice | خدمات السفر الفاخر | Servicios de viajes de lujo | No encontrado literalmente en los hubs revisados | Publicado en Services hub |

## Implementación

Se añadió un único bloque editorial breve a cada hub existente con el mensaje equivalente a «no necesitas conocer la palabra concierge». El bloque explica que esas expresiones son distintas formas de describir el brief y **no** servicios nuevos de Ibiza VIP Move.

No cambiaron URL, title, H1, canonical, hreflang, schema, sitemap, formularios, WhatsApp, tracking, precios, políticas, Google Business Profile ni inventario de servicios. El sitemap conserva 156 URLs únicas y el árabe mantiene RTL.

## Publicación verificada

PR #70 pasó CI completo `34767906968` y fue fusionado como `b29f83c7dbb4f761e3a2192575a04904eded4d96`. El deployment `34767975332` terminó en `success`, incluyendo GitHub Pages e IndexNow. El artefacto exacto de producción es `10321335103`, digest `sha256:630c21138a76d31247a5fa831b86705e4548412cd62a30bf803b3adb2e96ee75`.

El artefacto de producción coincide con el preview validado salvo el `.nojekyll` esperado de GitHub Pages. Frente a la Fase 140, los únicos cambios de salida son los cinco HTML de Services previstos. El audit de Fase 141 vuelve a pasar sobre producción. La lectura pública independiente confirmó el nuevo bloque en `/fr/services/`; la lectura de `/services/` aún devolvió una versión en caché anterior durante la comprobación inmediata, por lo que no se interpreta como fallo del deployment.

Estado final: **PUBLICADO Y VALIDADO EN EL ARTEFACTO DE PRODUCCIÓN**. Esto demuestra publicación y coherencia técnica/editorial; no demuestra ranking, indexación en Google, visibilidad en IA, tráfico, leads o ventas.
