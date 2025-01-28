---CASOS CONFIRMADOS e OBTIO CONFIRMADOS---
select casosacumulado
,casosnovos 
,round(casosacumulado::numeric/ populacaotcu2019::numeric,10) * 100000 as incidencia
,obitosacumulado
,obitosnovos 
,round(obitosacumulado::numeric/ populacaotcu2019::numeric,10) * 100000 as mortalidade
,round(obitosacumulado::numeric/ casosacumulado::numeric,10) * 100 as letalidade_percent
from covid_brasil
where regiao  = 'Brasil' 
and ref_data = (select max(ref_data) as max_date from covid_brasil)

---Síntese de casos, óbitos, incidência e mortalidade---
select 'Brasil' as pais,c.regiao,c.estado
	,sum(casosacumulado) as casos
	,sum(obitosacumulado) as obitos
	,sum(populacaotcu2019) as populacao
	,round(sum(casosacumulado)::numeric / sum(populacaotcu2019)::numeric,10) * 100000 as incidencia_estado
	,round(sum(obitosacumulado)::numeric/ sum(populacaotcu2019)::numeric,10) * 100000 as mortalidade_estado
from covid_brasil c 
where c.municipio is not null
	and c.ref_data = (select max(ref_data) as max_date from covid_brasil)
group by c.regiao,c.estado