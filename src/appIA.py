import PySimpleGUI as sg
import util.dados as dados
import CasosSimiliares as cs
import util.crud as crud

dados = dados.Dados()
crud = crud.CRUD()
atributos = dados.atributos
valores_atributos = dados.valores_atributos
d_nome_valores = dados.nome_valores
novo_caso = []
comboboxes = []
casos_similares_selecionados = []


def calc_similaridade():
    salvar_selecao()
    simG = cs.CasosSimilares(novo_caso)
    indices_maiores = sorted(simG.get_indices_maiores_valores(5))
    maiores_porcent = simG.get_maiores_valores(5)
    todos_casos = simG.get_todos_casos()

    casos_ordendados = [todos_casos[indice] if 0 <= indice < len(todos_casos) else None for indice in indices_maiores]
    casos_ordendados = [caso[:2] for caso in casos_ordendados]

    return maiores_porcent, casos_ordendados, todos_casos

def salvar_selecao():
    novo_caso.clear()
    for i, atributo in enumerate(atributos):
        selected_value = comboboxes[i].get()
        index = valores_atributos[i].index(selected_value)
        if selected_value == "?":
            novo_caso.append(None)
        else:
            novo_caso.append(index-1)

def salvar_caso(caso, nomes_casos_similares):
    layout = [
        [sg.Text("Selecione o nome do caso:")],
        [sg.Combo(values=nomes_casos_similares, key="-CASE-NAME-")],
        [sg.Button("Salvar", key="-SAVE-")],
    ]

    window = sg.Window("Salvar Caso no Banco", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-SAVE-":
            nome_caso = values["-CASE-NAME-"]
            if nome_caso:
                caso_banco = list(caso).copy()
                caso_banco.insert(0, nome_caso)
                crud.conectar()
                crud.create(caso_banco)
                crud.desconectar()
                sg.popup("Caso salvo com sucesso!")
                window.close()
                break

    window.close()



layout = [  # tela selecao de atributos
    [sg.Text("Caso Problema", font=("Arial", 20))],
    *[
        [
            sg.Text(atributo, size=(15, 1)),
            sg.Combo(
                values=valores_atributos[i],
                default_value=valores_atributos[i][0],
                size=(15, 1),
                key=f"-ATTR-{i}-",
            ),
        ]
        for i, atributo in enumerate(atributos)
    ],
    [sg.Button("Próximo", key="-NEXT-")],
]

column_layout = [
    [sg.Column(layout, size=(500, 500), scrollable=True, vertical_scroll_only=True)]
]

window = sg.Window("Seleção de Atributos", column_layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-NEXT-":
        for i in range(len(atributos)):
            selected_value = values[f"-ATTR-{i}-"]
            index = valores_atributos[i].index(selected_value)
            if selected_value == "?":
                novo_caso.append(None)
            else:
                novo_caso.append(index - 1)

        window.close()
        break

casos_similares = cs.CasosSimilares(novo_caso)
indices_maiores = sorted(casos_similares.get_indices_maiores_valores(5))
maiores_porcent = casos_similares.get_maiores_valores(5)
todos_casos = casos_similares.get_todos_casos()
nomes_casos_similares = [caso[1] for caso in todos_casos]

# Set the number of rows for the tables
num_rows = len(indices_maiores)

layout = [
    [sg.Text("Atributos Selecionados", font=("Arial", 20))],
    [
        sg.Table(
            values=[
                [atributos[i], d_nome_valores[i][novo_caso[i]] if novo_caso[i] is not None else "-"]
                for i in range(len(novo_caso))
            ],
            headings=["ATRIBUTO", "VALOR"],
            auto_size_columns=False,
            justification="left",
            key="-NEW-CASE-TABLE-",
            num_rows=num_rows,
            col_widths=[20, 43],
        )
    ],
    [sg.Text("Casos Similares", font=("Arial", 20))],
    [
        sg.Table(
            values=[
                [i + 1, todos_casos[case_index][1], f"{maiores_porcent[i]}%"]
                for i, case_index in enumerate(indices_maiores)
            ],
            headings=["ID", "Caso", "Porcentagem"],
            auto_size_columns=False,
            justification="left",
            key="-SIMILAR-CASES-TABLE-",
            num_rows=num_rows,
            col_widths=[20, 33],
        )
    ],
    [sg.Button("Selecionar caso", key="-SELECT-CASES-")],

    [sg.Text("Detalhes do caso", font=("Arial", 20))],
    [
        sg.Table(
            values=[],
            headings=["Atributo", "Valor"],
            auto_size_columns=False,
            justification="left",
            key="-SELECTED-CASE-DETAILS-",
            num_rows=num_rows,
            col_widths=[20, 43],
        )   
    ],
    [sg.Button("Salvar no banco", key="-SAVE-DB-SIMILAR-")],
    #[sg.Button("Novo Caso", key="-NEW-CASE-"), sg.Button("Fechar", key="Fechar")],
]

column_layout = [
    [sg.Column(layout, size=(600, 500), scrollable=True, vertical_scroll_only=True)]
]

window = sg.Window("Casos Similares", column_layout, resizable=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-SELECT-CASES-":
        selected_similar_case_index = values["-SIMILAR-CASES-TABLE-"][0]
        selected_similar_case = todos_casos[indices_maiores[selected_similar_case_index]]

        casos_similares_selecionados = [caso[1] for caso in todos_casos]

        values = []
        for atributo, valor in zip(atributos, selected_similar_case[2:]):  # Começamos do índice 2 para evitar o ID e o nome do caso
            try:
                if valor is not None:
                    if isinstance(valor, int):
                        value = d_nome_valores[atributos.index(atributo)][valor]
                    else:
                        value = valor
                else:
                    value = "-"
                values.append([atributo, value])
            except (ValueError, IndexError) as e:
                print(f"Error accessing attribute {atributo}: {e}")

        window["-SELECTED-CASE-DETAILS-"].update(values=values)

    if event == "-SAVE-DB-SIMILAR-":
        nomes_casos_similares = [todos_casos[case_index][1] for case_index in indices_maiores]
        salvar_caso(list(selected_similar_case), nomes_casos_similares)


    if event == "-NEW-CASE-":
        novo_caso.clear()
        window.close()
        window = sg.Window("Seleção de Atributos", column_layout)

    if event == "Fechar":
        break

window.close()
