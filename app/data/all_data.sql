with insumos_talhao as (
select
	iat.insumoid,
	iat.talhaoid,
	ins.insumogrupoid,
	ins.descricao
	from agrosig_novo_latest.insumoaplicacaotalhao as iat
	left join agrosig_novo_latest.insumo as ins
	on iat.insumoid = ins.insumoid
),
grupo_insumos_talhao as (
select
	it.talhaoid,
	it.descricao,
	ig.descricao as grupo
	from insumos_talhao as it
	left join agrosig_novo_latest.insumogrupo as ig
	on it.insumogrupoid = ig.insumogrupoid
),

frequencia_grupos as (
select
	git.talhaoid,
	git.grupo,
	COUNT(*) as frequencia
	from grupo_insumos_talhao as git
	group by
	git.talhaoid,
	git.grupo
),

pivotado as (
select 
	fg.talhaoid,
	MAX(case when fg.grupo = 'Herbicidas' then frequencia end) as herbicidas,
	MAX(case when fg.grupo = 'Fungicidas' then frequencia end) as fungicidas,
	MAX(case when fg.grupo = 'Inseticidas' then frequencia end) as inseticidas
	from frequencia_grupos as fg
	group by
	fg.talhaoid
),

datas AS (
    select f.nome as fazenda
        ,fs.nome as setor
        ,t.codigo as talhao
        ,t.talhaoid
        ,t.geometria
        ,t.pontocentral
        ,s.nome as safra
        ,sp.nome as safra_periodo
        ,oc.nome as cultura
        ,tex.nome as textura
        ,cast(t.dataemergencia as date) as dataemergencia
        ,cast(t.dataplantioinicio as date) as dataplantioinicio
        ,EXTRACT(WEEK FROM CAST(dataplantioinicio AS TIMESTAMP)) as semana_plantio
        ,cast(t.datacolheitainicio  as date) as datacolheitainicio
        ,year(cast(t.dataemergencia  as date)) as ano
        ,date_diff('day', cast(t.dataemergencia  as date), cast(t.datacolheitainicio  as date)) as emergencia_colheita
        ,date_diff('day', cast(t.dataplantioinicio as date), cast(t.datacolheitainicio  as date)) as duracao_safra
        ,date_diff('day', cast(t.dataplantioinicio as date), cast(t.datacolheitainicio as date)) as periodo
        ,seq AS dias_apos_plantio
        ,CASE 
            WHEN seq >= 0 AND seq < 13 THEN 'v0'
            WHEN seq >= 13 AND seq < 19 THEN 'v1'
            WHEN seq >= 19 AND seq < 27 THEN 'v2-v3'
            WHEN seq >= 27 AND seq < 42 THEN 'v4-v5'
            WHEN seq >= 42 AND seq < 46 THEN 'r1-r2'
            WHEN seq >= 46 AND seq < 51 THEN 'r2-r3'
            WHEN seq >= 51 AND seq < 54 THEN 'r3'
            WHEN seq >= 54 AND seq < 62 THEN 'r3-r4'
            WHEN seq >= 62 AND seq < 66 THEN 'r3-r4-2'
            WHEN seq >= 66 AND seq < 70 THEN 'r4'
            WHEN seq >= 70 AND seq < 80 THEN 'r4-r5'
            WHEN seq >= 80 AND seq < 86 THEN 'r5'
            WHEN seq >= 86 AND seq < 94 THEN 'r5-r6'
            WHEN seq >= 94 AND seq < 101 THEN 'r6'
            WHEN seq >= 101 AND seq < 110 THEN 'r6-2'
            ELSE 'r6-r7'
        END AS estadio
        ,CASE 
            WHEN seq >= 0 AND seq < 13 THEN 1
            WHEN seq >= 13 AND seq < 19 THEN 2
            WHEN seq >= 19 AND seq < 27 THEN 3
            WHEN seq >= 27 AND seq < 42 THEN 4
            WHEN seq >= 42 AND seq < 46 THEN 5
            WHEN seq >= 46 AND seq < 51 THEN 6
            WHEN seq >= 51 AND seq < 54 THEN 7
            WHEN seq >= 54 AND seq < 62 THEN 8
            WHEN seq >= 62 AND seq < 66 THEN 9
            WHEN seq >= 66 AND seq < 70 THEN 10
            WHEN seq >= 70 AND seq < 80 THEN 11
            WHEN seq >= 80 AND seq < 86 THEN 12
            WHEN seq >= 86 AND seq < 94 THEN 13
            WHEN seq >= 94 AND seq < 101 THEN 14
            WHEN seq >= 101 AND seq < 110 THEN 15
            ELSE 16
        END AS numero_estadio
        , DATE_ADD('day', seq, CAST(t.dataplantioinicio AS date)) AS data
        , t.produtividade
        from agrosig_novo_latest.talhao as t
        left join agrosig_novo_latest.safraperiodo as sp
        on t.safraperiodoid = sp.safraperiodoid 
            left join agrosig_novo_latest.safra as s
        on sp.safraid = s.safraid 
            left join agrosig_novo_latest.ocupacao as oc
        on oc.ocupacaoid = sp.ocupacaoid
            left join agrosig_novo_latest.fazendatalhao as ft
        on t.fazendatalhaoid = ft.fazendatalhaoid
            left join agrosig_novo_latest.fazendasetor as fs
        on fs.fazendasetorid = t.fazendasetorid
            left join agrosig_novo_latest.fazenda as f
        on f.fazendaid = fs.fazendaid
            left join agrosig_novo_latest.texturasolo as tex
        on t.texturasoloid = tex.texturasoloid
        CROSS JOIN 
    UNNEST(sequence(0, DATE_DIFF('day', CAST(t.dataplantioinicio AS date), CAST(t.datacolheitainicio AS date)))) AS t(seq)
        where 1=1
            and t.dataplantioinicio is not null 
            and t.datacolheitainicio is not null
            and cast(t.dataplantioinicio as date) >= DATE('2019-01-01')
            and t.codigo <> '99999'
            and regexp_like(sp.nome, 'Safra')
            and sp.nome not like '%Experimentos%'
),
meteorologia_diario as (
	select *
		,cast(mtd.data as date) as data_leitura 
		from cleansed.meteorologia_talhao_diaria as mtd
),
plantio_score AS (
    SELECT 
        semana_plantio,
        CASE 
            WHEN semana_plantio = 39 THEN 100.000000
            WHEN semana_plantio = 40 THEN 98.933902
            WHEN semana_plantio = 38 THEN 95.901445
            WHEN semana_plantio = 41 THEN 95.506594
            WHEN semana_plantio = 44 THEN 92.316197
            WHEN semana_plantio = 42 THEN 91.163231
            WHEN semana_plantio = 43 THEN 91.084261
            WHEN semana_plantio = 45 THEN 90.902630
            WHEN semana_plantio = 46 THEN 84.940377
            WHEN semana_plantio = 37 THEN 84.908789
            WHEN semana_plantio = 47 THEN 81.339335
            WHEN semana_plantio = 48 THEN 79.507226
            WHEN semana_plantio = 51 THEN 60.270078
            WHEN semana_plantio = 49 THEN 59.306641
            WHEN semana_plantio = 52 THEN 52.341467
            WHEN semana_plantio = 50 THEN 50.003949
            ELSE 53.999842 -- Valor padrão para outras semanas não listadas
        END AS score_semanal
        from datas
     	group by 1,2
),
gd_esperado AS (
    SELECT
    CASE 
	        WHEN estadio = 'v0'            THEN 150
	        WHEN estadio = 'v1'            THEN 218.6
	        WHEN estadio = 'v2-v3'         THEN 307.8
	        WHEN estadio = 'v4-v5'         THEN 464.9
	        WHEN estadio = 'r1-r2'         THEN 507.9
	        WHEN estadio = 'r2-r3'         THEN 541.9
	        WHEN estadio = 'r3'            THEN 592.2
	        WHEN estadio = 'r3-r4'         THEN 675.4
	        WHEN estadio = 'r3-r4-2'       THEN 711.6
	        WHEN estadio = 'r4'            THEN 794.4
	        WHEN estadio = 'r4-r5'         THEN 872.5
	        WHEN estadio = 'r5'            THEN 939.7
	        WHEN estadio = 'r5-r6'         THEN 1022.2 
	        WHEN estadio = 'r6'            THEN 1100.6
	        WHEN estadio = 'r6-2'          THEN 1196.4
        ELSE 1300
    	END AS graus_dias_esperado,
    	estadio
    FROM datas
    group by 1,2
),
ch_esperada AS (
    SELECT
        CASE 
	        WHEN estadio = 'v0'            THEN 132.8
	        WHEN estadio = 'v1'            THEN 27.6
	        WHEN estadio = 'v2-v3'         THEN 41.9
	        WHEN estadio = 'v4-v5'         THEN 117.4
	        WHEN estadio = 'r1-r2'         THEN 0.0
	        WHEN estadio = 'r2-r3'         THEN 101.9
	        WHEN estadio = 'r3'            THEN 26.8
	        WHEN estadio = 'r3-r4'         THEN 26.5
	        WHEN estadio = 'r3-r4-2'       THEN 45.9
	        WHEN estadio = 'r4'            THEN 42.0
	        WHEN estadio = 'r4-r5'         THEN 86.3
	        WHEN estadio = 'r5'            THEN 67.0
	        WHEN estadio = 'r5-r6'         THEN 96.5
	        WHEN estadio = 'r6'            THEN 62.8
	        WHEN estadio = 'r6-2'          THEN 28.8
        ELSE 40
    	END AS chuva_esperada,
    	estadio
    FROM datas
    group by 1,2
),
soma_graus_dias AS (
    select distinct
    dt.fazenda,
    dt.talhao,
    dt.safra,
    dt.numero_estadio,
    dt.cultura,
    SUM((mtd.temperatura_max + mtd.temperatura_min)/2 - 14) OVER (PARTITION BY dt.fazenda, dt.talhao, dt.safra ORDER BY dt.numero_estadio) AS soma_graus_dias_acumulado,
    COUNT(*) OVER (PARTITION BY dt.fazenda, dt.talhao, dt.safra ORDER BY dt.numero_estadio) AS dias_para_soma
	FROM 
        datas dt
	INNER JOIN meteorologia_diario mtd ON
	(
	    dt.fazenda = mtd.fazenda 
	    AND dt.setor = mtd.setor
	    AND dt.talhao = mtd.talhao
	    AND dt.safra = mtd.safra
	    AND dt.cultura = mtd.cultura
	    AND dt.data = mtd.data_leitura
	)
	ORDER BY dt.fazenda, dt.talhao, dt.safra, dt.numero_estadio ASC
),

