USE hr_analytics;

-- 1. Headcount, folha e salário médio por departamento
SELECT d.nome_departamento,
       COUNT(*) AS headcount_ativo,
       ROUND(SUM(f.salario), 2) AS folha_mensal,
       ROUND(AVG(f.salario), 2) AS salario_medio
FROM funcionarios f
JOIN departamentos d USING (id_departamento)
WHERE f.status_funcionario = 'Ativo'
GROUP BY d.id_departamento, d.nome_departamento
ORDER BY headcount_ativo DESC;

-- 2. Turnover: desligamentos / headcount médio aproximado
WITH movimentacao AS (
    SELECT d.id_departamento, d.nome_departamento,
           SUM(f.data_admissao BETWEEN '2025-01-01' AND '2025-12-31') admissoes,
           SUM(f.data_desligamento BETWEEN '2025-01-01' AND '2025-12-31') desligamentos,
           SUM(f.data_admissao <= '2025-01-01'
               AND (f.data_desligamento IS NULL OR f.data_desligamento >= '2025-01-01')) hc_inicio,
           SUM(f.data_admissao <= '2025-12-31'
               AND (f.data_desligamento IS NULL OR f.data_desligamento >= '2025-12-31')) hc_fim
    FROM departamentos d LEFT JOIN funcionarios f USING (id_departamento)
    GROUP BY d.id_departamento, d.nome_departamento
)
SELECT nome_departamento, admissoes, desligamentos, hc_inicio, hc_fim,
       ROUND(100 * desligamentos / NULLIF((hc_inicio + hc_fim) / 2, 0), 2)
       AS turnover_pct
FROM movimentacao ORDER BY turnover_pct DESC;

-- 3. Absenteísmo por departamento
SELECT d.nome_departamento,
       COUNT(*) registros,
       SUM(p.status_presenca IN ('Falta', 'Atestado')) ausencias,
       ROUND(100 * SUM(p.status_presenca IN ('Falta', 'Atestado')) / COUNT(*), 2)
       AS absenteismo_pct
FROM presencas p
JOIN funcionarios f USING (id_funcionario)
JOIN departamentos d USING (id_departamento)
GROUP BY d.id_departamento, d.nome_departamento
ORDER BY absenteismo_pct DESC;

-- 4. Desempenho médio e distribuição por departamento
SELECT d.nome_departamento, COUNT(*) avaliacoes,
       ROUND(AVG(a.nota_final), 2) nota_media,
       SUM(a.nota_final >= 8.5) alto_desempenho,
       SUM(a.nota_final < 6) abaixo_esperado
FROM avaliacoes a
JOIN funcionarios f USING (id_funcionario)
JOIN departamentos d USING (id_departamento)
GROUP BY d.id_departamento, d.nome_departamento
ORDER BY nota_media DESC;

-- 5. Equidade salarial por sexo, departamento e cargo
SELECT d.nome_departamento, c.nome_cargo, c.nivel, f.sexo,
       COUNT(*) pessoas, ROUND(AVG(f.salario), 2) salario_medio
FROM funcionarios f
JOIN departamentos d USING (id_departamento)
JOIN cargos c USING (id_cargo)
WHERE f.status_funcionario = 'Ativo'
GROUP BY d.nome_departamento, c.nome_cargo, c.nivel, f.sexo
HAVING COUNT(*) >= 2
ORDER BY d.nome_departamento, c.nome_cargo, c.nivel, f.sexo;

-- 6. Pessoas com alto desempenho e salário abaixo da referência do cargo
SELECT f.nome_completo, d.nome_departamento, c.nome_cargo, c.nivel,
       f.salario, c.salario_base, ROUND(AVG(a.nota_final), 2) nota_media
FROM funcionarios f
JOIN departamentos d USING (id_departamento)
JOIN cargos c USING (id_cargo)
JOIN avaliacoes a USING (id_funcionario)
WHERE f.status_funcionario = 'Ativo' AND f.salario < c.salario_base
GROUP BY f.id_funcionario, f.nome_completo, d.nome_departamento,
         c.nome_cargo, c.nivel, f.salario, c.salario_base
HAVING AVG(a.nota_final) >= 8.5
ORDER BY nota_media DESC;
