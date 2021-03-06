# 按自己的理解记忆

作为典型，还是得过一遍。这些不太好记的知识通过重新组织简写的方式来加深记忆，以便以后快速浏览恢复记忆。内存数据库的性能优势并不完全是因为它们不需要从磁盘读取的事实。即使是基于磁盘的存储引擎也可能永远不需要从磁盘读取，因为数据库引擎和操作系统都有缓存最近在内存中使用了磁盘块。相反，它们更快的原因在于省去了将内存数据结构编码为磁盘数据结构的开销。说白了就是落盘慢，即使异步写和把随机IO变成顺序IO也只是优化，改变不了写入效率的数量级。

## 基本数据结构

1. remote dictionary service, 以网络接口对外提供字典服务。使用跟sql类似，主要操作对象是内存，快硬盘几个数量级。个人理解是共享内存模型的变种。
2. 字符串不是原生内存byte级别，可以适应简单扩充。有全局描述信息包括长度，容量。
3. 通用双向列表，可以用作队列或者栈。
4. 压缩列表用来处理小规模数据，是以数组来模拟双向链表。单个数据限制64bytes，数据规模限制512个。
5. 快速列表是结合使用通用双向和压缩列表。就是通用列表上的每个节点都是一个压缩列表。
6. hash字典的值只能是字符串，不知道是什么梗。渐进式hash扩容是结合惰性策略（活动操作触发）和定时器来完成。
7. set集合，特殊字典（value是nil），key无序。小规模整数又弄出了intset优化。
8. zset是按照key的权重排序后的set，排序以跳表实现。
9. 数据容器的原则是如果不存在就创造，容器空了就删除。
10. 过期时间还可以针对整个容器，到期后整个容器全部元素都过期。

## 再思考一下

1. 本质上是共享内存模型的变种？就是多了一个中间人，不知道是否可以这样理解。
2. 全局描述信息这个思路有大量使用。以极小的空间换取时间，毕竟单线程。字符串省了strlen的开销，链表有头尾和长度可以提供额外信息方便使用。
3. 通用双向列表，可以用作队列或者栈。
4. 原理省掉双向指针，保存头尾后计算偏移量，可以降低内存开销（少碎片，低gc压力），还有个好处是对缓存友好。但这种太抠门的做法不太适应变更，会有扩容复制和级联更新的问题。后面有个紧凑列表好一点点，但由于历史原因没有普及。
5. 这才是redis的主战场之一，处理大规模的读多写少的小元素。尽量规避了压缩列表的变更短板又用好了压缩列表的低内存开销，外层使用通用链表来突破512的规模。在微观上用上微观的好处，宏观上还是使用通用结构。又想起那句话，没有增加一个间接层解决不了的软件问题。如果不行，那就再加一层...
6. 没啥特别感觉，还是数组和链表的维度组合。hash高维度是数组低维度是链表，快速列表高维度是链表低维度是数组。貌似golang的map也这样，出来的晚的东西看空间换时间还是划算的。
7. 没啥特别感觉。
8. 可以理解成字典是一个维度，跳表是另外一个正交的维度（注意不是高低，二者没有关系）。前者关注寻址，后者关注排序。类似的东西有LRU，就是字典加普通链表。跳表30年前就有了，其他地方记录了相关理解。
9. 这玩意难不成是引用计数带来的原则...
10. 主动式过期时间更多还是为了安全考虑的，顺带还用在分布式锁了（所以还不能用于处理长耗时任务，就是任务时间大于加锁时间，扯远了）。

## 应用场景记录

