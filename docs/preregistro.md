# Pre-registro: ¿suerte o habilidad en el balance de la ACB 25/26?

Este documento se commitea **antes** de calcular ningún exponente pitagórico, desvío, simulación ni correlación. El historial de git (fecha del primer commit) es la prueba.

**Transparencia.** Al validar los datos (306 partidos, 18 equipos × 34, sin empates) se vieron las victorias, puntos a favor y puntos en contra de cada equipo. No se calculó ningún porcentaje pitagórico, desvío, exponente ni test.

## Pregunta

¿Ganar por encima (o por debajo) de lo que dicen los puntos es una habilidad que se repite, o es ruido de 34 partidos?

## Datos

- Liga regular ACB 2025/26: 306 partidos, 18 equipos, 34 partidos por equipo. Se excluyen playoffs, Supercopa y Copa.
- Solo hay una temporada disponible. No se inventan ni se importan otras. Toda calibración es **in-sample** y se declara así.
- Todos los equipos juegan 34 partidos, así que no hace falta normalizar.
- Prórrogas: sus puntos cuentan en PF y PC. Se detectan por los minutos de equipo (225 = una, 250 = dos).
- La temporada 26/27 no se usa en ningún cálculo.

## Definiciones

- **Pitagórico:** `PF^k / (PF^k + PC^k)`. Victorias esperadas = partidos × pitagórico.
- **Desvío:** victorias reales − victorias esperadas.
- **Vueltas:** 1ª vuelta = jornadas 1-17; 2ª vuelta = jornadas 18-34.
- **Partido igualado:** diferencia final ≤ 5 puntos o prórroga. Solo se usa para describir, nunca para explicar.
- **Posesiones:** estimación de Oliver, media de la ofensiva y la defensiva: `FGA + 0.44·FTA − OREB + TOV`. NetRtg = 100·(PF − PC)/posesiones.

## Calibración de k

- k minimiza la suma de cuadrados entre el % de victorias real y el pitagórico, sobre los 18 equipos, en rango [1, 40].
- Validación: (a) mitades cruzadas (k ajustado en una vuelta, error en la otra); (b) dejar un equipo fuera. Métrica: error absoluto medio en victorias.
- Intervalo de k: bootstrap de partidos (10.000 remuestreos, percentiles 5-95).
- k = 14 (NBA, Morey) se muestra como referencia y se compara su error con el de k de la ACB.
- Que k de la ACB difiera de 14 es una hipótesis, no un supuesto.

## Simulación (banda del azar)

- Fuerza de cada equipo = su % pitagórico con el k calibrado.
- Probabilidad de cada partido del calendario real por log5, con ventaja de campo como multiplicador de odds `h`, calibrado para que la suma de probabilidades locales iguale las victorias locales observadas.
- 10.000 temporadas simuladas, semilla fija (2026).
- Banda del azar = percentiles 5 y 95 de las victorias simuladas de cada equipo.
- Un equipo queda "fuera de la banda" si sus victorias reales son estrictamente menores que el p5 o mayores que el p95. Con 18 equipos se esperan ~2 fuera por puro azar; se dirá.

## Tests de «¿se repite?»

- **Test A (correlación entre vueltas).** Desvío de cada equipo en la 1ª vuelta (victorias − 17·pitagórico de esa vuelta) frente al de la 2ª, con el k de la temporada completa. Pearson sobre los 18 equipos. IC90% por bootstrap de equipos (10.000 remuestreos, percentiles 5-95).
- **Test B (varianza).** Estadístico: raíz del desvío cuadrático medio de los 18 equipos en la temporada completa. Distribución nula: el mismo estadístico en las 10.000 temporadas simuladas. p = proporción de simuladas con estadístico ≥ al observado.
- **Comparación predictiva (descriptiva, sin regla de decisión).** Correlación con el % de victorias de la 2ª vuelta de tres predictores de la 1ª: % de victorias, % pitagórico (con k ajustado solo en la 1ª vuelta, para no filtrar información) y NetRtg. Diferencias con IC90% por bootstrap pareado de equipos.

## Regla de decisión

Se concluye **«hay señal de habilidad»** solo si se cumplen **las dos** condiciones: el límite inferior del IC90% del test A es > 0 **y** el p del test B es < 0,10. En cualquier otro caso se concluye **«compatible con el azar»**. Con 18 equipos el poder es bajo: no se interpretará nunca como «demostrado que es suerte».

## Regla del hero

El titular «+N victorias» (o «−N») solo se usa si el desvío de ese equipo queda fuera de la banda del azar. Si ninguno queda fuera, el artículo no usa titular de ese tipo.

## Conclusiones redactadas de antemano

**Si hay señal:** «Los datos de la ACB 25/26 son difíciles de explicar solo con el azar: los equipos que ganaron por encima de sus puntos en la primera vuelta tendieron a repetirlo en la segunda, y la dispersión de desvíos supera la de una liga puramente aleatoria. Es una sola temporada y 18 equipos, así que es un indicio, no una prueba, y no separa habilidad en finales de otras causas como la plantilla o el calendario.»

**Si es compatible con el azar:** «Con los datos de la ACB 25/26 no podemos distinguir los desvíos de lo que produciría el azar: la repetición entre vueltas no es distinguible de cero y la dispersión es la esperable de una liga aleatoria. Eso no demuestra que sea suerte: con 18 equipos y 34 partidos el test tiene poca potencia. Lo prudente es esperar que los equipos que ganaron por encima de sus puntos se acerquen a ellos.»

En ambos casos se reconoce la labor de los entrenadores: que la huella de los finales sea pequeña o indetectable en el balance no significa que no se entrenen.

## Predicción para la 26/27

Solo con datos de la 25/26: para cada equipo, victorias esperadas por su pitagórico como referencia de a dónde debería acercarse. Se revisará en enero de 2027 sin cambiar el método.

## Qué NO se hará

No se cambiarán la definición de igualado, el corte de vueltas, los umbrales ni los tests tras ver resultados. Si se añade algún análisis extra, se marcará como exploratorio y posterior.
