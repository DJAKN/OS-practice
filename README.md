Report for Assignment 1
=
一、数据中心操作系统的概念
---
<br>
为了在一个商用服务器集群中同时运行多个应用程序，并为每个应用程序提供最佳的框架，以满足其服务器集群软硬件资源的访问需求，需要对集群进行共享，由此产生了分布式系统和数据中心操作系统的概念。
<br><br>
Mesos 是一种典型的数据中心操作系统。相较于 Hadoop 等现有的框架，Mesos 实现了服务器集群资源的细粒度共享：它能够基于各种应用程序不同的调度需求和资源访问需求计算全局的调度方案，并为每个需求精确地分配资源。同时，为了应对未来可能出现的超大规模的应用场景，Mesos 还具有高度的扩展性和容错性，能够在大规模的应用中保持系统的稳定。
<br><br>
Mesos 在面对多个框架同时运行的情境时，具有较好的虚拟化性能。具体而言，可以把 Mesos 抽象成一个双层结构。在第一层中，Mesos 将一定的资源提供给对应的框架，而在第二层中，框架可以利用自己的调度算法使用这些资源。这样，多个框架实例可以彼此互不冲突地运行在同一个集群里，这是现有的调度器很难实现的。而随着新框架的诞生，它们可以被试验性地部署到现有的集群上，不会对已有框架产生影响。
<br><br>
在调研中了解到，Mesos 帮助 Twitter 解决了此前困扰其的服务器资源难以利用的问题，包括 Airbnb 和 eBay 在内的企业也是 Mesos 的用户。
<br><br>

## 二、虚拟机和容器技术
虚拟机是一个仿真的计算机系统。它可以在计算机平台和终端用户之间创建一种环境，用户基于这一环境来操作软件。虚拟机包括系统虚拟机和软件虚拟机，前者需要安装在宿主系统上，利用宿主系统分配的资源，虚拟出独立的 CPU、内存、硬盘等，为用户提供完整的一套操作系统服务，常用的 Vmware、VirtualBox 等平台提供这类服务；而后者则是类似 JVM 的机器。也有少数面向企业的虚拟机软件自带宿主操作系统，可以直接安装在一台裸机上。
<br><br>
容器是一些类、数据结构或抽象数据类型，它被实例为其他类的对象的集合。容器实际上是一种进程，它运行于一个独立的 命名空间之中，拥有自己的 root 文件系统和进程空间等。容器内的进程是运行在一个隔离的环境里，与虚拟机提供的环境类似。
<br><br>
与容器技术相比，虚拟机提供了更为完整的硬件虚拟化服务，功能更为强大，也因此而需要更大的启动和使用开销。容器技术由于直接利用硬件资源，具有比较高的硬件利用效率，但功能更为简单，在其上进行的一些操作也更可能对主系统产生不确定的影响，而虚拟机中的操作很难对宿主系统产生直接的影响。
<br>
## 三、Mesos 的配置过程
根据 Mesos 网站给出的配置方式，在 Ubuntu 16.04 中安装了Mesos。
<br><br>
1. 下载 Mesos：
```
$ wget http://www.apache.org/dist/mesos/1.1.0/mesos-1.1.0.tar.gz
$ tar -zxf mesos-1.1.0.tar.gz
```
2. 安装必要的包和依赖库等：
```
# Update the packages.
$ sudo apt-get update

# Install a few utility tools.
$ sudo apt-get install -y tar wget git

# Install the latest OpenJDK.
$ sudo apt-get install -y openjdk-8-jdk

# Install other Mesos dependencies.
$ sudo apt-get -y install build-essential python-dev libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev
```
3. Mesos 安装和配置（make 和 make check 操作都需要相当长的时间，可以采用 -j 并行运行的方式）：
```
# Change working directory.
$ cd mesos

# Bootstrap (Only required if building from git repository).
$ ./bootstrap

# Configure and build.
$ mkdir build
$ cd build
$ ../configure
$ make

# Run test suite.
$ make check

# Install
$ make install
```
4. 在本地启动一个 host 和一个 agent：
```
# Change into build directory.
$ cd build

# Start mesos master (Ensure work directory exists and has proper permissions).
$ ./bin/mesos-master.sh --ip=127.0.0.1 --work_dir=/var/lib/mesos

# Start mesos agent (Ensure work directory exists and has proper permissions).
$ ./bin/mesos-agent.sh --master=127.0.0.1:5050 --work_dir=/var/lib/mesos
```
5. 访问系统页面：
```
$ http://127.0.0.1:5050
```
Mesos运行效果如图所示（从上至下分别为：master运行状况、agent运行状况、本地网页）：
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/master.jpg)
<br><br>
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/agent.jpg)
<br><br>
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/webpage.jpg)
<br>
## 四、运行 Spark
1. 下载 Spark 2.1.0
<br><br>
2. 修改 ```spark-env.sh``` 和 ```spark.executor.uri``` 环境变量，在其中分别添加 ```MESOS_NATIVE_JAVA_LIBRARY=<path to libmesos.so>``` 、 ```SPARK_EXECUTOR_URI=<URL of spark-2.1.0.tar.gz uploaded above>``` 和 ```<URL of spark-2.1.0.tar.gz>``` 条目。
3. 考虑到本机硬件资源为四核的 Intel i5 处理器和 4GB 内存，分别利用 Spark 在分配 1、2 和 4 个核以及 600MB 内存的情况下运行 ```Wordcount.java``` 程序，对一个大小约为 220 MB 的英文文本文件进行处理，相应代码为：
```
./bin/spark-submit   --class org.apache.spark.examples.JavaWordCount   --master mesos://127.0.0.1:5050  --executor-memory 600M   --total-executor-cores 1   file:///home/usrname/Desktop/spark-2.1.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.0.jar   /home/usrname/Desktop/o

./bin/spark-submit   --class org.apache.spark.examples.JavaWordCount   --master mesos://127.0.0.1:5050  --executor-memory 600M   --total-executor-cores 2   file:///home/usrname/Desktop/spark-2.1.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.0.jar   /home/usrname/Desktop/o

./bin/spark-submit   --class org.apache.spark.examples.JavaWordCount   --master mesos://127.0.0.1:5050  --executor-memory 600M   --total-executor-cores 4   file:///home/usrname/Desktop/spark-2.1.0-bin-hadoop2.7/examples/jars/spark-examples_2.11-2.1.0.jar   /home/usrname/Desktop/o
```
处理结果和各自的运行时间如图所示（从上至下分别为：1、2、4核运行结果，运行时间统计）：
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/1.jpg)
<br><br>
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/2.jpg)
<br><br>
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/4.jpg)
<br><br>
![](https://github.com/DJAKN/Lab-of-microcomputer-experiment/blob/master/0.jpg)<br>
## 五、其他事项
本作业完成过程中，有一大部分时间花在了 build Mesos 系统之上，这一系统配置需要的时间较长，在网络和硬件资源良好的情况下，```make``` 和 ```make check``` 命令执行总共花费了大约 2.5 小时时间，这主要是由于之前不了解并行 ```-j``` 指令导致的，今后需要加强对于新情境下对工作带来显著帮助的新技术的学习。
<br><br>
Spark 在 Mesos 上的运行效果是相当显著的，处理规模较大的文本文件的速度比较好，表明了 Mesos 技术在利用集群系统中的优势。