1. 单机分布式锁，把锁和解锁都弄成原子操作（这是基本的要求。锁定同时包含超时设定，解锁就只好借助lua来做了）。多机有redlock，细节真多还请参考这位高手总结的Antirez和Martin之间的交流即可。[link] https://mp.weixin.qq.com/s?__biz=MzA4NTg1MjM0Mg==&mid=2657261514&idx=1&sn=47b1a63f065347943341910dddbb785d&chksm=84479e13b3301705ea29c86f457ad74010eba8a8a5c12a7f54bcf264a4a8c9d6adecbe32ad0b&scene=21#wechat_redirect
2. 消息队列简单版。如果消息的消费者少，而且没有高可靠性要求就可以用。尽量使用阻塞队列来降低两端的消耗，并在消费端做好服务端可能主动关闭连接的异常处理。
3. 位图（没啥特别，就是操作字符串，只是搬到了远端），理论上不复杂的数据结构都可以搬到远端。估计本地一维数据结构能做的事都能够搬到远端。不知道该怎么说，是舍本逐末还是懒，用个好听点的说法是工业界用法省时间。
4. RedisBloom，使用按比例缩小的空间成本的分布型概率数据结构。用来判断是否存在，不存在保证正确（过滤效果明显），存在只能保证大概率正确。可以用于防止缓存击穿而导致大量访问到达数据库。这类用法其实是在内存弄了个足够可用的缩小版本的数据库但只存储索引用于判定是否存在，是没有任何业务数据内容的。冷启动的时候的全量数据的内存重建发出的大量读请求以及数据删除都是麻烦问题。尽量用于语义合适的场景，例如快递公司的快递单号查询这种。这种容易输错也容易被滥用的查询入口，是很有必要做过滤的。方案可以将数据库中的所有能够用于用户查询的单号（假设只提供一个月内的查询），做成轮转的两个过滤器来阻挡不合理的输入。
5. HyperLoglog，使用固定的空间成本的推测型概率数据结构。为了概率的准确性，选取多样本的调和平均数。在数据样本足够大的场景可以做到90%以上准确性。
6. 限流。用rust写的模块，为啥都喜欢把这个事情搬到远端而且弄个自己喜欢的语言呢？linux的TC就有内核级别的限流代码。
7. 判断近邻。GeoHash本质上是把二维经纬度压扁成为一维数据，然后zset的范围功能就用上了。这些东西真不用都放redis里面，公益性质的微服务就可以了，免得浪费资源。估计各个具体行业的大佬有可能提会供这种接口，这应该成为一种趋势。
8. scan，为了减少对线上数据的影响提供的查找功能。主要是没有使用key做索引的容器，像查找特定前缀的key这种操作在mysql就很容易。
9. 单线程。只要不阻塞，G赫兹级别的CPU的单核单线程的处理能力飙到飞起，那可是9个0，每秒10亿级别的时钟频率基数。而主板能够带的起来的有效内存频率（ddr4 2000MHZ）数量级也差不远，加上内核提供的多路复用机制提供的缓冲，10W/s级别的QPS太正常了。这种存内存操作的程序都算是cpu密集型，估计网络（包含链路以及协议栈）最有可能是瓶颈。CPU也有可能，毕竟只用单核心。这个好解决，在内存足够的情况下部署多个实例做水平扩展即可。
10. 内存快照RDB snapshot是基于COW由fork出的子进程完成（还别说，古老的fork机制很适合这种单进程单线程的场景）。是个密集写磁盘的过程，频繁写会增加IO负担，但太久写数据丢太多了意义也不大。又得增加个间接层来解决，就是时间点配合增量记录。
11. 追加记录日志文件AOF是指令集的回放，这块有点类似mysql的binlog日志，但很大的区别在于过程的可追溯性。AOF可以重写来减少数据，单个文件对应整个完整的数据集，只保证最终结果不保证过程。binlog是连续的过程记录，可以按策略分成多段，状态可以跳回到任意过去的时间点。鉴于高性能与普通可靠性，生产环境下多采用秒级落盘。要性能又要安全的话，就搭建主从，主机高速对外服务不做持久化，从机不对外定期做持久化备份数据。
12. AOF恢复完整度高，RDB恢复速度快。
13. 混合持久化。增量AOF不再对应完整数据集，只对应快照点后面的小段增量记录操作。这样也可以做到恢复到任意过去时间点（没有重写AOF）
14. 事务（阉割版），估计用的人不太多吧。还有引申实现的乐观锁，真的并发高争抢严重的话那失败率和重试也是杠杠的。
15. 订阅发布，有那么多问题应该没人用吧。貌似后面出的stream带有消息持久化，明显借鉴kafka，要不专业的事情还是请专业的人做吧。
16. 主从。只有异步复制，只能追求最终一致性。同步借助与环形缓冲，快照同步（有无盘复制的优化）用来处理掉线太久的节点（数据量太大的话就算无盘复制够快，本地load的时间太久的话，主机环形缓冲不够用的时候就救不活了。看来设置大一点好，这个缓冲区跟从机数量没啥关系）看来持久化的功能是不是那么好用的，还是只做缓存就好了。（github就把redis中的持久化数据搬到GitHub::KV，一个基于Innodb的mysql键值对）
17. codis原理是使用hash来分片，再映射片与实例之间的关系，解耦了客户对实例的直接关联。片就是负载，负载均衡的技术一样有效（hash不错的话但靠片的个数就可以表示负载了）。codis集群的维护交给zk或者etcd，还有做片与实例的映射关系的持久化和更新共享。像MariaDB和mysql一样，第三方和官方的东西总是有点区别，工具做得快但核心功能被牵着鼻子走。
18. cluster去中心化，客户端也要知道映射关系了。我也没看出这个有啥好处，沟通成本会随着集群变大急剧增加，是N*N的关系。
19. 集群就不支持事务了，rename也不是原子操作了，基本上就是只能当缓存用了。话说不管是codis还是cluster都说不是特别给力，现在的redis的云存储就省功夫了。就是价格贵点，云厂商确实靠这个赚钱。
20. 过期策略中的数据隔离，增加扫描效率。这个从设计上看得出带过期的和不带过期的key分成两个集合就能看出谨慎之处了，高性能必然不能被过期策略拖累。最好不要让大量key同时过期，产生服务卡顿。还有一点过期后异步删除从机上的key可能出现主从不一致。
21. 过期策略中的LRU，没啥好记的。没有像mysql那样，在刷脏页的时候还有个热度分区的概念。
22. 过期策略中的惰性删除，这跟渐进式hash扩容神似。来个操作就顺带检查一下发现key过期了再做删除，把成本分摊下去。剩下的就靠后台异步线程慢慢处理了。
23. 安全。重定向危险指令，改变默认端口，增加授权。

