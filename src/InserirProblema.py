import tkinter as tk
from tkinter import ttk
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
valor_selecionado = None
todos_casos = []
NOME_CASO = None


def calc_similiaridade():
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
        else: novo_caso.append(index-1)
    
def salvar_caso(caso, nome_caso):
    caso_banco = caso.copy()
    caso_banco.insert(0, nome_caso)   
    crud.conectar()
    crud.create(caso_banco)
    crud.desconectar()
    return True


def tela_selecao_atributos():
    janela = tk.Tk()
    janela.title("Seleção de Atributos")
    janela.geometry("600x500")
    # Crie um canvas dentro da janela
    canvas = tk.Canvas(janela)


    texto = tk.Label(janela, text="Caso Problema", font=("Arial", 20))
    texto.pack(side=tk.TOP, pady=0)

        


    scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)
    

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for i, atributo in enumerate(atributos):
        subframe = tk.Frame(frame)
        subframe.pack(side=tk.TOP, padx=100, pady=10)

        label = tk.Label(subframe, text=atributo, width=30, anchor="w")
        label.pack(side=tk.LEFT)

        combobox = ttk.Combobox(subframe, values=valores_atributos[i], state="readonly")
        combobox.current(0)
        combobox.pack(side=tk.LEFT)

        comboboxes.append(combobox)

    def tela_casos_similares():
        maiores_porcent, casos_ordendados, todos_casos = calc_similiaridade()
        casos_ordendados = [caso[:2] for caso in casos_ordendados]
        caso_selecionado = []
        

        #calc_similiaridade()
        janela2 = tk.Tk()
        janela2.title("Casos Similares")
        janela2.geometry("800x900")
        

        texto = tk.Label(janela2, text="Casos Similares", font=("Arial", 20))
        texto.grid(row=0, sticky="n", columnspan=3)
        

        # Cria uma barra de rolagem vertical
        scrollbar = tk.Scrollbar(janela2, orient="vertical")
        
        texto = tk.Label(janela2, text="CASO NOVO", font=("Arial", 12))
        texto.grid(row=1, sticky="n", columnspan=3, pady=5)

        # Cria um Listbox e associa a barra de rolagem a ele
        treeCasos = ttk.Treeview(janela2, yscrollcommand=scrollbar.set, columns=("H1", "H2"), show="headings")
        treeCasos.heading("H1", text="ATRIBUTO",)
        treeCasos.heading("H2", text="VALOR")
        treeCasos.column("H1", width=150, anchor="center")
        treeCasos.column("H2", width=150, anchor="center")
        treeCasos.grid(row=2, column=0, sticky="nsew", columnspan=3, padx=10)
        scrollbar.grid(row=2, column=1, sticky="ns")
        scrollbar.config(command=treeCasos.yview)

        texto = tk.Label(janela2, text="CASO SELECIONADO", font=("Arial", 12) )
        texto.grid(row=3, sticky="n", columnspan=3, pady=5)

        tree_casos_selecao = ttk.Treeview(janela2, columns=("H1", "H2"), show="headings")
        tree_casos_selecao.heading("H1", text="ATRIBUTO",)
        tree_casos_selecao.heading("H2", text="VALOR")
        tree_casos_selecao.column("H1", width=150, anchor="center")
        tree_casos_selecao.column("H2", width=150, anchor="center")
        tree_casos_selecao.grid(row=4, column=0, sticky="nsew", columnspan=3, padx=10)
        scrollbar.grid(row=4, column=1, sticky="ns")
        scrollbar.config(command=tree_casos_selecao.yview)



        for atributo in atributos:
            nome_valores = []
            nome_valores.clear()
            for i in range(len(novo_caso)):
                if novo_caso[i] is None:
                    nome_valores.append("?")
                else:
                    nome_valores.append(d_nome_valores[i][novo_caso[i]])

            treeCasos.insert("", "end", values=(atributo, nome_valores[atributos.index(atributo)]))

        def atualizar_treeview(valor_selecionado):
            tree_casos_selecao.delete(*tree_casos_selecao.get_children())
            caso_selecionado = sorted(todos_casos, key=lambda x: x[0])
            caso_selecionado = caso_selecionado[valor_selecionado-1]
            caso_selecionado = caso_selecionado[2:]

            nome_valores = []
            nome_valores.clear()
            
            for atributo in atributos:
                nome_valores = []
                nome_valores.clear()
                
                for i in range(len(caso_selecionado)):
                    if caso_selecionado[i] is None:
                        nome_valores.append("?")
                    else:
                        nome_valores.append(d_nome_valores[i][caso_selecionado[i]])

                tree_casos_selecao.insert("", "end", values=(atributo, nome_valores[atributos.index(atributo)]))

               
        def btn_atualizar():
            item_selecionado = tree.focus()

            # Se houver um item selecionado, imprima suas informações
            if item_selecionado:
                valores = tree.item(item_selecionado, 'values')
                atualizar_treeview(int(valores[0]))
            else:
                pass
            

        texto = tk.Label(janela2, text="SELECIONAR CASOS SIMILARES", font=("Arial", 12) )
        texto.grid(row=5, sticky="n", columnspan=3, pady=5)
            
        tree = ttk.Treeview(janela2, columns=("ID", "Caso", "Porcentagem"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Caso", text="CASO")
        tree.heading("Porcentagem", text="PORCENTAGEM %")
        tree.column("ID", width=50, anchor="center")
        tree.column("Caso", width=150, anchor="center")
        tree.column("Porcentagem", width=50, anchor="center")
        
        for i in range(5):
            tree.insert("", "end", values=(casos_ordendados[i][0], casos_ordendados[i][1], maiores_porcent[i]))
        
        tree.grid(row=6, column=0, sticky="nsew", columnspan=3, padx=10)
        

        btn = tk.Button(janela2, text='Selecionar caso', command=btn_atualizar)
        btn.grid(row=7, column=1, pady=5, padx=10)

        janela2.grid_columnconfigure(1, weight=1)

        btn_voltar = tk.Button(janela2, text="Voltar", command= lambda:[janela.deiconify(), janela2.destroy()])
        btn_voltar.grid(row=7, column=0, pady=5, padx=10)


        #--------------------------------------------proxima tela------------------------------------------------

        def tela_salvar_no_bd():
            janela3 = tk.Tk()
            janela3.title("Salvar Caso")
            janela3.geometry("800x900")

            texto = tk.Label(janela3, text="Salvar Caso", font=("Arial", 20))
            texto.grid(row=0, sticky="n", columnspan=3)
            # Cria uma barra de rolagem vertical
            scrollbar = tk.Scrollbar(janela3, orient="vertical")
            
            texto = tk.Label(janela3, text="CASO NOVO", font=("Arial", 12))
            texto.grid(row=1, sticky="n", columnspan=3, pady=5)

            # Cria um Listbox e associa a barra de rolagem a ele
            treeCasos = ttk.Treeview(janela3, yscrollcommand=scrollbar.set, columns=("H1", "H2"), show="headings")
            treeCasos.heading("H1", text="ATRIBUTO",)
            treeCasos.heading("H2", text="VALOR")
            treeCasos.column("H1", width=150, anchor="center")
            treeCasos.column("H2", width=150, anchor="center")
            treeCasos.grid(row=2, column=0, sticky="nsew", columnspan=3, padx=10)
            scrollbar.grid(row=2, column=1, sticky="ns")
            scrollbar.config(command=treeCasos.yview)

            texto = tk.Label(janela3, text="CASO SELECIONADO", font=("Arial", 12) )
            texto.grid(row=3, sticky="n", columnspan=3, pady=5)

            tree_casos_selecao = ttk.Treeview(janela3, columns=("H1", "H2"), show="headings")
            tree_casos_selecao.heading("H1", text="ATRIBUTO",)
            tree_casos_selecao.heading("H2", text="VALOR")
            tree_casos_selecao.column("H1", width=150, anchor="center")
            tree_casos_selecao.column("H2", width=150, anchor="center")
            tree_casos_selecao.grid(row=4, column=0, sticky="nsew", columnspan=3, padx=10)
            scrollbar.grid(row=4, column=1, sticky="ns")
            scrollbar.config(command=tree_casos_selecao.yview)



            for atributo in atributos:
                nome_valores = []
                nome_valores.clear()
                for i in range(len(novo_caso)):
                    if novo_caso[i] is None:
                        nome_valores.append("?")
                    else:
                        nome_valores.append(d_nome_valores[i][novo_caso[i]])

                treeCasos.insert("", "end", values=(atributo, nome_valores[atributos.index(atributo)]))
                

            def atualizar_treeview(valor_selecionado):
                tree_casos_selecao.delete(*tree_casos_selecao.get_children())
                caso_selecionado = sorted(todos_casos, key=lambda x: x[0])
                caso_selecionado = caso_selecionado[valor_selecionado-1]
                caso_selecionado = caso_selecionado[2:]

                nome_valores = []
                nome_valores.clear()
                
                for atributo in atributos:
                    nome_valores = []
                    nome_valores.clear()
                    
                    for i in range(len(caso_selecionado)):
                        if caso_selecionado[i] is None:
                            nome_valores.append("?")
                        else:
                            nome_valores.append(d_nome_valores[i][caso_selecionado[i]])

                    tree_casos_selecao.insert("", "end", values=(atributo, nome_valores[atributos.index(atributo)]))

                
            def btn_atualizar():
                item_selecionado = casos_ordendados[combobox.current()][0] 

                # Se houver um item selecionado, imprima suas informações
                if item_selecionado:                    
                    atualizar_treeview(item_selecionado)
                    return atualizar_texto(item_selecionado)
                else:
                    pass
            
            combobox = ttk.Combobox(janela3, values=[f"{casos_ordendados[0][1]}",f"{casos_ordendados[1][1]}", f"{casos_ordendados[2][1]}", f"{casos_ordendados[3][1]}", f"{casos_ordendados[4][1]}"], state="readonly")
            combobox.current(0)
            combobox.grid(row=5, column=0, pady=5, padx=10)


            def atualizar_texto(item_selecionado):
                for i in range(len(casos_ordendados)):
                    if item_selecionado == casos_ordendados[i][0]:                    
                        texto_selecao.config(text=f"{casos_ordendados[i][1]}")
                        return casos_ordendados[i][1]
                        break

            texto_selecao = tk.Label(janela3, font=("Arial", 12))
            texto_selecao.grid(row=5, column=1, pady=5, padx=10, sticky='n')

            janela3.grid_columnconfigure(1, weight=1)

            btn = tk.Button(janela3, text='Selecionar caso', command=btn_atualizar)
            btn.grid(row=6, column=0, pady=5, padx=100, sticky='w')


            btn_voltar = tk.Button(janela3, text="Voltar", command= lambda:[janela2.deiconify(), janela3.destroy()])
            btn_voltar.grid(row=9, column=0, pady=5, padx=20, sticky='w')

            def popup_salvar_bd():
                nome_caso = btn_atualizar()
                
                def popup_fechar():
                    popup = tk.Toplevel(janela3)
                    popup.title("Salvar Caso")
                    popup.geometry("300x100")
                    salvar_caso(novo_caso, nome_caso)
                    texto = tk.Label(popup, text="O novo caso foi salvo como: " + nome_caso)
                    texto.pack(pady=10)
                    btn_fechar = tk.Button(popup, text="Fechar", command= lambda:[popup.destroy()])
                    btn_fechar.pack(pady=10)
                    popup.grab_set()
                
                popup = tk.Toplevel(janela3)
                popup.title("Salvar Caso")
                popup.geometry("300x100")
                texto_confirm = tk.Label(popup, text="Salvar caso como: " + nome_caso + " ?")
                texto_confirm.pack(pady=10)
                btn_cancelar = tk.Button(popup, text="Cancelar", command= lambda:[popup.destroy()])
                btn_salvar = tk.Button(popup, text="Salvar", command=lambda:[popup.destroy(), popup_fechar()])
                btn_cancelar.pack(side=tk.LEFT, padx=40)
                btn_salvar.pack(side=tk.RIGHT, padx=40)
                popup.grab_set()
                
                
                
                

            btn_salvar = tk.Button(janela3, text="Salvar no Banco", command= lambda : popup_salvar_bd())
            btn_salvar.grid(row=6, column=2, pady=5, padx=100)

            btn_novo_caso = tk.Button(janela3, text="Novo Caso", command= lambda:[janela.deiconify(), janela3.destroy()])
            btn_novo_caso.grid(row=9, column=1, pady=5, padx=5)

            btn_fechar = tk.Button(janela3, text="Fechar", command= lambda:[janela3.destroy(), janela2.destroy(), janela.destroy()])
            btn_fechar.grid(row=9, column=2, pady=5, padx=20, sticky='e')




        btn_nova_janela = tk.Button(janela2, text="proximo", command= lambda:[tela_salvar_no_bd(), janela2.withdraw()])
        btn_nova_janela.grid(row=7, column=2, pady=5, padx=10)

    # proxima tela
    btn_nova_janela = tk.Button(janela, text="proximo", command= lambda:[tela_casos_similares(), janela.withdraw()])
    btn_nova_janela.pack(side=tk.BOTTOM, pady=20, padx=20)


    frame.update_idletasks()  
    canvas.config(scrollregion=canvas.bbox("all"))

    janela.mainloop()


tela_selecao_atributos()