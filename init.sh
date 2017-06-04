if [ "$1." == "init." ];
then
	uname=$(uname)
	if [ $uname == "Linux" ];
	then
		sudo apt-get -y install python-pip
		sudo pip install virtualenv
		virtualenv -p python3 env
		sudo apt-get install python-opencv
	fi

	if [ $uname == "Darwin" ];
	then
		python3 -m venv env
		env/bin/pip3 install opencv-python
	fi

	env/bin/pip install -r requirements.txt
elif [ "$1." == "deploy." ];
	then
	sudo apt-get -y install python3, python, python-pip
	pip install -r requirements.txt
	sudo apt-get install python-opencv
else
	env/bin/python manage.py $*
fi