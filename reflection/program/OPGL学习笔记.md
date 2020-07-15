## 词汇

https://www.jianshu.com/p/2f093554ad57

https://www.jianshu.com/p/c33c7e2bdfd4

- 顶点数组对象：Vertex Array Object，VAO
- 顶点缓冲对象：Vertex Buffer Object，VBO
- 索引缓冲对象：Element Buffer Object，EBO或Index Buffer Object，IBO
- OpenGL着色器语言(OpenGL Shading Language, GLSL



## 基础

#### 链路

作者：Ritsuka ding
链接：https://www.zhihu.com/question/66848391/answer/247151912
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

GPU 图形硬件，图形处理器。和CPU差别在于计算单元是CPU的上百倍，不过计算功能更为有限，可以想象成适合对大量浮点数异步运算的芯片。

显存，GPU可以快速读取的一种内存。

OpenGL，图形编程的接口，也就是图形API。DX同理。

Unity3D，游戏引擎，内部包含渲染模块可以让用户能够更简单的与Opengl交互。



1，不管是ray-tracing还是光栅化渲染，场景内容是一样的，无非就是一堆位置坐标，字符串信息，以及贴图信息。

2，这些信息需要先用CPU讲硬盘里的内容转移到内存，然后经过CPU的一定处理后（比如角色移动）用Opengl接口转交给显存。然后通过GPU来处理显存内容。

这部分深入理解的话可以参考一下计算机图形学的历史。

20-30年以前，显卡是不具备3D处理功能的。当时的开发者需要完全自己从头写汇编来实现3D。当时的显卡只是将显存中的内容转交给显示器。

后来，出现了Voodoo卡，也就是专门用来计算3D数据的卡，当时需要既有一块Voodoo也要有一块显卡，也就是需要先把数据交给Voodoo卡运算出结果，然后结果再输给显卡。

再后来，显卡厂商开始在显卡中加入3D运算芯片，也就是GPU了，后来就越来越强大。然而当时的运算方式比现在更有限，都是固定好的计算方式。并且没家厂商的SDK也都不一样。

再后来，opengl/DX成为了行业标准，出现了可编程的接口，也就是shader。逐步从Vertex shader进化出pixel shader，geometry shader，也就成了今天这个样子。

历史进程证明了把3D运算放到显卡里是合理的选择。

说了这些，答案也就显而易见了。

比方说游戏程序用C写，那么C用到的内存都只是内存，通过opengl分配的才是缓存。shader中用的都是显存。具体布局查看相关文档就好了。

3，OpenGL/DX是行业标准，也就是说显卡厂商倒也可以自己做SDK，但做了又怎样，也没人买账啊。Opengl/DX已经很完善了，显卡厂商做个驱动，对接上Opengl/DX就好了。自己做定制化其实也不少见，比如Nvidia的CUDA这种。这种呢，就是把个别的技术接口对应转交给app程序员了。

4，渲染只是游戏引擎的一部分，不是全部，所以Unity3D是对OpenGL的封装这点来说，对Opengl封装只是Unity3D的一小部分。

游戏图形绘制主要差别在于实时渲染。实时渲染需要以降低精确度为代价来加速运算。

拿Blender来说比较合适，Blender既有raytracing，也有实时渲染（eevee），如果题主对这方面感兴趣的话，个人觉得倒是可以从blender下手试试。毕竟blender功能特别全，还开源。

如果只是想专注看游戏渲染的部分，可以先参考下开源的ogre。



#### 成像

https://www.jianshu.com/p/0711c00be449

通过定义投影矩阵，我们实际上是在虚拟的3D空间中，创建了一个视野，也就是视景体。在接着，我们通过定义视口，来描述视景体中的内容如何映射到一个虚拟的画布之上，并且这个画布最终将显示在屏幕上的什么位置。当所有的这些都设置完毕，我们绘制完毕场景之后，就能够通过硬件在我们的显示器屏幕上看到最终的画面。更理论的表述就是，通过定义投影矩阵，将3D场景投影到一个投影平面之上。通过定义视口，我们将投影平面上的内容映射到这个视口中去，并且填满它，同时根据定义视口是给定的屏幕坐标的位置，将这个视口中的图像映射到窗口的指定位置之上，最终我们就看到了图像。

- 窗口(Screen)
  窗口其实就是屏幕。所有的场景最终都是要被光栅化成显示器上的图像，屏幕是所有场景（2D、3D等）的最终输出目的地。一个screen可以显示多个视口中的内容；

- 视口(Viewport)
   视口就是窗口中用来显示图形的一块矩形区域，它可以和窗口等大，也可以比窗口大或者小。它具有两个意义:
   　• 定义了视镜体中的景物要被绘制到一张什么尺寸的画布之上；
   　• 定义了画布在屏幕的什么区域；

  Processed coordinates in OpenGL are between -1 and 1 so we effectively map from the range (-1 to 1) to (0, 800) and (0, 600). For example, a processed point of location `(-0.5,0.5)` would (as its final transformation) be mapped to `(200,450)` in screen coordinates. 

- 裁剪区域（平行投影）
  裁剪区域就是视口矩形区域的最小最大x坐标（left,right)和最小最大y坐标(bottom,top)，而不是窗口的最小最大x坐标和y坐标。

