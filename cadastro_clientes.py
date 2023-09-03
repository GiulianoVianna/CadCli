# -----------------------------
# Importações
# -----------------------------
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox
import sys
import re
import cadastro_dao


# -----------------------------
# Classe MinhaJanela
# -----------------------------
class MinhaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        cadastro_dao.configurar_banco_de_dados()
        self.configurar_interface()    

# -----------------------------
# Configuração de estilo de botões
# -----------------------------          

    def configurar_botoes_gerais(self, salvar_ativo, editar_ativo, excluir_ativo, estilo_salvar, estilo_editar, estilo_excluir):
        self.configurar_botoes_estilo_e_estado(self.bt_salvar, salvar_ativo, estilo_salvar)
        self.configurar_botoes(editar_ativo, excluir_ativo, estilo_editar, estilo_excluir)

# -----------------------------
# Configuração de estilo de botões
# -----------------------------

    def configurar_botoes_estilo_e_estado(self, botao, estado, estilo):
        botao.setEnabled(estado)
        botao.setStyleSheet(estilo)

# -----------------------------
# Chama a função dos botões editar e excluir
# -----------------------------

    def configurar_botoes(self, editar_ativo, excluir_ativo, estilo_editar, estilo_excluir):
        self.configurar_botoes_estilo_e_estado(self.bt_editar, editar_ativo, estilo_editar)
        self.configurar_botoes_estilo_e_estado(self.bt_excluir, excluir_ativo, estilo_excluir)

# -----------------------------
# Inicializa a interface do usuário e elementos da UI.
# -----------------------------

    def configurar_interface(self):
        uic.loadUi('cadastro_clientes.ui', self)
        self.conectar_eventos()
        self.configurar_campos(True, False)
        self.configurar_tabela()
        self.atualizar_combobox()
        self.configurar_botoes(False, False, self.estilo_bt_grey(), self.estilo_bt_grey())
        self.bt_excluir.setEnabled(False)
        self.bt_editar.setStyleSheet(self.estilo_bt_grey())
        self.bt_excluir.setStyleSheet(self.estilo_bt_grey())

# -----------------------------
# Configura as propriedades iniciais da tabela.
# -----------------------------

    def configurar_tabela(self):
        colunas = [10, 360, 100, 148]
        for i, largura in enumerate(colunas):
            self.tb_cadastros.setColumnWidth(i, largura) 
        self.tb_cadastros.setEditTriggers(QAbstractItemView.NoEditTriggers)

# -----------------------------
# Conecta os eventos aos seus respectivos métodos.
# -----------------------------
        
    def conectar_eventos(self):
        self.cb_nome.currentIndexChanged.connect(self.atualizar_tabela_filtrada)
        self.tb_cadastros.cellDoubleClicked.connect(self.preencher_campos)
        self.ln_nome.textChanged.connect(self.transformar_em_maiuscula)
        self.rdb_fisica.toggled.connect(lambda: self.configurar_campos(True, False))
        self.rdb_juridica.toggled.connect(lambda: self.configurar_campos(False, True))
        self.bt_salvar.clicked.connect(self.cadastrar)
        self.bt_editar.clicked.connect(self.editar)
        self.bt_excluir.clicked.connect(self.excluir)

# -----------------------------
# Atualiza estilo botão salvar.
# -----------------------------    

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
    
# -----------------------------
# Atualiza estilo genério dos botões.
# -----------------------------
    
    def estilo_bt_grey(self):
        self.estilo = """
            QPushButton {
                background-color: grey; 
                color: rgb(255, 255, 255);
                border-radius: 10px;
            }
            """
        return self.estilo
    
# -----------------------------
# Atualiza o estilo do botão excluir.
# -----------------------------

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
            
# -----------------------------
# Atualiza estilo do botão excluir.
# -----------------------------

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

# -----------------------------
# Transforma o texto do campo 'ln_nome' em letras maiúsculas.
# -----------------------------

    def transformar_em_maiuscula(self):
        texto = self.ln_nome.text()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            self.ln_nome.setText(texto_maiusculo)

# -----------------------------
# Criar e exibir a caixa de diálogo
# -----------------------------

    def mensagem(self, icone, titulo, texto):
        msg = QMessageBox(icone, titulo, texto)
        msg.exec_()

# -----------------------------
# Configura a visibilidade dos campos com base na escolha do tipo de pessoa (Física ou Jurídica).
# -----------------------------

    def configurar_campos(self, cpf_visivel, cnpj_visivel):
        self.lb_cpf.setVisible(cpf_visivel)
        self.ln_cpf.setVisible(cpf_visivel)
        self.lb_cnpj.setVisible(cnpj_visivel)
        self.ln_cnpj.setVisible(cnpj_visivel)
        self.rd_botao()
        self.ln_nome.setFocus(True)

# -----------------------------
# Valida o tipo de cadastro. Obs: se for pessoa física o campo cnpj = ""
# -----------------------------

    def rd_botao(self):
        if self.rdb_fisica.isChecked():
            self.ln_cnpj.setText("")
        if self.rdb_juridica.isChecked():
            self.ln_cpf.setText("")

# -----------------------------
# Validaçao do tipo de cadastro, física ou jurídica para habilitar os campos
# -----------------------------

    def validacao_mascara(self):
        nome = self.ln_nome.text()
        cpf = self.ln_cpf.text()
        cnpj = self.ln_cnpj.text()
        
        if not re.search(r"\d", cpf):
            cpf = ""
        if not re.search(r"\d", cnpj):
            cnpj = ""

        return nome,cpf,cnpj
    
# -----------------------------
# Limpa os campos de texto da interface.
# -----------------------------

    def limpar_dados(self):
        self.ln_nome.setText("")
        self.ln_cpf.setText("")
        self.ln_cnpj.setText("")

