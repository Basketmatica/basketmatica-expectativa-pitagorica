# ¿Suerte o habilidad? Cuántas victorias merece cada equipo de la ACB

BAXI Manresa ganó 16 partidos en la liga regular 2025/26. Sus puntos a favor y en contra eran los de un equipo de unas 12,7 victorias. Es el mayor desvío positivo de la temporada: **+3,3 victorias** sobre lo esperado. En el otro extremo, Coviran Granada se quedó seis victorias cuando sus puntos valían 8,6.

La pregunta es qué hay detrás. ¿Ganar por encima de lo que dicen tus puntos es una habilidad que se repite, de esos equipos que saben cerrar los finales, o es ruido de 34 partidos?

Para responderla no basta una temporada, así que usé ocho. Y antes de decirte lo que salió, una advertencia: este artículo **no tiene titular de «+N victorias»**. Fijé una regla antes de mirar y el desvío de Manresa, como verás, cae dentro de lo que el azar produce solo.

## Qué es la expectativa pitagórica

Bill James observó en el béisbol que el balance de un equipo se parece mucho a la proporción de carreras que anota frente a las que encaja:

> % de victorias esperado = PF^k / (PF^k + PC^k)

donde PF son los puntos a favor, PC los puntos en contra y k un exponente. En béisbol k ronda 2. Daryl Morey adaptó la idea al baloncesto y el valor que se cita para la NBA es k ≈ 14.

¿Por qué tan alto? Porque en baloncesto hay muchas posesiones por partido: cada una es un pequeño sorteo y, con tantos, el mejor equipo gana con más regularidad que en béisbol. Una ventaja pequeña de puntos se traduce en muchas victorias. Es una intuición, no una demostración.

Que en la ACB el exponente salga distinto de 14 era **una hipótesis**: la liga juega 40 minutos y no 48, tiene otro ritmo y otra dispersión de niveles. La comprobaremos con datos.

Con k, las **victorias esperadas** son los partidos jugados por el porcentaje pitagórico, y el **desvío** es la diferencia entre victorias reales y esperadas. Todos los desvíos se expresan por 34 partidos.

## Datos y reglas fijadas de antemano

Uso la liga regular ACB de las temporadas 2017/18 a 2025/26, **salvo la 2019/20**, suspendida por la pandemia: quedó con 229 partidos y equipos con entre 22 y 27 jugados, no es una liga completa. Quedan **8 temporadas y 145 equipos-temporada de 24 clubes**. Sin playoffs, Copa ni Supercopa. Tres detalles:

- **2020/21** tuvo 19 equipos y 36 partidos cada uno. Trabajo con porcentajes y lo expreso por 34. Como comprobación, repito todo sin ella.
- **Los clubes cambian de nombre con el patrocinador.** Emparejo por franquicia: Montakit, Urbas, Baloncesto y Carplus Fuenlabrada son el mismo club; igual Barça Lassa y FC Barcelona, Delteco y Acunsa GBC, y Monbus Obradoiro y Leyma Basquet Coruña.
- Los puntos de las prórrogas cuentan.

Las reglas están fijadas por escrito en dos documentos con fecha. El primero ([`c0c12be`](../docs/preregistro.md)) es anterior a cualquier cálculo y solo contemplaba la 25/26. El segundo ([`8d42f05`](../docs/preregistro_v2.md)) se escribió al disponer de las demás temporadas y antes de calcular nada con ellas. Debo decir dos cosas sobre él: para entonces ya conocía el resultado de la 25/26 con una sola temporada, y cambié una regla por lo que vi entonces (te lo cuento en la sección 6). Ambas cosas están declaradas en el propio documento. Las reglas:

- **k se calibra sin la temporada que se evalúa.** El desvío de cada temporada se mide con un k ajustado con las otras siete.
- **Test principal:** correlación entre el desvío de un equipo en una temporada y el de la siguiente, con intervalo de confianza al 90 % por bootstrap sobre clubes enteros.
- **Regla de decisión:** «hay señal de habilidad» solo si el límite inferior de ese intervalo supera 0. Si no, «compatible con el azar».
- **Partido igualado:** margen de 5 puntos o menos, o prórroga. Solo se usa para describir.
- **Titular «+N victorias»:** solo si ese desvío queda fuera de la banda del azar.

## Calibrar k para la ACB

El k que mejor ajusta las ocho temporadas es **10,7**, con un intervalo al 90 % de **10,3 a 11,4** (bootstrap de partidos).

![Error medio frente a k](../outputs/figuras/fig1_curva_k.png)

