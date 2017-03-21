Report for Assignment 2
----
## 一、Mesos 的组成结构

Mesos 架构主要分为三部分：Master, Agent, Frameworks. 其中 Frameworks 又可以被分为 Scheduler 和 Executor. 各个部分之间的关联结构如论文中插图所示：

### master
master 代码位于 /src/master 目录下。
master 在 Mesos 架构中居于核心位置。master 负责管理每一个集群节点上运行的 agent 守护进程，以及 agent 上执行具体任务的 frameworks.
master 进行对 agent 的管理的重要手段是统筹管理集群资源。master 利用 resource offer 机制实现这一点。resource offer 记录每个节点上有哪些处于空闲状态的资源（包括 CPU、内存、磁盘、网络等），资源列表的维护和更新由 master 完成。master 会根据这一列表中的信息、利用某种分配策略决定下一步为各个节点分配哪些资源。
<br><br>
master 的资源分配机制可能需要根据不同运行状况和节点需求而有所改变。为了适应多种分配机制的需求，master 使用了一种模块化的体系结构来使得添加新的分配策略变得更为容易。
<br><br>
在实际应用中，常常会有多个 master 同时存在的情况，它们互为备份，防止由于某一个 master 终止运行造成整个系统意外停止。Mesos 使用 Zookeeper 管理多个 master，并选择其中一个作为主节点执行各项功能。
### agent
agent 在一些旧的文档中被称为 slave，代码位于 /src/sched 和 /src/slave 目录下。
<br><br>
agent 一方面向处于运行状态的 master 报告目前节点上的空闲资源，从而更新 resource offer 的资源列表，另一方面接收 master 关于分配资源和执行任务的指令，将资源分配给具体 framework 的 executor.
### frameworks
frameworks 分为 scheduler 和 executor 两部分，负责具体执行某一个任务时的资源调度和执行工作，代码分别位于 /src/scheduler 和 /src/executor 目录下。
scheduler 负责与 master 交流目前 framework 运行需要哪些资源，以及 master 能够提供哪些资源。scheduler 向 master 注册框架信息后，master 会不断告知 scheduler 目前有哪些资源可用，由 scheduler 决定是否接受。若是，scheduler 还需要在接收资源并在节点内部进行分配后，告知 master 各项资源的具体分配信息。
<br><br>
executor 负责在接收资源后具体执行任务。新的框架加入集群时也需要 executor 启动框架。
### Zookeeper
Zookeeper 是一个 Apache 顶级项目。它是一个针对大型应用的数据管理、提供应用程序协调服务的分布式服务框架，提供的功能包括：配置维护、统一命名服务、状态同步服务、集群管理等。在生产环境中， Zookeeper 能够通过同时监控多个 master 在前台或后台运行或挂起，为 Mesos 提供一致性服务。
<br><br>
代码位于 /src/zookeeper 目录下。
### 工作流程
1. master 监控各个 agent 运行情况，不断更新资源列表，用 resource offer 向各个 scheduler 提供资源 offer.
2. agent 每隔一段时间向 master 更新可用资源情况。
4. framework 接收用户的任务请求，接受 master 提供的资源 offer, 并告知 master 需要每个任务具体需要多少资源. master 采用某种调度算法为该 framework 分配一定的资源。
0. 得到资源后，agent 调用 executor 执行各个任务，并继续向 master 报告有多少资源可用。
## 二、框架在 Mesos 上的运行过程
以 Spark on Mesos 为例。
<br><br><br>
大致运行架构如上图。Mesos master 代替 Cluster Manager 负责节点资源监控和资源列表更新工作。在 Mesos 接收用户提交的任务请求后，会将任务分配给集群中的一些工作节点执行。Spark 启动后，首先由 scheduler 向 master 注册，之后若收到了 master 分配的任务，则由 scheduler 根据 master 在 resource offer 中提供的资源情况，在框架内部进行调度，并将资源调度结果和剩余的空闲资源信息返回给 master，最后由 master 调度 executor 来执行任务。
### 与在传统操作系统上运行程序对比
相似点：
+ 都要对任务的具体执行单元提供抽象的资源信息。
+ 都涉及多个任务共同执行时，资源的分配和调度问题。
<br><br>
不同点：
+ 资源分配时决定
