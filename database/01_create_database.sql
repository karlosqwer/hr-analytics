DROP DATABASE IF EXISTS hr_analytics;

CREATE DATABASE hr_analytics
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE hr_analytics;

CREATE TABLE departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_departamento VARCHAR(100) NOT NULL UNIQUE,
    localizacao VARCHAR(100) NOT NULL,
    orcamento_mensal DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    data_criacao DATE NOT NULL,

    CONSTRAINT chk_orcamento_mensal
        CHECK (orcamento_mensal >= 0)
);

CREATE TABLE cargos (
    id_cargo INT AUTO_INCREMENT PRIMARY KEY,
    nome_cargo VARCHAR(100) NOT NULL,
    nivel ENUM(
        'Estagiário',
        'Júnior',
        'Pleno',
        'Sênior',
        'Coordenação',
        'Gerência',
        'Diretoria'
    ) NOT NULL,
    salario_base DECIMAL(10, 2) NOT NULL,
    id_departamento INT NOT NULL,

    CONSTRAINT fk_cargos_departamentos
        FOREIGN KEY (id_departamento)
        REFERENCES departamentos(id_departamento)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_salario_base
        CHECK (salario_base > 0),

    CONSTRAINT uq_cargo_departamento_nivel
        UNIQUE (nome_cargo, nivel, id_departamento)
);

CREATE TABLE funcionarios (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome_completo VARCHAR(150) NOT NULL,
    sexo ENUM('Masculino', 'Feminino', 'Outro') NOT NULL,
    data_nascimento DATE NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    data_admissao DATE NOT NULL,
    data_desligamento DATE NULL,
    status_funcionario ENUM('Ativo', 'Desligado') NOT NULL DEFAULT 'Ativo',
    id_departamento INT NOT NULL,
    id_cargo INT NOT NULL,

    CONSTRAINT fk_funcionarios_departamentos
        FOREIGN KEY (id_departamento)
        REFERENCES departamentos(id_departamento)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_funcionarios_cargos
        FOREIGN KEY (id_cargo)
        REFERENCES cargos(id_cargo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_salario_funcionario
        CHECK (salario > 0),

    CONSTRAINT chk_data_desligamento
        CHECK (
            data_desligamento IS NULL
            OR data_desligamento >= data_admissao
        ),

    CONSTRAINT chk_status_desligamento
        CHECK (
            (status_funcionario = 'Ativo' AND data_desligamento IS NULL)
            OR
            (status_funcionario = 'Desligado' AND data_desligamento IS NOT NULL)
        )
);

CREATE TABLE presencas (
    id_presenca BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT NOT NULL,
    data_registro DATE NOT NULL,
    status_presenca ENUM(
        'Presente',
        'Falta',
        'Atestado',
        'Férias',
        'Folga'
    ) NOT NULL,

    CONSTRAINT fk_presencas_funcionarios
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionarios(id_funcionario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_presenca_funcionario_data
        UNIQUE (id_funcionario, data_registro)
);

CREATE TABLE avaliacoes (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT NOT NULL,
    data_avaliacao DATE NOT NULL,
    comunicacao DECIMAL(3, 1) NOT NULL,
    trabalho_equipe DECIMAL(3, 1) NOT NULL,
    qualidade_entrega DECIMAL(3, 1) NOT NULL,
    proatividade DECIMAL(3, 1) NOT NULL,
    lideranca DECIMAL(3, 1) NULL,
    nota_final DECIMAL(3, 1) NOT NULL,
    observacao VARCHAR(255),

    CONSTRAINT fk_avaliacoes_funcionarios
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionarios(id_funcionario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_comunicacao
        CHECK (comunicacao BETWEEN 0 AND 10),

    CONSTRAINT chk_trabalho_equipe
        CHECK (trabalho_equipe BETWEEN 0 AND 10),

    CONSTRAINT chk_qualidade_entrega
        CHECK (qualidade_entrega BETWEEN 0 AND 10),

    CONSTRAINT chk_proatividade
        CHECK (proatividade BETWEEN 0 AND 10),

    CONSTRAINT chk_lideranca
        CHECK (lideranca IS NULL OR lideranca BETWEEN 0 AND 10),

    CONSTRAINT chk_nota_final
        CHECK (nota_final BETWEEN 0 AND 10),

    CONSTRAINT uq_avaliacao_funcionario_data
        UNIQUE (id_funcionario, data_avaliacao)
);

CREATE INDEX idx_cargos_departamento
ON cargos(id_departamento);

CREATE INDEX idx_funcionarios_departamento
ON funcionarios(id_departamento);

CREATE INDEX idx_funcionarios_cargo
ON funcionarios(id_cargo);

CREATE INDEX idx_funcionarios_status
ON funcionarios(status_funcionario);

CREATE INDEX idx_funcionarios_admissao
ON funcionarios(data_admissao);

CREATE INDEX idx_funcionarios_desligamento
ON funcionarios(data_desligamento);

CREATE INDEX idx_presencas_data
ON presencas(data_registro);

CREATE INDEX idx_presencas_status
ON presencas(status_presenca);

CREATE INDEX idx_avaliacoes_data
ON avaliacoes(data_avaliacao);

CREATE INDEX idx_avaliacoes_nota
ON avaliacoes(nota_final);

SHOW TABLES;
