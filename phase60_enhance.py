from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path('_site')
BASE='https://ibizavipmove.com'
ORG=BASE+'/#organization'
WA='https://wa.me/34600703303'
TODAY='2026-09-03'
SCRIPT_RE=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)

SOURCES={
 'es':ROOT/'es'/'concierge-privado-ibiza'/'index.html',
 'fr':ROOT/'fr'/'conciergerie-privee-ibiza'/'index.html',
 'de':ROOT/'de'/'privater-concierge-ibiza'/'index.html',
 'ar':ROOT/'ar'/'private-concierge-ibiza'/'index.html',
}
HUBS={'es':'/es/servicios/','fr':'/fr/services/','de':'/de/services/','ar':'/ar/services/'}

SERVICES={
'chef':{
 'en':'/private-chef-staffing-ibiza/','image':'/assets/images/chef.jpg','type':'Private chef and villa staffing coordination in Ibiza',
 'es':{'path':'/es/chef-privado-staffing-ibiza/','title':'Chef privado y personal de villa Ibiza | Ibiza VIP Move','desc':'Chef privado, mayordomos, housekeeping y personal de villa en Ibiza con coordinación discreta alrededor de la estancia por Ibiza VIP Move.','kicker':'At Home · Ibiza','h1':'Chef privado y villa staff, coordinados alrededor de la estancia.','lead':'Los servicios en villa funcionan mejor cuando horarios, perfil de los huéspedes y necesidades prácticas forman parte del mismo brief.','section':'El servicio en villa empieza con un brief claro.','large':'Coordinamos solicitudes de chef y personal según el alcance confirmado, la villa, los horarios y las necesidades de la estancia.','items':[('01','Necesidades','Fechas, huéspedes, villa, horarios y tipo de soporte requerido.'),('02','Alcance','Aclaramos funciones, timing y requisitos antes de confirmar cualquier servicio.'),('03','Coordinación','Los servicios confirmados pueden alinearse con villa, chauffeur, dining y resto del itinerario.'),('04','Cambios','Si evoluciona la estancia, revisamos el alcance afectado según disponibilidad y condiciones aplicables.')],'cta':'Solicitar chef y staffing privado'},
 'fr':{'path':'/fr/chef-prive-personnel-villa-ibiza/','title':'Chef privé & personnel de villa à Ibiza | Ibiza VIP Move','desc':'Chef privé, majordomes, housekeeping et personnel de villa à Ibiza avec coordination discrète autour du séjour par Ibiza VIP Move.','kicker':'At Home · Ibiza','h1':'Chef privé et personnel de villa, coordonnés autour du séjour.','lead':'Les services en villa sont plus fluides lorsque horaires, profil des invités et besoins pratiques font partie du même brief.','section':'Le service en villa commence par un brief clair.','large':'Nous coordonnons les demandes de chef et de personnel selon le périmètre confirmé, la villa, les horaires et les besoins du séjour.','items':[('01','Besoins','Dates, invités, villa, horaires et type de support recherché.'),('02','Périmètre','Nous clarifions fonctions, timing et exigences avant toute confirmation.'),('03','Coordination','Les services confirmés peuvent être alignés avec villa, chauffeur, dining et itinéraire.'),('04','Changements','Si le séjour évolue, nous réexaminons le périmètre concerné selon disponibilité et conditions applicables.')],'cta':'Demander chef & personnel privé'},
 'de':{'path':'/de/privatkoch-villa-staff-ibiza/','title':'Privatkoch & Villa Staff Ibiza | Ibiza VIP Move','desc':'Privatkoch, Butler, Housekeeping und Villa Staff auf Ibiza mit diskreter Koordination rund um den Aufenthalt durch Ibiza VIP Move.','kicker':'At Home · Ibiza','h1':'Privatkoch und Villa Staff, rund um den Aufenthalt koordiniert.','lead':'Villa-Services funktionieren besser, wenn Zeiten, Gästeprofil und praktische Anforderungen Teil desselben Briefings sind.','section':'Villa-Service beginnt mit einem klaren Briefing.','large':'Wir koordinieren Anfragen für Koch und Personal passend zum bestätigten Umfang, zur Villa, zu den Zeiten und Anforderungen des Aufenthalts.','items':[('01','Bedarf','Daten, Gäste, Villa, Zeiten und gewünschte Unterstützung.'),('02','Umfang','Rollen, Timing und Anforderungen werden vor einer Bestätigung geklärt.'),('03','Koordination','Bestätigte Services können mit Villa, Chauffeur, Dining und Reiseroute abgestimmt werden.'),('04','Änderungen','Wenn sich der Aufenthalt verändert, prüfen wir betroffene Leistungen nach Verfügbarkeit und Bedingungen neu.')],'cta':'Privatkoch & Villa Staff anfragen'},
 'ar':{'path':'/ar/private-chef-staffing-ibiza/','title':'شيف خاص وطاقم فيلا في إيبيزا | Ibiza VIP Move','desc':'تنسيق شيف خاص وطاقم الفيلا وخدمات المنزل في إيبيزا حول الإقامة بشكل خاص عبر Ibiza VIP Move.','kicker':'At Home · إيبيزا','h1':'شيف خاص وطاقم فيلا ضمن تنسيق واحد للإقامة.','lead':'تكون خدمات الفيلا أكثر سلاسة عندما تكون المواعيد وملف الضيوف والاحتياجات العملية جزءاً من نفس الطلب.','section':'تبدأ خدمة الفيلا بتفاصيل واضحة.','large':'ننسق طلبات الشيف والطاقم وفق النطاق المؤكد والفيلا والمواعيد واحتياجات الإقامة.','items':[('01','الاحتياجات','التواريخ والضيوف والفيلا والمواعيد ونوع الدعم المطلوب.'),('02','النطاق','نوضح المهام والتوقيت والمتطلبات قبل تأكيد أي خدمة.'),('03','التنسيق','يمكن ربط الخدمات المؤكدة بالفيلا والسائق والمطاعم وبقية البرنامج.'),('04','التغييرات','عند تغير الإقامة نراجع النطاق المتأثر وفق التوفر والشروط المطبقة.')],'cta':'طلب شيف وطاقم خاص'}
},
'car':{
 'en':'/luxury-car-rental-ibiza/','image':'/assets/images/chauffeur.jpg','type':'Luxury car rental coordination in Ibiza',
 'es':{'path':'/es/alquiler-coches-lujo-ibiza/','title':'Alquiler de coches de lujo en Ibiza | Ibiza VIP Move','desc':'Coordinación de alquiler de coches de lujo, SUV y deportivos en Ibiza con entrega, recogida y logística alrededor de la estancia.','kicker':'Drive · Ibiza','h1':'Luxury car rental, coordinado alrededor de tu estancia.','lead':'La solicitud del vehículo, la entrega, la recogida y el timing se coordinan según el brief confirmado y la logística de la estancia.','section':'El vehículo correcto empieza por el uso real.','large':'Coordinamos solicitudes de rental según fechas, categoría, pasajeros, equipaje, ubicación y necesidades confirmadas. La disponibilidad depende del proveedor y del vehículo solicitado.','items':[('01','Vehicle brief','Fechas, categoría, conductores, pasajeros, equipaje y uso previsto.'),('02','Disponibilidad','Revisamos opciones adecuadas; modelo y categoría permanecen sujetos a disponibilidad y confirmación.'),('03','Entrega','La entrega o recogida puede coordinarse con villa, hotel o movimientos confirmados.'),('04','Cambios','Extensiones o cambios se revisan según disponibilidad y condiciones del proveedor.')],'cta':'Solicitar luxury car rental'},
 'fr':{'path':'/fr/location-voiture-luxe-ibiza/','title':'Location de voiture de luxe à Ibiza | Ibiza VIP Move','desc':'Coordination de location de voitures de luxe, SUV et sportives à Ibiza avec livraison, reprise et logistique autour du séjour.','kicker':'Drive · Ibiza','h1':'Luxury car rental, coordonné autour de votre séjour.','lead':'Demande du véhicule, livraison, reprise et timing sont coordonnés selon le brief confirmé et la logistique du séjour.','section':'Le bon véhicule commence par l’usage réel.','large':'Nous coordonnons les demandes selon dates, catégorie, conducteurs, passagers, bagages et besoins confirmés. La disponibilité dépend du fournisseur et du véhicule demandé.','items':[('01','Vehicle brief','Dates, catégorie, conducteurs, passagers, bagages et usage prévu.'),('02','Disponibilité','Nous examinons les options adaptées ; modèle et catégorie restent soumis à disponibilité et confirmation.'),('03','Livraison','Livraison ou reprise peuvent être coordonnées avec villa, hôtel ou mouvements confirmés.'),('04','Changements','Extensions ou modifications sont réexaminées selon disponibilité et conditions du fournisseur.')],'cta':'Demander un luxury car rental'},
 'de':{'path':'/de/luxusauto-mieten-ibiza/','title':'Luxusauto mieten auf Ibiza | Ibiza VIP Move','desc':'Koordination von Luxusauto-, SUV- und Sportwagenmiete auf Ibiza inklusive Übergabe, Rückgabe und Logistik rund um den Aufenthalt.','kicker':'Drive · Ibiza','h1':'Luxury Car Rental, rund um Ihren Aufenthalt koordiniert.','lead':'Fahrzeuganfrage, Übergabe, Rückgabe und Timing werden passend zum bestätigten Briefing und zur Aufenthaltslogistik abgestimmt.','section':'Das richtige Fahrzeug beginnt mit dem tatsächlichen Bedarf.','large':'Wir koordinieren Mietanfragen nach Daten, Kategorie, Fahrern, Passagieren, Gepäck und bestätigtem Bedarf. Verfügbarkeit hängt vom Anbieter und angefragten Fahrzeug ab.','items':[('01','Vehicle Brief','Daten, Kategorie, Fahrer, Passagiere, Gepäck und geplanter Einsatz.'),('02','Verfügbarkeit','Passende Optionen werden geprüft; Modell und Kategorie bleiben von Verfügbarkeit und Bestätigung abhängig.'),('03','Übergabe','Übergabe oder Rückgabe können mit Villa, Hotel oder bestätigten Bewegungen abgestimmt werden.'),('04','Änderungen','Verlängerungen oder Änderungen werden nach Verfügbarkeit und Anbieterbedingungen geprüft.')],'cta':'Luxury Car Rental anfragen'},
 'ar':{'path':'/ar/luxury-car-rental-ibiza/','title':'تأجير سيارات فاخرة في إيبيزا | Ibiza VIP Move','desc':'تنسيق تأجير السيارات الفاخرة وSUV والسيارات الرياضية في إيبيزا مع التسليم والاستلام واللوجستيات حول الإقامة.','kicker':'Drive · إيبيزا','h1':'تأجير سيارة فاخرة منسق حول إقامتك.','lead':'ننسق طلب السيارة والتسليم والاستلام والتوقيت وفق الطلب المؤكد ولوجستيات الإقامة.','section':'اختيار السيارة يبدأ من الاستخدام الفعلي.','large':'ننسق طلبات التأجير حسب التواريخ والفئة والسائقين والركاب والأمتعة والاحتياجات المؤكدة. ويعتمد التوفر على المورد والسيارة المطلوبة.','items':[('01','تفاصيل السيارة','التواريخ والفئة والسائقون والركاب والأمتعة والاستخدام المتوقع.'),('02','التوفر','نراجع الخيارات المناسبة؛ ويبقى الموديل والفئة خاضعين للتوفر والتأكيد.'),('03','التسليم','يمكن تنسيق التسليم أو الاستلام مع الفيلا أو الفندق أو التحركات المؤكدة.'),('04','التغييرات','تتم مراجعة التمديد أو التغييرات وفق التوفر وشروط المورد.')],'cta':'طلب سيارة فاخرة'}
},
'wellness':{
 'en':'/wellness-ibiza/','image':'/assets/images/wellness.jpg','type':'Private wellness coordination in Ibiza',
 'es':{'path':'/es/wellness-ibiza/','title':'Wellness privado en Ibiza | Ibiza VIP Move','desc':'Wellness privado en Ibiza con coordinación de masaje, trainers, yoga, beauty y sesiones en villa según disponibilidad y brief confirmado.','kicker':'Wellness · Ibiza','h1':'Wellness privado, integrado en el ritmo de la estancia.','lead':'Sesiones, ubicación y horarios pueden coordinarse alrededor del itinerario para evitar que el wellness se convierta en otra pieza aislada.','section':'El wellness funciona mejor cuando respeta el ritmo del día.','large':'Coordinamos solicitudes de bienestar y beauty con profesionales y proveedores según disponibilidad, ubicación y alcance confirmado. No sustituimos asesoramiento médico.','items':[('01','Preferencias','Tipo de sesión, huéspedes, ubicación, horario y preferencias relevantes.'),('02','Profesional','Revisamos opciones adecuadas según disponibilidad y alcance solicitado.'),('03','Timing','La sesión puede alinearse con villa, transporte y resto del itinerario confirmado.'),('04','Ajustes','Cambios de horario o alcance se revisan según disponibilidad del profesional.')],'cta':'Solicitar wellness privado'},
 'fr':{'path':'/fr/wellness-ibiza/','title':'Wellness privé à Ibiza | Ibiza VIP Move','desc':'Wellness privé à Ibiza avec coordination de massage, trainers, yoga, beauty et séances en villa selon disponibilité et brief confirmé.','kicker':'Wellness · Ibiza','h1':'Wellness privé, intégré au rythme du séjour.','lead':'Séances, lieu et horaires peuvent être coordonnés autour de l’itinéraire afin que le wellness ne devienne pas un élément isolé.','section':'Le wellness fonctionne mieux lorsqu’il respecte le rythme de la journée.','large':'Nous coordonnons les demandes wellness et beauty avec professionnels et prestataires selon disponibilité, lieu et périmètre confirmé. Nous ne remplaçons pas un avis médical.','items':[('01','Préférences','Type de séance, invités, lieu, horaire et préférences utiles.'),('02','Professionnel','Nous examinons les options adaptées selon disponibilité et périmètre demandé.'),('03','Timing','La séance peut être alignée avec villa, transport et itinéraire confirmé.'),('04','Ajustements','Les changements d’horaire ou de périmètre sont réexaminés selon la disponibilité du professionnel.')],'cta':'Demander un wellness privé'},
 'de':{'path':'/de/wellness-ibiza/','title':'Private Wellness auf Ibiza | Ibiza VIP Move','desc':'Private Wellness auf Ibiza mit Koordination von Massage, Trainern, Yoga, Beauty und Villa-Sessions nach Verfügbarkeit und bestätigtem Briefing.','kicker':'Wellness · Ibiza','h1':'Private Wellness, in den Rhythmus des Aufenthalts integriert.','lead':'Sessions, Ort und Zeiten können rund um die Reiseroute koordiniert werden, damit Wellness nicht als getrennte Planung läuft.','section':'Wellness funktioniert besser, wenn es zum Tagesrhythmus passt.','large':'Wir koordinieren Wellness- und Beauty-Anfragen mit Professionals und Anbietern nach Verfügbarkeit, Ort und bestätigtem Umfang. Dies ersetzt keine medizinische Beratung.','items':[('01','Präferenzen','Art der Session, Gäste, Ort, Zeit und relevante Wünsche.'),('02','Professional','Passende Optionen werden nach Verfügbarkeit und angefragtem Umfang geprüft.'),('03','Timing','Die Session kann mit Villa, Transport und bestätigter Reiseroute abgestimmt werden.'),('04','Anpassungen','Zeit- oder Umfangsänderungen werden nach Verfügbarkeit des Professionals geprüft.')],'cta':'Private Wellness anfragen'},
 'ar':{'path':'/ar/wellness-ibiza/','title':'Wellness خاص في إيبيزا | Ibiza VIP Move','desc':'تنسيق Wellness خاص في إيبيزا للمساج والمدربين واليوغا والجمال والجلسات في الفيلا حسب التوفر والطلب المؤكد.','kicker':'Wellness · إيبيزا','h1':'Wellness خاص منسق مع إيقاع الإقامة.','lead':'يمكن تنسيق الجلسة والموقع والمواعيد حول البرنامج حتى لا تصبح خدمات العافية جزءاً منفصلاً عن اليوم.','section':'تعمل خدمات العافية بشكل أفضل عندما تتناسب مع إيقاع اليوم.','large':'ننسق طلبات العافية والجمال مع المختصين والموردين وفق التوفر والموقع والنطاق المؤكد. ولا تحل هذه الخدمات محل الاستشارة الطبية.','items':[('01','التفضيلات','نوع الجلسة والضيوف والموقع والوقت والتفضيلات المهمة.'),('02','المختص','نراجع الخيارات المناسبة وفق التوفر والنطاق المطلوب.'),('03','التوقيت','يمكن ربط الجلسة بالفيلا والتنقل وبقية البرنامج المؤكد.'),('04','التعديلات','تتم مراجعة تغيير الوقت أو النطاق وفق توفر المختص.')],'cta':'طلب Wellness خاص'}
},
'events':{
 'en':'/private-events-ibiza/','image':'/assets/images/events.jpg','type':'Private event coordination in Ibiza',
 'es':{'path':'/es/eventos-privados-ibiza/','title':'Eventos privados en Ibiza | Ibiza VIP Move','desc':'Eventos y celebraciones privadas en Ibiza con coordinación de invitados, ubicación, proveedores, transporte y timing por Ibiza VIP Move.','kicker':'Occasions · Ibiza','h1':'Eventos privados, coordinados como un único brief.','lead':'Invitados, ubicación, transporte, proveedores y timing necesitan una misma línea operativa para que la experiencia sea coherente.','section':'Un evento privado es una suma de detalles conectados.','large':'Coordinamos solicitudes de eventos y celebraciones alrededor del alcance confirmado, trabajando con proveedores según disponibilidad, condiciones y necesidades del brief.','items':[('01','Event brief','Fecha, invitados, ocasión, ubicación, formato y prioridades.'),('02','Alcance','Aclaramos necesidades, proveedores y logística antes de confirmar elementos.'),('03','Operación','Transportes, accesos y servicios confirmados pueden alinearse alrededor del timing del evento.'),('04','Evolución','Los cambios se revisan con las partes afectadas según disponibilidad y condiciones aplicables.')],'cta':'Solicitar evento privado'},
 'fr':{'path':'/fr/evenements-prives-ibiza/','title':'Événements privés à Ibiza | Ibiza VIP Move','desc':'Événements et célébrations privées à Ibiza avec coordination des invités, lieu, prestataires, transport et timing par Ibiza VIP Move.','kicker':'Occasions · Ibiza','h1':'Événements privés, coordonnés comme un seul brief.','lead':'Invités, lieu, transport, prestataires et timing nécessitent une même ligne opérationnelle pour maintenir une expérience cohérente.','section':'Un événement privé est une somme de détails connectés.','large':'Nous coordonnons les demandes d’événements et célébrations autour du périmètre confirmé, avec des prestataires selon disponibilité, conditions et besoins du brief.','items':[('01','Event brief','Date, invités, occasion, lieu, format et priorités.'),('02','Périmètre','Nous clarifions besoins, prestataires et logistique avant de confirmer les éléments.'),('03','Opération','Transport, accès et services confirmés peuvent être alignés autour du timing de l’événement.'),('04','Évolution','Les changements sont réexaminés avec les parties concernées selon disponibilité et conditions applicables.')],'cta':'Demander un événement privé'},
 'de':{'path':'/de/private-events-ibiza/','title':'Private Events auf Ibiza | Ibiza VIP Move','desc':'Private Events und Feiern auf Ibiza mit Koordination von Gästen, Location, Anbietern, Transport und Timing durch Ibiza VIP Move.','kicker':'Occasions · Ibiza','h1':'Private Events, als ein gemeinsames Briefing koordiniert.','lead':'Gäste, Location, Transport, Anbieter und Timing brauchen eine gemeinsame operative Linie für ein stimmiges Erlebnis.','section':'Ein privates Event besteht aus verbundenen Details.','large':'Wir koordinieren Event- und Feier-Anfragen rund um den bestätigten Umfang mit Anbietern nach Verfügbarkeit, Bedingungen und Anforderungen des Briefings.','items':[('01','Event Brief','Datum, Gäste, Anlass, Location, Format und Prioritäten.'),('02','Umfang','Bedarf, Anbieter und Logistik werden vor Bestätigungen geklärt.'),('03','Operation','Bestätigte Transporte, Access und Services können am Event-Timing ausgerichtet werden.'),('04','Entwicklung','Änderungen werden mit betroffenen Parteien nach Verfügbarkeit und Bedingungen neu geprüft.')],'cta':'Private Event anfragen'},
 'ar':{'path':'/ar/private-events-ibiza/','title':'فعاليات خاصة في إيبيزا | Ibiza VIP Move','desc':'تنسيق الفعاليات والاحتفالات الخاصة في إيبيزا للضيوف والموقع والموردين والتنقل والتوقيت عبر Ibiza VIP Move.','kicker':'Occasions · إيبيزا','h1':'فعالية خاصة ضمن طلب وتشغيل واحد.','lead':'الضيوف والموقع والتنقل والموردون والتوقيت تحتاج إلى خط تشغيلي واحد حتى تبقى التجربة مترابطة.','section':'الفعالية الخاصة مجموعة من التفاصيل المترابطة.','large':'ننسق طلبات الفعاليات والاحتفالات حول النطاق المؤكد ومع الموردين وفق التوفر والشروط واحتياجات الطلب.','items':[('01','تفاصيل الفعالية','التاريخ والضيوف والمناسبة والموقع والشكل والأولويات.'),('02','النطاق','نوضح الاحتياجات والموردين واللوجستيات قبل تأكيد العناصر.'),('03','التشغيل','يمكن ربط التنقل والوصول والخدمات المؤكدة بتوقيت الفعالية.'),('04','التغييرات','تتم مراجعة التغييرات مع الأطراف المتأثرة وفق التوفر والشروط المطبقة.')],'cta':'طلب فعالية خاصة'}
},
'bespoke':{
 'en':'/bespoke-concierge-ibiza/','image':'/assets/images/bespoke.jpg','type':'Bespoke private concierge coordination in Ibiza',
 'es':{'path':'/es/concierge-a-medida-ibiza/','title':'Concierge a medida en Ibiza | Ibiza VIP Move','desc':'Concierge a medida en Ibiza para solicitudes privadas que requieren sourcing, coordinación y seguimiento fuera de categorías estándar.','kicker':'Bespoke · Ibiza','h1':'Para lo que no encaja en una categoría.','lead':'Algunas solicitudes necesitan más contexto que un formulario estándar. Las tratamos como un brief privado, definiendo alcance y viabilidad antes de coordinar.','section':'Bespoke significa empezar por la necesidad, no por el catálogo.','large':'Revisamos solicitudes especiales dentro de un marco legal, seguro y viable, aclarando alcance, disponibilidad y condiciones antes de cualquier confirmación.','items':[('01','Solicitud','Explícanos qué necesitas, para quién, cuándo y en qué contexto.'),('02','Viabilidad','Aclaramos alcance, disponibilidad, restricciones y próximos pasos.'),('03','Coordinación','Los elementos confirmados se conectan con el resto del itinerario cuando corresponde.'),('04','Privacidad','La información se mantiene limitada a las personas necesarias para gestionar la solicitud confirmada.')],'cta':'Enviar solicitud a medida'},
 'fr':{'path':'/fr/conciergerie-sur-mesure-ibiza/','title':'Conciergerie sur mesure à Ibiza | Ibiza VIP Move','desc':'Conciergerie sur mesure à Ibiza pour demandes privées nécessitant sourcing, coordination et suivi hors catégories standard.','kicker':'Bespoke · Ibiza','h1':'Pour ce qui ne rentre pas dans une catégorie.','lead':'Certaines demandes ont besoin de plus de contexte qu’un formulaire standard. Nous les traitons comme un brief privé, en définissant périmètre et faisabilité avant coordination.','section':'Bespoke signifie partir du besoin, pas du catalogue.','large':'Nous examinons les demandes spéciales dans un cadre légal, sûr et réalisable, en clarifiant périmètre, disponibilité et conditions avant toute confirmation.','items':[('01','Demande','Expliquez le besoin, pour qui, quand et dans quel contexte.'),('02','Faisabilité','Nous clarifions périmètre, disponibilité, restrictions et prochaines étapes.'),('03','Coordination','Les éléments confirmés sont reliés au reste de l’itinéraire lorsque cela est pertinent.'),('04','Confidentialité','Les informations restent limitées aux personnes nécessaires pour gérer la demande confirmée.')],'cta':'Envoyer une demande sur mesure'},
 'de':{'path':'/de/bespoke-concierge-ibiza/','title':'Bespoke Concierge auf Ibiza | Ibiza VIP Move','desc':'Bespoke Concierge auf Ibiza für private Anforderungen, die Sourcing, Koordination und Betreuung außerhalb standardisierter Kategorien benötigen.','kicker':'Bespoke · Ibiza','h1':'Für Anforderungen außerhalb einer Standardkategorie.','lead':'Manche Anfragen brauchen mehr Kontext als ein Standardformular. Wir behandeln sie als privates Briefing und klären Umfang und Machbarkeit vor der Koordination.','section':'Bespoke beginnt beim Bedarf, nicht beim Katalog.','large':'Wir prüfen besondere Anfragen in einem legalen, sicheren und realisierbaren Rahmen und klären Umfang, Verfügbarkeit und Bedingungen vor Bestätigungen.','items':[('01','Anfrage','Beschreiben Sie Bedarf, Person, Zeitpunkt und Kontext.'),('02','Machbarkeit','Umfang, Verfügbarkeit, Einschränkungen und nächste Schritte werden geklärt.'),('03','Koordination','Bestätigte Elemente werden, wenn sinnvoll, mit der restlichen Reiseroute verbunden.'),('04','Privatsphäre','Informationen bleiben auf Personen beschränkt, die für die bestätigte Anfrage notwendig sind.')],'cta':'Bespoke Anfrage senden'},
 'ar':{'path':'/ar/bespoke-concierge-ibiza/','title':'كونسيرج مخصص في إيبيزا | Ibiza VIP Move','desc':'كونسيرج مخصص في إيبيزا للطلبات الخاصة التي تحتاج إلى sourcing وتنسيق ومتابعة خارج الفئات المعتادة.','kicker':'Bespoke · إيبيزا','h1':'للطلبات التي لا تنتمي إلى فئة واحدة.','lead':'بعض الطلبات تحتاج إلى سياق أكبر من نموذج عادي. نتعامل معها كطلب خاص ونوضح النطاق والإمكانية قبل التنسيق.','section':'الخدمة المخصصة تبدأ من الحاجة وليس من القائمة.','large':'نراجع الطلبات الخاصة ضمن إطار قانوني وآمن وقابل للتنفيذ، مع توضيح النطاق والتوفر والشروط قبل أي تأكيد.','items':[('01','الطلب','اشرح ما تحتاجه ولمن ومتى وفي أي سياق.'),('02','الإمكانية','نوضح النطاق والتوفر والقيود والخطوات التالية.'),('03','التنسيق','يتم ربط العناصر المؤكدة ببقية البرنامج عندما يكون ذلك مناسباً.'),('04','الخصوصية','تبقى المعلومات ضمن الأشخاص الضروريين لإدارة الطلب المؤكد.')],'cta':'إرسال طلب مخصص'}
}}


