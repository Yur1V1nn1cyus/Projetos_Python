#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
PUR='\033[0;34m'
NC='\033[0m' # No Color
echo -e "\n\n#### ${RED}Iniciado instalação da api-gestaoparts.${NC}\n\n"

# Atualiza o sistema e instala pacotes necessários
apt-get install -y python3.8 python-dev python3.8-dev
apt-get install -y build-essential libssl-dev libffi-dev
apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev
apt-get install -y libsqlite3-dev
apt-get install -y postgresql-client
echo -e "\n\n #### ${GREEN}Instalação de pacotes concluída.${NC} \n\n"

# Instala o pip e atualiza
apt-get install -y python3-pip
python3 -m pip install pip
echo -e "\n\n #### ${GREEN}Instalação do python3-pip concluída.${NC} \n\n"

# Instala os pacotes Python necessários
python3.8 -m pip install -U setuptools pip before
python3.8 -m pip install fastapi==0.64.0 python-multipart uvicorn twilio
python3.8 -m pip install pyjwt
python3.8 -m pip install passlib[bcrypt]
python3.8 -m pip install psycopg2-binary
python3.8 -m pip install asyncio
python3.8 -m pip install pysqlite3
python3.8 -m pip install logging42
python3.8 -m pip install unidecode
python3.8 -m pip install schedule==1.1.0
python3.8 -m pip install aiopg==1.4.0
python3.8 -m pip install jinja2==3.0.3
python3.8 -m pip install aiofiles
python3.8 -m pip install pydantic==1.8.1
echo -e "\n\n #### ${GREEN}Instalação dos pacotes Python concluída.${NC} \n\n"

# Clona o repositório e ajusta permissões
git clone https://ss_sistemas@bitbucket.org/ss_sistemas/api-suite-integration-compiler.git /api-suite-integration-compiler
chmod -R 777 /api-suite-integration-compiler
echo -e "\n\n #### ${GREEN}Clone da API Gestaoparts concluída.${NC} \n\n"

# Edita o arquivo db.json com as informações do banco de dados
db_file="/api-suite-integration-compiler/db.json"

if [ -f "$db_file" ]; then
    echo -e "\n\n #### ${RED}Preencha os dados de conexão do DB.${NC} \n"
    read -p "Digite host: " host
    read -p "Digite port: " port
    read -p "Digite dbname: " dbname


    # Tentativa de conexão
    echo -e "\n\n#### ${RED}Verificando se o usuário 'ssapisuite' existe...${NC}\n"
    PGPASSWORD="SSs1st3m@s2o!7" psql -h "$host" -U "ssplus" -d "$dbname" -p "$port" -tAc "SELECT 1 FROM pg_roles WHERE rolname='ssapisuite';"

    # Verifica se a conexão foi bem-sucedida
    if [ $? -ne 0 ]; then
        echo -e "\n\n#### ${RED}Erro: Não foi possível conectar ao banco de dados. Verifique os dados de conexão (host, porta, dbname, usuário, ou senha).${NC}\n"
        exit 1
    fi

    # Atualiza o db.json
    sed -i "s/\"dbname\" *: *\"[^\"]*\"/\"dbname\"                 : \"$dbname\"/" "$db_file"
    sed -i "s/\"port\" *: *\"[^\"]*\"/\"port\"                   : \"$port\"/" "$db_file"
    sed -i "0,/\"host\" *: *\"[^\"]*\"/s//\"host\"                   : \"$host\"/" "$db_file"

    echo -e "\n\n #### ${GREEN}Arquivo db.json atualizado com sucesso.${NC}\n"
    

    # Se o usuário não existir, cria
    if ! PGPASSWORD="SSs1st3m@s2o!7" psql -h "$host" -U "ssplus" -d "$dbname" -p "$port" -tAc "SELECT 1 FROM pg_roles WHERE rolname='ssapisuite';" | grep -q 1; then
        echo -e "\n\n#### ${RED}Usuário 'ssapisuite' não encontrado,${GREEN} criando usuário...${NC}\n"
        PGPASSWORD="SSs1st3m@s2o!7" psql -h "$host" -U "ssplus" -d "$dbname" -p "$port" -c "CREATE ROLE ssapisuite LOGIN ENCRYPTED PASSWORD 'md58915d5f8aa33770e3f9264bec9877170' SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION;"
        echo -e "\n\n #### ${GREEN}Usuário 'ssapisuite' criado com sucesso.${NC}\n\n"
    else
        echo -e "\n\n #### ${GREEN}Usuário 'ssapisuite' já existe.${NC}\n\n"
    fi

    # Migrate api
    cd /api-suite-integration-compiler
    chmod -R 777 /api-suite-integration-compiler
    ./upgrade-unix.sh 
    echo -e "\n\n #### ${GREEN}Migrade da api concluído.${NC}\n\n"
else
    echo -e "\n\n#### ${RED}Arquivo db.json não encontrado.${NC}\n\n"
fi

# Criação do serviço principal
cat <<EOF > /etc/systemd/system/api-gestaoparts.service
[Unit]
Description=api-gestaoparts
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/api-suite-integration-compiler/run-unix.sh

[Install]
WantedBy=multi-user.target
EOF
echo -e "\n\n #### ${GREEN}Criação do serviço principal concluída.${NC}\n\n"
# Criação do serviço de notificação
cat <<EOF > /etc/systemd/system/api-gestaoparts-notify.service
[Unit]
Description=api-gestaoparts-notify
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/api-suite-integration-compiler/run-unix-notify.sh

[Install]
WantedBy=multi-user.target
EOF
echo -e "\n\n #### ${GREEN}Criação do serviço de notificação concluída.${NC}\n\n"
# Recarrega os serviços
systemctl start api-gestaoparts
systemctl start api-gestaoparts-notify

systemctl enable api-gestaoparts
systemctl enable api-gestaoparts-notify

systemctl restart api-gestaoparts
systemctl restart api-gestaoparts-notify
echo -e "\n\n #### ${GREEN}Recarrega os serviços concluída.${NC}\n\n"

echo -e "\n\n #### ${GREEN}Instalação da api-gestaoparts concluída.${NC}\n\n"