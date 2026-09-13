# Ibiza VIP Move — control del vocabulario restante

Fecha de revisión: 13 de septiembre de 2026, Europe/Madrid.

Fuente de vocabulario utilizada: **exclusivamente** `IBIZA_VIP_MOVE_REVISAR_ANTES_DE_AGREGAR.pdf`, por instrucción del usuario. Este control continúa las Fases 140 y 141 y no introduce vocabulario externo.

## Evidencia revisada

Se contrastó el artefacto exacto de producción posterior a la Fase 148: GitHub Pages artifact `10326480885`, digest `sha256:e54760c9a27598c44d939f4269588777c6c61340caa5a241bcab668c512cde5f`, correspondiente al deployment exitoso `34784857326` desde `ad13b6ef78f1a59322fc9970e9b869b784b98b3c`.

El PDF indica que B01–B24 describen necesidades/servicios, B25–B34 son principalmente perfiles o tipos de empresas y B35–B40 son servicios concretos que deben corresponder a la oferta real. También exige comparar la intención ya cubierta antes de añadir texto y no convertir cada equivalencia en una página o keyword nueva.

Fase 140 ya publicó A1–A8 y B25–B34 en Partners / Private Office. Fase 141 ya publicó una selección no-«concierge» de B01, B02, B04, B06, B07, B23 y B24 en los hubs de Services. Este documento controla el resto para evitar duplicación.

## Resultado del resto de B01–B24

| IDs | Estado verificado en producción | Decisión |
| --- | --- | --- |
| B03, B05 | La intención de diseño/planificación de viaje y vacaciones a medida ya queda cubierta por el bloque de Services publicado en Fase 141 con luxury travel planning, bespoke/custom travel e itinerary planning y sus equivalentes localizados. | No añadir otra lista de sinónimos. |
| B08, B10 | Personal Concierge ya explica asistencia directa, day-to-day private assistance, reservas, transporte y apoyo durante la estancia. | Cobertura por intención; no añadir por coincidencia literal. |
| B09 | Existe la arquitectura específica de Luxury Lifestyle Management y su intención está ampliamente visible. | Ya cubierto. |
| B11 | Existe la página VIP Services y describe hospitality, access, mobility y coordinación VIP. | Ya cubierto. |
| B12 | Existe Private Client Services para principals, familias, PAs y family offices. | Ya cubierto. |
| B13–B15 | VIP Services y Personal Concierge ya explican hospitality support, guest timing, guest logistics, apoyo personal y un contacto dedicado. Las traducciones usan formulaciones naturales equivalentes. | No forzar Guest services / Guest experience management / Personal hosting como etiquetas adicionales. |
| B16–B18 | Personal Concierge y VIP Services ya incluyen experiences, bespoke requests, hospitality y access, siempre sujetos a disponibilidad y confirmación. | Cobertura por intención; no añadir sin una necesidad editorial nueva. |
| B19–B20 | Restaurants & Nightlife publica restaurant reservations, VIP table requests y access; FR/DE/AR usan lenguaje equivalente de reservas, mesas/entrada y disponibilidad. | Ya cubierto por término o variante. |
| B21 | Private Events publica private events / celebrations / event coordination y sus equivalentes localizados. | Ya cubierto; no crear URL por “planning”. |
| B22 | Luxury Villas publica villa support, guest logistics, staffing y apoyo durante la estancia; las páginas localizadas describen el mismo alcance. | Cobertura por intención; no añadir una etiqueta aislada. |

## Resultado de B35–B40

Estos seis conceptos corresponden a servicios reales ya representados por páginas existentes. La ausencia de una frase exacta en un idioma no se trata como ausencia del servicio.

| ID | Concepto | Evidencia de arquitectura actual | Decisión |
| --- | --- | --- | --- |
| B35 | Conductor privado | Private Chauffeur / Chauffeur privé / Privater Chauffeur / سائق خاص / Chauffeur privado | Ya cubierto. |
| B36 | Servicio de chófer | Las mismas páginas describen el servicio de chauffeur y disponibilidad coordinada. | Ya cubierto; no duplicar landing. |
| B37 | Traslados al aeropuerto | Las páginas de chauffeur describen llegadas/salidas, vuelo, equipaje, destino y movimientos de aeropuerto. | Cubierto dentro de Chauffeur; no crear URL solo por el sinónimo. |
| B38 | Alquiler de villas de lujo | Luxury Villas y equivalentes localizados describen selección/sourcing, solicitudes de villa y coordinación de estancia. | Ya cubierto por la oferta real; no crear variante de rental. |
| B39 | Alquiler de yates | Yacht Charter y equivalentes localizados describen yacht, marina, charter y coordinación del día. | Ya cubierto. |
| B40 | Seguridad privada | Private Security y equivalentes localizados describen protección privada y coordinación de seguridad. | Ya cubierto. |

## Idiomas

EN, FR, DE y AR se revisaron como idiomas prioritarios. ES se revisó únicamente como referencia existente, sin ampliar su prioridad. No se abrió ningún mercado nuevo.

En FR/DE/AR varias equivalencias exactas del PDF no aparecen literalmente, pero las páginas localizadas actuales cubren la misma intención con redacción natural. Según el propio PDF, eso no justifica insertar automáticamente cada variante.

## Decisión final

**No se justifica un nuevo cambio de contenido para los conceptos restantes del PDF en esta revisión.** Añadirlos ahora como listas o repeticiones aumentaría redundancia y riesgo de keyword stuffing sin aportar una necesidad distinta.

No se modifican HTML, URLs, titles, H1, canonicals, hreflang, schema, sitemap, robots, formularios, WhatsApp, tracking, precios, políticas, Google Business Profile ni inventario de servicios. Este commit es únicamente de control documental y no debe disparar un deployment del sitio.

Reabrir un concepto de este PDF solo si una futura auditoría demuestra una intención comercial real no cubierta, un problema de comprensión del usuario o evidencia de Search Console que justifique mejorar una página existente. La coincidencia literal por sí sola no basta.
