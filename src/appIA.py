import PySimpleGUI as sg
import util.dados as dados
import similaridade as cs
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
    simG = cs.Similaridade(novo_caso)
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

def salvar_caso(caso, nome_caso):
    caso_banco = caso.copy()
    caso_banco.insert(0, nome_caso)   
    crud.conectar()
    crud.create(caso_banco)
    crud.desconectar()
    return True



sg.theme('GreenMono')

layout = [
    # tela selecao de atributos
    [sg.Text("CASO PROBLEMA", expand_x=True, justification='center', 
             text_color='Green', background_color='white', font=('Helvetica', 14, "bold"))],
    *[
        [
            sg.Text(atributo, size=(20, 1)),
            sg.Combo(
                values=valores_atributos[i],
                default_value=valores_atributos[i][0],
                size=(30, 1),
                key=f"-ATTR-{i}-",
            ),
        ]
        for i, atributo in enumerate(atributos)
    ],
    [sg.Button("Próximo", key="-NEXT-", expand_x=True )],
]

column_layout = [
    [sg.Column(layout, size=(420, 500), scrollable=True, vertical_scroll_only=True)]
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

casos_similares = cs.Similaridade(novo_caso)
indices_maiores = sorted(casos_similares.get_indices_maiores_valores(5))
maiores_porcent = casos_similares.get_maiores_valores(5)
todos_casos = casos_similares.get_todos_casos()
nomes_casos_similares = [caso[1] for caso in todos_casos]

# Set the number of rows for the tables
num_rows = len(indices_maiores)

layout = [
    [sg.Text("ATRIBUTOS SELECIONADOS", expand_x=True, justification='center', 
             text_color='Green', background_color='white', font=('Helvetica', 14, "bold"))],
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
    [sg.Text("CASOS SIMILARES", expand_x=True, justification='center', 
             text_color='Green', background_color='white', font=('Helvetica', 14, "bold"))],
    [
        sg.Table(
            values=[
                [todos_casos[case_index][0], todos_casos[case_index][1], f"{maiores_porcent[i]}%"]
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

    [sg.Text("DETALHES DO CASO", expand_x=True, justification='center', 
             text_color='Green', background_color='white', font=('Helvetica', 14, "bold"))],
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
    [sg.Button("Salvar no banco", key="-SAVE-DB-SIMILAR-"),
     #sg.Button("Novo Caso", key="-NEW-CASE-"), 
     sg.Button("Fechar", key="Fechar")],
]


column_layout = [
    [sg.Column(layout, size=(600, 510), scrollable=True, vertical_scroll_only=True)]
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

        values = [["ID", selected_similar_case[0]], ["Nome", selected_similar_case[1]]]
        for atributo, valor in zip(atributos, selected_similar_case[2:]):
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
        opcoes = nomes_casos_similares
        layout = [
            [sg.Text('Salvar caso como:')],
            [sg.Combo(opcoes, default_value=opcoes[0], key='-COMBO-')],
            [sg.Button('OK')]
        ]
        popup_window = sg.Window('Salvar no banco', layout, modal=True)
        while True:
            event, values = popup_window.read()

            if event == sg.WIN_CLOSED:
                break

            if event == 'OK':
                opcao_selecionada = values['-COMBO-']
                salvar_caso(novo_caso, opcao_selecionada) 
                sg.popup(f"Caso salvo no banco de dados como: {opcao_selecionada}!")
                popup_window.close()


    if event == "-NEW-CASE-":
        novo_caso.clear()
        window.close()
        window = sg.Window("Seleção de Atributos", column_layout)


    if event == "Fechar":
        break

window.close()
