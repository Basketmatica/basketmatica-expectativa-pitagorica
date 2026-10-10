# Pre-registro v2: ocho temporadas de la ACB

Enmienda al [pre-registro v1](preregistro.md) (commit `c0c12be`), que se conserva intacto. Este documento se commitea **antes** de calcular ningún exponente, desvío, correlación ni simulación sobre las temporadas añadidas.

## Transparencia

- **Lo que se ha visto de la 25/26:** todos los resultados del análisis v1 (k = 11,27 ajustado in-sample; ningún equipo fuera de la banda; r entre vueltas = −0,02; p = 0,96 en el test de varianza).
- **Lo que se ha visto de las temporadas nuevas (2017/18 a 2024/25):** solo comprobaciones estructurales: número de filas, partidos y partidos por equipo, nulos, empates, coherencia local/visitante, nombres de equipo y número de pares equipo-temporada. **No se ha calculado ningún pitagórico, k, desvío, correlación ni simulación sobre ellas.**

## Qué cambia respecto a v1, y por qué

1. **k se calibra sin la temporada que se evalúa.** El brief original ya lo exigía («k se calibra sin la 25/26»), y v1 no podía cumplirlo por falta de datos. Ahora la 25/26 se evalúa con un k calibrado solo con las temporadas anteriores.
2. **El test principal pasa a ser entre temporadas (t → t+1)**, que es el que planteaba el brief. Las mitades de v1 se conservan solo como lectura descriptiva de la 25/26.
3. **El test de varianza (test B de v1) deja de formar parte de la regla de decisión.** Motivo, detectado al ver los resultados de v1: la fuerza de cada equipo en la simulación se estima con los mismos puntos de la temporada, que ya contienen parte de la suerte. Eso encoge los desvíos observados frente a los simulados y hace el test conservador por construcción, sea cual sea la realidad. Este cambio **está motivado por haber visto el resultado de v1** y se declara como tal. El test se sigue calculando, de forma descriptiva y con esa advertencia.

El resultado de v1 (compatible con el azar en la 25/26 con datos de una sola temporada) se mantiene como resultado histórico y se menciona en el artículo.

## Datos

- Liga regular ACB, temporadas 2017/18 a 2025/26 (9 ficheros en `data/`). Sin playoffs, Copa ni Supercopa.
- **Excluida: 2019/20.** Suspendida por la pandemia, 229 partidos, equipos con 22 a 27 partidos jugados. No es una liga completa.
- **Incluida con tasas: 2020/21.** 19 equipos y 36 partidos por equipo, no 34. Se trabaja con porcentajes (por partido); las victorias esperadas se expresan por 34 partidos para comparar entre temporadas. Como sensibilidad, todo se repite sin 2020/21.
- **Franquicias.** Los equipos se emparejan entre temporadas por club, no por nombre de patrocinador: Montakit / Urbas / Baloncesto / Carplus Fuenlabrada; Barça Lassa = FC Barcelona; Delteco / Acunsa GBC; Monbus Obradoiro / Leyma Basquet Coruña.
- **Temporadas utilizables: 8** (2017/18, 2018/19, 2020/21, 2021/22, 2022/23, 2023/24, 2024/25, 2025/26).
- **Pares consecutivos t → t+1 con la misma franquicia en ambas:** 99 (16 en 2017/18→2018/19, 17 en 2020/21→2021/22, 16 en 2021/22→2022/23, 16 en 2022/23→2023/24, 17 en 2023/24→2024/25, 17 en 2024/25→2025/26). Los pasos 2018/19→2019/20 y 2019/20→2020/21 no cuentan; 2018/19→2020/21 tampoco se une.

## Definiciones (sin cambios salvo lo indicado)

- **Pitagórico:** `PF^k / (PF^k + PC^k)`. **Desvío** de un equipo-temporada: % de victorias − % pitagórico (se muestra ×34 como «victorias»).
- **k de una temporada s (k_{−s}):** el que minimiza la suma de cuadrados entre % de victorias real y % pitagórico sobre todos los equipos-temporada de **las otras 7 temporadas**, rango [1, 40]. Los desvíos de la temporada s se calculan siempre con k_{−s}. La 25/26 usa por tanto un k calibrado solo con 2017/18–2024/25.
- **Partido igualado, posesiones, NetRtg, vueltas:** como en v1.

## Calibración de k

