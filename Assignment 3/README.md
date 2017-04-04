Report for Assignment 3
----
## 一、Docker 的安装和配置
按照 Docker 网站说明在 Ubuntu 系统中安装了 Docker Community Edition for Ubuntu, 安装成功后运行 Hello-world 测试程序结果如下：

![](1.png)

## 二、Docker 基本命令介绍
### 1. 镜像管理命令 images

**含义**

列出机器上的镜像
<br><br>
**用法**

```
docker images [OPTIONS] [REPOSITORY[:TAG]]
```
在本机执行的结果：
<br><br>
**选项**

| 名字和缩写 | 缺省值 | 描述
| ------| ------ | ------ |
--all, -a | false | Show all images (default hides intermediate images)
--digests | false | Show digests
--filter, -f | | Filter output based on conditions provided
--format | | Pretty-print images using a Go template
--no-trunc | false | Don’t truncate output
--quiet, -q | false | Only show numeric IDs

<br><br>
**例子**
```
$ docker images java:8
```
打印所有位于```java```仓库中且带有标记```8```的镜像
<br><br>
```
$ docker images --filter "label=com.example.version=1.0"
```
打印所有带有标记```com.example.version```且值为```1.0```的镜像

### 2. 容器管理命令 run

**含义**

在特定镜像上创建一个新容器，并在其中运行一个命令。在这一过程中，Docker 在后台运行的标准操作包括：
+ 检查本地是否存在指定的镜像，若不存在则从公有仓库下载
+ 利用镜像创建并启动一个容器
+ 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
+ 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
+ 从地址池配置一个 ip 地址给容器
+ 执行用户指定的应用程序
+ 执行完毕后容器被终止

**用法**

```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**例子**

```
docker run -i -t --name mytest centos:centos6 /bin/bash
```

使用镜像创建容器并进入交互模式, login shell 为 /bin/bash. ```--name```参数指定启动后的容器名字，如果不指定则 Docker 会为其自行取一个名字。镜像 centos:centos6 也可以用 IMAGE ID 代替。选项```-i```保持标准输入接口开启，```-t```参数令 Docker 创建pseudo-TTY设备。pseudo-TTY 负责 client 与容器进程进行交互。

**相关命令**
```
docker ps [OPTIONS]
```
列出容器

```
docker start [OPTIONS] CONTAINER [CONTAINER...]
```
启动一个或多个已停止的容器

```
docker stop [OPTIONS] CONTAINER [CONTAINER...]
```
停止一个或多个运行中的容器

```
docker logs [OPTIONS] CONTAINER
```
取得容器日志

### 3. 网络管理命令 network