grouped_data as (
SELECT dt.fazenda, dt.setor, dt.talhao, dt.talhaoid, dt.safra, dt.safra_periodo, dt.cultura, dt.textura, dt.geometria, dt.pontocentral, dt.dataemergencia, dt.dataplantioinicio, dt.semana_plantio, dt.datacolheitainicio, ano, emergencia_colheita, duracao_safra, periodo, dt.estadio, dt.numero_estadio, produtividade, 
	sgd.soma_graus_dias_acumulado, sgd.dias_para_soma,
	AVG((temperatura_max + temperatura_min)/2 - 14) AS graus_dias,
	SUM(chuva_soma) AS soma_chuva, 
    AVG(temperatura_media) AS media_temperatura, 
    AVG(radiacao_solar_media) AS media_radiacao_solar, 
    AVG(umidade_media) AS media_umidade,
    AVG(velocidade_vento_media) AS media_velocidade_vento, 
    AVG(direcao_vento_media) AS media_direcao_vento, 
    AVG(velocidade_rajada_media) AS media_velocidade_rajada, 
    AVG(direcao_rajada_media) AS media_direcao_rajada
FROM datas as dt
left JOIN meteorologia_diario mtd ON
(
    1 = 1
    AND dt.fazenda = mtd.fazenda 
    AND dt.setor = mtd.setor
    AND dt.talhao = mtd.talhao
    AND dt.safra = mtd.safra
    AND dt.cultura = mtd.cultura
    AND dt.data = mtd.data_leitura
)
inner JOIN soma_graus_dias sgd ON 
(
	1 = 1
	and sgd.fazenda = dt.fazenda
	and sgd.talhao = dt.talhao
	and sgd.safra = dt.safra
	and sgd.cultura = dt.cultura
	and dt.numero_estadio = sgd.numero_estadio
)
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,21, 22, 23
ORDER BY 1, 2, 3, 4, 5, dt.numero_estadio
),
score_data as (
SELECT 
	gd.fazenda,
	gd.setor,
	gd.talhao,
	gd.talhaoid,
    gd.safra,
    gd.safra_periodo,
    gd.cultura as ocupacao,
	gd.textura,
	gd.geometria,
	gd.pontocentral,
	gd.dataemergencia,
	gd.dataplantioinicio,
	gd.semana_plantio,
	gd.datacolheitainicio, 
	gd.ano, 
	gd.emergencia_colheita, 
	gd.duracao_safra, 
	gd.periodo, 
	gd.produtividade,
	gd.estadio, 
	gd.numero_estadio,
	gd.graus_dias,
	gd.soma_graus_dias_acumulado,
	graus_dias_esperado,
	AVG(COALESCE(1 - ABS(soma_graus_dias_acumulado - graus_dias_esperado) / NULLIF(soma_graus_dias_acumulado, 0), 0)) AS graus_dias_score,
	gd.soma_chuva,
	chuva_esperada,
	AVG(COALESCE(1 - ABS(soma_chuva - chuva_esperada) / NULLIF(soma_chuva, 0), 0)) AS soma_chuva_score,
	score_semanal,
	dias_para_soma,
    gd.media_temperatura, 
    gd.media_radiacao_solar, 
    gd.media_umidade
FROM
    grouped_data gd
inner JOIN 
    gd_esperado ON gd.estadio = gd_esperado.estadio
inner join 
	ch_esperada on gd.estadio = ch_esperada.estadio
inner join
	plantio_score ps on gd.semana_plantio = ps.semana_plantio

GROUP BY 
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,29,30,31,32,33
order by 
	1,2,3,4,5,7,18
),

final_data as (
select	sd.*
	,pvt.herbicidas
	,pvt.inseticidas
	,pvt.fungicidas
from score_data sd
left join
	pivotado pvt on sd.talhaoid = pvt.talhaoid
)
select * from final_data