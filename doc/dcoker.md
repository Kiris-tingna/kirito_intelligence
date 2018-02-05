## docker 安装  \[ linux \]
- 1. 安装docker 

> step1: 换源

`sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak`

go `http://mirrors.163.com/.help/ubuntu.html` download `sources.list`

`sudo apt-get update`

`sudo apt-get -y install apt-transport-https ca-certificates curl`

> step 2: 安装GPG证书

`curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -`

`sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"`

> Step 3: 更新并安装 Docker-CE

`sudo apt-get -y update`

`sudo apt-get -y install docker-ce`

- 2. 查看docker 
`sudo docker version`

- 3. 查看images 
`sudo docker images`