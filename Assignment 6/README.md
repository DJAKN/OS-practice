Report for Assignment 6

------

# 一、简单叙述 Paxos 算法的基本思想

Paxos 算法用于处理基于消息传递机制的分布式系统通信过程中，可能出现的一致性问题。这里，假设系统不会出现拜占庭错误（即有可能一个消息被传递了两次，但不会出现错误的消息）的情况。Paxos 是算法的设计者莱斯利·兰伯特（Leslie Lamport）提出的虚构的希腊城邦的名字，他利用城邦中议员制定法律的场景解释本算法。

议员可能有三种身份，每人可以有多个身份：

+ proposer，负责提出法律提案，信息包括提案编号和数值。
+ acceptor，在收到提案后可以选择接受提案，若一个提案被多数 acceptor 所接受，则这一提案被批准。
+ learner，负责学习被批准的提案的数值。

算法执行中涉及到以下命题：

命题 1：如果一个编号为 n 的提案具有 value v，那么存在一个多数派，要么他们中的所有人都没有 accept 编号小于 n 的任何提案，要么他们已经 accept 的所有编号小于 n 的提案中,编号最大的那个提案具有 value v。

算法开始执行后，通过一个决议分为两个阶段：

1. prepare 阶段

+ proposer 选择一个提案编号 n，并将 prepare 请求发送给 acceptors 中数量达到多数派的一部分；
+ acceptor 在收到 prepare 消息后，如果提案的编号大于它已经回复的所有 prepare 消息，则 acceptor 将自己上次接受的提案回复给 proposer，并承诺不再回复小于 n 的提案。
+ 在任何时刻，如果一个 proposer 发现已经有其他 proposers 提出了编号更高的提案，则他应该中断正在进行的过程。因此，如果一个 acceptor 发现存在一个更高编号的提案，则需要通知 proposer，告知其中断这次提案。
2. accept 阶段

+ 当一个 proposer 收到了多数 acceptors 对 prepare 的回复后，就进入 accept 阶段。它要向回复 prepare 请求的所有 acceptors 发送 accept 请求，包括编号 n 和根据命题 1 决定的 value（如果根据命题 1，没有已经接受的 value，那么它可以自由决定一个 value）。
+ 在不违背自己向其他 proposer 的承诺的前提下，acceptor 收到 accept 请求后即接受这个请求。

在实际应用中，若某个 proposer 在 propose 阶段没有竞争者，且信息及时传达到了所有他希望传达的 acceptor 处，则过程退化为普通的二阶段提交。

若在 propose 阶段产生竞争者，所有仅收到一份提案的 acceptor 会向相应的提案发送者回复；若某个 proposer 因此而获得了多数人的赞同，他将向所有人发送信息，说明提案已经通过；若某个 acceptor 收到了多份提案，则他会根据提案接收的先后顺序或 proposer 的权重，选择向其中一个 proposer 发送接受回复，另一个发送拒绝回复。

简要的算法流程图如下：

![](1.png)

# 二、模拟 Raft 协议工作的一个场景并叙述处理过程

Raft 一致性协议将整个通信过程分为三个阶段，leader election，log replication 和 commit。

每个 server 可能处于三个状态：leader，follower，candidate：

+ leader 为集群主节点，整个集群仅有一个 leader 节点可以存在
+ follower 为跟随节点，follower 知晓自己的 leader，并与 leader 进行通信
+ candidate 是当 follower 无法联系上 leader 节点时所转化而成，candidate 的作用是在自己无法联系上 leader 的情况下联系 leader

节点状态的转换关系约束如下：

- 集群启动时，所有节点初始化为 follower
- 节点具有 follower，candidate，leader 这样的等级队列，不能跨级别升降

具体的转换关系大致可以用下图表示：

![](2.png)

## 工作场景模拟

1. 初始化，所有节点均为 follower

![](3.png)

2. S2 和 S5 节点成为 candidate，对任期 +1，并向其他节点发送 vote 申请

![](4.png)

3. vote 结束后，S2获得 4 张选票，S5 获得一张；S2 成为 leader

![](5.png)

4. 之后，leader 会以一定的周期向 followers 发送消息，followers 进行回复。若 followers 没有接到这个消息，它会在 timeout 之后成为 candidate，并开始新的投票阶段。
5. 系统的某些部分如果产生变化，将会由 leader 通知 followers 这些变化并由 followers 回复。

# 三、Mesos 的容错机制

Mesos 包括一个运行中的 master 节点和多个备用 master 节点，由 zookeeper 进行监控。当运行中的 master 节点发生故障时，zookeeper 负责启动新 master 的选举工作。建议的节点总数是 5 个，实际上，生产环境至少需要 3 个 master 节点。 

Mesos 将 master 设计为持有软件状态，这意味着当 master 节点发生故障时，其状态可以很快地在新选举的 master 节点上重建。 Mesos 的状态信息实际上驻留在Framework 调度器和 Slave 节点集合之中。当一个新的 master 当选后，zookeeper 会通知 Framework 和选举后的 Slave 节点集合，使其在新的 master 上被注册。彼时，新的 master 可以根据 Framework 和 Slave 节点集合发送过来的信息，重建内部状态。