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
        self.conectar_eventos()
        self.configurar_campos(True, False)
        self.atualizar_tabela()
        self.configurar_tabela()
        self.atualizar_combobox()
        

    def configurar_interface(self):
        """Inicializa a interface do usuário e elementos da UI."""
        uic.loadUi('cadastro_clientes.ui', self)
        
        

    def configurar_tabela(self):
        """Configura as propriedades iniciais da tabela."""
        colunas = [10, 360, 100, 130]
        for i, largura in enumerate(colunas):
            self.tb_cadastros.setColumnWidth(i, largura) 
        self.tb_cadastros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def conectar_eventos(self):
        """Conecta os eventos aos seus respectivos métodos."""
        self.cb_nome.currentIndexChanged.connect(self.atualizar_tabela_filtrada)
        self.tb_cadastros.cellDoubleClicked.connect(self.preencher_campos)
        self.ln_nome.textChanged.connect(self.transformar_em_maiuscula)
        self.rdb_fisica.clicked.connect(lambda: self.configurar_campos(True, False))
        self.rdb_juridica.clicked.connect(lambda: self.configurar_campos(False, True))
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
            self.cb_nome.addItem("Todos")
            
            # Preenche o ComboBox com a lista de nomes
            self.cb_nome.addItems(nomes)
            
        except Exception as e:
            print(f"Ocorreu um erro durante a atualização do ComboBox: {e}")

    def validacao_mascara(self):
        nome = self.ln_nome.text()
        cpf = self.ln_cpf.text()
        cnpj = self.ln_cnpj.text()
        
        if not re.search(r"\d", cpf):
            cpf = None
        if not re.search(r"\d", cnpj):
            cnpj = None
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
            self.atualizar_tabela()
            self.atualizar_combobox()
            
        except Exception as e:
            print(f"Ocorreu um erro durante o cadastro: {e}")

    def limpar_dados(self):
        """Limpa os campos de texto da interface."""
        self.ln_nome.setText("")
        self.ln_cpf.setText("")
        self.ln_cnpj.setText("")

    def atualizar_tabela(self):
        """Atualiza a tabela com os dados do banco de dados."""
        try:
            # Desabilita a ordenação para atualizar a tabela
            self.tb_cadastros.setSortingEnabled(False)
            
            # Limpa a tabela
            self.tb_cadastros.setRowCount(0)

            # Pega os registros do banco de dados
            registros = cadastro_dao.listar_dados()

            if registros is None:
                print("Nenhum registro encontrado.")
                return

            for i, registro in enumerate(registros):
                # Insere uma nova linha na tabela
                self.tb_cadastros.insertRow(i)
                #print(i)

                # Preenche as células com os dados dos registros
                for j, dado in enumerate(registro):
                    # QTableWidgetItem converte o dado para um objeto que o QTableWidget pode exibir
                    item_tabela = QTableWidgetItem(str(dado))
                    self.tb_cadastros.setItem(i, j, item_tabela)
                    print(i, j)

            # Habilita a ordenação e ordena pela coluna de nomes
            self.tb_cadastros.setSortingEnabled(True)
            self.tb_cadastros.sortByColumn(1, Qt.AscendingOrder)
            

        except Exception as e:
            print(f"Um erro ocorreu durante a atualização da tabela: {e}")


    def atualizar_tabela_filtrada(self):
        """Atualiza a tabela com base no nome selecionado no ComboBox."""
        try:
            # Obtém o nome selecionado no ComboBox
            nome_selecionado = self.cb_nome.currentText()
            
            # Limpa a tabela antes de preenchê-la
            self.tb_cadastros.setRowCount(0)
            
            # Tenta obter registros filtrados do banco de dados
            registros = cadastro_dao.filtro_listar_dados(nome_selecionado)
            
            # Verifica se a consulta ao banco de dados retornou uma lista vazia ou None
            if not registros:
                print("Nenhum registro encontrado para preencher a tabela.")
                return
            
            # Preenche a tabela com registros
            for i, registro in enumerate(registros):
                self.tb_cadastros.insertRow(i)
                for j, dado in enumerate(registro):
                    item_tabela = QTableWidgetItem(str(dado))
                    self.tb_cadastros.setItem(i, j, item_tabela)
                    
        except Exception as e:
            print(f"Ocorreu um erro durante a atualização da tabela filtrada: {e}")


    def preencher_campos(self, linha):
        """Preenche os campos com os dados da linha selecionada na tabela."""
        id_registro = self.tb_cadastros.item(linha, 0).text() if self.tb_cadastros.item(linha, 0) else ""
        nome = self.tb_cadastros.item(linha, 1).text() if self.tb_cadastros.item(linha, 1) else ""
        cpf = self.tb_cadastros.item(linha, 2).text() if self.tb_cadastros.item(linha, 2) else ""
        cnpj = self.tb_cadastros.item(linha, 3).text() if self.tb_cadastros.item(linha, 3) else ""

        self.ln_nome.setText(nome)
        self.ln_cpf.setText(cpf)
        self.ln_cnpj.setText(cnpj)

        self.id_registro_selecionado = id_registro  # Armazena o ID para uso posterior
        self.ln_nome.setFocus(True)
        self.bt_salvar.setEnabled(False)


    def editar(self):
        """Edita o registro selecionado."""
        print(f"ID de Registro Selecionado: {self.id_registro_selecionado}")  # Depuração
        id_registro = self.id_registro_selecionado
        
        nome, cpf, cnpj = self.validacao_mascara()

        try:
            cadastro_dao.editar(id_registro, nome, cpf, cnpj)
            print("Registro atualizado com sucesso!")
            self.atualizar_tabela()
            
        except Exception as e:
            print(f"Erro ao atualizar registro: {e}")

        
        self.limpar_dados()
        self.atualizar_combobox()
        self.bt_salvar.setEnabled(True)
        self.rdb_fisica.setChecked(True)

    def excluir(self):
        """Exclui o registro selecionado."""
        print("")

# -----------------------------
# 3. Inicialização
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec_())
