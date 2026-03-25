**## Set up Jenkins Locally on Ubuntu**



sudo apt update

sudo apt install openjdk-17-jdk -y



java -version





curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \\

&nbsp; /usr/share/keyrings/jenkins-keyring.asc > /dev/null



echo deb \[signed-by=/usr/share/keyrings/jenkins-keyring.asc] \\

&nbsp; https://pkg.jenkins.io/debian-stable binary/ | sudo tee \\

&nbsp; /etc/apt/sources.list.d/jenkins.list > /dev/null



sudo apt update

sudo apt install jenkins -y



sudo systemctl start jenkins

sudo systemctl enable Jenkins



\# access Jenkins Web Interface

http://<server ip>:8080



\# get initial admin password

sudo cat /var/lib/jenkins/secrets/initialAdminPassword







**# Generate SSH key on Jenkins server**



\# save the key files in /home/jenkins\_sh/.ssh/id\_ed25519.pub

ssh-keygen -t ed25519 

\# copy the public key file's content by

cat /home/jenkins\_sh/.ssh/id\_ed25519.pub

\# add public key to bitbucket

go to bitbucket -> settings -> add SSH key -> add workspace key and paste the public key

\# copy the .ssh folder to /var/lib/Jenkins/.ssh, since Jenkins run as "Jenkins" user

sudo mkdir -p /var/lib/jenkins/.ssh

sudo cp ~/.ssh/id\_ed25519 /var/lib/jenkins/.ssh/

sudo cp ~/.ssh/id\_ed25519.pub /var/lib/jenkins/.ssh/



\# set permissions

sudo chown -R jenkins:jenkins /var/lib/jenkins/.ssh

sudo chmod 700 /var/lib/jenkins/.ssh

sudo chmod 600 /var/lib/jenkins/.ssh/id\_ed25519



\# generate hostkey

sudo -u jenkins ssh-keyscan bitbucket.org | sudo tee -a /var/lib/jenkins/.ssh/known\_hosts > /dev/null



\# add SSH to Jenkins GUI

in Jenkins GUI -> manage Jenkins -> Credentials -> global -> add SSH key with name -> username: git and copy paste the private key content to key



\# test using a pipeline and build it

pipeline {

&nbsp;   agent any



&nbsp;   stages {

&nbsp;       stage('Checkout') {

&nbsp;           steps {

&nbsp;               git credentialsId: 'bitbucket\_ssh',

&nbsp;                   url: 'git@bitbucket.org:sionpowerdataanalytics/airflow\_k8s\_test.git',

&nbsp;                   branch: 'main'

&nbsp;           }

&nbsp;       }



&nbsp;       stage('Verify') {

&nbsp;           steps {

&nbsp;               sh 'ls -la'





\# install python3 and pip on Jenkins server

sudo apt update

sudo apt install -y python3 python3-pip

sudo apt install python3-venv





\## set up worker nodes

\# create a root directory. Permission should be given to the user who operate the worker node

sudo mkdir /home/Jenkins

sudo chown mongodb\_sh:mongodb\_sh /home/jenkins



from Jenkins -> manage Jenkins -> nodes -> add nodes

select connect from controller





\# on worker node, install java

sudo apt install openjdk-21-jdk



\# get the connection command from Jenkins GUI

java -jar agent.jar -url http://10.10.10.37:8080/ -secret 6c0fb7759891bc000903b3ebf5e416cb5d01ffc188aee1dbed03cf351c83f2fb -name "airflow\_worker" -webSocket -workDir "/home/jenkins"





\# embed the command to systemd file



\[Unit]

Description=Jenkins Agent

After=network.target



\[Service]

User=your-username

WorkingDirectory=/home/jenkins

ExecStart=java -jar agent.jar -url http://10.10.10.37:8080/ -secret 6c0fb7759891bc000903b3ebf5e416cb5d01ffc188aee1dbed03cf351c83f2fb -name "airflow\_worker" -webSocket -workDir "/home/jenkins"



Restart=always



\[Install]

WantedBy=multi-user.target