# -----------------------------
# Validar número de CPF.
# -----------------------------

    def validar_cpf(self, cpf):
        cpf = ''.join(re.findall(r'\d', str(cpf)))
        
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        for i in range(9, 11):
            soma = sum(int(a) * b for a, b in zip(cpf[:i], range(i+1, 1, -1)))
            d = (soma * 10) % 11
            if d == 10:
                d = 0
            if int(cpf[i]) != d:
                return False
        
        return True

# -----------------------------
# Validar número de CNPJ.
# -----------------------------

    def validar_cnpj(self, cnpj):
        cnpj = ''.join(re.findall(r'\d', str(cnpj)))

        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        for i in range(12, 14):
            soma = sum(int(a) * b for a, b in zip(cnpj[:i], pesos[-i:]))
            d = (soma * 10) % 11
            if d == 10:
                d = 0
            if int(cnpj[i]) != d:
                return False
        
        return True
    
# -----------------------------
# Realiza o cadastro de um novo cliente.
# -----------------------------

    def cadastrar(self):
        try:
            nome, cpf, cnpj = self.validacao_mascara()
            
            if not nome.strip():
                self.mensagem(QMessageBox.Warning, "Atenção!", "O campo nome não pode estar vazio.")
                return

            if cpf and not self.validar_cpf(cpf):
                self.mensagem(QMessageBox.Warning, "Atenção!", "O CPF informado é inválido.")
                return

            if cnpj and not self.validar_cnpj(cnpj):
                self.mensagem(QMessageBox.Warning, "Atenção!", "O CNPJ informado é inválido.")
                return

            cadastro_dao.cadastrar(nome, cpf, cnpj)
            self.mensagem(QMessageBox.Information, "Informação!", "Cadastro realizado!")
            self.limpar_dados()
            self.atualizar_combobox()
            self.rdb_fisica.setChecked(True)
            
        except Exception as e:
            self.mensagem(QMessageBox.Critical, "Informação!", f"Ocorreu um erro durante o cadastro: {e}")


# -----------------------------
# Editar o registro selecionado.
# -----------------------------

    def editar(self):
        #print(f"ID de Registro Selecionado: {self.id_registro_selecionado}")  # Depuração
        id_registro = self.id_registro_selecionado
        
        nome, cpf, cnpj = self.validacao_mascara()

        try:
            cadastro_dao.editar(id_registro, nome, cpf, cnpj)
            #print("Registro atualizado com sucesso!")
            self.mensagem(QMessageBox.Information, "Informação!", "Registro atualizado com sucesso!")
            self.limpar_dados()
            self.atualizar_combobox()
            
        except Exception as e:
            #print(f"Erro ao atualizar registro: {e}")
            self.mensagem(QMessageBox.Critical, "Informação!", f"Erro ao atualizar registro: {e}")
                    

        self.configurar_botoes_gerais(True, False, False, self.estilo_bt_salvar(), self.estilo_bt_grey(), self.estilo_bt_grey())
        self.rdb_fisica.setChecked(True)
        self.bt_salvar.setEnabled(True)

# -----------------------------
# Exclui o registro selecionado.
# -----------------------------

    def excluir(self):
        try:
            id_registro = self.id_registro_selecionado
            if id_registro:
                cadastro_dao.excluir(id_registro)
                #print(f"Registro com ID {id_registro} foi excluído com sucesso!")
                self.mensagem(QMessageBox.Information, "Informação!", f"Registro com ID {id_registro} foi excluído com sucesso!")
                self.limpar_dados()
                self.atualizar_combobox()

        except Exception as e:
            #print(f"Erro ao excluir registro: {e}")
            self.mensagem(QMessageBox.Critical, "Informação!", f"Erro ao excluir registro: {e}")

        self.configurar_botoes_gerais(True, False, False, self.estilo_bt_salvar(), self.estilo_bt_grey(), self.estilo_bt_grey())
        self.rdb_fisica.setChecked(True)

# -----------------------------
# Atualiza a tabela com base no nome selecionado no ComboBox.
# -----------------------------

    def atualizar_tabela_filtrada(self):
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
            #print(f"Ocorreu um erro durante a atualização da tabela filtrada: {e}")
            self.mensagem(QMessageBox.Critical, "Informação!", f"Ocorreu um erro durante a atualização da tabela filtrada: {e}")

# -----------------------------
# Preenche os campos com os dados da linha selecionada na tabela.
# -----------------------------

    def preencher_campos(self, linha):

        self.limpar_dados()
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
        self.configurar_botoes_gerais(False, True, True, self.estilo_bt_grey(), self.estilo_bt_editar(), self.estilo_bt_excluir()) 

# -----------------------------
# Atualiza o ComboBox com os nomes do banco de dados.
# -----------------------------

    def atualizar_combobox(self):
        try:
            # Consulta o banco de dados para obter a lista de nomes
            nomes = cadastro_dao.listar_nomes()

            # Limpa o ComboBox para prepará-lo para atualização
            self.cb_nome.clear()
            
            # Adiciona uma opção 'Todos' para permitir seleção completa no ComboBox
            self.cb_nome.addItem("Selecione um Cadastro para Edição")
            
            # Preenche o ComboBox com a lista de nomes
            self.cb_nome.addItems(nomes)
            
        except Exception as e:
            #print(f"Ocorreu um erro durante a atualização do ComboBox: {e}")
            self.mensagem(QMessageBox.Critical, "Informação!", f"Ocorreu um erro durante a atualização do ComboBox: {e}")

# -----------------------------
# Inicialização
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MinhaJanela()
    janela.show()
    sys.exit(app.exec_())
