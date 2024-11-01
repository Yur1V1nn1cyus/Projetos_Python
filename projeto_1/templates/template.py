import sys, os

sys.path.append(os.path.abspath(os.path.join(os.curdir, 'C:/Users/marci/Desktop/teste/pythonando/projeto/projeto_1')))

from models.password import passdate

from views.pass_views import FernetHasher


acao = input('Insere 1 para gravar senha ou Insere 2 para ver senha')

if acao == '1':
    if len (passdate.get()) == 0:
        key, path = FernetHasher.create_key(arquive=True)
        print(f'Chave criada com sucesso')
        print(f'Chave : {key.decode("utf-8")}')
        if path : 
            print(f'Arquivo criado com sucesso')
            print(f'Local : {path}')
    else:
        key = input('Digite sua key ')
    domain = input('Domain: ')
    password = input('Pass: ')
    fernet_user = FernetHasher(key)
    p1 = passdate(domain=domain, password=fernet_user.encriptar(password).decode("utf-8"))
    p1.save()

elif acao == '2':
    domain = input('Domínio: ')
    key = input('Key: ')
    fernet = FernetHasher(key)
    data = passdate.get()
    password = ''
    for i in data:
        if domain in i['domain']:
            password = fernet.decriptar(i['password'])

        if password:
            print(f'Sua senha: {password}')
        else:
            print('Nenhuma senha encontrada para esse domínio.')