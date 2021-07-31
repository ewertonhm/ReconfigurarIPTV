import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from twt_rw import *
import time

options = selenium.webdriver.chrome.options.Options()
options.headless = True
options.add_argument('log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = selenium.webdriver.Chrome(executable_path=r"C:\webdriver\chromedriver.exe", options=options)

login = 'ewerton.marschalk@redeunifique.com.br'
senha = '32071996ca536Ewe6'
compatible_ztes = ['F660','F670L','F670']
passwords = ['glock9mm','Unisc202@']
users = ['multipro','admin']


Clientes = read_file('clientes.txt')

def get_ip(pppoe):
    url = 'http://189.45.192.17/daloinfo/index.php?username=' + pppoe
    driver.get(url)
    table = driver.find_element_by_id('session_info').find_element_by_class_name('table').find_elements_by_tag_name('td')
    ip = table[4].text[:-22]
    return ip


def get_status(pppoe):
    url = 'http://189.45.192.17/daloinfo/index.php?username=' + pppoe
    driver.get(url)
    time.sleep(0.1)
    try:
        table = driver.find_element_by_id('session_info').find_element_by_class_name('table').find_elements_by_tag_name('td')
        status = table[0].text
    except:
        status = False
    return status

def access_zte(pppoe):
    status = get_status(pppoe)
    time.sleep(0.1)
    if status != 'Usuário está desconectado' and status != False:
        url = 'http://' + get_ip(pppoe)
        print('{0}: Acessando ZTE através do endereço: {1}'.format(time.strftime("%H:%M:%S"),url))
        time.sleep(0.1)
        driver.get(url)
        return True
    else:
        return False

def check_is_zte(pppoe):
    if access_zte(pppoe):
        if driver.title in compatible_ztes:
            return True
        else:
            return False

def login_zte(pppoe):
    if check_is_zte(pppoe):
        counter_user = len(users) - 1
        while counter_user >= 0:
            counter_pass = len(passwords) - 1
            while counter_pass >= 0:
                try:
                    driver.find_element_by_id('Frm_Username').send_keys(users[counter_user])
                    driver.find_element_by_id('Frm_Password').send_keys(passwords[counter_pass])
                    driver.find_element_by_id('LoginId').click()
                    wait = WebDriverWait(driver, 1)
                    terms = wait.until(EC.presence_of_element_located((By.ID, "mainFrame")))
                    driver.switch_to.frame('mainFrame')
                    if driver.find_element_by_id('Fnt_mmHelp').text == 'Help':
                        counter_pass = -10
                        return True
                except Exception as e:
                    counter_pass = counter_pass - 1

            if counter_pass == -10:
                counter_user = 0
            counter_user = counter_user - 1
    return False

def get_sn():
    return driver.find_element_by_id("Frm_PonSerialNumber").text

def config_zte(pppoe):
    driver.find_element_by_id('mmApp').click()
    time.sleep(0.5)
    driver.find_element_by_id('smMultiCast').click()
    time.sleep(0.5)
    try:
        driver.find_element_by_id('Btn_Delete1').click()
    except:
        print('{0}: Não existe IPTV 1'.format(time.strftime("%H:%M:%S")))
    time.sleep(1)
    try:
        driver.find_element_by_id('Btn_Delete0').click()
    except:
        print('{0}: Não existe IPTV 0'.format(time.strftime("%H:%M:%S")))
    time.sleep(1)

    ## click vlan config
    driver.find_element_by_id('ssmMultiCastVlan').click()
    time.sleep(0.5)



    counter = 0
    while counter <= 3:
        try:
            select = Select(driver.find_element_by_class_name('list_10'))
            select.select_by_value(str(counter))
            driver.find_element_by_id('delete0').click()
            time.sleep(1)
        except:
            c = counter+1
            print('Erro ao deletar a vlan na LAN'+str(c))
        counter = counter + 1
    print('{0}: Finalizado configurações no ZTE'.format(time.strftime("%H:%M:%S")))
    return True

def sa_site_login():
    driver.get("http://ativacaofibra.redeunifique.com.br/")
    driver.find_element_by_name("login").send_keys(login)
    driver.find_element_by_name("senha").send_keys(senha)
    driver.find_element_by_id("entrar").click()


def remove_iptv(sn):
    driver.get("http://ativacaofibra.redeunifique.com.br/cadastro/interno.php?pg=interno&pg1=alteracoes/remove_iptv")

    try:
        driver.find_element_by_name('sn').send_keys(sn)
        driver.find_element_by_name('sn').send_keys(Keys.ENTER)

        print('{0}: Removendo IPTV no Sistema de Ativação'.format(time.strftime("%H:%M:%S")))
        driver.find_element_by_name("pesquisar").click()

    except:
        print('Erro ao remover o IPTV no Sistema de Ativação')

def adicionar_iptv(sn):
    driver.get("http://ativacaofibra.redeunifique.com.br/cadastro/interno.php?pg=interno&pg1=novos_cadastros/adicionar_iptv2")
    try:
        driver.find_element_by_name('sn').send_keys(sn)
        driver.find_element_by_name('sn').send_keys(Keys.ENTER)

        print('{0}: Adicionando IPTV no Sistema de Ativação'.format(time.strftime("%H:%M:%S")))
        driver.find_element_by_name("pesquisar").click()
    except:
        print('Erro ao adicionar o IPTV no Sistema de Ativação')


if __name__ == '__main__':
    write_to_log('##################################################################################################')
    counter = 0
    lenght = len(Clientes)

    while counter < lenght:
        cliente = Clientes[counter].strip()
        print('####################################################################################################')
        print('{0}: Iniciando configurações no PPPoE: {1}'.format(time.strftime("%H:%M:%S"), cliente))
        if login_zte(cliente):
            sn = get_sn()
            config_zte(cliente)
            sa_site_login()
            remove_iptv(sn)
            adicionar_iptv(sn)

            print('{0}: Finalizando configurações no PPPoE: {1} SN: {2}'.format(time.strftime("%H:%M:%S"), cliente, sn))
            write_to_log('{0} - {1} - OK'.format(cliente,sn))

        else:
            print('{0}: Erro ao realizar configurações no PPPoE: {1}'.format(time.strftime("%H:%M:%S"), cliente))
            write_to_log('{0} - Fail'.format(cliente))
        print()
        counter = counter + 1

    # close webdriver

    driver.quit()
    driver = None

