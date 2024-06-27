sudo apt update

sudo apt upgrade

sudo apt install python3-pip

sudo apt install python3-virtualenv

# create folder for application
mkdir app

# get inside that folder
cd app

# create an virtual environment using virtualenv library
virtualenv venv

# activate the virtual env
source venv/bin/activate

# clone the project from github repo
git clone https://github.com/adventuresoul/MedscanRx.git

# get inside the campus_connect application
cd MedscanRx

# install the dependency
sudo apt install libpq-dev

# install all the required modules as specified in requirements.txt
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html


# enable the firewall
sudo ufw enable

# enable the machine to listen on port 8000
sudo ufw allow 8000

echo "Add .env file and configure connections with database and other things"