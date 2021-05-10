# 初学语言看特色，不看细节

基本信息说明（这个决定了语言的后台硬不硬，有没有可能产业化，不然学来干嘛。基金会是2个月前成立，说明目前由研发进入推广阶段了。这才是无国界的技术，有华为的财力支持哦，大国可以名正言顺的使用）：

https://learnku.com/rust/wikis/29009
Rust 是由 Mozilla 主导开发的通用、编译型编程语言。设计准则为「安全、并发、实用」，支持函数式、并发式、过程式以及面向对象的编程风格。在 2010 年官方首次揭露了它的存在。也在同一年，其编译器由原本的 OCaml 语言编写的源代码开始转移到用 Rust 语言编写，进行 Bootstrapping 工作，称做 rustc，并于 2011 年完成。这个可实现自我编译的编译器在架构上采用了 LLVM 作为它的后端。

Rust 语言作者
Rust 语言原本是 Mozilla 员工 Graydon Hoare 的私人项目，Mozilla 于 2009 年开始赞助这个项目。目前，Graydon Hoare 已经从 Mozilla 离职。

Graydon Hoare 自称为职业编程语言工程师，关于 Graydon Hoare 的相关信息非常少，感兴趣的同学可以关注他的推特。

Rust 维护组织
Rust 有一个庞大的项目系统维护组织，其中最突出的是由 Rust 开发者 组织的，在 GitHub 上负责维护 Rust 的 rust-lang 组织。

Rust 基金会的成立
2021 年 2 月 8 日，Rust 基金会在其临时执行董事的一篇 hello world 文章发布后宣布成立，其基金会董事成员有：aws、Google、华为、微软、Mozilla 。Rust 基金会诞生自 Rust 核心团队，并且得到了五位全球行业领先公司的财务承诺。这标志着 Rust 向成熟化迈出了坚实的一步，相信 Rust 会在基金会的领导下与社区的努力下不断进步。



**一看内存管理（所有权机制以及智能指针）**

**二看编程范式。这家伙有泛型（golang2.0即将引入，看看跟C++有啥区别），有函数式（看纯粹程度，是否实用。是一个lambda还是haskell的级别），也有面向对象（应该类似golang以组合为本，不是C++的继承。或者还有新意）。大概率没有啥新意，只是支持这些范式而已**

**三看runtime。看看线程的调度和并发（感觉可能类似golang的GMP，是以消息传递为主的并发模型）**

**四看大佬对缺点的评价。太阳底下没有多少新鲜事，如果一个新语言什么都是最优秀还没有短板那还有其他语言什么事情**



## 1. 内存管理

内存管理就是如何使用堆与栈。堆上的分配与回收（这里有 https://www.ituring.com.cn/book/1460 ”垃圾回收的算法与实现“的总结）。栈管理没啥花样，有特色一点的golang改变了划分单位（每个协程都有自己的栈空间，来存放变量，函数，寄存器等信息，避免上下文切换开销）。rust在这高度产业化的局面中还能玩出花说明发起者肯定是另辟蹊径了。

### 1.1 所有权

这是个化繁为简的操作，第一作者Graydon Hoare肯定是有深刻认知之人。从C时代开始的手动管理内存，到RAII然后再到GC，这是一个持续的工程化的进步（个人观点：不一定是技术进步，只能说绝大部分需求可以容忍GC的延迟，毕竟GC的进步非常大已经有非常好的民用体验了。如果换到竞争性质的军事或者交易行业，STW基本不可接受，下达指令后执行慢了20ms大概率就会被吊打）。