- 视景体(View Volume)

  定义了我们能够通过虚拟的3D摄像机所能看到的场景。在一个3D场景中站立中，需要摄像机的**摆放位置**和**视野**来定义我们所能够看到的东西，而这个视野就是通过视景体来定义的。

  

#### 图形渲染

在OpenGL中，任何事物都在3D空间中，而屏幕和窗口却是2D像素数组，这导致OpenGL的大部分工作都是关于把3D坐标转变为适应你屏幕的2D像素。3D坐标转为2D坐标的处理过程是由OpenGL的图形渲染管线（Graphics Pipeline，大多译为管线，实际上指的是一堆原始图形数据途经一个输送管道，期间经过各种变化处理最终出现在屏幕的过程）管理的。图形渲染管线可以被划分为两个主要部分：第一部分把3D坐标转换为2D坐标，第二部分是把2D坐标转变为实际的有颜色的像素。

##### 图元

OpenGL需要你去指定这些数据所表示的渲染类型。我们是希望把这些数据渲染成一系列的点？一系列的三角形？还是仅仅是一个长长的线？做出的这些提示叫做图元(Primitive)，任何一个绘制指令的调用都将把图元传递给OpenGL。这是其中的几个GL_POINTS, GL_TRIANGLES and GL_LINE_STRIP. 

##### 顶点着色器（Vertex Shader）

图形渲染管线的第一个阶段，一般用于处理每个图形的顶点变换的（旋转/平移/投影等）

顶点着色器是OpenGL中可用于计算顶点属性的程序。顶点着色器是逐顶点运算的程序。也就是每个顶点都会执行一次顶点着色器，当然这是并行的，并且顶点着色器运算过程中无法访问其他顶点数据。典型的计算的顶点属性质保包括顶点坐标变换、顶点光照运算等。顶点坐标由自身坐标系转换归一化坐标系的计算。

##### 图元装配(Primitive Assembly)

顶点着色器输出的所有顶点作为输入（如果是GL_POINTS，那么就是一个顶点），并所有的点装配成指定图元的形状

##### 几何着色器(Geometry Shader)

把图元形式的一系列顶点的集合作为输入，它可以通过产生新顶点构造出新的（或是其它的）图元来生成其他形状

##### 光栅化(Rasterization Stage)

它会把图元映射为最终屏幕上相应的像素，生成供片段着色器(Fragment Shader)使用的片段(Fragment)。在片段着色器运行之前会执行裁切(Clipping)。裁切会丢弃超出你的视图以外的所有像素，用来提升执行效率。

##### 片段着色器（**fragment Shader**）

的主要目的是计算一个像素的最终颜色，这也是所有OpenGL高级效果产生的地方。通常，片段着色器包含3D场景的数据（比如光照、阴影、光的颜色等等），这些数据可以被用来计算最终像素的颜色。片段着色器是OpenGL中用于计算片段（像素）颜色的程序。片段着色器是逐像素运算的程序，也就是说每个像素都会执行一次片段着色器，当然也是并行的。

##### Alpha测试和混合(Blending)

这是最后一个阶段，检测片段的对应的深度（和模板(Stencil)）值，用它们来判断这个像素是其它物体的前面还是后面，决定是否应该丢弃。这个阶段也会检查alpha值（alpha值定义了一个物体的透明度）并对物体进行混合(Blend)。



#### 顶点缓存

https://blog.csdn.net/dcrmg/article/details/53556664

https://www.photoneray.com/opengl-vao-vbo/

