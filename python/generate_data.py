from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd
from faker import Faker


# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------

fake = Faker("pt_BR")

Faker.seed(42)
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_REFERENCIA = date(2025, 12, 31)
TOTAL_FUNCIONARIOS = 500


# ---------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------

def gerar_data_aleatoria(data_inicial: date, data_final: date) -> date:
    """Retorna uma data aleatória dentro do intervalo informado."""

    if data_inicial > data_final:
        raise ValueError("A data inicial não pode ser maior que a data final.")

    quantidade_dias = (data_final - data_inicial).days
    dias_aleatorios = random.randint(0, quantidade_dias)

    return data_inicial + timedelta(days=dias_aleatorios)


def salvar_csv(df: pd.DataFrame, nome_arquivo: str) -> None:
    """Salva um DataFrame na pasta data."""

    caminho = DATA_DIR / nome_arquivo

    df.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )

    print(f"Arquivo criado: {caminho}")


# ---------------------------------------------------------
# DEPARTAMENTOS
# ---------------------------------------------------------

def gerar_departamentos() -> pd.DataFrame:
    departamentos = [
        {
            "id_departamento": 1,
            "nome_departamento": "Tecnologia",
            "localizacao": "São Paulo",
            "orcamento_mensal": 850000.00,
            "data_criacao": "2015-01-10",
        },
        {
            "id_departamento": 2,
            "nome_departamento": "Recursos Humanos",
            "localizacao": "São Paulo",
            "orcamento_mensal": 280000.00,
            "data_criacao": "2015-02-15",
        },
        {
            "id_departamento": 3,
            "nome_departamento": "Financeiro",
            "localizacao": "São Paulo",
            "orcamento_mensal": 420000.00,
            "data_criacao": "2015-03-20",
        },
        {
            "id_departamento": 4,
            "nome_departamento": "Comercial",
            "localizacao": "Rio de Janeiro",
            "orcamento_mensal": 700000.00,
            "data_criacao": "2015-04-05",
        },
        {
            "id_departamento": 5,
            "nome_departamento": "Marketing",
            "localizacao": "Rio de Janeiro",
            "orcamento_mensal": 350000.00,
            "data_criacao": "2016-01-12",
        },
        {
            "id_departamento": 6,
            "nome_departamento": "Operações",
            "localizacao": "Belo Horizonte",
            "orcamento_mensal": 650000.00,
            "data_criacao": "2016-03-18",
        },
        {
            "id_departamento": 7,
            "nome_departamento": "Atendimento",
            "localizacao": "Recife",
            "orcamento_mensal": 390000.00,
            "data_criacao": "2017-05-22",
        },
        {
            "id_departamento": 8,
            "nome_departamento": "Jurídico",
            "localizacao": "Brasília",
            "orcamento_mensal": 300000.00,
            "data_criacao": "2017-08-30",
        },
    ]

    return pd.DataFrame(departamentos)


# ---------------------------------------------------------
# CARGOS
# ---------------------------------------------------------

def gerar_cargos() -> pd.DataFrame:
    cargos = [
        # Tecnologia
        (1, "Estagiário de Tecnologia", "Estagiário", 1800.00, 1),
        (2, "Desenvolvedor Back-end", "Júnior", 5200.00, 1),
        (3, "Desenvolvedor Back-end", "Pleno", 7800.00, 1),
        (4, "Desenvolvedor Back-end", "Sênior", 11000.00, 1),
        (5, "Analista de Dados", "Júnior", 4800.00, 1),
        (6, "Analista de Dados", "Pleno", 7200.00, 1),
        (7, "Cientista de Dados", "Pleno", 8500.00, 1),
        (8, "Coordenador de Tecnologia", "Coordenação", 13500.00, 1),
        (9, "Gerente de Tecnologia", "Gerência", 18500.00, 1),

        # Recursos Humanos
        (10, "Estagiário de RH", "Estagiário", 1600.00, 2),
        (11, "Assistente de RH", "Júnior", 3200.00, 2),
        (12, "Analista de RH", "Pleno", 5500.00, 2),
        (13, "Analista de RH", "Sênior", 7800.00, 2),
        (14, "Coordenador de RH", "Coordenação", 10500.00, 2),
        (15, "Gerente de RH", "Gerência", 15000.00, 2),

        # Financeiro
        (16, "Assistente Financeiro", "Júnior", 3400.00, 3),
        (17, "Analista Financeiro", "Júnior", 4700.00, 3),
        (18, "Analista Financeiro", "Pleno", 6500.00, 3),
        (19, "Analista Financeiro", "Sênior", 8700.00, 3),
        (20, "Coordenador Financeiro", "Coordenação", 11500.00, 3),
        (21, "Gerente Financeiro", "Gerência", 16500.00, 3),

        # Comercial
        (22, "Representante Comercial", "Júnior", 3800.00, 4),
        (23, "Executivo de Vendas", "Júnior", 4800.00, 4),
        (24, "Executivo de Vendas", "Pleno", 6800.00, 4),
        (25, "Executivo de Vendas", "Sênior", 9200.00, 4),
        (26, "Coordenador Comercial", "Coordenação", 12000.00, 4),
        (27, "Gerente Comercial", "Gerência", 17500.00, 4),

        # Marketing
        (28, "Assistente de Marketing", "Júnior", 3200.00, 5),
        (29, "Analista de Marketing", "Júnior", 4600.00, 5),
        (30, "Analista de Marketing", "Pleno", 6000.00, 5),
        (31, "Analista de Marketing", "Sênior", 8200.00, 5),
        (32, "Coordenador de Marketing", "Coordenação", 11000.00, 5),
        (33, "Gerente de Marketing", "Gerência", 16000.00, 5),

        # Operações
        (34, "Assistente de Operações", "Júnior", 3000.00, 6),
        (35, "Analista de Operações", "Pleno", 5600.00, 6),
        (36, "Supervisor de Operações", "Coordenação", 9800.00, 6),
        (37, "Gerente de Operações", "Gerência", 15500.00, 6),

        # Atendimento
        (38, "Atendente", "Júnior", 2600.00, 7),
        (39, "Analista de Atendimento", "Pleno", 4800.00, 7),
        (40, "Supervisor de Atendimento", "Coordenação", 8200.00, 7),

        # Jurídico
        (41, "Assistente Jurídico", "Júnior", 3600.00, 8),
        (42, "Analista Jurídico", "Pleno", 6500.00, 8),
        (43, "Advogado Corporativo", "Sênior", 10500.00, 8),
        (44, "Coordenador Jurídico", "Coordenação", 13500.00, 8),
        (45, "Gerente Jurídico", "Gerência", 18000.00, 8),
    ]

    colunas = [
        "id_cargo",
        "nome_cargo",
        "nivel",
        "salario_base",
        "id_departamento",
    ]

    return pd.DataFrame(cargos, columns=colunas)


