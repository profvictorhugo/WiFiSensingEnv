# SensingFI
Plataforma SensingFI

## Pré-requisitos para conseguir rodar o Framework

- Ter o python 3.0.0 pra cima instalado em seu computador
- Ter a biblioteca Flask do python instalada
- Ter o docker para poder rodar o banco de dados localmente

- [Estou usando Windows](#Windows)
- [Estou usando Linux](#Linux)
- [Estou usando macOS](#macOS)



## Passos de instalação
### Linux 
Rode o programa abaixo pra conseguir instalar o python (siga a ordem colocada para evitar erros)
```
sudo apt update
sudo apt install python3 python3-pip
pip3 install Flask Flask-SQLAlchemy Flask-Cors
```

Agora com o python instalado, [esse](https://docs.docker.com/desktop/setup/install/linux/#where-to-go-next) é o site para você conseguir baixar o docker desktop na sua distro  

É com ele que vamos rodar nosso mysql para o framework, deixe seu docker desktop aberto e sempre veja se a engine dele está rodando, para isso, é só deixar ele aberto e ver se não aconteceu nenhum tipo de erro como "engine stoped".  

O docker vai estar parecido com isso:  

![docker-running](images-readme/docker-running.png)  

Perceba que na parte de baixo, na esquerda está escrito "Engine running", se estiver desse jeito no seu, o docker está rodando.   

Com ele instalado e aberto/rodando, abra um terminal externo e rode o comando:  
```
docker run --name wifisensing-mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=wifisensing \
  -p 3306:3306 \
  -d mysql:8.0 \
  --default-authentication-plugin=mysql_native_password
```

Esse comando é a criação do banco de dados do mysql para funcionar o framework, execute ele.  

Dentro da pasta "backend", rode `python3 main.py` ou `python3 .\main.py` (python3 porque as vezes só python aponta para python2)  

deverá aparecer assim para você no seu terminal:  


---
### macOS
Com o Mac, usaremos o comando do Homebrew, segue o código de instalação dele
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Com o comando funcionando, vamos instalar o python
```
brew install python
```

---
### Windows
Pode ser baixado de 2 formas: 
- Usar o [site oficial](https://www.python.org/downloads/)
- Usar o terminal

#### Usando o site
Se você escolheu baixar pelo site, no site vai ter um botão amarelo falando baixar o python mais recente, após baixar, ao abrir a janela do programa, marque as caixas que falam sobre usar privilégios de administrador e de adicionar ao PATH do sistema e espere baixar, e estará tudo pronto

#### Usando o terminal
Agora, se escolheu o terminal, vamos precisar do "Chocolatey", pra isso, abra o PowerShell como administrador e coloque o código:
```
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
Pra garantir se instalou rode no terminal:  `choco --version`

Com tudo instalado, podemos baixar o python 3 com: `choco install python -y`
Depois, pra garantir que o python está instalado rode: `python --version`

Pra garantir que o python está no PATH do sistema execute:
```
python --version
pip --version
```
Se aparecer as versões válidas deles, tá tudo certo, se não:

- Pressione Win + R, digite sysdm.cpl e pressione Enter.
- Clique em Avançado > Variáveis de Ambiente.
- Na seção Variáveis do sistema, encontre e selecione Path, depois clique em Editar.
- Clique em Novo e adicione o caminho para a pasta Scripts do Python, um exemplo: (o python39 é a versão 3.9 do python, troque pela versão que foi instalada, se foi 3.11 será 311 e assim por diante)
```
C:\Python39\Scripts\
C:\Python39\
```
- Clique em OK em todas as janelas para salvar as alterações.
- Reinicie o PowerShell e verifique novamente com
```
python --version
pip --version
```

---
## Instalando o Flask
Com o python instalado devidamente, podemos instalar o flask
```
pip3 install flask
pip3 install flask-sqlalchemy
pip3 install flask-cors
```
---
## Ambiente Virtual
(Certifique de ter instalado o python da forma que foi mostrada)

Caso prefira instalar as coisas em um ambiente virtual, segue os passos

### Linux/macOS
Precisaremos usar o comando "venv", pra baixar ele rode: `sudo apt install python3-venv`

Agora, vá no diretório que você quer usar e execute o comando: `python3 -m venv nome_que_quiser_pro_ambiente`

E para ativar ele rode: `source nome_do_ambiente/bin/activate`

Com ele ativo, podemos rodar o código: `pip3 install flask flask-sqlalchemy flask-cors`

Pra desativar o ambiente é só rodar: `deactivate` (ele só fecha o que você está no momento, não afeta outros)

---
### Windows
Pra fazer o mesmo com o Windows, rode o programa: `python -m venv nome_que_quiser_pro_ambiente`

Para ativar ele, rode: `.\nome_do_ambiente\Scripts\activate`

Com ele ativo:  

Instale o flask: `pip3 install Flask`  
Instale o flask_sqlalchemy: `pip3 install flask-sqlalchemy`  
Instale o flask_cors: `pip3 install flask-cors`


Pra desativar o ambiente, rode no terminal: `deactivate` (ele só fecha o que você está no momento, não afeta outros)