理解之后其实也不复杂。VBO是为了均衡数据的传输效率与灵活修改性；EBO是为了重组VBO中的数据，最终绘制所需要的顶点的个数没有变化，但对于重复使用的顶点只需要一份原始数据即可（多次绘制都是使用的索引而已）。然后VAO的本质是储存绘制状态，简化绘制代码。就是把VBO的数据绘制方式（数据的格式glVertexAttribPointer）给存起来了，等于是个半成品了（说白了就是可复用组件）。

##### VBO  (Vertex Buffer Object)

顶点缓冲对象VBO是在显卡存储空间中开辟出的一块内存缓存区，用于存储顶点的各类属性信息，如顶点坐标，顶点法向量，顶点颜色数据等。在渲染时，可以直接从VBO中取出顶点的各类属性数据，由于VBO在显存而不是在内存中，不需要从CPU传输数据，处理效率更高。所以可以理解为VBO就是显存中的一个存储区域，可以保持大量的顶点属性信息。并且可以开辟很多个VBO，每个VBO在OpenGL中有它的唯一标识ID，这个ID对应着具体的VBO的显存地址，通过这个ID可以对特定的VBO内的数据进行存取操作。VBO本质上是一块服务端buffer（缓存），对应着client端的某份数据，在数据传输给VBO之后，client端的数据是可以删除的。系统会根据用户设置的 `target` 和 `usage` 来决定VBO最适合的存放位置（系统内存/AGP/显存）。*当然，GL规范是一回事，显卡厂商的驱动实现又是另一回事了*。

1. 需要开辟（声明/获得）显存空间并分配VBO的ID：

   函数原型：void glGenBuffers(GLsizei n,GLuint * buffers);

   第一个参数是要生成的缓冲对象的数量，第二个是要输入用来存储缓冲对象名称的数组

2. 创建的VBO可用来保存不同类型的顶点数据,创建之后需要通过分配的ID绑定（bind）一下制定的VBO，对于同一类型的顶点数据一次只能绑定一个VBO。

   函数原型：void glBindBuffer(GLenum target,GLuint buffer);

3. 填充数据，把用户定义的数据传输到当前绑定的显存缓冲区中。就是CPU到GPU的数据传输

   函数原型：glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

4. 解释数据的使用格式。直到这里才知道数据是怎么使用的

   函数原型：glVertexAttribPointer
   第一个参数指定顶点属性位置，与顶点着色器中layout(location=0)对应。
   第二个参数指定顶点属性大小。
   第三个参数指定数据类型。
   第四个参数定义是否希望数据被标准化。
   第五个参数是步长（Stride），指定在连续的顶点属性之间的间隔。
   第六个参数表示我们的位置数据在缓冲区起始位置的偏移量。
   
5. 最后开启顶点着色器中layout具体的location才能使用，真的是够古板。也能够理解，CPU的事情做完了还得做GPU的事情。

   函数原型：glEnableVertexAttribArray

   

##### EBO （Element Buffer Object）

索引缓冲对象EBO相当于OpenGL中的顶点数组的概念，是为了解决同一个顶点多次重复调用的问题，可以减少内存空间浪费，提高执行效率。当需要使用重复的顶点时，通过顶点的位置索引来调用顶点，而不是对重复的顶点信息重复记录，重复调用。EBO中存储的内容就是顶点位置的索引indices，EBO跟VBO类似，也是在显存中的一块内存缓冲器，只不过EBO保存的是顶点的索引。EBO+VBO等于是用组合的方式来增强表现力，减少冗余的数据。理论上顶点这种这么原始的表现方式，经过该点的线段有多少条那这个信息就会重复多少次，毕竟从实际的三维物体拆成各种表面再变成形状，这里面的数据重复量还是挺多的。

当用EBO绑定顶点索引的方式绘制模型时，需要使用glDrawElements而不是glDrawArrays，等于这里需要翻译后间接调用


      glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
第一个参数指定了要绘制的模式；
第二个参数指定要绘制的顶点个数；
第三个参数是索引的数据类型；
第四个参数是可选的EBO中偏移量设定。

##### VAO (Vertex Array Object)