# ---------------------------------------------------------
# FUNCIONÁRIOS
# ---------------------------------------------------------

def gerar_funcionarios(
    df_cargos: pd.DataFrame,
    quantidade: int = TOTAL_FUNCIONARIOS,
) -> pd.DataFrame:

    localidades = [
        ("São Paulo", "SP"),
        ("Campinas", "SP"),
        ("Rio de Janeiro", "RJ"),
        ("Niterói", "RJ"),
        ("Belo Horizonte", "MG"),
        ("Contagem", "MG"),
        ("Recife", "PE"),
        ("Olinda", "PE"),
        ("Brasília", "DF"),
        ("Goiânia", "GO"),
        ("Curitiba", "PR"),
        ("Salvador", "BA"),
        ("Fortaleza", "CE"),
        ("João Pessoa", "PB"),
        ("Patos", "PB"),
    ]

    ids_departamentos = [1, 2, 3, 4, 5, 6, 7, 8]

    pesos_departamentos = [
        0.22,  # Tecnologia
        0.08,  # Recursos Humanos
        0.10,  # Financeiro
        0.17,  # Comercial
        0.10,  # Marketing
        0.15,  # Operações
        0.12,  # Atendimento
        0.06,  # Jurídico
    ]

    funcionarios = []

    for id_funcionario in range(1, quantidade + 1):
        sexo = random.choices(
            population=["Masculino", "Feminino", "Outro"],
            weights=[0.49, 0.49, 0.02],
            k=1,
        )[0]

        if sexo == "Masculino":
            nome_completo = fake.name_male()
        elif sexo == "Feminino":
            nome_completo = fake.name_female()
        else:
            nome_completo = fake.name()

        id_departamento = random.choices(
            population=ids_departamentos,
            weights=pesos_departamentos,
            k=1,
        )[0]

        cargos_departamento = df_cargos[
            df_cargos["id_departamento"] == id_departamento
        ]

        cargo = cargos_departamento.sample(
            n=1,
            random_state=random.randint(1, 1_000_000),
        ).iloc[0]

        id_cargo = int(cargo["id_cargo"])
        salario_base = float(cargo["salario_base"])

        variacao_salarial = random.uniform(0.92, 1.22)
        salario = round(salario_base * variacao_salarial, 2)

        data_admissao = gerar_data_aleatoria(
            date(2018, 1, 1),
            date(2025, 12, 1),
        )

        idade_admissao = random.randint(18, 55)

        data_nascimento = data_admissao.replace(
            year=data_admissao.year - idade_admissao
        )

        data_nascimento -= timedelta(days=random.randint(0, 364))

        cidade, estado = random.choice(localidades)

        pode_ser_desligado = (
            data_admissao <= DATA_REFERENCIA - timedelta(days=120)
        )

        desligado = (
            random.random() < 0.18
            if pode_ser_desligado
            else False
        )

        if desligado:
            data_minima_desligamento = data_admissao + timedelta(days=90)

            data_desligamento = gerar_data_aleatoria(
                data_minima_desligamento,
                DATA_REFERENCIA,
            )

            status_funcionario = "Desligado"
        else:
            data_desligamento = None
            status_funcionario = "Ativo"

        funcionarios.append(
            {
                "id_funcionario": id_funcionario,
                "nome_completo": nome_completo,
                "sexo": sexo,
                "data_nascimento": data_nascimento,
                "cidade": cidade,
                "estado": estado,
                "salario": salario,
                "data_admissao": data_admissao,
                "data_desligamento": data_desligamento,
                "status_funcionario": status_funcionario,
                "id_departamento": id_departamento,
                "id_cargo": id_cargo,
            }
        )

    return pd.DataFrame(funcionarios)


