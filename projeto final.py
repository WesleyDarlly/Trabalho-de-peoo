from tkinter import *
from tkinter import messagebox
import numpy as np
import sqlite3
import pickle
import datetime


class App:
    def __init__(self):
        self.janela = Tk()
        self.janela.geometry('790x800')
        self.janela.title('Sistema de Venda de Passagem')

        self.image = PhotoImage(file="onibus.jpeg") 
        self.image_label = Label(self.canvas1, image=self.image)
        self.image_label.place(x=20, y=0)

        self.canvas1 = Canvas(self.janela, width=790, height=800)
        self.canvas1.pack()

        # Lista de capitais do Brasil
        self.capitais_brasileiras = [
            "Rio Branco", "Maceió", "Macapá", "Manaus", "Salvador", "Fortaleza", "Brasília", "Vitória",
            "Goiânia", "São Luís", "Cuiabá", "Campo Grande", "Belo Horizonte", "Belém", "João Pessoa",
            "Curitiba", "Recife", "Teresina", "Rio de Janeiro", "Natal", "Porto Alegre", "Porto Velho",
            "Boa Vista", "Florianópolis", "São Paulo", "Aracaju", "Palmas"
        ]

       
        
        self.label_identificador_numero = self.criar_label('', 20, 395,  font='Helvetica 15',)

        self.label_numero_aleatorio = self.criar_label('Número da sua passagem: ', 20, 405, font='Helvetica 14 bold')

        self.criar_label('Saindo de:', 20, 100, font='Helvetica 14 bold')
        self.caixaPartindo_de = self.criar_entry(20, 135, 510, font='Helvetica 14 bold', validate='focusout', validatecommand=(self.janela.register(self.verificar_cidade), '%P', 'Saindo de'))

        self.criar_label('Indo para:', 20, 190, font='Helvetica 14 bold')
        self.caixaIndo_para = self.criar_entry(20, 225, 510, font='Helvetica 14 bold', validate='focusout', validatecommand=(self.janela.register(self.verificar_cidade), '%P', 'Indo para'))

        self.criar_label('Data de Saída:', 20, 280, fg='black', font='Helvetica 12 bold')
        self.textoNome1 = self.criar_label('dd/mm/aaaa: ', 20, 315, font='Helvetica 12')
        self.entry_data_saida = self.criar_entry(20, 350, 10, font='Helvetica 14')

        self.criar_label('Data de Retorno:', 300, 280, fg='black', font='Helvetica 12 bold')
        self.textoNome2 = self.criar_label('dd/mm/aaaa: ', 300, 315, font='Helvetica 12')
        self.entry_data_retorno = self.criar_entry(300, 350, 10, font='Helvetica 14')

        self.Button1 = Button(self.canvas1, background='green', font='Arial 12 bold', text='Comprar', command=self.comprar_passagem)
        self.Button1.place(x=100, y=460, height=50, width=130)
        
        self.criar_label('Número da passagem:', 20, 515, font='Helvetica 14 bold')
        self.nomeArq2 = Entry(
            self.canvas1,
            width=21,
            font='Helvetica 14'
        )
        self.nomeArq2.place(x=20,y=550)
        
        

        self.Button2 = Button(self.canvas1, background='blue', font='Arial 12 bold', text='Consultar', command=self.consultar_passagem)
        self.Button2.place(x=200, y=585, height=50, width=130)

        self.Button3 = Button(self.canvas1, background='red', font='Arial 12 bold', text='Deletar', command=self.deletar )
        self.Button3.place(x=0, y=585, height=50, width=130)


        self.janela.mainloop()

    def criar_label(self, text, x, y, **kwargs):
        label = Label(self.canvas1, text=text, **kwargs)
        label.place(x=x, y=y)
        return label

    def criar_entry(self, x, y, width, **kwargs):
        entry = Entry(self.canvas1, width=width, **kwargs)
        entry.place(x=x, y=y, height=40)

        if 'Data' in kwargs.get('font', ''):
            # só para aceitar apenas dígitos e / nos campos de data
            entry.config(validate='key', validatecommand=(self.janela.register(self.validar_entrada_data), '%P'))
        else:
            # deixando possível letras nos campos "Saindo de" e "Indo para"
            entry.config(validate='key', validatecommand=(self.janela.register(self.validar_entrada), '%P'))

        return entry

    def verificar_cidade(self, texto, tipo):
        if texto not in self.capitais_brasileiras:
            messagebox.showinfo('Aviso', f'Digite uma capital válida para o Campo de entrada: {tipo}.')
            return False
        elif tipo == 'Indo para' and texto == self.caixaPartindo_de.get():
            messagebox.showinfo('Aviso', 'A capital de destino não pode ser igual à capital de partida.')
            return False
        elif tipo == 'Saindo de' and texto == self.caixaIndo_para.get():
            messagebox.showinfo('Aviso', 'A capital de partida não pode ser igual à capital de destino.')
            return False
        return True

    def comprar_passagem(self):
        # Verifica se as capitais e datas são válidas
        partida_valida = self.verificar_cidade(self.caixaPartindo_de.get(), 'Saindo de:')
        destino_valido = self.verificar_cidade(self.caixaIndo_para.get(), 'Indo para:')
        data_saida_valida = self.validar_data(self.entry_data_saida.get(), 'Data Saída:')
        data_retorno_valida = self.validar_data(self.entry_data_retorno.get(), 'Data Retorno:')

        if partida_valida and destino_valido and data_saida_valida and data_retorno_valida:
            # Verifica se a data de retorno não é anterior à data de saída
            if self.comparar_datas(self.entry_data_retorno.get(), self.entry_data_saida.get()):

                # Gera um número aleatório usando numpy
                numero_aleatorio = np.random.randint(100000, 999999)
                # Atualiza o label de identificador
                self.label_identificador_numero.config(text=f'{numero_aleatorio}')
                # Atualiza o label do número aleatório
                self.label_numero_aleatorio.config(text=f'O número da sua passagem é: {numero_aleatorio}')

                con = sqlite3.connect('teste.db')
                sql = con.cursor()

                dic = {numero_aleatorio:[self.caixaPartindo_de.get(),self.caixaIndo_para.get(),self.entry_data_saida.get(),self.entry_data_retorno.get(),] }
                b=pickle.dumps(dic)   

                sql.execute('''CREATE TABLE IF NOT EXISTS plau (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, dados BLOB)''')
                sql.execute("INSERT INTO plau (nome,dados) VALUES (?, ?)", (numero_aleatorio,sqlite3.Binary(b),))

                con.commit()
                con.close()
            else:
                # Exibe uma mensagem de erro se a data de retorno for anterior à data de saída
                messagebox.showinfo('Aviso', 'A data de retorno não pode ser anterior à data de saída.')

    def comparar_datas(self, data_retorno, data_saida):
        # Compara as datas e retorna True se a data de retorno for igual ou posterior à data de saída
        try:
            data_retorno = datetime.datetime.strptime(data_retorno, '%d/%m/%Y')
            data_saida = datetime.datetime.strptime(data_saida, '%d/%m/%Y')
            return data_retorno >= data_saida
        except ValueError:
            return False

    def validar_entrada(self, novo_valor):
        # Aceita letras nos campos "Saindo de" e "Indo para"
        return True

    def validar_entrada_data(self, novo_valor):
        # Aceita dígitos e / nos campos de data, ou apenas dígitos
        if novo_valor.count('/') > 1:
            return False
        return all(char.isdigit() or (char == '/') for char in novo_valor) and len(novo_valor) <= 10

    def validar_data(self, data, tipo):
        try:
            # Tentar converter a data para o formato desejado
            datetime.datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            messagebox.showinfo('Aviso', f'Digite uma data válida para o campo de entrada: {tipo} (dd/mm/aaaa).')
            return False
    
    def deletar (self):

        print("Você cancelou essa viagem")
        con = sqlite3.connect('teste.db')
        sql = con.cursor()

        sql.execute("DELETE FROM plau WHERE nome = (?)", (int(self.nomeArq2.get()),))

        con.commit()
        con.close()



    def consultar_passagem(self):
        # Cria uma nova janela para exibir as informações
        janela_consulta = Toplevel(self.janela)
        janela_consulta.title('Consulta de Passagem')

        con = sqlite3.connect('teste.db')
        sql = con.cursor()

        sql.execute("SELECT * FROM plau WHERE nome = (?)", (self.nomeArq2.get(),))

        registros = sql.fetchall()
        registros_index = 0

        resu = None  # Initialize resu with a default value
        while registros_index < len(registros):
            reg = registros[registros_index]
            jou = pickle.loads(reg[2])
            resu = jou.get(int(self.nomeArq2.get()))
            registros_index += 1

        # Check if resu is not None before using it
        if resu is not None:
            # Cria um dicionário com as informações
            info_passagem = {
                'Saindo de': resu[0],
                'Indo para': resu[1],
                'Data de Saída': resu[2],
                'Data de Retorno': resu[3],
                'Número da sua passagem': self.nomeArq2.get()
            }

            # Adiciona labels na nova janela com as informações
            for i, (chave, valor) in enumerate(info_passagem.items()):
                label_info = Label(janela_consulta, text=f'{chave}: {valor}', font='Helvetica 14')
                label_info.grid(row=i, column=0, padx=10, pady=5, sticky=W)
        else:
            messagebox.showinfo('Aviso', f'Passagem com número {self.nomeArq2.get()} não encontrada.')

        con.close()

# Criando uma instância da classe App
aplicacao = App()