## 性能

redis已经是极致的快了，那还有啥因数会影响性能呢？

1. 网络带宽和延迟通常是最大短板。两个金山云的主机， 同样的benchmark测试从本地发起和从另一个主机发起的测试结果相差几倍。按理一个是loopback的TCPsocket，一个相当于是外网的TCPsocket。![redis_benchmark](https://github.com/lichongsw/thinking/blob/master/images/redis_benchmark.png)
2. 在单核心的硬件，redis是更喜欢高频率大缓存，当然这个必须更贵。多核的意义不大，只能开多个实例。
3. redis在VM上会变慢，在docker容器中变化不大。

## 思考

1. 缓存穿透。这个严格意义上讲不是缓存的问题，就算用上布隆过滤器那冷启动的时候一样是要全表扫描的。让非法请求尽早被识别是另外一个话题，不管是代码错误还是外部攻击应该都要算在安全方面的，防御性编程的思想是一直要有的。例如最早都可以在客户端那拦截住请求，例如etcd的负载均衡的实现机制就是这种嵌入在客户端进程的。
2. 缓存击穿。这个又有点矛盾的感觉，为什么一个热点缓存会被清理掉导致大量的流量到达数据库？如果是为了不出现大量过期key占用内存的问题而强制所有的key都必须带有过期时间的话，那就没办法了。这玩意业务怎么的也会给你个热榜，首页之类的相对静态的东西，这类访问量大而且持续时间久的数据难道不应该是持久化数据吗？
3. 缓存雪崩。这个说法感觉有那么点伪命题。如果是缓存集群或者数据库冷启动，那刚开始数据库一样都是扛不住的。等于说要是加保险的话，不如直接监控数据库的状态决定要不要放流量进来。这跟汽车发动机类似，冷启动的时候需要限制油门和转速，等到各种油水温度上来了保证了润滑效果之后才能够稳定输出是一个道理。

## 参考记录

阿里社区的这篇经验性总结不错：https://developer.aliyun.com/article/728028?spm=a1z389.11499242.0.0.65452413JPs6l3&utm_content=g_1000089486