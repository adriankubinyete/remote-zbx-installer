import time
import paramiko
from tkinter import *
#from tkinter.ttk import *



# PACOTES NECESSÁRIOS:
# Python 3.10 Microsoft (VSudio)
# https://www.python.org/downloads/ (atualmente 3.11.1)
# pip install paramiko
#

# VERSÃO 2.0
# implementação do código no TKINTER


# <@------------------------------------------------------------------------@>
# GUI

root = Tk()
root.title("Auto Install Zabbix")

# DIMENSÕES
LARGURA_APP = 500
ALTURA_APP = 400
DEFAULT_PADX = 60
DEFAULT_PADY = 20
SHORT_PADX = 10
SHORT_PADY = 8
LONG_PADX = 80
LONG_PADY = 25
# DIMENSOES DO SISTEMA
LARGURA_TELA = root.winfo_screenwidth()
ALTURA_TELA = root.winfo_screenheight()
# POSIÇÃO DA JANERA
POS_X = LARGURA_TELA/2 - LARGURA_APP/2
POS_Y = ALTURA_TELA/2 - ALTURA_APP/2
# GEOMETRIA
root.geometry("%dx%d+%d+%d" % (LARGURA_APP, ALTURA_APP, POS_X, POS_Y))
root.resizable(False, False)
root.wm_attributes('-transparentcolor', '#add123')
#root.minsize(LARGURA_APP, ALTURA_APP)
#root.maxsize()

# <@------------------------------------------------------------------------@>
# Frames POR CLASSE