def alternates(service):
    tags=f'<link rel="alternate" hreflang="en" href="{BASE}{service["en"]}">'
    for lang in ('es','fr','de','ar'):
        tags+=f'<link rel="alternate" hreflang="{lang}" href="{BASE}{service[lang]["path"]}">'
    return tags+f'<link rel="alternate" hreflang="x-default" href="{BASE}{service["en"]}">'


def main_html(data,image):
    process=''.join(f'<article><span>{n}</span><h3>{escape(h)}</h3><p>{escape(p)}</p></article>' for n,h,p in data['items'])
    return f'''<main id="main-content"><section class="page-hero"><div class="page-hero-media"><img src="{image}" alt="{escape(data['h1'])} — Ibiza VIP Move" width="1800" height="1200" fetchpriority="high" decoding="async"></div><div><div class="kicker light">{escape(data['kicker'])}</div><h1>{escape(data['h1'])}</h1><p>{escape(data['lead'])}</p><a class="btn gold" href="{WA}">{escape(data['cta'])}</a></div></section><section class="editorial"><div><div class="kicker dark">Ibiza VIP Move</div><h2>{escape(data['section'])}</h2></div><div><p class="large">{escape(data['large'])}</p></div></section><section class="process"><div class="section-head"><div class="kicker dark">Private coordination</div><h2>{escape(data['section'])}</h2></div><div class="process-grid">{process}</div></section><section class="closing-simple"><h2>{escape(data['cta'])}</h2><p>Ibiza VIP Move · Private client support · Ibiza</p><a class="btn dark" href="{WA}">{escape(data['cta'])}</a></section></main>'''


