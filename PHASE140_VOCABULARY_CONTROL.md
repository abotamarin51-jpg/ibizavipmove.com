# Phase 140 — control de vocabulario aplicado

Fecha: 13 de septiembre de 2026 (Europe/Madrid).

Fuente nueva utilizada: **exclusivamente** `IBIZA_VIP_MOVE_REVISAR_ANTES_DE_AGREGAR.pdf`, según la instrucción del usuario. El archivo indica que sus 48 conceptos por idioma son material de referencia, no 48 servicios nuevos ni 240 oportunidades SEO independientes. También pide reutilizar páginas existentes, distinguir perfiles profesionales de servicios y evitar inserción automática de sinónimos.

## Alcance revisado antes del cambio

Se contrastó el artefacto exacto de producción de la Fase 139 (`10320131089`, SHA256 `df72d8dba188e936164f3795cf20e1e630c2d905dd56ccfc591a8e3e3abc3684`) con las páginas Partners y Private Office en EN/FR/DE/AR/ES. Los A1–A8 no aparecían literalmente en esa muestra. Entre B25–B34, el inglés ya cubría literalmente `Luxury travel advisor` y `Executive assistant`; PA/DMC y otros perfiles tenían cobertura conceptual parcial, mientras que la mayoría de las etiquetas localizadas exactas no aparecían en esas diez páginas.

B01–B24 y B35–B40 se conservaron como referencia: describen necesidades/servicios y servicios concretos que ya están representados por la arquitectura y páginas de servicio existentes. No se volcaron como listas de palabras clave ni se crearon URLs por sinónimos.

## Tabla de control

Cada fila agrupa las cinco equivalencias EN / FR / DE / AR / ES del mismo concepto. `Partners` significa `/partners/`, `/fr/partners/`, `/de/partners/`, `/ar/partners/`, `/es/partners/`; `Private Office` usa las cinco rutas equivalentes.

| ID | Términos EN / FR / DE / AR / ES | Página comprobada | Evidencia previa | Estado / acción final |
|---|---|---|---|---|
| A1 | Lifestyle Coordinator / Coordinateur de voyages et de services lifestyle / Koordinator für Reise- und Lifestyle-Services / منسق خدمات السفر ونمط الحياة / Coordinador de viajes y servicios lifestyle | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| A2 | VIP Host / Hôte VIP / VIP-Gästebetreuer / مضيف كبار الشخصيات / Anfitrión VIP | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| A3 | Family Assistant / Assistant personnel de famille / Private Familienassistenz / مساعد شخصي للعائلة / Asistente personal de familias | Private Office | Exactos ausentes en muestra F139 | Publicado como perfil de equipo privado |
| A4 | Household Manager / Intendant de maison / Hausmanager für Privathaushalte / مدير شؤون المنزل / Administrador del hogar | Private Office | Exactos ausentes en muestra F139 | Publicado con límite de coordinación local |
| A5 | Estate Manager / Intendant de propriétés privées / Verwalter privater Anwesen / مدير الأملاك السكنية الخاصة / Gestor de propiedades residenciales privadas | Private Office | Exactos ausentes en muestra F139 | Publicado con aclaración de no gestión inmobiliaria |
| A6 | Director of Residences / Directeur de résidences privées / Leiter privater Residenzen / مدير المساكن الخاصة / Director de residencias privadas | Private Office | Exactos ausentes en muestra F139 | Publicado con límite de coordinación local |
| A7 | Artist Liaison / Chargé de l’accueil des artistes / Künstlerbetreuer / منسق شؤون الفنانين / Coordinador de atención a artistas | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| A8 | Tour Manager / Responsable de tournée / Tourmanager für Musikproduktionen / مدير الجولات الفنية / Mánager de giras musicales | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| B25 | Luxury travel advisor / Conseiller en voyages de luxe / Luxusreiseberater / مستشار سفر فاخر / Asesor de viajes de lujo | Partners | EN ya visible; etiquetas localizadas exactas ausentes en muestra | Cobertura ampliada/publicada |
| B26 | Travel designer / Créateur de voyages / Reisedesigner / مصمم رحلات / Diseñador de viajes | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| B27 | Destination specialist / Spécialiste de la destination / Destinationsspezialist / خبير وجهات سياحية / Especialista en destinos | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| B28 | Independent travel agent / Agent de voyages indépendant / Selbstständiger Reiseberater / وكيل سفر مستقل / Agente de viajes independiente | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| B29 | Boutique travel agency / Agence de voyages à taille humaine / Boutique-Reisebüro / وكالة سفر متخصصة / Agencia boutique de viajes | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| B30 | Luxury tour operator / Tour-opérateur de luxe / Luxusreiseveranstalter / منظم رحلات فاخرة / Operador de viajes de lujo | Partners | Exactos ausentes en muestra F139 | Publicado como perfil profesional |
| B31 | Destination management company / Agence réceptive / Destinationsmanagement-Agentur / شركة إدارة الوجهات السياحية / Agencia receptiva | Partners | Intención DMC ya cubierta; exactos ausentes en muestra Partners | Cobertura ampliada/publicada |
| B32 | Private personal assistant / Assistant personnel privé / Privatassistent / مساعد شخصي خاص / Asistente personal privado | Private Office | Intención PA ya cubierta; exactos ausentes en muestra | Cobertura ampliada/publicada |
| B33 | Executive assistant / Assistant de direction / Assistenz der Geschäftsführung / مساعد تنفيذي / Asistente ejecutivo | Private Office | EN ya visible; localizados exactos ausentes en muestra | Cobertura ampliada/publicada |
| B34 | Guest relations manager / Responsable des relations clients / Guest Relations Manager / مدير علاقات الضيوف / Responsable de relaciones con huéspedes | Private Office | Exactos ausentes en muestra F139 | Publicado como perfil profesional |

## Implementación y publicación verificadas

PR #68 fue fusionado como `628aec9ec6e509e26ddab3fd0d1547154b91e417`. El CI completo `34767216531` terminó correctamente y el deployment de producción `34767294117` terminó en `success`, incluyendo GitHub Pages e IndexNow. El artefacto de producción es `10320468878`, digest `sha256:90651df9065d24213e15dc316e54d1510fd212603492eb04697e12b24f4c2ed7`.

La comparación exacta con la producción F139 cambia únicamente diez HTML generados: Partners y Private Office en EN/FR/DE/AR/ES. No cambia sitemap, robots, URLs, canonicals, hreflang, schema, formularios, tracking, precios, políticas ni inventario de servicios. El sitemap conserva 156 URLs únicas.

PR #67 fue una preparación concurrente del mismo archivo, limitada a A1–A8. Se cerró sin merge después de comprobar que PR #68 ya cubría esos conceptos y B25–B34; así se evita duplicar bloques de vocabulario.

Estado final de esta tabla: **PUBLICADO Y VALIDADO EN EL ARTEFACTO DE PRODUCCIÓN**. Esto registra cobertura editorial/técnica; no demuestra ranking, indexación, visibilidad en IA, tráfico, leads o ventas.