class Menu_Principal_Get_Host_Info(Frame):

    def __init__(self, *args, **kwargs):
        global root
        super().__init__(*args, **kwargs)
        self.grid_propagate(False) # permite resize da janela, resize esse feito nos kwargs
        self.master.title("ZBX/Installer - Menu Inicial")
        self.initUI()

    def initUI(self):
        global menu_principal

        # /--------------------------------------------------------/ APP INFO
        #self.master.title("ZBX/Installer - Menu Inicial")
        #self.grid_rowconfigure(4,minsize=ALTURA_APP, weight=1) # CONSTANTE "ALTURA_APP"
        # /--------------------------------------------------------/ FRAME WIDGETS
        
        #
        frame_conteudo=Frame(self, bg='purple')
        frame_footer=Frame(self, bg='green')
        #
        
        # ---------------------- HOSTNAME
        frame_hostname = Frame(frame_conteudo, bg='red', width=MENU_PRINCIPAL_WIDTH-(MENU_PRINCIPAL_PADX*3),height=21)
        frame_hostname.grid_columnconfigure(0, weight=1)
        frame_hostname.grid_columnconfigure(1, weight=9)
        frame_hostname.grid_propagate(0)
        # HOSTNAME (Widgets)
        label_hostname = Label( 
            frame_hostname, 
            text="ZBX/Hostname:",
            width=15,
            anchor=W)
        entry_hostname = Entry(frame_hostname)
        # HOSTNAME (Grid)
        label_hostname.grid(row = 0, column=0, sticky='EW')
        entry_hostname.grid(row = 0, column=1, sticky='EW')


        # ---------------------- HOST
        frame_host = Frame(frame_conteudo, bg='blue', width=MENU_PRINCIPAL_WIDTH-(MENU_PRINCIPAL_PADX*3),height=21)
        frame_host.grid_columnconfigure(0, weight=1)
        frame_host.grid_columnconfigure(1, weight=9)
        frame_host.grid_propagate(0)
        # HOST (Widgets)
        label_host = Label(
            frame_host, 
            text="SSH/Host:",
            width=15,
            anchor=W)
        entry_host = Entry(frame_host)
        # HOST (Grid)
        label_host.grid(row = 0, column=0, sticky='EW')
        entry_host.grid(row = 0, column=1, sticky='EW')

        # ---------------------- PORTA
        frame_porta = Frame(frame_conteudo, bg='yellow', width=MENU_PRINCIPAL_WIDTH-(MENU_PRINCIPAL_PADX*3),height=21)
        frame_porta.grid_columnconfigure(0, weight=1)
        frame_porta.grid_columnconfigure(1, weight=9)
        frame_porta.grid_propagate(0)
        # PORTA (Widgets)
        label_porta = Label(
            frame_porta, 
            text="SSH/Port:",
            width=15,
            anchor=W)
        entry_porta = Entry(frame_porta)
        # PORTA (Grid)
        label_porta.grid(row = 0, column=0, sticky='EW')
        entry_porta.grid(row = 0, column=1, sticky='EW')

        # ---------------------- USERNAME
        frame_username = Frame(frame_conteudo, bg='green', width=MENU_PRINCIPAL_WIDTH-(MENU_PRINCIPAL_PADX*2),height=21)
        frame_username.grid_columnconfigure(0, weight=1)
        frame_username.grid_columnconfigure(1, weight=9)
        frame_username.grid_propagate(0)
        # USERNAME (Widgets)
        label_username = Label(
            frame_username, 
            text="SSH/User:",
            width=15,
            anchor=W)
        entry_username = Entry(frame_username)
        # USERNAME (Grid)
        label_username.grid(row=0, column=0, sticky='EW')
        entry_username.grid(row=0, column=1, sticky='EW')

        # ---------------------- BOTTOM PART OF APP (TWO BUTTONS)
        frame_bottom_buttons = Frame(frame_footer, width=MENU_PRINCIPAL_WIDTH, height=21) #---------------------------<<<
        frame_bottom_buttons.configure(bg='purple')
        frame_bottom_buttons.grid_rowconfigure(0, weight=1)
        frame_bottom_buttons.grid_columnconfigure(0, weight=5)
        frame_bottom_buttons.grid_columnconfigure(1, weight=5)
        frame_bottom_buttons.grid_propagate(False)
        # BOTTOM (Widgets)
        cmd_via_senha = Button(
            frame_bottom_buttons, 
            text="Acessar via Senha",
            command=lambda: via_senha_click(entry_hostname.get(), entry_host.get(), entry_porta.get(), entry_username.get()))
        cmd_via_chave = Button(
            frame_bottom_buttons, 
            text="Acessar via Chave", 
            command=lambda: via_chave_click(entry_hostname.get(), entry_host.get(), entry_porta.get(), entry_username.get()))
        # BOTTOM (Grid)
        cmd_via_senha.grid(row=5, column=0, sticky='SEW')
        cmd_via_chave.grid(row=5, column=1, sticky='SEW')


        # /--------------------------------------------------------/ self WIDGETS
        

        # /----------/ LAYOUT


        # FRAME SELF

        # FRAME DE SELF.CONTEUDO
        frame_hostname.grid(row=0, column=0, padx=5, pady=(5,3), columnspan=2, sticky = 'EW')
        frame_host.grid(row=1, column=0, padx=5, pady=(0,3), columnspan=2, sticky = 'EW')
        frame_porta.grid(row=2, column=0, padx=5, pady=(0,3), columnspan=2, sticky = 'EW')
        frame_username.grid(row=3, column=0, padx=5, pady=(0,3), columnspan=2, sticky = 'EW')
        frame_conteudo.grid(row=0, column=0, sticky='NEW')
        
        # FRAME DO SELF.FOOTER
        frame_bottom_buttons.grid(row=4, column=0, padx=5, pady=(0,5), columnspan=3, sticky='SEW')
        frame_footer.grid(row=1, column=0, sticky='SEW')
        
        self.rowconfigure(0, weight=8)
        self.rowconfigure(1, weight=2)

        