def service_schema(lang,data,service):
    return {'@context':'https://schema.org','@type':'Service','name':data['h1'],'serviceType':service['type'],'url':BASE+data['path'],'inLanguage':lang,'provider':{'@id':ORG},'areaServed':{'@type':'Place','name':'Ibiza, Balearic Islands, Spain'},'image':BASE+service['image']}


def breadcrumb_schema(lang,data):
    hub=HUBS[lang]
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ibiza VIP Move','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Services','item':BASE+hub},{'@type':'ListItem','position':3,'name':data['h1'],'item':BASE+data['path']}]}


def update_schemas(html,lang,data,service):
    seen={'web':False,'service':False,'bread':False}
    def repl(m):
        try:o=json.loads(m.group(1))
        except Exception:return m.group(0)
        if not isinstance(o,dict):return m.group(0)
        typ=o.get('@type')
        if typ in ('WebPage','AboutPage','CollectionPage') and not seen['web']:
            o['@type']='WebPage';o['name']=data['title'];o['url']=BASE+data['path'];o['description']=data['desc'];o['inLanguage']=lang;o['about']={'@id':ORG};o['publisher']={'@id':ORG};o['primaryImageOfPage']={'@type':'ImageObject','url':BASE+service['image']};seen['web']=True
        elif typ=='Service':o=service_schema(lang,data,service);seen['service']=True
        elif typ=='BreadcrumbList':o=breadcrumb_schema(lang,data);seen['bread']=True
        return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
    html=SCRIPT_RE.sub(repl,html)
    additions=[]
    if not seen['service']:additions.append(service_schema(lang,data,service))
    if not seen['bread']:additions.append(breadcrumb_schema(lang,data))
    if additions:html=html.replace('</head>',''.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>' for o in additions)+'</head>',1)
    return html


def set_meta(html,attr,key,value):
    pat=rf'(<meta\s+{attr}="{re.escape(key)}"\s+content=")[^"]*(")'
    if re.search(pat,html,re.I):return re.sub(pat,lambda m:m.group(1)+escape(value)+m.group(2),html,count=1,flags=re.I)
    return html.replace('</head>',f'<meta {attr}="{key}" content="{escape(value)}"></head>',1)

created=[]
for key,service in SERVICES.items():
    tags=alternates(service)
    for lang in ('es','fr','de','ar'):
        data=service[lang];source=SOURCES[lang]
        if not source.exists():raise SystemExit(f'Phase 60 source missing: {lang}')
        html=source.read_text(encoding='utf-8');canonical=BASE+data['path']
        html=re.sub(r'<title>.*?</title>',f'<title>{escape(data["title"])}</title>',html,count=1,flags=re.I|re.S)
        html=re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")',lambda m:m.group(1)+escape(data['desc'])+m.group(2),html,count=1,flags=re.I)
        html=re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")',lambda m:m.group(1)+canonical+m.group(2),html,count=1,flags=re.I)
        html=re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">','',html,flags=re.I)
        for prop,val in [('og:title',data['title']),('og:description',data['desc']),('og:url',canonical),('og:image',BASE+service['image'])]:html=set_meta(html,'property',prop,val)
        for name,val in [('twitter:title',data['title']),('twitter:description',data['desc']),('twitter:image',BASE+service['image'])]:html=set_meta(html,'name',name,val)
        html=re.sub(r'<main\b[^>]*>.*?</main>',main_html(data,service['image']),html,count=1,flags=re.I|re.S)
        html=update_schemas(html,lang,data,service)
        html=html.replace('</head>',tags+'</head>',1)
        dest=ROOT/data['path'].strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8')
        created.append((key,lang,data['path'],service['image']))
    # Reciprocal hreflang on English canonical.
    en=ROOT/service['en'].strip('/')/'index.html'
    if not en.exists():raise SystemExit(f'Phase 60 English service missing: {key}')
    h=en.read_text(encoding='utf-8');h=re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+">','',h,flags=re.I);h=h.replace('</head>',tags+'</head>',1);en.write_text(h,encoding='utf-8')

# Localized hub visible links + Phase 58 ItemList only. Corporate OfferCatalog remains canonical English.
for lang,hub in HUBS.items():
    file=ROOT/hub.strip('/')/'index.html';html=file.read_text(encoding='utf-8')
    relmap={service['en']:service[lang]['path'] for service in SERVICES.values()}
    for en_path,local_path in relmap.items():html=html.replace(f'href="{en_path}"',f'href="{local_path}"')
    def hub_schema(m):
        try:o=json.loads(m.group(1))
        except Exception:return m.group(0)
        if isinstance(o,dict) and o.get('@type')=='CollectionPage':
            main=o.get('mainEntity')
            if isinstance(main,dict) and main.get('@type')=='ItemList':
                for item in main.get('itemListElement',[]):
                    if isinstance(item,dict):
                        for en_path,local_path in relmap.items():
                            if item.get('url')==BASE+en_path:item['url']=BASE+local_path
        return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
    html=SCRIPT_RE.sub(hub_schema,html);file.write_text(html,encoding='utf-8')

# Main sitemap.
sitemap=ROOT/'sitemap.xml';ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9');tree=ET.parse(sitemap);root=tree.getroot();ns='http://www.sitemaps.org/schemas/sitemap/0.9';existing={u.find(f'{{{ns}}}loc').text for u in root.findall(f'{{{ns}}}url') if u.find(f'{{{ns}}}loc') is not None}
for _,_,path,_ in created:
    url=BASE+path
    if url not in existing:
        u=ET.SubElement(root,f'{{{ns}}}url');ET.SubElement(u,f'{{{ns}}}loc').text=url;ET.SubElement(u,f'{{{ns}}}lastmod').text=TODAY;ET.SubElement(u,f'{{{ns}}}changefreq').text='monthly';ET.SubElement(u,f'{{{ns}}}priority').text='0.72'
tree.write(sitemap,encoding='utf-8',xml_declaration=True)

# Image sitemap.
imgmap=ROOT/'image-sitemap.xml'
if imgmap.exists():
    SM='http://www.sitemaps.org/schemas/sitemap/0.9';IMG='http://www.google.com/schemas/sitemap-image/1.1';ET.register_namespace('',SM);ET.register_namespace('image',IMG);it=ET.parse(imgmap);ir=it.getroot();iex={u.find(f'{{{SM}}}loc').text for u in ir.findall(f'{{{SM}}}url') if u.find(f'{{{SM}}}loc') is not None}
    for _,_,path,image in created:
        url=BASE+path
        if url not in iex:
            u=ET.SubElement(ir,f'{{{SM}}}url');ET.SubElement(u,f'{{{SM}}}loc').text=url;im=ET.SubElement(u,f'{{{IMG}}}image');ET.SubElement(im,f'{{{IMG}}}loc').text=BASE+image
    it.write(imgmap,encoding='utf-8',xml_declaration=True)

# Validation.
assert len(created)==20
for key,lang,path,image in created:
    service=SERVICES[key];html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    assert html.count('<h1')==1,(key,lang,'h1')
    assert 'id="main-content"' in html and 'ivm-skip-link' in html,(key,lang,'a11y')
    assert BASE+path in html and image in html,(key,lang,'canonical/image')
    assert '"@type": "Service"' in html and 'BreadcrumbList' in html,(key,lang,'schema')
    for l in ('en','es','fr','de','ar'):assert f'hreflang="{l}"' in html,(key,lang,l)
for lang,hub in HUBS.items():
    html=(ROOT/hub.strip('/')/'index.html').read_text(encoding='utf-8')
    collection=None
    for m in SCRIPT_RE.finditer(html):
        try:o=json.loads(m.group(1))
        except Exception:continue
        if isinstance(o,dict) and o.get('@type')=='CollectionPage':collection=o
    assert collection,(lang,'CollectionPage')
    item_urls={x.get('url') for x in collection['mainEntity']['itemListElement'] if isinstance(x,dict)}
    for service in SERVICES.values():
        local=service[lang]['path'];assert f'href="{local}"' in html,(lang,local,'visible hub');assert BASE+local in item_urls,(lang,local,'ItemList')
print('PASS: Phase 60 created 20 localized lifestyle service pages and localized all extended Services hub links')