Que no sea 14 se sostiene en la validación fuera de muestra. Dejando cada temporada fuera, el k de las otras siete tiene un error medio de **1,53 victorias por equipo**, frente a **1,81** con el 14 de la NBA, y gana en 6 de las 8 temporadas. Se cumplen mis dos criterios pre-registrados (el intervalo excluye el 14 y gana en al menos 5 de 8): **el exponente de la ACB es menor que el de la NBA**. Hay un matiz honesto: el k de cada temporada por separado va de 9,2 a 12,2, más disperso de lo que sugiere el intervalo, y en la 25/26 el 14 rindió algo mejor (1,55 frente a 1,59). Usa 10,7 como valor central, no como constante de la naturaleza.

## La 25/26, equipo por equipo

La tabla recoge victorias reales, esperadas con el k calibrado sin la 25/26 (10,6) y desvío. La **banda del azar** viene de simular 10.000 temporadas partido a partido sobre el calendario real: la probabilidad de cada partido sale de la fuerza pitagórica de ambos equipos (log5) y de la ventaja de campo observada. La banda es del percentil 5 al 95.

| Equipo | V | Esperadas | Desvío | Banda del azar (90 %) |
|---|---:|---:|---:|---:|
| Manresa | 16 | 12,7 | +3,3 | 9 – 18 |
| Bilbao | 19 | 15,8 | +3,2 | 11 – 20 |
| Real Madrid | 26 | 24,1 | +1,9 | 19 – 28 |
| Lleida | 12 | 10,1 | +1,9 | 7 – 15 |
| Baskonia | 25 | 23,3 | +1,7 | 19 – 27 |
| Murcia | 25 | 23,7 | +1,3 | 19 – 27 |
| Joventut | 22 | 21,3 | +0,7 | 17 – 25 |
| Girona | 14 | 13,7 | +0,3 | 10 – 18 |
| Barça | 24 | 23,7 | +0,3 | 19 – 27 |
| Breogán | 15 | 14,8 | +0,2 | 11 – 19 |
| Unicaja | 17 | 17,7 | −0,7 | 13 – 22 |
| Zaragoza | 10 | 11,0 | −1,0 | 7 – 16 |
| Andorra | 10 | 11,6 | −1,6 | 8 – 16 |
| Gran Canaria | 10 | 11,9 | −1,9 | 8 – 17 |
| Tenerife | 18 | 20,0 | −2,0 | 15 – 24 |
| Burgos | 12 | 14,0 | −2,0 | 10 – 19 |
| Valencia | 25 | 27,1 | −2,1 | 23 – 30 |
| Granada | 6 | 8,6 | −2,6 | 5 – 13 |

![Desvío de cada equipo con la banda del azar](../outputs/figuras/fig2_desvios.png)

**Ningún equipo queda fuera de la banda.** Por la regla fijada, no hay titular de «+N victorias»: el desvío de Manresa es compatible con el azar. En las ocho temporadas, solo 2 de 145 equipos-temporada salieron de su banda (el 10 % nominal serían unos 14). Esa escasez no es un hallazgo: la banda es conservadora por construcción (lo explico en la sección 6).

Los partidos igualados, como **descripción y no como explicación**: Manresa fue 6-4, Bilbao 8-5 y Lleida 4-4; Valencia 5-3 y Tenerife 5-7. Entre equipos, el desvío y el balance en igualados se parecen (correlación de 0,69), lo esperable porque el desvío se construye precisamente con victorias que los puntos no explican. No dice si esos finales se ganan por saber o por suerte.

## ¿Se repite?

Si ganar por encima de los puntos fuera una habilidad, los equipos con desvío positivo un año deberían repetirlo al siguiente.

![Desvío de un año frente al siguiente](../outputs/figuras/fig3_pares.png)

Con las ocho temporadas hay **99 pares** (el mismo club en dos temporadas consecutivas completas). La correlación es **r = 0,05**, con un intervalo al 90 % de **−0,11 a +0,20**. La pendiente dice lo mismo: de cada victoria de desvío, **se mantiene alrededor de 0,05**. El patrón por pasos de temporada no ayuda a ver señal: las seis correlaciones van de −0,27 a +0,27, con 16-17 pares cada una, es decir, ruido. Sin la 2020/21, r = 0,02 (−0,18 a 0,20).

**Decisión pre-registrada:** el límite inferior del intervalo (−0,11) no supera 0. La conclusión es:

> Con ocho temporadas de la ACB no se detecta que el desvío se repita de una temporada a la siguiente. Con esta muestra, un efecto de tamaño moderado (r ≈ 0,25 o más) habría sido detectado con alta probabilidad, así que es improbable que exista; un efecto pequeño no se puede descartar.

Dos lecturas más, sin regla de decisión. **Los finales:** el % de victorias en partidos igualados de un año frente al siguiente da r = 0,13 (−0,07 a +0,30), también compatible con cero, aunque el intervalo no excluye un efecto pequeño. **La 25/26 por vueltas:** el desvío de la primera mitad frente al de la segunda, r = −0,01.

Una explicación sobre el cambio de regla. En el primer pre-registro había un segundo test: comparar la dispersión de los desvíos con la de temporadas simuladas por azar. Salió muy por debajo del azar en la 25/26 (p = 0,96), y al repetirlo en las ocho sale igual en todas: la dispersión observada es de 1,7 a 2,1 victorias frente a 2,6 simulado. Ese patrón constante revela una limitación del test: la fuerza de cada equipo en la simulación sale de los mismos puntos, que ya contienen parte de la suerte, así que los desvíos observados quedan comprimidos sea cual sea la realidad. Lo saqué de la regla de decisión (lo declaré en el segundo pre-registro, motivado por haber visto ese resultado) y lo dejé como dato descriptivo. Es la razón por la que la banda del azar es conservadora.

## Qué significa y qué no

Que los finales se entrenan es una evidencia: hay jugadas específicas, decisiones de tiempos muertos y gestión de faltas. Los entrenadores trabajan eso y este análisis no dice lo contrario. Dice algo más estrecho: **si ese trabajo deja huella en el balance, es pequeña o no la detectamos con 99 pares**.

Sospechaba que el **NetRtg** (diferencial por 100 posesiones) predeciría mejor que los puntos brutos. Con los datos de un año, la correlación con el % de victorias del siguiente es de 0,74 para el % de victorias, 0,73 para el pitagórico y 0,73 para el NetRtg.

![Capacidad predictiva de un año sobre el siguiente](../outputs/figuras/fig4_prediccion.png)

Las diferencias entre ellos son de una o dos centésimas, con intervalos que incluyen el cero. **No puedo decir que el NetRtg, ni el pitagórico, predigan mejor que el balance de victorias.** Mi interpretación, que no he contrastado: el nivel de los equipos y el cambio de plantilla pesan mucho más que el ruido de unas dos victorias por temporada, y ese ruido es lo único que corregirían el pitagórico o el NetRtg.

Limitaciones:

- **99 pares y ocho temporadas.** Un efecto de r ≈ 0,1 sigue sin ser detectable.
- **Plantillas y entrenadores cambian** de un año a otro; es parte de por qué no hay persistencia que medir.
- **k es heterogéneo entre temporadas** (9,2 a 12,2) y está estimado con partidos, no con calendarios distintos.
- **Una enmienda tras ver resultados.** El cambio descrito arriba es reconocible y está declarado, pero no deja de ser un cambio.
- **Posesiones estimadas** con la fórmula estándar, no contadas.
- **Datos:** la 2019/20 queda fuera y la 2020/21 es atípica (19 equipos).

## Predicción para la 26/27

Si el desvío fuera sobre todo ruido, lo esperable es que los equipos se acerquen a lo que dicen sus puntos. Con la pendiente medida (0,05), espero que se mantenga solo un 5 % del desvío de la 25/26 y que el resto se corrija. Con datos hasta la 25/26:

- **Deberían bajar hacia sus puntos:** Manresa (de 16 victorias a unas 12,7), Bilbao (de 19 a 15,8), Real Madrid (de 26 a 24,1) y Lleida (de 12 a 10,1).
- **Deberían subir:** Granada (de 6 a 8,6), Valencia (de 25 a 27,1), Burgos (de 12 a 14,0) y Tenerife (de 18 a 20,0).

Con una salvedad importante: eso describe la distancia entre victorias y puntos de la 25/26, no un pronóstico de la 26/27, porque las plantillas cambian. Lo revisaré en enero con el mismo método, sin retocarlo.

## Recurso y código

La tabla de victorias esperadas de las ocho temporadas (145 equipos-temporada, con sus bandas) está en CSV: [PENDIENTE: enlace a la entrega en la newsletter de Basketmática].

El código completo es público y reproducible, con los datos de partido incluidos: [repositorio en GitHub, PENDIENTE: URL]. El notebook (`notebooks/metodo.ipynb`) reproduce las cifras de este artículo y los dos pre-registros están en `docs/`. Las clasificaciones y los resultados de partido son datos públicos.