class Menu_Via_Chave(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.initUI()

    def initUI(self):
        
        # /--------------------------------------------------------/ APP INFO
        self.master.title("ZBX/Installer - Autenticação via Chave")
        # /--------------------------------------------------------/ WIDGETS
        text_chave_pathatual = StringVar()
        text_chave_pathatual.set(f"O key path atual é: {key}")

        label_chave_pathatual = Label(self, textvariable=text_chave_pathatual)
        label_chave_mudarkeypath = Label(self, text="KEYPATH:")

        entry_chave_mudarkeypath = Entry(self)

        button_chave_mudarkeypath = Button(
            self, 
            text="ATUALIZAR", 
            command=lambda: chave_mudarkeypath_click(entry_chave_mudarkeypath.get(),text_chave_pathatual))
        button_chave_voltar = Button(
            self, 
            text="Voltar", 
            command=chave_voltar_click)
        button_chave_continuar = Button(
            self, 
            text="Continuar", 
            command=chave_continuar_click)

        # /--------------------------------------------------------/ LAYOUT
        label_chave_pathatual.grid(row=0, column=0, columnspan=2)

        label_chave_mudarkeypath.grid(row=1, column=0, sticky=E)
        entry_chave_mudarkeypath.grid(row=1, column=1)
        button_chave_mudarkeypath.grid(row=1, column=2, sticky=W)

        button_chave_voltar.grid(row=2, column=0)
        button_chave_continuar.grid(row=2, column=2)

class Menu_Via_Senha(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.initUI()

    def initUI(self):
        # /--------------------------------------------------------/ APP INFO
        self.master.title("ZBX/Installer - Autenticação via Senha")
        # /--------------------------------------------------------/ WIDGET
        label_senha_digite = Label(self, text="Senha:")
        entry_senha_digite = Entry(self, show="*")

        button_senha_voltar = Button(self, text="Voltar", command=senha_voltar_click)
        button_senha_continuar = Button(self, text="Continuar", command=lambda: senha_continuar_click(entry_senha_digite.get()))

        # /--------------------------------------------------------/ LAYOUT
        label_senha_digite.grid(row=0, column=0)
        entry_senha_digite.grid(row=0, column=1)

        button_senha_voltar.grid(row=1, column=0)
        button_senha_continuar.grid(row=1, column=1)

class Menu_Confirmacao(Frame):
    def __init__(self, *args, **kwargs):
        global hostname, host, porta, username, key
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.tvar_confirm_hostname = StringVar()
        self.tvar_confirm_host = StringVar()
        self.tvar_confirm_porta = StringVar()
        self.tvar_confirm_username = StringVar()
        self.tvar_confirm_keypath = StringVar()
        self.initUI()

    def update(self): # // Atualiza as text variables com os valores globais
        global hostname, host, porta, username, key
        self.tvar_confirm_hostname.set(hostname)
        self.tvar_confirm_host.set(host)
        self.tvar_confirm_porta.set(porta)
        self.tvar_confirm_username.set(username)
        self.tvar_confirm_keypath.set(key)

    def initUI(self):
        # /--------------------------------------------------------/ APP INFO
        self.master.title("ZBX/Installer - test")
        # /--------------------------------------------------------/ WIDGET
        label_confirm_text_hostname = Label(self, text="ZBX/HOSTNAME")
        label_confirm_text_host = Label(self, text="SSH/HOST")
        label_confirm_text_porta = Label(self, text="SSH/PORTA:") 
        label_confirm_text_username = Label(self, text="SSH/USERNAME:")
        label_confirm_text_keypath = Label(self, text="SSH/KEYPATH:")

        label_confirm_value_hostname = Label(self, textvariable=self.tvar_confirm_hostname)
        label_confirm_value_host = Label(self, textvariable=self.tvar_confirm_host)
        label_confirm_value_porta = Label(self, textvariable=self.tvar_confirm_porta)
        label_confirm_value_username = Label(self, textvariable=self.tvar_confirm_username)
        label_confirm_value_keypath = Label(self, textvariable=self.tvar_confirm_keypath)

        button_confirm_retornar = Button(self, text="Reconfigurar", command=confirm_reconfigurar_click)
        button_confirm_instalar = Button(self, text="Instalar", command=confirm_instalar_click)

        # /--------------------------------------------------------/ LAYOUT
        label_confirm_text_hostname.grid(row=0, column=0)
        label_confirm_text_host.grid(row=1, column=0)
        label_confirm_text_porta.grid(row=2, column=0)
        label_confirm_text_username.grid(row=3, column=0)
        label_confirm_text_keypath.grid(row=4, column=0)

        label_confirm_value_hostname.grid(row=0, column=1)
        label_confirm_value_host.grid(row=1, column=1)
        label_confirm_value_porta.grid(row=2, column=1)
        label_confirm_value_username.grid(row=3, column=1)
        label_confirm_value_keypath.grid(row=4, column=1)

        button_confirm_retornar.grid(row=5, column=0)
        button_confirm_instalar.grid(row=5, column=1)

# <@------------------------------------------------------------------------@>
# Funções

# Local da public key para auth (pode ser alterado no Menu)
key = "C:\\Users\\Operação 03\\.ssh\\id_rsa.pub"
# IP do servidor zabbix (public ip)
ipzserver = '189.124.85.75'

hostname = None
host = None
porta = None
username = None
senha = None


def atualizar_texto_confirmacao():
    menu_confirmacao.update()
    # atualiza os valores exibidos no menu de confirmação
    # deve ser chamado ANTES de entrar no menu de confirmação (antes de gridá-lo)


# MENU VIA SENHA ------------------------------------
def via_senha_click(c_hostname, c_host, c_porta, c_username):
    global hostname
    global host
    global porta
    global username
    hostname = c_hostname
    host = c_host
    porta = c_porta
    username = c_username
    menu_principal.grid_forget()

    menu_via_senha.grid()
    # do menu principal escolheu ir pro menu de senha

    

def senha_continuar_click(c_senha):
    global senha
    senha = c_senha
    menu_via_senha.grid_forget()
    atualizar_texto_confirmacao()
    menu_confirmacao.grid()
    # atualiza a variável senha e envia pro menu de confirmação

def senha_voltar_click():
    menu_via_senha.grid_forget()
    menu_principal.grid()
    # envia pro menu principal




# MENU VIA CHAVE ------------------------------------
def via_chave_click(c_hostname, c_host, c_porta, c_username):
    global hostname
    global host
    global porta
    global username
    hostname = c_hostname
    host = c_host
    porta = c_porta
    username = c_username
    menu_principal.grid_forget()

    menu_via_chave.grid()
    # do menu principal escolheu ir pro menu de chaves.


def chave_mudarkeypath_click(novo_keypath, textvar):
    global key
    key = novo_keypath
    textvar.set(f"O key path atual é: {key}")
    # atualiza o valor da variavel key

def chave_continuar_click():
    menu_via_chave.grid_forget()
    atualizar_texto_confirmacao()
    menu_confirmacao.grid()
    # envia pro menu de confirmação

def chave_voltar_click():
    menu_via_chave.grid_forget()
    menu_principal.grid()
    # envia pro menu principal




# MENU CONFIRMAÇÃO ------------------------------------
def confirm_reconfigurar_click():
    menu_confirmacao.grid_forget()
    menu_principal.grid()
    # envia pro menu principal


def confirm_instalar_click():
    print("INSTALAR CLICK")
    # envia para o menu, display de instalação.

# <@------------------------------------------------------------------------@>
# Styling

#s = Style()
#s.configure('Principal.TFrame', width=20, height=20, background='#3A3845') # grey-ish
#s.configure('Principal.TFrame', width=20, height=20, background='#FF0000') # red
#s.configure('PrincipalInner.TFrame', width = 100, height = 10, background ='#F7CCAC') # latte-ish

# <@------------------------------------------------------------------------@>
# Widgets
MENU_PRINCIPAL_WIDTH = LARGURA_APP
MENU_PRINCIPAL_HEIGHT = ALTURA_APP

MENU_PRINCIPAL_PADX = SHORT_PADX
MENU_PRINCIPAL_PADY = SHORT_PADY

#menu_principal = Menu_Principal_Get_Host_Info(style='Principal.TFrame', width=LARGURA_APP-(MENU_PRINCIPAL_PADX*2), height=ALTURA_APP-(MENU_PRINCIPAL_PADY*2))
#menu_principal = Menu_Principal_Get_Host_Info(width=LARGURA_APP-(MENU_PRINCIPAL_PADX*2), height=ALTURA_APP-(MENU_PRINCIPAL_PADY*2), bg='grey')
menu_principal = Menu_Principal_Get_Host_Info(width=MENU_PRINCIPAL_WIDTH-((MENU_PRINCIPAL_PADX*2)-MENU_PRINCIPAL_PADX), height=MENU_PRINCIPAL_HEIGHT-(MENU_PRINCIPAL_PADY*3), bg='#add8e6')



menu_via_chave = Menu_Via_Chave()

menu_via_senha = Menu_Via_Senha()

menu_confirmacao = Menu_Confirmacao()

# a partir de root

menu_principal.grid(row=0, column=0, padx=MENU_PRINCIPAL_PADX, pady=MENU_PRINCIPAL_PADY, sticky='NSWE')


root.mainloop()




exit()



# código


# Local da public key para auth
key = "C:\\Users\\Operação 16\\.ssh\\id_rsa.pub"
# IP do servidor zabbix (public ip)
ipzserver = '189.124.85.75'

def sshcommit(comando):
    print(f'> "{comando}"...')
    stdin, stdout, stderr = client.exec_command(comando, get_pty=True)
    resultpmk = stdout.read().decode('utf-8')
    erro = 'Erro!'
    if stdout.channel.recv_exit_status() == 0:
        print(f'RETURN: ' + str(stdout.channel.recv_exit_status()))
    else:
        print(f'RETURN: ' + str(stdout.channel.recv_exit_status()))
    if "Permission denied" in resultpmk:
        print('PERMISSION DENIED!')
        print(f'{resultpmk}')
        stdin.close()
        stdout.close()
        stderr.close()
        return erro
    else:
        stdin.close()
        stdout.close()
        stderr.close()
        return resultpmk

def menu_hostname():
    while True:
        empresa = input('Zabbix HOSTNAME:\n> ').upper()
        if len(empresa) == 0:
            print('Inválido!\n')
        else:
            break
    return empresa

def menu_host():
    while True:
        host = input('IP/DNS:\n> ')
        if len(host) == 0:
            print('Inválido!\n')
        else:
            break
    return host

def menu_porta():
    while True:
        porta = input('Porta SSH (Padrão = 22):\n> ').upper()
        if len(porta) == 0:
            porta = 22
            break
        elif len(porta) != 0:
            try:
                porta = int(porta)
                break
            except ValueError:
                print('Inválido!\n')
        else:
            break
    return porta

def menu_username():
    while True:
        username = input('Usuário:\n> ')
        if len(username) == 0:
            print('Inválido!\n')
        else:
            break
    return username

def menu_autenticacao():
    while True:
        autenticacao = input('Autenticação por CHAVE ou SENHA? (c/s)\n> ').lower()
        if autenticacao == "c":
            break
        elif autenticacao == "s":
            break
        else:
            print('Inválido!\n')
    return autenticacao

def menu_credenciais(aut):
    global key
    if aut == 'c':
        while True:
            resp = input(f'O PATH da chave pública é "{key}", está correto? (s/n)\n> ').lower()
            if resp == 's':
                return 'AUTH_BY_KEY' # Valor simbólico para a senha, já que a autenticação será feita por Chave
            elif resp == 'n':
                resp2 = input('Digite o PATH completo da chave pública:\n> ')
                key = resp2
            else:
                print('Inválido!\n')
    elif aut == 's':
        while True:
            password = input('Senha:\n> ')
            if len(password) == 0:
                print('Inválido?\n')
            else:
                break
        return password
    else:
        print("Algum erro ocorreu, e a variável autenticacao não é 'c' nem 's'. ")
        exit()
        
# Exibo os menus
while True:
    print('\n')
    empresa = menu_hostname()
    host = menu_host()
    porta = menu_porta()
    username = menu_username()
    password = menu_credenciais(menu_autenticacao()) # senha ou chave, nao necessariamente será usado
    continua = input(f"""
EMPRESA: {empresa}
   HOST: {host}
   PORT: {porta}
USUARIO: {username}
  SENHA: {password}
KEYPATH: {key}

As informações para autenticação SSH estão corretas? (s/n)
""").lower()
    if continua == 's':
        break
    elif continua == 'n':
        pass
    else:
        print("Inválido!")


print("-- INICIANDO CONEXÃO PARAMIKO --")

# Abrindo o processo SSH PARAMIKO
client = paramiko.client.SSHClient()
# Aceitando/adicionando a KEY
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Conectando SSH
try:
    client.connect(host, username=username, password=password, port=porta, key_filename=key)
except Exception as e:
    client.close()
    print('ERRO AO SE CONECTAR COM O CLIENTE SSH')
    print(e)
    exit()
else:
    print(f"""
   HOST: {host}
   PORT: {porta}
USUARIO: {username}
  SENHA: {password}
EMPRESA: {empresa}""")

    print('\n-- DESCENDO FIREWALL --')
    print('nada')
    # Parando o firewall para a instalação
    # sshcommit('sudo iptables -F')

    print('\n-- INSTALAÇÃO --')
    # Instalando as dependências
    sshcommit('sudo rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-agent-5.0.22-1.el7.x86_64.rpm')
    # Instalando o ZABBIX-AGENT
    sshcommit('sudo yum -y install zabbix-agent')
    # Iniciando o ZABBIX-AGENT
    sshcommit('sudo systemctl start zabbix-agent')

    print('\n-- EDITANDO ZABBIX_AGENTD.CONF --')
    # SERVIDOR
    sshcommit("sudo sed -i 's/Server=127.0.0.1/Server={}/g' /etc/zabbix/zabbix_agentd.conf".format(ipzserver))
    # SERVIDOR ATIVO
    sshcommit("sudo sed -i 's/ServerActive=127.0.0.1/ServerActive={}/g' /etc/zabbix/zabbix_agentd.conf".format(ipzserver))
    # HOSTNAME
    sshcommit("sudo sed -i 's/Hostname=Zabbix server/Hostname={}/g' /etc/zabbix/zabbix_agentd.conf".format(empresa))
    # HOSTMETADATAITEM (utilizando sed por problemas de permissão AWS)
    sshcommit("sudo sed -i 's,# HostMetadataItem=,HostMetadataItem=release,g' /etc/zabbix/zabbix_agentd.conf")
    # USERPARAMETER (utilizando sed por problemas de permissão AWS)
    sshcommit("sudo sed -i 's@# UserParameter=@UserParameter=release,cat /etc/redhat-release@g' /etc/zabbix/zabbix_agentd.conf")

    print('\n-- FINALIZANDO INSTALAÇÃO --')
    # Adicionando ZABBIX à lista de sudoers
    sshcommit('echo "%zabbix ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
    # Reiniciando o agent
    sshcommit('sudo systemctl restart zabbix-agent')
    # Permitindo que o ZA inicie no boot
    sshcommit('sudo systemctl enable zabbix-agent')

    print('\n-- SUBINDO FIREWALL --')
    print('nada')
    # Reativando o Firewall
    # sshcommit('sudo bash /etc/firewall.sh')

# Finalizando as sessões abertas no usuário remoto
print('\n-- FINALIZANDO SESSÃO PARAMIKO --')
client.close()
time.sleep(5)
