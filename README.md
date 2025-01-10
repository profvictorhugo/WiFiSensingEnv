# SensingFI
Plataforma SensingFI

## Pré-requisitos para conseguir rodar o Framework

- Ter o python 3.0.0 pra cima instalado em seu computador
- Ter a biblioteca Flask do python instalada

## Passos de instalação
### Linux 
Rode o programa abaixo pra conseguir instalar o python
```
sudo apt update
sudo apt install python3 python3-pip
```

---
### Mac Os
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
Vamos precisar do "Chocolatey", pra isso, abra o PowerShell como administrador e coloque o código:
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











Com o python instalado, podemos instalar o flask
```
pip3 install flask
```


