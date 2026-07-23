USE hr_analytics;

-- Execute este arquivo a partir da raiz do projeto. O MySQL precisa ter
-- permissão de leitura local (mysql --local-infile=1).
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE avaliacoes;
TRUNCATE TABLE presencas;
TRUNCATE TABLE funcionarios;
TRUNCATE TABLE cargos;
TRUNCATE TABLE departamentos;
SET FOREIGN_KEY_CHECKS = 1;

LOAD DATA LOCAL INFILE 'data/departamentos.csv'
INTO TABLE departamentos CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(id_departamento, nome_departamento, localizacao, orcamento_mensal, data_criacao);

LOAD DATA LOCAL INFILE 'data/cargos.csv'
INTO TABLE cargos CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(id_cargo, nome_cargo, nivel, salario_base, id_departamento);

LOAD DATA LOCAL INFILE 'data/funcionarios.csv'
INTO TABLE funcionarios CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(id_funcionario, nome_completo, sexo, data_nascimento, cidade, estado,
 salario, data_admissao, @data_desligamento, status_funcionario,
 id_departamento, id_cargo)
SET data_desligamento = NULLIF(@data_desligamento, '');

LOAD DATA LOCAL INFILE 'data/presencas.csv'
INTO TABLE presencas CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(id_presenca, id_funcionario, data_registro, status_presenca);

LOAD DATA LOCAL INFILE 'data/avaliacoes.csv'
INTO TABLE avaliacoes CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(id_avaliacao, id_funcionario, data_avaliacao, comunicacao, trabalho_equipe,
 qualidade_entrega, proatividade, @lideranca, nota_final, observacao)
SET lideranca = NULLIF(@lideranca, '');

SELECT 'departamentos' tabela, COUNT(*) registros FROM departamentos
UNION ALL SELECT 'cargos', COUNT(*) FROM cargos
UNION ALL SELECT 'funcionarios', COUNT(*) FROM funcionarios
UNION ALL SELECT 'presencas', COUNT(*) FROM presencas
UNION ALL SELECT 'avaliacoes', COUNT(*) FROM avaliacoes;
