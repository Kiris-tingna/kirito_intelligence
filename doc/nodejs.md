# linux 安装最新
### 下载文件并解压
`wget http://cdn.npm.taobao.org/dist/node/v8.9.3/node-v8.9.3-linux-x64.tar.xz`
`tar -xvf  node-v8.9.3-linux-x64.tar.xz`


### 切换目录 
`cd /usr/local`
`mkdir node`
`cp -r ~/node-v8.9.3-linux-x64/* /usr/local/node`

### 路径

`sudo vim /ect/profile`

> 在最后加入

```
export NODE_HOME=/usr/local/node/bin
export PATH=$NODE_HOME:$PATH
```

退出终端重新登录即可

`rm ~/node-v8.9.3-linux-x64.tar.xz`
`rm ~/node-v8.9.3-linux-x64.tar.xz`