- k_{−s} para cada temporada y k conjunto con las 8.
- Error absoluto medio en victorias por 34 partidos, de k_{−s} sobre s, frente a k = 14, en cada temporada (dejar una temporada fuera) y en media.
- IC90 de k: bootstrap de partidos dentro de cada temporada (10.000 remuestreos, percentiles 5-95) ajustando el k conjunto.
- **Criterio para decir que «k de la ACB difiere de 14»:** el IC90 excluye 14 **y** k_{−s} tiene menor error que 14 en al menos 5 de las 8 temporadas. Si no se cumplen ambas, se dice que no está demostrado.

## Test principal: ¿se repite el desvío de una temporada a la siguiente?

- Para cada par (equipo-franquicia en t, el mismo en t+1): desvío_t y desvío_{t+1}, con sus k_{−s} respectivos.
- Estadístico: correlación de Pearson r sobre los pares conjuntos. También la pendiente β de la regresión de desvío_{t+1} sobre desvío_t (fracción del desvío que se mantiene).
- IC90% (percentiles 5-95) por **bootstrap por clubes**: se remuestrean franquicias enteras con todos sus pares (10.000 remuestreos), para respetar que el mismo club aparece en pasos consecutivos.

## Regla de decisión

Se concluye **«hay señal de habilidad»** solo si el **límite inferior del IC90% de r es mayor que 0**. En cualquier otro caso, **«compatible con el azar»** (incluido el caso en que el IC quede por debajo de 0, que se comentaría aparte). Con 99 pares y 18 equipos por temporada el test, ignorando la dependencia entre pares, tiene aproximadamente un 76 % de potencia para un efecto r = 0,20, un 89 % para r = 0,25 y un 96 % para r = 0,30. Un efecto de r ≈ 0,10 no es detectable con estos datos.

## Conclusiones redactadas de antemano

**Si hay señal:** «Con ocho temporadas de la ACB, los equipos que ganan por encima de lo que dicen sus puntos tienden a repetirlo la temporada siguiente: la correlación entre el desvío de una temporada y el de la siguiente es distinguible de cero. Se mantiene aproximadamente una fracción β del desvío. Esto no identifica la causa (finales, plantilla, estilo, calendario) y el efecto, aunque detectable, es [pequeño/moderado].»

**Si es compatible con el azar:** «Con ocho temporadas de la ACB no se detecta que el desvío se repita de una temporada a la siguiente. Con esta muestra un efecto de tamaño moderado (r ≈ 0,25 o más) habría sido detectado con alta probabilidad, así que es improbable que exista; un efecto pequeño no se puede descartar. Lo prudente es esperar que los equipos que ganaron por encima de sus puntos se acerquen a ellos.»

En ambos casos se reconoce el trabajo de los entrenadores: que la huella de los finales sea pequeña o indetectable en el balance no significa que no se entrenen.

## Análisis secundarios (descriptivos, sin regla de decisión)

1. **Finales:** correlación entre el % de victorias en partidos igualados de t y el de t+1, con el mismo bootstrap por clubes.
2. **Predicción:** correlación con el % de victorias de t+1 de tres predictores de t: % de victorias, % pitagórico (con k_{−t}) y NetRtg. Diferencias con IC90% por bootstrap por clubes.
3. **Banda del azar:** por cada temporada, simulación partido a partido sobre su calendario (log5 y ventaja de campo calibrada en esa temporada, 10.000 simulaciones, semilla 2026) con fuerza = % pitagórico con k_{−s}; banda p5-p95. Proporción de equipos-temporada fuera de la banda frente al 10 % nominal, **con la advertencia de sesgo conservador descrita arriba**. El test de varianza de v1 se calcula con la misma salvedad.
4. **Mitades de la 25/26** (J1-17 frente a J18-34), igual que v1 pero con k_{−25/26}.
5. **Sensibilidad:** todo lo anterior sin 2020/21. No cambia la conclusión oficial.

## Regla del hero

Sin cambios: el titular «+N victorias» solo se usa si el desvío de ese equipo en la 25/26 (con k_{−25/26}) queda fuera de su banda del 90 %.

## Predicción para la 26/27

Desvío esperado de cada equipo en la 26/27 = max(β̂, 0) × desvío de la 25/26, con β̂ el estimado en el test principal. Las victorias esperadas «por sus puntos» siguen siendo las del pitagórico de la 25/26. Solo datos hasta la 25/26; se revisará en enero de 2027.

## Qué NO se hará

No se cambiarán las exclusiones, los umbrales, las definiciones ni los tests tras ver resultados. Cualquier análisis adicional se marcará como exploratorio y posterior.
