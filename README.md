# AutoYaproto

_Proyecto para la enseñanza educativa de Redes, y poder probar protocolos de encaminamiento RIPv2_
_Basandonos en el proyecto yaproto https://github.com/javierrledesma/yaproto_

_Con esta web podremos diseñar nuestro propio laboratorio y ejecutar el protocolo de encaminamiento_


### Pre-requisitos 📋
_Pasos probados para Ubuntu 18.04.4 LTS_
_Para otros sistemas operativos importante tener instalado **Python 3.6**_

_Primero instalaremos Vitual Box_
```
sudo apt install virtualbox
```
_Necesitaremos hacer un update del sistema_
```
sudo apt update
```
_Ahora instalaremos la version de Vagrant correspondiente a nuestra distribucion_
_64-bit_
```
curl -O https://releases.hashicorp.com/vagrant/2.2.7/vagrant_2.2.7_x86_64.deb
sudo apt install ./vagrant_2.2.7_x86_64.deb
```
_o 32-bit__
```
curl -O https://releases.hashicorp.com/vagrant/2.2.7/vagrant_2.2.7_i686.deb
sudo apt install ./vagrant_2.2.7_i686.deb
```
_Por ultimo necesitamos unos los paquetes de pip3 git virtualenv_
```
sudo apt-get install python3-pip
sudo apt install git
sudo sudo pip3 install virtualenv
```





### Instalación

_Para la ejecución e instalación del proyecto propiamente dicho seguiremos las siguientes instrucciones_

_Descargamos el código_
```
git clone git@github.com:oredondo/auto-yaproto.git
cd auto-yaproto
```

_Creamos un entorno virtual e instalamos los requirements_
```
virtualenv venv -p python3.6
source venv/bin/activate
pip3 install -r requirements.txt
```

_Por ultimo podemos ejecutar Flask para poder acceder a la web que nos facilitara la instalación del laboratorio_
```
python3.6 web-flask/main.py FLASK_APP=main.py flask run
```

_Ahora podremos entrar en la web atraves del siguiente enlace_

```
auto-yaproto
```