[所有权规则](https://kaisery.github.io/trpl-zh-cn/ch04-01-what-is-ownership.html#所有权规则)

首先，让我们看一下所有权的规则。当我们通过举例说明时，请谨记这些规则：

> 1. Rust 中的每一个值都有一个被称为其 **所有者**（*owner*）的变量。
> 2. 值在任一时刻有且只有一个所有者。
> 3. 当所有者（变量）离开作用域，这个值将被丢弃。



大神直接把生命周期的管理给明确的限制住了，这不同于C的纯程序员管理，也不是C++的半自动管理，更不是golang完全由系统管理。像小说或者游戏里面的宝宝必须订立契约才能出生一样，不隶属于谁的时候就死了。没有孤岛，角色死了宝宝也死了。这个模型足够简单，但工程化方面有诸多不便。所以需要放松一些限制。契约（拥有权）可以转移了（move语义，新的owner负责生命周期。等于锲约被转让了），和被引用（完全不同于C++的引用，这里是借用）

**转移：转让之后原有的契约失效，原主失去拥有权，也没有使用权**

将值传递给函数在语义上与给变量赋值相似。向函数传递值可能会移动或者复制，就像赋值语句一样

```rust
let s1 = String::from("hello");
let s2 = s1;

println!("{}, world!", s1);

error[E0382]: use of moved value: `s1`
 --> src/main.rs:5:28
  |
3 |     let s2 = s1;
  |         -- value moved here
4 |
5 |     println!("{}, world!", s1);
  |                            ^^ value used here after move
  |
  = note: move occurs because `s1` has type `std::string::String`, which does
  not implement the `Copy` trait
```

**引用（借用）：临时借用一下，再还回去。拥有权没有变更**

不能随便调用个函数就把契约转来转去，有时候只是用一下。借用分读和写借用，就是C++的const变量语义。既然是借那原主只有一个宝宝，所以无损借用可以借给多方，反正是顺序执行。至于写契约，那借用后是可以修改。

如果同时借出读和写两种(前提是原契约就必须包含可写)，就有竞争问题了，在编译期就能避免这是多么安全（如果没有被race condition折磨的很惨，大概率编程是在工具层面，例如翻译数学和物理公式以及调用成熟的库的接口完成业务功能，要么因为你不用做，要么因为别人给你做好了。看起来编程没有太多门槛或者叫做科学的东西，因为这个不容易描述或者还没有被很好的描述，但事实上这玩意跟内存问题（都有幽灵效果）在C++的项目中花费的时间能够占到解决问题的8层以上，逻辑bug的耗时绝对低于2层。这点不用反驳，懂的自然懂）

```rust
    let mut s = String::from("hello");
    let r1 = &s;
    // let r2 = &s;
    // println!("r1:{}, r2:{}", r1, r2);
    // let r1 = &mut s;
    let r2 = &mut s;
    println!("r1:{}, r2:{}", r1, r2);
```

错误如下：

```
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> src\main.rs:7:14
  |
3 |     let r1 = &s;
  |              -- immutable borrow occurs here
...
7 |     let r2 = &mut s;
  |              ^^^^^^ mutable borrow occurs here
8 |     println!("r1:{}, r2:{}", r1, r2);
  |    
```



对于可写的契约，是不能多次出借的。

```rust
let mut s = String::from("hello");

let r1 = &mut s;
let r2 = &mut s;

println!("{}, {}", r1, r2);
```

错误如下：

```text
error[E0499]: cannot borrow `s` as mutable more than once at a time
 --> src/main.rs:5:14
  |
4 |     let r1 = &mut s;
  |              ------ first mutable borrow occurs here
5 |     let r2 = &mut s;
  |              ^^^^^^ second mutable borrow occurs here
6 |
7 |     println!("{}, {}", r1, r2);
  |                        -- first borrow later used here
```

这跟读写锁的思想类似，但在语义层面把明确下来，用明确的归属权来确认谁可以操作。

这个限制的好处是 Rust 可以在编译时就避免数据竞争。**数据竞争**（*data race*）类似于竞态条件，它可由这三个行为造成：

- 两个或更多指针同时访问同一数据。（通常讲的是多线程环境，但多协程也是有可能的。就是数据发生了执行单元预期以外的修改，调试问题不就是在确认是谁在捣蛋嘛）
- 至少有一个指针被用来写入数据。（都是读没问题，至少有一个人写才会有问题）
- 没有同步数据访问的机制。（独写锁，互斥锁，原子操作之类）

注意一个引用的作用域从声明的地方开始一直持续到最后一次使用为止。所以这个照顾了安全编程，但又照顾了工程化效率：

```rust
let mut s = String::from("hello");

let r1 = &s; // 没问题
let r2 = &s; // 没问题
println!("{} and {}", r1, r2);
// 此位置之后 r1 和 r2 不再使用

let r3 = &mut s; // 没问题
println!("{}", r3);
```

这个可能会有点不习惯，一段代码放的位置不一样直接就编译失败。鼓励在最小范围内高类聚的完成紧耦合的事情，所以编码习惯好的人更容易接受（变量只在必须用的时候才申明，有明确的作用域概念不用立马就还回去，不随意保留和扩大作用域）。个人推测：作者可能希望内存的使用方式尽量靠近栈，没办法了再使用堆（golang里面已经可以有逃逸控制的概念，就是编译器有能力就尽量使用更可控的内存）。栈可以高效的快速完成一项工作再以干净的现场来进入下一项（工作之间是无状态的，不会被各种共享变量所牵制）



概括一下引用（借用）的约束：

- 在任意给定时间，**要么** 只能有一个可变引用，**要么** 只能有多个不可变引用。
- 引用必须总是有效的。

**由此可见rust内存和生命周期的管理核心思想大道至简，只要控制点是唯一的就不可能发生冲突。而且这是编译时就能够确定的事情，会提示你潜在的风险。**



### 1.2 生命周期

从手册上看这段话，有点不知所云：

*大部分时候生命周期是隐含并可以推断的，正如大部分时候类型也是可以推断的一样。类似于当因为有多种可能类型的时候必须注明类型，也会出现引用的生命周期以一些不同方式相关联的情况，所以 Rust 需要我们使用泛型生命周期参数来注明他们的关系，这样就能确保运行时实际使用的引用绝对是有效的。*

接着还有个结论：生命周期的主要目标是避免悬垂引用。虽然不知所云，但还是描述一下为什么野指针是不存在的，在rust中搞不出来这种问题。

```rust
{
    let r;

    {
        let x = 5;
        r = &x;
        // r = x;
    }

    println!("r: {}", r);
}

error[E0597]: `x` does not live long enough
  --> src/main.rs:7:5
   |
6  |         r = &x;
   |              - borrow occurs here
7  |     }
   |     ^ `x` dropped here while still borrowed
...
10 | }
   | - borrowed value needs to live until here

```

这段r可以借用x，但只能在x还有意义的时候使用。也好理解，借用没有改变所属权，如果原主x没有了岂不是借的东西不用还啦。不存在持有一个引用，指向的内存可能已经被回收或者分配给别人的情况。能够合法持有这个引用的前提就是这玩意还有效，借出来之后如果原主（主动或者被动）清理了就自动失效了，编译器会盯着这一切。



这个例子说明了生命周期很有可能是rust的一等公民。就像引用，类型之类的一个级别的元属性（例如模板元编程中的type）。比较函数明确了result的生命周期等同于两个输入x, y二者中比较短的那个。所以string2结束了result也结束了，不能再访问了。

```rust
fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
        println!("The first test longest string is {}", result);
    }
    // println!("The second test longest string is {}", result);
}

fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// 注释掉的第二个打印语句报错
error[E0597]: `string2` does not live long enough
  --> src\main.rs:40:44
   |
40 |         result = longest(string1.as_str(), string2.as_str());
   |                                            ^^^^^^^ borrowed value does not live long enough
41 |         println!("The first test longest string is {}", result);
42 |     }
   |     - `string2` dropped here while still borrowed
43 |     println!("The second  test longest string is {}", result);
   |                                                       ------ borrow later used here
```

当从函数返回一个引用，返回值的生命周期参数需要与一个参数的生命周期参数相匹配。如果返回的引用 **没有** 指向任何一个参数，那么唯一的可能就是它指向一个函数内部创建的值，它将会是一个悬垂引用。

对于一类属性那应该有很明显的代码痕迹，但很多时候编译器可以推断出来的时候就不需要写了。例如这个在早期的编译器中不行，但后期就可以。缺省的规则被隐藏在编译器里面了，可以适当的减轻不爽的感觉（前提是你知道在干啥。例如下面的例子返回字符串中第一个单词，你并不需要新的变量，所以返回一个slice的引用即可。自然这个生命周期就跟输入参数一致了）。

```rust
// fn first_word<'a>(s: &'a str) -> &'a str {
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
```

第一条规则是每一个是引用的参数都有它自己的生命周期参数。换句话说就是，有一个引用参数的函数有一个生命周期参数：`fn foo<'a>(x: &'a i32)`，有两个引用参数的函数有两个不同的生命周期参数，`fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`，依此类推。

第二条规则是如果只有一个输入生命周期参数，那么它被赋予所有输出生命周期参数：`fn foo<'a>(x: &'a i32) -> &'a i32`。

第三条规则是如果方法有多个输入生命周期参数并且其中一个参数是 `&self` 或 `&mut self`，说明是个对象的方法(method)(译者注： 这里涉及rust的面向对象), 那么所有输出生命周期参数被赋予 `self` 的生命周期。第三条规则使得方法更容易读写，因为只需更少的符号。



## 2. 编程范式

泛型，函数式，面向对象三种都支持，看看分别做到什么程度了

### 2.1 泛型

泛型是具体类型或其他属性的抽象替代。我们可以表达泛型的属性，比如他们的行为或如何与其他泛型相关联，而不需要在编写和编译代码时知道他们在这里实际上代表什么。看看这个返回整型以及字符slice中最大的那个值，是不是跟C++非常的相似。看起来是一个模子，泛型的参数，成员之类都是可以用的。

```rust
fn largest_i32(list: &[i32]) -> i32 {
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn largest_char(list: &[char]) -> char {
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest_i32(&number_list);
    println!("The largest number is {}", result);

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest_char(&char_list);
    println!("The largest char is {}", result);
}
```

立马可以追溯一下会不会同样有模板展开的问题呢？Rust 通过在编译时进行泛型代码的 **单态化**（*monomorphization*）来保证效率。单态化是一个通过填充编译时使用的具体类型，将通用代码转换为特定代码的过程。这明显是跟C++有同样问题的，编译时间和体积都是爆炸的。哈哈，golang目前没有这个问题，但2.0引入泛型之后那不是一样也得掉到这坑里，就看有没有创新的办法了。看看大牛Brian Anderson （Rust 编程语言及其姊妹项目 Servo Web 浏览器的共同创始人之一）的积累：Rust 编译模型之殇 https://cloud.tencent.com/developer/article/1594498



这种既视感明显就是元编程的精髓了，golang就是这个方向。如果实现了某类操作就可以使用接口，而不是C++继承语义中的必须是某类东西才可以用该类东西的接口。这里有比较（PartialOrd），还有赋值（largest = list[0]，需要Copy）。任何实现了这两个操作的类型都可以调用这个方法。

```
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }

    largest
}
```

### 2.2 函数式

两个基础特性，看起来是中等程度。

- **闭包**（*Closures*），一个可以储存在变量里的类似函数的结构
- **迭代器**（*Iterators*），一种处理元素序列的方式

#### 2.2.1 闭包

先贴一个来自[维基百科](https://zh.wikipedia.org/wiki/闭包_(计算机科学))上的描述概念：

闭包（英语：`Closure`），又称词法闭包（`Lexical Closure`）或函数闭包（`function closures`），是**引用了自由变量的函数**。这个被引用的自由变量将和这个函数一同存在，即使已经离开了创造它的环境也不例外。所以，有另一种说法认为闭包是由函数和与其相关的引用环境组合而成的实体。闭包在运行时可以有多个实例，不同的引用环境和相同的函数组合可以产生不同的实例。

<font color='red'>明确说明是使用了自由变量的函数，一种特殊的函数（闭包作为变量或者作为参数影响函数）</font>

[闭包类型推断和注解](https://kaisery.github.io/trpl-zh-cn/ch13-01-closures.html#闭包类型推断和注解)

闭包不要求像 `fn` 函数那样在参数和返回值上注明类型。函数中需要类型注解是因为他们是暴露给用户的显式接口的一部分。严格的定义这些接口对于保证所有人都认同函数使用和返回值的类型来说是很重要的。但是闭包并不用于这样暴露在外的接口：他们储存在变量中并被使用，不用命名他们或暴露给库的用户调用。

**闭包通常很短，并只关联于小范围的上下文而非任意情境。在这些有限制的上下文中，编译器能可靠的推断参数和返回值的类型，类似于它是如何能够推断大部分变量的类型一样。**

```rust
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

第一行展示了一个函数定义，而第二行展示了一个完整标注的闭包定义。第三行闭包定义中省略了类型注解，而第四行去掉了可选的大括号，因为闭包体只有一行。这些都是有效的闭包定义，并在调用时产生相同的行为。

闭包定义会为每个参数和返回值推断一个具体类型，如果尝试对同一闭包使用不同类型则会得到类型错误。

<font color='red'>这段内容为摘录，没看出新意。如果只是一个匿名函数而已，看不出有何不同</font>



接着看更细节的内容，闭包被分为了三种类型列举如下（应该说是更精细，被迫要适应可变/不可变的共享，还有传值的基本套路。看起来就是传统闭包和rust独有的生命周期管理相结合，可能用起来有点绕）：

- [Fn(&self)](https://doc.rust-lang.org/std/ops/trait.Fn.html)

  参数类型是`&self`，这种类型的闭包是不可变借用，不会改变变量也不会释放该变量。可以运行多次

  ```rust
  pub trait Fn<Args>: FnMut<Args> {
      pub extern "rust-call" fn call(&self, args: Args) -> Self::Output;
  }
  ```

- [FnMut(&mut self)](https://doc.rust-lang.org/std/ops/trait.FnMut.html)

  参数类型是`&mut self`，这种类型的闭包是可变借用，会改变变量但不会释放该变量。可以运行多次

  ```rust
  pub trait FnMut<Args>: FnOnce<Args> {
      pub extern "rust-call" fn call_mut(&mut self, args: Args) -> Self::Output;
  }
  ```

  

- FnOnce(self)](https://doc.rust-lang.org/std/ops/trait.FnOnce.html)

  参数类型是`self`，这种类型的闭包会获取变量的所有权（就是rust的默认move语义，变量赋值就移交了），生命周期只能是当前作用域就会被释放了。只能运行一次

  ```rust
  pub trait FnOnce<Args> {
      type Output;
      pub extern "rust-call" fn call_once(self, args: Args) -> Self::Output;
  }
  ```

  

来自于这篇文章整理的图片：（https://tonydeng.github.io/2019/11/09/rust-closure-type/）

[![Rust的三种闭包类型](https://tonydeng.github.io/images/blog/rust/rust-closure.jpg)](https://tonydeng.github.io/images/blog/rust/rust-closure.jpg)



#### 2.2.2 迭代器

这里是更好的表现方式

```rust

#![allow(unused)]
fn main() {
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // 此处省略了方法的默认实现
}
}
```

`next` 是 `Iterator` 实现者被要求定义的唯一方法，在迭代器上调用 `next` 方法改变了迭代器中用来记录序列位置的状态，迭代器被使用完后就失效了。再举个具体的例子，`iter` 方法生成vector中的值的不可变引用的迭代器之后被消费函数（map，filter各种操作都行）消费后得到新的迭代器，最后使用collect把处理后的数据放入新的vector：

```rust
let numbers = vec![3, 6, 9, 12];
let result: Vec<i32> = numbers
    .iter()
    .map(|n| n * 10)
    .collect();
// result is now [30, 60, 90, 120]

We declare a new variable called numbers and use the macros vec! in order to initialize a new vector with the provided number values.

We use the .iter() method on the vector in order to obtain an iterator.

We use the .map() method to execute a closure over each element yielded by the iterator. In other words, the closure is executed for each element in the vector of numbers.
```



闭包和迭代器是 Rust 受函数式编程语言观念所启发的功能，牛逼的地方是迭代器是 Rust 的 **零成本抽象**（*zero-cost abstractions*）之一，它**意味着抽象并不会引入运行时开销**（编译器高级可以优化得很好，写应用程序的人比较容易写出易懂还有好性能的代码，高级概念来实现底层代码就有优势了）。他们对 Rust 以底层的性能来明确的表达高级概念的能力有很大贡献。闭包和迭代器的实现达到了不影响运行时性能的程度。

```rust
let buffer: &mut [i32];
let coefficients: [i64; 12];
let qlp_shift: i16;

for i in 12..buffer.len() {
    let prediction = coefficients.iter()
                                 .zip(&buffer[i - 12..i])
                                 .map(|(&c, &s)| c * s as i64)
                                 .sum::<i64>() >> qlp_shift;
    let delta = buffer[i];
    buffer[i] = prediction as i32 + delta;
}
```

<font color='red'>看起来挺美，这种优化应该是对迭代和闭包的小范围使用中的循环控制以及寄存器使用达到了一定的水平。高级特性被翻译成了高性能的汇编代码，这种因该是比较难的，这个零成本抽象的概念很好，但实现程度也不一定有多高（这个得学的多用的多才有发言权）</font>

## 3. runtime

**并发编程**（*Concurrent programming*），代表程序的不同部分相互独立的执行，而 **并行编程**（*parallel programming*）代表程序不同部分于同时执行。<font color='red'>理解并发模型基本上就明白核心的运行时操作了，例如golang的GMP调度+Chanel消息传递。至于其他的库都是功能扩展，需要使用时按照手册直到使用即可</font>

### 3.1 线程

编程语言有一些不同的方法来实现线程。很多操作系统提供了创建新线程的 API。这种由编程语言调用操作系统 API 创建线程的模型有时被称为 *1:1*，一个 OS 线程对应一个语言线程。

很多编程语言提供了自己特殊的线程实现。编程语言提供的线程被称为 **绿色**（*green*）线程，使用绿色线程的语言会在不同数量的 OS 线程的上下文中执行它们。为此，绿色线程模式被称为 *M:N* 模型：`M` 个绿色线程对应 `N` 个 OS 线程，这里 `M` 和 `N` 不必相同。

绿色线程的 M:N 模型需要更大的语言运行时来管理这些线程。因此，Rust 标准库只提供了 1:1 线程模型实现。由于 Rust 是较为底层的语言，如果你愿意牺牲性能来换取抽象，以获得对线程运行更精细的控制及更低的上下文切换成本，你可以使用实现了 M:N 线程模型的 crate。

<font color='red'>看起来跟golang并不一样，但是提供M:N的实现方式。</font>

**Go 有栈协程**

`Go`语言的出现提供了一种新的思路。`Go`语言的协程则相当于提供了一种很低成本的类似于多线程的执行体。在`Go`语言中，协程的实现与操作系统多线程非常相似。操作系统一般使用抢占的方式来调度系统中的多线程，而`Go`语言中，依托于操作系统的多线程，在运行时刻库中实现了一个协作式的调度器。这里的调度真正实现了上下文的切换，简单地说，`Go`系统调用执行时，调度器可能会保存当前执行协程的上下文到堆栈中。然后将当前协程设置为睡眠，转而执行其他的协程。这里需要注意，所谓的`Go`系统调用并不是真正的操作系统的系统调用，而是`Go`运行时刻库提供的对底层操作系统调用的一个封装。

```go
func routine() int
{
    var a = 5
    sleep(1000)
    a += 1
    return a
}
```

sleep调用时，会发生上下文的切换，当前的执行体被挂起，直到约定的时间再被唤醒。局部变量a 在切换时会被保存在栈中，切换回来后从栈中恢复，从而得以继续运行。所谓有栈就是指执行体本身的栈。每次创建一个协程，需要为它分配栈空间。究竟分配多大的栈的空间是一个技术活。分的多了，浪费，分的少了，可能会溢出。`Go`在这里实现了一个协程栈扩容的机制，相对比较优雅的解决了这个问题。有栈协程看起来还是比较直观，特别是对于开发人员比较友好。

**rust无栈协程**

早期的`Rust`支持一个所谓的绿色线程，其实就是有栈协程的实现，与`Go`协程实现很相似。在0.7之后，绿色线程就被删除了。其中一个原因是，如果引入这样的机制，那么运行时刻库也必须如`Go`语言一样能够支持有栈协程，也就是之前讨论`Go`题外话提到的内容。`Go`没有Native thread的概念，语言层面只支持协程，选择封装全部的系统调用很合理。rust的无栈协程不使用栈和上下文切换来执行异步代码逻辑的机制。这里异步代码虽然是异步的，但执行起来看起来是一个同步的过程。从这一点上来看`Rust`协程与`Go`协程也没什么两样。举例说明：

```rust
async fn routine() 
{
    let mut a = 5;
    sleep(1000).await;
    a = a + 1;
    a
}
```

 Generator 生成的状态机。Generator 和闭包类似，能够捕获变量a，放入一个匿名的结构中，在代码中看起来是局部变量的数据 a，会被放入结构，保存在全局（线程）栈中。另外值得一提的是，Generator 生成了一个状态机以保证代码正确的流程。从sleep.await 返回之后会执行 a=a+1 这行代码。async routine() 会根据内部的 .await 调用生成这样的状态机，驱动代码按照既定的流程去执行。<font color='red'>这里还是使用了线程的栈，只能说不同于golang的协程栈，该保存还是要保存的。看来async/await才是rust提供的解决方案（就是future/promise的机制。一个Future代表一个现在**可能还没有结果**（或者在等待IO完毕或者还没有被调度到CPU上去实际执行），但是**将来会返回某个结果**的抽象过程。将来会返回的结果抽象为`Promise`，即承诺一定会返回的某个东西）</font>

```rust
trait Future {
    type Output;
    fn poll(self: Pin<&mut self>, ctx: &mut Context<'_>) -> Poll::(Self::Output);
}
```

<font color='red'>对地并发问题有完全不同的实现方式，真的很精彩。golang以强大的运行时来分解语言的功能来做出清晰简单的高并发程序（并发是一等公民，go是解决问题的生产力工具）。而rust的选择把并发做成了一种可扩展的特性，而且可以证明并发的正确性。个人意见：**二者并不是真正的竞争关系，rust是系统级的最有选择，而go是应用级的最佳选择（明显超出其他竞品的性能）。以国内项目的需求来说大部分时候应该选go，rust是性能真的非常重要的项目才选。**rust似乎是大型平台公司C++项目的有力竞争者（要求性能，主要是给应用程序提供底层能力产品，例如存储系统，浏览器内核甚至游戏引擎），go似乎独一档适合中小规模的后台服务（目前应该是没有竞争对手的，即使用rust去重写go的项目意义不大。对于业务的快速响应，go的学习曲线和正确的姿势都是大优势。这种场景中对性能没有那么敏感，简洁快速才是网络高并发程序的痛点）。目前站台的大佬aws、Google、华为、微软、Mozilla都是有这类需求的，还真说不好以后rust会产出许多重量级的产品（Firefox 的新的内核 Servo，TiDB 的存储层 TiKV）</font>



## 4. 大佬评价缺点

本章节来自翻译文章 Rust 编译模型之殇 https://cloud.tencent.com/developer/article/1594498。在记录的同时可能会补充一下对某些事实的观点

### 4.1 运行时优先于编译时的早期决策

<font color='red'>先表面个人观点，从一般开发者的角度看这个方向没有问题。没有多少企业的单个产品是100W行代码级别（全新构建要以小时为单位），编译期间如果能够付出代价带来运行期的安全和效率那我个人持支持态度，在线上救火（解决由于弱类型，竞争产生问题用掉的时间不会比编译时间少，而且已经伤害到用户了）。大神的视角不一样，做的是平台型大项目当然会吐槽这个等待时间的问题（这是精益求精的工程师视角才会有的严苛要求，不代表大部分群体的看法。按照以前的经验这个级别的项目要规划好模块拆分与单元测试，大部分的修改只需要少量的模块重新编译即可在单元测试中完成功能验证。全量构建的随机测试和覆盖测试的频率跟迭代周期相关，而且主要是测试来负责，不会明显影响开发人员的效率）。编译时间和体积只是牺牲机器资源，相比人力资源和用户体验来说这些不在一个层次（机器的效率和资源的价格随着工艺和规模的成熟会变成白菜价）。赚快钱的产品除外（怎么快就怎么来，出大问题就解决问题不行就赔偿，1~2年关门收工赚的盆满钵满大家都开心）</font>

如果是 Rust 设计导致了糟糕的编译时间，那么这些设计具体又是什么呢？我会在这里简要地描述一些。本系列的下一集将会更加深入。有些在编译时的影响比其他的更大，但是我断言，所有这些都比其他的设计耗费更多的编译时间。

现在回想起来，我不禁会想，“当然，Rust 必须有这些特性”。确实，如果没有这些特性，Rust 将会是另一门完全不同的语言。然而，语言设计是折衷的，这些并不是注定要成 Rust 的部分。

- **借用（Borrowing）**——Rust 的典型功能。其复杂的指针分析以编译时的花费来换取运行时安全。 <font color='red'>如果去掉借用语义，只有移动语义的话会有什么问题？Rust默认就是移动语义，在需要拷贝的时候要明确的实现clone，而不是像C++提供那么多的默认行为给使用者负担（copy，move，copy assign, move assign）。Rust 的引用更接近原始的 C的指针，与取地址运算符（&）与解引用符号（*）的用法是一致的（甚至*作为指针类型这点也是通用的）。rust的指针类型还有smart point（实现了 Deref、drop 相关的trait，例如String）。 raw point和一个有争议的fat point（例如切片有指针和长度两个字段）。声明一下在写这个记录的时候本人对于后面几种类型的指针还没有深入学习，没有能力评价）。这个功能恐怕是不能去掉的，这可不是哪个语言的专利。如果rust还想要C语言级别的效率，是很难避免取地址和解引用的功能的，只能在上面包装各种限制来制衡操作地址的副作用。</font>

- **单态化（Monomorphization）**——Rust 将每个泛型实例转换为各自的机器代码，从而导致代码膨胀并增加了编译时间。<font color='red'>如果不这样，那泛型还能怎么做？期待golang2.0的泛型思路，看看能不能在工程角度取得更好的平衡</font>

- **栈展开（Stack unwinding）**——不可恢复异常发生后，栈展开向后遍历调用栈并运行清理代码。它需要大量的编译时登记（book-keeping）和代码生成。

- **构建脚本（Build scripts）**——构建脚本允许在编译时运行任意代码，并引入它们自己需要编译的依赖项。它们未知的副作用和未知的输入输出限制了工具对它们的假设，例如限制了缓存的可能。<font color='red'>这似乎可以不被吐槽。除非语言生态强大到自举，外部依赖都是本语言实现</font>

- **宏（Macros）**——宏需要多次遍历才能展开，展开得到的隐藏代码量惊人，并对部分解析施加限制。过程宏与构建脚本类似，具有负面影响。<font color='red'>golang就没有支持宏，但要付出代价。如果不乱使用（宏的使用可是分好坏的。处理文本的preprocessor的宏难以维护，C/C++中还有各种所谓的展开技巧，还有人拿这个面试只能MMP。好一点的用法是服用语言的功能，结合语言做一些简化编程顺便提高性能的技巧），这里举个例子。</font>

  ```go
  type errWriter struct {
   w   io.Writer
   err error
  }
  func (ew *errWriter) write(buf []byte) {
   if ew.err != nil {
    return // 当已经出错时，什么都不写入
   }
   _, ew.err = ew.w.Write(buf) // 这一行
  }
  func doIt(fd io.Writer) {
   ew := &errWriter{w: fd}
   ew.write(p0[a:b])
   ew.write(p1[c:d])
   ew.write(p2[e:f])
   // 等等
   if ew.err != nil {
    return ew.err
   }
  }
  
  // rust 用try！ 或者 ？ 来返回`Result <T, Error>`, 任何一个步骤错误直接就返回了
  // try!(xx.write(p0[a:b])) 
  // try!(xx.encode(p0[a:b])) 
  // try!(xx.encrypt(p0[a:b])) 
  ```

  <font color='red'>golang一直检查错误是很痛苦的，所以这里提供了直到结束之前都会忽略错误的方法，否则你得每一步都写一个啰嗦的东西。这只能说刚好连续3个同样的操作可以用这种创可贴代码，如果是不同类型的操作那这个创可贴是不是要继续扩展下去（io.Writer用来写，加个新步骤就得在struct中继续添加类型是典型大杂烩创可贴，只能添加新的errEncode, errEncrypt结构体不胜其烦）。try! 宏（后期换成? operator就更加合理）在方法执行失败后返回泛型结果Result <T, Error>，岂不简洁。golang看来已经抵挡不了泛型的诱惑了，2.0正在研究中。扯远了这个例子中宏能够换成operator说明正确的用法也可以被更加良好的方式替代，这是语言进化的能力</font>

- **LLVM 后端（LLVM backend）**——LLVM 产生良好的机器代码，但编译相对较慢。<font color='red'>主流都这么干了，这点可以不被吐槽</font>

- **过于依赖LLVM优化器（Relying too much on the LLVM optimizer）**——Rust 以生成大量 LLVM IR 并让 LLVM 对其进行优化而闻名。单态化则会加剧这种情况。

- **拆分编译器/软件包管理器（Split compiler/package manager）**——尽管对于语言来说，将包管理器与编译器分开是很正常的，但是在 Rust 中，至少这会导致 cargo 和 rustc 同时携带关于整个编译流水线的不完善和冗余的信息。当流水线的更多部分被短路以便提高效率时，则需要在编译器实例之间传输更多的元数据。这主要是通过文件系统进行传输，会产生开销。

- **每个编译单元的代码生成（Per-compilation-unit code-generation）**——rustc 每次编译单包（crate）时都会生成机器码，但是它不需要这样做，因为大多数 Rust 项目都是静态链接的，直到最后一个链接步骤才需要机器码。可以通过完全分离分析和代码生成来提高效率。

- **单线程的编译器（Single-threaded compiler）**——理想情况下，整个编译过程都将占用所有 CPU 。然而，Rust 并非如此。由于原始编译器是单线程的，因此该语言对并行编译不够友好。目前正在努力使编译器并行化，但它可能永远不会使用所有 CPU 核心。

- **trait 一致性（trait coherence）**——Rust 的 trait（特质）需要遵循“一致性（conherence）”，这使得开发者不可能定义相互冲突的实现。trait  一致性对允许代码驻留的位置施加了限制。这样，很难将 Rust 抽象分解为更小的、易于并行化的编译单元。

- **“亲密”的代码测试（Tests next to code）**——Rust 鼓励测试代码与功能代码驻留在同一代码库中。由于 Rust 的编译模型，这需要将该代码编译和链接两次，这份开销非常昂贵，尤其是对于有很多包（crate）的大型项目而言。