# ---------------------------------------------------------
# PRESENÇAS E AVALIAÇÕES
# ---------------------------------------------------------

def gerar_presencas(df_funcionarios: pd.DataFrame) -> pd.DataFrame:
    """Gera registros em dias úteis de 2025, respeitando o vínculo."""
    registros = []
    id_presenca = 1

    for funcionario in df_funcionarios.itertuples(index=False):
        inicio = max(funcionario.data_admissao, date(2025, 1, 1))
        fim = min(
            funcionario.data_desligamento or DATA_REFERENCIA,
            DATA_REFERENCIA,
        )
        if inicio > fim:
            continue

        for dia in pd.bdate_range(inicio, fim):
            status = random.choices(
                ["Presente", "Falta", "Atestado", "Férias", "Folga"],
                weights=[0.88, 0.025, 0.035, 0.045, 0.015],
                k=1,
            )[0]
            registros.append(
                {
                    "id_presenca": id_presenca,
                    "id_funcionario": funcionario.id_funcionario,
                    "data_registro": dia.date(),
                    "status_presenca": status,
                }
            )
            id_presenca += 1

    return pd.DataFrame(registros)


def gerar_avaliacoes(df_funcionarios: pd.DataFrame) -> pd.DataFrame:
    """Gera avaliações semestrais durante a vigência do contrato."""
    registros = []
    id_avaliacao = 1
    datas_avaliacao = [date(2024, 6, 30), date(2024, 12, 31),
                       date(2025, 6, 30), date(2025, 12, 31)]

    for funcionario in df_funcionarios.itertuples(index=False):
        for data_avaliacao in datas_avaliacao:
            fim_vinculo = funcionario.data_desligamento or DATA_REFERENCIA
            if not (funcionario.data_admissao + timedelta(days=90)
                    <= data_avaliacao <= fim_vinculo):
                continue

            notas = [round(min(10, max(0, random.gauss(7.3, 1.25))), 1)
                     for _ in range(4)]
            lideranca = (
                round(min(10, max(0, random.gauss(7.2, 1.3))), 1)
                if funcionario.id_cargo in {8, 9, 14, 15, 20, 21, 26, 27,
                                            32, 33, 36, 37, 40, 44, 45}
                else None
            )
            componentes = notas + ([lideranca] if lideranca is not None else [])
            nota_final = round(sum(componentes) / len(componentes), 1)
            observacao = (
                "Desempenho acima do esperado."
                if nota_final >= 8.5
                else "Plano de desenvolvimento recomendado."
                if nota_final < 6
                else "Desempenho dentro do esperado."
            )
            registros.append(
                {
                    "id_avaliacao": id_avaliacao,
                    "id_funcionario": funcionario.id_funcionario,
                    "data_avaliacao": data_avaliacao,
                    "comunicacao": notas[0],
                    "trabalho_equipe": notas[1],
                    "qualidade_entrega": notas[2],
                    "proatividade": notas[3],
                    "lideranca": lideranca,
                    "nota_final": nota_final,
                    "observacao": observacao,
                }
            )
            id_avaliacao += 1

    return pd.DataFrame(registros)


# ---------------------------------------------------------
# EXECUÇÃO
# ---------------------------------------------------------

def main() -> None:
    print("Iniciando geração dos dados...\n")

    df_departamentos = gerar_departamentos()
    df_cargos = gerar_cargos()
    df_funcionarios = gerar_funcionarios(df_cargos)
    df_presencas = gerar_presencas(df_funcionarios)
    df_avaliacoes = gerar_avaliacoes(df_funcionarios)

    salvar_csv(df_departamentos, "departamentos.csv")
    salvar_csv(df_cargos, "cargos.csv")
    salvar_csv(df_funcionarios, "funcionarios.csv")
    salvar_csv(df_presencas, "presencas.csv")
    salvar_csv(df_avaliacoes, "avaliacoes.csv")

    ativos = (
        df_funcionarios["status_funcionario"] == "Ativo"
    ).sum()

    desligados = (
        df_funcionarios["status_funcionario"] == "Desligado"
    ).sum()

    print("\nResumo da geração:")
    print(f"Departamentos: {len(df_departamentos)}")
    print(f"Cargos: {len(df_cargos)}")
    print(f"Funcionários: {len(df_funcionarios)}")
    print(f"Funcionários ativos: {ativos}")
    print(f"Funcionários desligados: {desligados}")
    print(f"Registros de presença: {len(df_presencas)}")
    print(f"Avaliações: {len(df_avaliacoes)}")

    print("\nDados gerados com sucesso.")


if __name__ == "__main__":
    main()