顶点数组对象，但和Vertex Array（顶点数组）毫无联系（什么鬼，命名的时候完全不相干的概念随手就用）！VBO保存了一个模型的顶点属性信息，每次绘制模型之前需要绑定顶点的所有信息，当数据量很大时，重复这样的动作变得非常麻烦。VAO可以把这些所有的配置都存储在一个对象中，每次绘制模型时，只需要绑定这个VAO对象就可以了。VAO是一个保存了所有顶点数据属性的状态结合，它存储了顶点数据的格式以及顶点数据所需的VBO对象的引用。VAO本身并没有存储顶点的相关属性数据，这些信息是存储在VBO中的，VAO相当于是对很多个VBO的引用，把一些VBO组合在一起作为一个对象统一管理。可以看作索引与数据分离的表现形式，VAO本质上是state-object（状态对象）,记录的是一次绘制所需要的信息，包括数据在哪，数据格式之类的信息（*VBO, *EBO）。

```c++
//创建vertex array object对象   
GLuint vaoId;//vertext array object句柄
glGenVertexArrays(1, &vaoId);
glBindVertexArray(vaoId);
glDrawArrays (GLenum mode, GLint first, GLsizei count)
```


#### GLSL(图形领域DSL语言) 

看起来比较精简也很明确。参与的实体如下：

Shader：一段特定功能的程序，有源码可编译

Program：可以把多个编译后的Shader目标进行链接成一个大的程序(等于是工艺定制的过程)

glCreateShader->glShaderSource->glCompileShader->glAttachShader->glLinkProgram->glUseProgram

```c++c
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    unsigned int fragmentShaderOrange = glCreateShader(GL_FRAGMENT_SHADER); // the first fragment shader that outputs the color orange
    unsigned int fragmentShaderYellow = glCreateShader(GL_FRAGMENT_SHADER); // the second fragment shader that outputs the color yellow
    unsigned int shaderProgramOrange = glCreateProgram();
    unsigned int shaderProgramYellow = glCreateProgram(); // the second shader program
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);
    glShaderSource(fragmentShaderOrange, 1, &fragmentShader1Source, NULL);
    glCompileShader(fragmentShaderOrange);
    glShaderSource(fragmentShaderYellow, 1, &fragmentShader2Source, NULL);
    glCompileShader(fragmentShaderYellow);
    // link the first program object
    glAttachShader(shaderProgramOrange, vertexShader);
    glAttachShader(shaderProgramOrange, fragmentShaderOrange);
    glLinkProgram(shaderProgramOrange);
```

再抽象一点来看，其实就是浮点运算。三维坐标以及颜色三原色都抽象成了同一种数学模型，这个才是牛逼的地方（不知道是偶然还一种必然，RGB三原色不是唯一的正交基（对于人类，其他动物就不见得是正交的了），还可以有其他选择。只不过RGB能组合出来的颜色更为丰富。也许是因为二者都符合所谓的线性空间）。扩展阅读：

https://www.zhihu.com/question/24886171

https://www.jianshu.com/p/85c3f1cbcecb

与指令性程序相比（CPU串行流程），这里应该是多单元分工（GPU并行计算）的模型。

与C++之间的数据交换也很清晰，uniform 关键字直接按照唯一的变量名称来交换数据，没有什么奇特的做法。

#### 纹理

纹理坐标起始于(0, 0)，也就是纹理图片的左下角，终始于(1, 1)，即纹理图片的右上角。这种做法有点像是把颜色与位置再次正交化，顶点的纹理坐标变成新的维度，然后纹理就可以复用了。纹理坐标获取纹理颜色叫做采样(Sampling)，在采样坐标点后其他的值也会进行纹理的填充叫做插值（这跟颜色因该是一样的道理，只不过换了一种更加工程化的表现方式，就是把颜色数据给弄到一个二维矩阵里面去了）。

整个也是非常规整，先产生ID然后bind类型，

```c++
    unsigned int texture;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture); // all upcoming GL_TEXTURE_2D operations now have effect on this texture object
    // set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);	// set texture wrapping to GL_REPEAT (default wrapping method)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    // set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    // load image, create texture and generate mipmaps
    int width, height, nrChannels;
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
    glGenerateMipmap(GL_TEXTURE_2D);
```

##### 纹理环绕（Texture Wrapping）

纹理坐标的范围通常是从(0, 0)到(1, 1)，但还有简单扩充方式。OpenGL默认的行为是重复这个纹理图像（基本上忽略浮点纹理坐标的整数部分），但OpenGL提供了更多的选择：

