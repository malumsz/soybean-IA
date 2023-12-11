import psycopg2 
import PySimpleGUI as sg

class CRUD:
    def __init__(self):
        self.database = "soybean"
        self.user = "postgres"
        self.password = "admin"
        self.host = "localhost"
        self.port = "5432"
        self.table = "tabela_doenca"
        self.conexao = None
        self.cursor = None
        self.atributos = ["caso", "DescDoenca",  "AreaDanificada",  "Lesao",  "HistoricoCorte",  "Data",  "DecadenciaExterna",  "Manchas",  "CorposFrutas",  "VagensFrutas",  "Germinacao",  "Granizo",  "DescoloracaoInterna",  "FolhaDefeituosa",  "FolhaSuave",  "FragmentoFolhas",  "ManchasCirculares",  "TamanhoManchas",  "ManchasMargem",  "Folhas",  "Alojamento",  "CrescimentoMofo",  "Micelio",  "CrescimentoPlanta",  "SuportePlantas",  "Precipitado",  "Raizes",  "Esclerocio",  "Semente",  "SementeDescolorida",  "TamanhoSemente",  "SementeTMT",  "Gravidade",  "Murchando",  "Tronco", "CancroCaule",  "Temperatura"]

    def conectar(self):
        try:
            self.conexao = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conexao.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def desconectar(self):
        self.conexao.close()

    def read(self):
        self.conectar()
        try:
            self.cursor.execute(f"SELECT * FROM {self.table}")
            registros = self.cursor.fetchall()
            return registros
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.desconectar()

    def create(self, caso):
            caso.insert(0, len(self.read()) + 1)
            self.conectar()
            try:
                # Crie uma string de placeholders para os valores
                placeholders = ','.join(['%s'] * len(self.atributos))

                # Construa a instrução SQL com placeholders para os valores
                sql = f"INSERT INTO tabela_doenca ({','.join(self.atributos)}) VALUES ({placeholders})"

                # Execute a instrução SQL com os valores como argumentos separados
                self.cursor.execute(sql, tuple(caso))
                self.conexao.commit()
            except psycopg2.Error as error:
                print(f"Erro ao inserir dados no banco de dados: {error}")
            finally:
                self.desconectar()
