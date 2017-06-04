if [ "$1." == "init." ];
then
	uname=$(uname)
	if [ $uname == "Linux" ];
	then
		sudo apt-get -y install python-pip
		sudo pip install virtualenv
		virtualenv -p python3 env
	fi

	if [ $uname == "Darwin" ];
	then
		python3 -m venv env
	fi

	env/bin/pip install -r requirements.txt
elif [ "$1." == "deploy." ];
	then
	sudo apt-get -y install python3, python, python-pip
	pip install -r requirements.txt
else
	env/bin/python manage.py $*
fi