import time
import paramiko
from tkinter import *
from tkinter.ttk import *

# PACOTES NECESSÁRIOS:
# Python 3.10 Microsoft (VSudio)
# https://www.python.org/downloads/ (atualmente 3.11.1)
# pip install paramiko

# VERSÃO 2.0
# pre-implementação no TKINTER

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
    print('\n-- CONEXÃO PARAMIKO (SSH) --')
    client.connect(host, username=username, password=password, port=porta, key_filename=key)
except Exception as e:
    client.close()
    print(f"falha ao se conectar...")
    print(e)
    exit()
else:
    print(f"conectado com êxito!")

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
