# -----------------------------
# 1. Importações
# -----------------------------
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt
import sys
import re
import cadastro_dao


# -----------------------------
# 2. Classe MinhaJanela
# -----------------------------
class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        cadastro_dao.configurar_banco_de_dados()
        self.configurar_interface()              

    def configurar_interface(self):
        """Inicializa a interface do usuário e elementos da UI."""
        uic.loadUi('cadastro_clientes.ui', self)
        self.conectar_eventos()
        self.configurar_campos(True, False)
        self.configurar_tabela()
        self.atualizar_combobox()
        self.bt_editar.setEnabled(False)
        self.bt_excluir.setEnabled(False)
        self.bt_editar.setStyleSheet(self.estilo_bt_grey())
        self.bt_excluir.setStyleSheet(self.estilo_bt_grey())

    def configurar_tabela(self):
        """Configura as propriedades iniciais da tabela."""
        colunas = [10, 360, 100, 148]
        for i, largura in enumerate(colunas):
            self.tb_cadastros.setColumnWidth(i, largura) 
        self.tb_cadastros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def conectar_eventos(self):
        """Conecta os eventos aos seus respectivos métodos."""
        self.cb_nome.currentIndexChanged.connect(self.atualizar_tabela_filtrada)
        self.tb_cadastros.cellDoubleClicked.connect(self.preencher_campos)
        self.ln_nome.textChanged.connect(self.transformar_em_maiuscula)
        self.rdb_fisica.toggled.connect(lambda: self.configurar_campos(True, False))
        self.rdb_juridica.toggled.connect(lambda: self.configurar_campos(False, True))

        self.bt_salvar.clicked.connect(self.cadastrar)
        self.bt_editar.clicked.connect(self.editar)
        self.bt_excluir.clicked.connect(self.excluir)

    def transformar_em_maiuscula(self):
        """Transforma o texto do campo 'ln_nome' em letras maiúsculas."""
        texto = self.ln_nome.text()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            self.ln_nome.setText(texto_maiusculo)

    def configurar_campos(self, cpf_visivel, cnpj_visivel):
        """Configura a visibilidade dos campos com base na escolha do tipo de pessoa (Física ou Jurídica)."""
        self.lb_cpf.setVisible(cpf_visivel)
        self.ln_cpf.setVisible(cpf_visivel)
        self.lb_cnpj.setVisible(cnpj_visivel)
        self.ln_cnpj.setVisible(cnpj_visivel)
        self.rd_botao()
        self.ln_nome.setFocus(True)


    def rd_botao(self):
        if self.rdb_fisica.isChecked():
            self.ln_cnpj.setText("")
        if self.rdb_juridica.isChecked():
            self.ln_cpf.setText("")

    def atualizar_combobox(self):
        """Atualiza o ComboBox com os nomes do banco de dados."""
        try:
            # Consulta o banco de dados para obter a lista de nomes
            nomes = cadastro_dao.listar_nomes()
            
            # Verifica se a consulta ao banco de dados retornou uma lista vazia ou None
            if not nomes:
                print("Nenhum nome encontrado para preencher o ComboBox.")
                return

            # Limpa o ComboBox para prepará-lo para atualização
            self.cb_nome.clear()
            
            # Adiciona uma opção 'Todos' para permitir seleção completa no ComboBox
            self.cb_nome.addItem("Selecione um Cadastro para Edição")
            
            # Preenche o ComboBox com a lista de nomes
            self.cb_nome.addItems(nomes)
            
        except Exception as e:
            print(f"Ocorreu um erro durante a atualização do ComboBox: {e}")

    def validacao_mascara(self):
        nome = self.ln_nome.text()
        cpf = self.ln_cpf.text()
        cnpj = self.ln_cnpj.text()
        
        if not re.search(r"\d", cpf):
            cpf = ""
        if not re.search(r"\d", cnpj):
            cnpj = ""
        print(nome, cpf, cnpj)

        return nome,cpf,cnpj

    def cadastrar(self):
        """Realiza o cadastro de uma nova pessoa."""
        try:
            nome, cpf, cnpj = self.validacao_mascara()          
            
            # Assume que a função cadastrar() no módulo cadastro_dao lança uma exceção se algo der errado
            cadastro_dao.cadastrar(nome, cpf, cnpj)
            
            print("Cadastro realizado")
            self.limpar_dados()
            self.atualizar_combobox()
            
        except Exception as e:
            print(f"Ocorreu um erro durante o cadastro: {e}")

    def limpar_dados(self):
        """Limpa os campos de texto da interface."""
        self.ln_nome.setText("")
        self.ln_cpf.setText("")
        self.ln_cnpj.setText("")

    def atualizar_tabela_filtrada(self):
        """Atualiza a tabela com base no nome selecionado no ComboBox."""
        try:
            # Obtém o nome selecionado no ComboBox
            nome_selecionado = self.cb_nome.currentText()
            
            # Limpa a tabela antes de preenchê-la
            self.tb_cadastros.setRowCount(0)
            
            # Tenta obter registros filtrados do banco de dados
            registros = cadastro_dao.filtro_listar_dados(nome_selecionado)
                        
            # Preenche a tabela com registros
            for i, registro in enumerate(registros):
                self.tb_cadastros.insertRow(i)
                for j, dado in enumerate(registro):
                    item_tabela = QTableWidgetItem(str(dado))
                    self.tb_cadastros.setItem(i, j, item_tabela)
                    
        except Exception as e:
            print(f"Ocorreu um erro durante a atualização da tabela filtrada: {e}")


    def preencher_campos(self, linha):

        self.limpar_dados()
        """Preenche os campos com os dados da linha selecionada na tabela."""
        id_registro = self.tb_cadastros.item(linha, 0).text() if self.tb_cadastros.item(linha, 0) else ""
        nome = self.tb_cadastros.item(linha, 1).text() if self.tb_cadastros.item(linha, 1) else ""
        cpf = self.tb_cadastros.item(linha, 2).text() if self.tb_cadastros.item(linha, 2) else ""
        cnpj = self.tb_cadastros.item(linha, 3).text() if self.tb_cadastros.item(linha, 3) else ""

        if cpf != "" and cnpj == "":
            self.rdb_fisica.setChecked(True)            
        else:
            self.rdb_juridica.setChecked(True)

        self.ln_nome.setText(nome)
        self.ln_cpf.setText(cpf)
        self.ln_cnpj.setText(cnpj)
        self.id_registro_selecionado = id_registro  # Armazena o ID para uso posterior
        self.ln_nome.setFocus(True)
        self.bt_salvar.setEnabled(False)
        self.bt_editar.setEnabled(True)
        self.bt_excluir.setEnabled(True)
        self.bt_salvar.setStyleSheet(self.estilo_bt_grey())
        self.bt_editar.setStyleSheet(self.estilo_bt_editar())
        self.bt_excluir.setStyleSheet(self.estilo_bt_excluir())

    def estilo_botoes(self):
        self.bt_salvar.setEnabled(True)
        self.bt_editar.setEnabled(False)
        self.bt_excluir.setEnabled(False)
        self.bt_editar.setStyleSheet(self.estilo_bt_grey())
        self.bt_excluir.setStyleSheet(self.estilo_bt_grey())
        self.bt_salvar.setStyleSheet(self.estilo_bt_salvar())
        self.rdb_fisica.setChecked(True)
        


    def estilo_bt_salvar(self):
        self.estilo = """
            QPushButton {
                background-color: rgb(46, 194, 126);
                color: rgb(255, 255, 255);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgb(87, 227, 137);
            }
            """
        return self.estilo
    
    def estilo_bt_grey(self):
        self.estilo = """
            QPushButton {
                background-color: grey; 
                color: rgb(255, 255, 255);
                border-radius: 10px;
            }
            """
        return self.estilo

    def estilo_bt_editar(self):
        self.estilo = """
            QPushButton{	
                background-color: rgb(28, 113, 216);
                color: rgb(255, 255, 255);
                border-radius: 10px;
            }
            QPushButton:hover {	
                background-color: rgb(98, 160, 234);
            }
            """
        return self.estilo
            

    def estilo_bt_excluir(self):
        self.estilo = """
            QPushButton {
                background-color: rgb(192, 28, 40);
                color: rgb(255, 255, 255);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgb(246, 97, 81);
            }
            """
        return self.estilo

    def editar(self):
        """Edita o registro selecionado."""
        print(f"ID de Registro Selecionado: {self.id_registro_selecionado}")  # Depuração
        id_registro = self.id_registro_selecionado
        
        nome, cpf, cnpj = self.validacao_mascara()

        try:
            cadastro_dao.editar(id_registro, nome, cpf, cnpj)
            print("Registro atualizado com sucesso!")
            self.limpar_dados()
            self.atualizar_combobox()
            
        except Exception as e:
            print(f"Erro ao atualizar registro: {e}")        

        self.estilo_botoes()

    def excluir(self):
        """Exclui o registro selecionado."""
        try:
            id_registro = self.id_registro_selecionado
            if id_registro:
                cadastro_dao.excluir(id_registro)
                print(f"Registro com ID {id_registro} foi excluído com sucesso!")
                self.limpar_dados()
                self.atualizar_combobox()
            else:
                print("Nenhum registro selecionado para exclusão.")
        except Exception as e:
            print(f"Erro ao excluir registro: {e}")

        self.bt_salvar.setEnabled(True)
        self.bt_editar.setEnabled(False)
        self.bt_excluir.setEnabled(False)
        self.bt_editar.setStyleSheet(self.estilo_bt_grey())
        self.bt_excluir.setStyleSheet(self.estilo_bt_grey())
        self.bt_salvar.setStyleSheet(self.estilo_bt_salvar())
        self.rdb_fisica.setChecked(True)


# -----------------------------
# 3. Inicialização
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec_())