| 环绕方式           | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| GL_REPEAT          | 对纹理的默认行为。重复纹理图像。                             |
| GL_MIRRORED_REPEAT | 和GL_REPEAT一样，但每次重复图片是镜像放置的。                |
| GL_CLAMP_TO_EDGE   | 纹理坐标会被约束在0到1之间，超出的部分会重复纹理坐标的边缘，产生一种边缘被拉伸的效果。 |
| GL_CLAMP_TO_BORDER | 超出的坐标为用户指定的边缘颜色。                             |

实在点，纹理坐标如果超出纹理是取不到颜色数据的，但有些时候为了简单的复用数据就弄了个超出范围的环绕概念，推到或者指定这些超出范围的数据。在平铺式的纹理应用到大型几何图形的时候，非常有用。一个设计良好的无缝小型纹理紧挨着平铺到大型几何图形上看起来像是无缝的大型纹理(就是说重复型的纹理只需要一个小的子集即可，其他部分就可以自然扩展)。可以说环绕是一种扩展方式的技巧，以比较少的数据加上扩展项来推演更多的数据，是一种精确计算。

##### 纹理过滤（Texture Filtering）

区别于环绕的精确计算，过滤在获取到环绕的精确值之后还需要进行细化调整。如果继续使用精确计算，在很大的物体上应用一张低分辨率的纹理的时候会出现某一块区域都选中同一个纹理点，就会出现像素格子失真的感觉。效果真实一些就需要做一些润色，把临近点的数据引入后加权运算。实际效果可能会出现模糊，因为临近点的区分度太小了看起来就会糊掉。

GL_NEAREST（也叫邻近过滤，Nearest Neighbor Filtering）是OpenGL默认的纹理过滤方式（还是精确运算）。当设置为GL_NEAREST的时候，OpenGL会选择中心点最接近纹理坐标的那个像素。说白了就是最近的那个点的权重就是100%，其他的点不考虑。（4选1的游戏）

GL_LINEAR（也叫线性过滤，(Bi)linear Filtering）它会基于纹理坐标附近的纹理像素，计算出一个插值，近似出这些纹理像素之间的颜色。一个纹理像素的中心距离纹理坐标越近，那么这个纹理像素的颜色对最终的样本颜色的贡献越大。（4选4的游戏，有权重润色）。

GL_TEXTURE_MIN_FILTER 是多个纹素对应一个片元的解决方案。GL_TEXTURE_MAG_FILTER 是没有足够的纹素来映射片元的解决方案。（老实讲纹理被缩小的时候使用邻近过滤，被放大时使用线性过滤这种难道要运行时去做判定吗？还是说引擎能够更加智能的选择，展示出比较好的效果）

## 其他概念

1.  Alpha通道的概念与功能

   在计算机图形学中，一个RGB颜色模型的真彩图形，用由红、绿、蓝三个色彩信息通道合成的，每个通道用了8位色彩深度，共计24位，包含了所有彩色信息。为实现图形的透明效果，采取在图形文件的处理与存储中附加上另一个8位信息的方法，这个附加的代表图形中各个素点透明度的通道信息就被叫做Alpha通道。

   Alpha通道使用8位二进制数，就可以表示256级灰度，即256级的透明度。白色（值为255）的Alpha像素用以定义不透明的彩色像素，而黑色（值为0）的Alpha通道像素用以定义透明像素，介于黑白之间的灰度（值为30-255）的Alpha像素用以定义不同程度的半透明像素。因而通过一个32位总线的图形卡来显示带Alpha通道的图形，就可能呈现出透明或半透明的视觉效果。

     一个透明或半透明图形的数学模型应当如下：

   为了便于下面的分析，设Alpha值[0，255]区间映射为[0，1]区间相对应的值表示，即Alpha值为0—1之间的数值。则图形文件中各个像素点可表示为：

     Graphx（Redx，Greenx，Bulex，Alphax）

     屏幕上相应像素点的显示值就转换为：

     Dispx（Redx * Alphax，Greenx * Alphax，Bluex * Alphax）

     Alpha通道不仅用于单个图形的透明或半透明显示，更重要的是在图像合成中被广泛运用。



## 规范与实现

- 基于插件发布新功能。
- 使用状态机实现。更改的都是上下文，表现是异步执行的。屏幕刷新率可以算作状态机的驱动力
- 对象。不是实体的概念，是一种对属性集合的抽象（应该说是一堆属性的惯用的逻辑抽象）。这里的出发点应该是把基础抽象化成一些可复用的逻辑组件，以便上层应用轻松复用。





