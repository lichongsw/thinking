



# 词汇

https://www.jianshu.com/p/2f093554ad57

https://www.jianshu.com/p/c33c7e2bdfd4

- **顶点数组对象：Vertex Array Object，VAO**
- **顶点缓冲对象：Vertex Buffer Object，VBO**
- **索引缓冲对象：Element Buffer Object，EBO或Index Buffer Object，IBO**
- **OpenGL着色器语言(OpenGL Shading Language, GLSL**）
- **透视：Perspective**
- **视场：Field of View（FOV）** 
- **标准化设备坐标(Normalized Device Coordinates, NDC)**： 顶点在通过在剪裁坐标系中剪裁与透视除法后最终呈现在的坐标系。所有位置在NDC下-1.0到1.0的顶点将不会被丢弃并且可见
- **纹理缠绕(Texture Wrapping)**： 定义了一种当纹理顶点超出范围(0, 1)时指定OpenGL如何采样纹理的模式
- **纹理过滤(Texture Filtering)**： 定义了一种当有多种纹素选择时指定OpenGL如何采样纹理的模式。这通常在纹理被放大情况下发生
- **多级渐远纹理(Mipmaps)**： 被存储的材质的一些缩小版本，根据距观察者的距离会使用材质的合适大小
- **向量(Vector)**： 一个定义了在空间中方向和/或位置的数学实体
- **矩阵(Matrix)**： 一个矩形阵列的数学表达式
- **环境光照：Ambient lighting**
- **漫反射光照：Diffuse lighting**
- **镜面光照：Specular lighting**



# 静态认知基础

## 链路

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



## 成像

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

  

## 图形渲染

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



## 顶点

https://blog.csdn.net/dcrmg/article/details/53556664

https://www.photoneray.com/opengl-vao-vbo/

理解之后其实也不复杂。VBO是为了均衡数据的传输效率与灵活修改性；EBO是为了重组VBO中的数据，最终绘制所需要的顶点的个数没有变化，但对于重复使用的顶点只需要一份原始数据即可（多次绘制都是使用的索引而已）。然后VAO的本质是储存绘制状态，简化绘制代码。就是把VBO的数据绘制方式（数据的格式glVertexAttribPointer）给存起来了，等于是个半成品了（说白了就是可复用组件）。

### VBO  (Vertex Buffer Object)

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

   

### EBO （Element Buffer Object）

索引缓冲对象EBO相当于OpenGL中的顶点数组的概念，是为了解决同一个顶点多次重复调用的问题，可以减少内存空间浪费，提高执行效率。当需要使用重复的顶点时，通过顶点的位置索引来调用顶点，而不是对重复的顶点信息重复记录，重复调用。EBO中存储的内容就是顶点位置的索引indices，EBO跟VBO类似，也是在显存中的一块内存缓冲器，只不过EBO保存的是顶点的索引。EBO+VBO等于是用组合的方式来增强表现力，减少冗余的数据。理论上顶点这种这么原始的表现方式，经过该点的线段有多少条那这个信息就会重复多少次，毕竟从实际的三维物体拆成各种表面再变成形状，这里面的数据重复量还是挺多的。

当用EBO绑定顶点索引的方式绘制模型时，需要使用glDrawElements而不是glDrawArrays，等于这里需要翻译后间接调用


      glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
第一个参数指定了要绘制的模式；
第二个参数指定要绘制的顶点个数；
第三个参数是索引的数据类型；
第四个参数是可选的EBO中偏移量设定。

### VAO (Vertex Array Object)

顶点数组对象，但和Vertex Array（顶点数组）毫无联系（什么鬼，命名的时候完全不相干的概念随手就用）！VBO保存了一个模型的顶点属性信息，每次绘制模型之前需要绑定顶点的所有信息，当数据量很大时，重复这样的动作变得非常麻烦。VAO可以把这些所有的配置都存储在一个对象中，每次绘制模型时，只需要绑定这个VAO对象就可以了。VAO是一个保存了所有顶点数据属性的状态结合，它存储了顶点数据的格式以及顶点数据所需的VBO对象的引用。VAO本身并没有存储顶点的相关属性数据，这些信息是存储在VBO中的，VAO相当于是对很多个VBO的引用，把一些VBO组合在一起作为一个对象统一管理。可以看作索引与数据分离的表现形式，VAO本质上是state-object（状态对象）,记录的是一次绘制所需要的信息，包括数据在哪，数据格式之类的信息（*VBO, *EBO）。

```c++
//创建vertex array object对象   
GLuint vaoId;//vertext array object句柄
glGenVertexArrays(1, &vaoId);
glBindVertexArray(vaoId);
glDrawArrays (GLenum mode, GLint first, GLsizei count)
```


### GLSL(图形领域DSL语言) 

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

与指令性程序相比（CPU串行流程），这里应该是多单元分工（GPU并行计算）的模型。

与C++之间的数据交换也很清晰，uniform 关键字直接按照唯一的变量名称来交换数据，没有什么奇特的做法。复杂点的给多个shader使用的uniform块是一个数据结构，对应关系是绑定点（binding points）的形式：

```c++
// first. We get the relevant block indices
unsigned int uniformBlockIndexRed = glGetUniformBlockIndex(shaderRed.ID, "Matrices");
// then we link each shader's uniform block to this uniform binding point
glUniformBlockBinding(shaderRed.ID, uniformBlockIndexRed, 0);
```

可以理解成每个shader都持有一个缓冲的引用，需要显示的指定每个引用指向的真实缓冲块。除了自定义变量以外GLSL提供一些标准变量

输出型：

gl_Position：设置顶点位置（这个最常见了）

gl_PointSize：设置顶点大小（粒子效果）

gl_FragDepth：片段深度值（着色器中没有像gl_FragDepth变量写入，它就会自动采用gl_FragCoord.z的值）

输入型：

gl_VertexID：当前顶点的ID（貌似没啥作用）

gl_FragCoord：片段着色器当前顶点（有坐标和深度值）

gl_FrontFacing：片段着色器中正反面标记（以前是用顶点顺时针逆时针来判定的）



## 颜色

再抽象一点来看，三维坐标以及颜色三原色都抽象成了同一种数学模型，这个才是牛逼的地方（不知道是偶然还一种必然，RGB三原色不是唯一的正交基（对于人类，其他动物就不见得是正交的了），还可以有其他选择。只不过RGB能组合出来的颜色更为丰富。也许是因为二者都符合所谓的线性空间）。扩展阅读：

https://www.zhihu.com/question/24886171

https://www.jianshu.com/p/85c3f1cbcecb

https://juejin.im/post/5ba352766fb9a05d353c72a8

**加法是没有关系的颜色之间的叠加，而乘法是模拟光的照射过程。**

### 分量乘法

光照射到一个物体表面时，是光的颜色和物体的颜色属性共同决定了照射后物体看起来是什么颜色。物体的贴图颜色可以理解为吸光的比率，光照和纹理的颜色一起做分量乘法来决定最终反射出去的关（也就是被观察到的颜色）。**三基色**：一般指的是颜料三原色，在纯白光照射下颜色为绛红、黄、青，简称 CMYK，属于**减色系（小于1的值越乘越小，被吸收之后变暗）**。**它们本身不发光，靠反光被看见**。由于材料吸收特定波段的光，所以只有不被吸收的部分反射了回来。加上的颜色越多吸收的光也越多。

(R0, G0, B0) x (R1, G1, B1) = (R0R1, G0G1, B0B1)

```
fixed4 baseColor = tex2D( _MainTex, i.uv );//采样贴图对应uv坐标处的颜色
baseColor = baseColor * _LightColor0 * (dot( worldNormal, worldLightDir )*0.5 + 0.5 );
```

### 加法

**三原色**一般指的是红、绿、蓝三种，简称 RGB，这是**加色系（蚊子再小也是肉，叠加之后更亮）**。就是光源只含有特定的波段，本身就是**色光**，将不同颜色的光加在一起形成新的颜色。在计算最终颜色返回值时各种高光，漫反射，环境光这三部分的颜色用的是加法。自发光（emissive），环境光（ambient），漫反射（diffuse），高光反射（specular）这四个部分可以说是没有关系的，相互没有影响和交互，是四个独立的部分，所以最后使用加法来进行叠加。加法的值都是向1这个方向靠近的，也就是向白色方向靠近，约趋近白色也就表示越亮。各种光最后是一个叠加效果。

```
fixed4( diffuse + specular + ambient, 1.0 );
```

### 混合

物体透明技术通常被叫做**混合(Blending)**，这个词用的也许不够精确（貌似windows上的API都是用opacity来描述透明度，再不济正常情况下transparent也比较常用）。

这里先记录下透明度相关的信息：（Alpha通道的概念与功能）

在计算机图形学中，一个RGB颜色模型的真彩图形，用由红、绿、蓝三个色彩信息通道合成的，每个通道用了8位色彩深度，共计24位，包含了所有彩色信息。为实现图形的透明效果，采取在图形文件的处理与存储中附加上另一个8位信息的方法，这个附加的代表图形中各个素点透明度的通道信息就被叫做Alpha通道。

Alpha通道使用8位二进制数，就可以表示256级灰度，即256级的透明度。白色（值为255）的Alpha像素用以定义不透明的彩色像素，而黑色（值为0）的Alpha通道像素用以定义透明像素，介于黑白之间的灰度（值为30-255）的Alpha像素用以定义不同程度的半透明像素。因而通过一个32位总线的图形卡来显示带Alpha通道的图形，就可能呈现出透明或半透明的视觉效果。

  一个透明或半透明图形的数学模型应当如下：

为了便于下面的分析，设Alpha值[0，255]区间映射为[0，1]区间相对应的值表示，即Alpha值为0—1之间的数值。则图形文件中各个像素点可表示为：

  Graphx（Redx，Greenx，Bulex，Alphax）

  屏幕上相应像素点的显示值就转换为：

  Dispx（Redx * Alphax，Greenx * Alphax，Bluex * Alphax）

  Alpha通道不仅用于单个图形的透明或半透明显示，更重要的是在图像合成中被广泛运用。基于这里的运算规则，比较技术宅的命名方式混合就有点形象了。



```c++
glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
```

$$
\begin{equation}\bar{C}_{result} = \bar{\color{green}C}_{source} * \color{green}F_{source} + \bar{\color{red}C}_{destination} * \color{red}F_{destination}\end{equation}
$$

- Csource：源颜色向量。这是来自纹理的本来的颜色向量。
- Cdestination：目标颜色向量。这是储存在颜色缓冲中当前位置的颜色向量。
- FsourceFsource：源因子。设置了对源颜色的alpha值影响。
- FdestinationFdestination：目标因子。设置了对目标颜色的alpha影响。

在图片或视频滤镜中，一般不会直接使用加减乘除来做颜色混合。而是使用 mix() 函数，它的公式是：`x*(1−a)+y*a`，其实也是颜色相加，但是算上了一定的比重。这样不会因为一个白色的颜色和其他颜色相加后只有白色，现实世界中也不是这样的。混合也有线性和非线性的做法，看来也是套路。GLSL内建的mix函数需要接受两个值作为参数，并对它们根据第三个参数进行线性插值。如果第三个值是`0.0`，它会返回第一个输入；如果是`1.0`，会返回第二个输入值。`0.2`会返回`80%`的第一个输入颜色和`20%`的第二个输入颜色，即返回两个纹理的混合色。

```
FragColor = mix(texture(texture1, TexCoord), texture(texture2, TexCoord), 0.2);
```

没有透明物体时，依赖深度缓冲足以确认遮挡关系。但有透明物体时有特殊处理，因为写入深度缓冲的时候，深度测试不关心片段是否有透明度，所以靠前的透明部分被写入深度缓冲，后面的就被丢弃了。简单的做法时先绘制所有不透明物体然后为所有透明物体排序后按从远到近的顺序绘制透明物体。虽然这个按照它们的距离对物体进行排序的方法在这个特定的场景中能够良好工作，但它不能进行旋转、缩放或者进行其他的变换，奇怪形状的物体需要一种不同的方式，而不能简单的使用位置向量。在场景中排序物体是个有难度的技术，它很大程度上取决于你场景的类型，更不必说会耗费额外的处理能力了。完美地渲染带有透明和不透明的物体的场景并不那么容易。有更高级的技术例如次序无关透明度（order independent transparency）

## 纹理

纹理坐标起始于(0, 0)，也就是纹理图片的左下角，终始于(1, 1)，即纹理图片的右上角。这种做法有点像是把颜色与位置再次正交化，顶点的纹理坐标变成新的维度，然后纹理就可以复用了。纹理坐标获取纹理颜色叫做采样(Sampling, 类型：sampler1D,sampler2D,sampler3D)，在采样坐标点后其他的值也会进行纹理的填充叫做插值（这跟颜色因该是一样的道理，只不过换了一种更加工程化的表现方式，就是把颜色数据给弄到一个二维矩阵里面去了）。

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
    // The FileSystem::getPath(...) is part of the GitHub repository so we can find files on any IDE/platform; replace it with your own image path.
    unsigned char *data = stbi_load(FileSystem::getPath("resources/textures/container.jpg").c_str(), &width, &height, &nrChannels, 0);
    if (data)
    {
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
        glGenerateMipmap(GL_TEXTURE_2D);
    }
```

glTexImage2D 参数茫茫多。老实说只有width， height， data这三比较有意义（清晰），其他的可以用默认值，然后提供设置接口就好了（正交）。

- 第一个参数指定了纹理目标(Target)。设置为GL_TEXTURE_2D意味着会生成与当前绑定的纹理对象在同一个目标上的纹理（任何绑定到GL_TEXTURE_1D和GL_TEXTURE_3D的纹理不会受到影响）。
- 第二个参数为纹理指定多级渐远纹理的级别，如果你希望单独手动设置每个多级渐远纹理的级别的话。这里我们填0，也就是基本级别。
- 第三个参数告诉OpenGL我们希望把纹理储存为何种格式。我们的图像只有RGB值，因此我们也把纹理储存为RGB值。
- 第四个和第五个参数设置最终的纹理的宽度和高度。我们之前加载图像的时候储存了它们，所以我们使用对应的变量。
- 第六个参数应该总是被设为0（历史遗留的问题）。
- 第七第八个参数定义了源图的格式和数据类型。我们使用RGB值加载这个图像，并把它们储存为char(byte)数组，我们将会传入对应值。
- 第九个参数是真正的图像数据。



然后纹理在使用的时候需要采样器，GL_TEXTURE0~GL_TEXTURE31（如果不显示指定则默认使用GL_TEXTURE0）。看这个做法似乎有问题，如果一个物体需要的纹理数量超过32会有什么问题呢？（Texture Atlas，纹理集合？压缩？这些目前暂不需要理解，不影响流程）

        glUniform1i(glGetUniformLocation(ourShader.ID, "texture1"), 2);
        glActiveTexture(GL_TEXTURE2);
        glBindTexture(GL_TEXTURE_2D, texture1);
        
        uniform sampler2D texture1;
### 纹理环绕（Texture Wrapping）

纹理坐标的范围通常是从(0, 0)到(1, 1)，但还有简单扩充方式。OpenGL默认的行为是重复这个纹理图像（基本上忽略浮点纹理坐标的整数部分），但OpenGL提供了更多的选择：

| 环绕方式           | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| GL_REPEAT          | 对纹理的默认行为。重复纹理图像。                             |
| GL_MIRRORED_REPEAT | 和GL_REPEAT一样，但每次重复图片是镜像放置的。                |
| GL_CLAMP_TO_EDGE   | 纹理坐标会被约束在0到1之间，超出的部分会重复纹理坐标的边缘，产生一种边缘被拉伸的效果。 |
| GL_CLAMP_TO_BORDER | 超出的坐标为用户指定的边缘颜色。                             |

实在点，纹理坐标如果超出纹理是取不到颜色数据的，但有些时候为了简单的复用数据就弄了个超出范围的环绕概念，推到或者指定这些超出范围的数据。在平铺式的纹理应用到大型几何图形的时候，非常有用。一个设计良好的无缝小型纹理紧挨着平铺到大型几何图形上看起来像是无缝的大型纹理(就是说重复型的纹理只需要一个小的子集即可，其他部分就可以自然扩展)。可以说环绕是一种扩展方式的技巧，以比较少的数据加上扩展项来推演更多的数据，是一种精确计算。

### 纹理过滤（Texture Filtering）

区别于环绕的精确计算，过滤在获取到环绕的精确值之后还需要进行细化调整。如果继续使用精确计算，在很大的物体上应用一张低分辨率的纹理的时候会出现某一块区域都选中同一个纹理点，就会出现像素格子失真的感觉。效果真实一些就需要做一些润色，把临近点的数据引入后加权运算。实际效果可能会出现模糊，因为临近点的区分度太小了看起来就会糊掉。

GL_NEAREST（也叫邻近过滤，Nearest Neighbor Filtering）是OpenGL默认的纹理过滤方式（还是精确运算）。当设置为GL_NEAREST的时候，OpenGL会选择中心点最接近纹理坐标的那个像素。说白了就是最近的那个点的权重就是100%，其他的点不考虑。（4选1的游戏）

GL_LINEAR（也叫线性过滤，(Bi)linear Filtering）它会基于纹理坐标附近的纹理像素，计算出一个插值，近似出这些纹理像素之间的颜色。一个纹理像素的中心距离纹理坐标越近，那么这个纹理像素的颜色对最终的样本颜色的贡献越大。（4选4的游戏，有权重润色）。

GL_TEXTURE_MIN_FILTER 是多个纹素对应一个片元的解决方案。

GL_TEXTURE_MAG_FILTER 是没有足够的纹素来映射片元的解决方案。

### 多级渐远纹理（mipmap）

当同一个场景中相同的物体有远近之分的时候，如果统一使用相同的纹理数据在小物体上只取样很少的数据会有不真实感，而且浪费内存。多级简单来说就是一系列的纹理图像，后一个纹理图像是前一个的二分之一对应了各种距离（有范围上限，而且缩小到1*1其实也有点夸张）。多级渐远纹理背后的理念很简单：距观察者的距离超过一定的阈值，OpenGL会使用不同的多级渐远纹理，即最适合物体的距离的那个。由于距离远，解析度不高也不会被用户注意到。为了加快渲染速度和减少图像锯齿，贴图被处理成由一系列被预先计算和优化过的图片组成的文件, 这样的贴图被称为MIP map 或者mipmap。 “MIP”来自于拉丁语multum in parvo 的首字母，意思是“放置很多东西的小空间”。多级渐远纹理的加分之处是它的性能非常好，等于是把有规律的数据预先制作好，使用时按照规格直接取用。可以理解成用内存换显存，小规格的东西就不用全规格的资源了。

同样有邻近与线性两种取样方式：

| 过滤方式                  | 描述                                                         |
| :------------------------ | :----------------------------------------------------------- |
| GL_NEAREST_MIPMAP_NEAREST | 使用最邻近的多级渐远纹理来匹配像素大小，并使用邻近插值进行纹理采样 |
| GL_LINEAR_MIPMAP_NEAREST  | 使用最邻近的多级渐远纹理级别，并使用线性插值进行采样         |
| GL_NEAREST_MIPMAP_LINEAR  | 在两个最匹配像素大小的多级渐远纹理之间进行线性插值，使用邻近插值进行采样 |
| GL_LINEAR_MIPMAP_LINEAR   | 在两个邻近的多级渐远纹理之间使用线性插值，并使用线性插值进行采样 |

更多信息：

http://www.cppblog.com/wc250en007/archive/2011/08/06/152653.html

https://www.zhihu.com/question/66993945



# 动态变换基础

## 向量与矩阵

静态认知基础中已经提到了空间与颜色向量的运算。偏数学的东西就写一下理解，不搬内容了。

https://zhuanlan.zhihu.com/p/91311929(点乘与叉乘的推到过程)

### 点乘

向量的点乘,也叫向量的内积、数量积，对两个向量执行点乘运算，就是对这两个向量对应位一一相乘之后求和的操作，点乘的结果是一个标量。两个向量的点乘等于它们的数乘结果乘以两个向量之间夹角的余弦值。带角度的乘法，看的是协同效果（其实可以理解成计算角度）。
$$
\bar{v} \cdot \bar{k} = ||\bar{v}|| \cdot ||\bar{k}|| \cdot \cos \theta 
\\[0.1in]
\cos \theta = \frac{\bar{v} \cdot \bar{k}}{||\bar{v}|| \cdot ||\bar{k}||}
$$

$$
\begin{pmatrix} \color{red}{0.6}, -\color{green}{0.8}, \color{blue}0 \end{pmatrix} \cdot \begin{pmatrix} \color{red}0 \\ \color{green}1 \\ \color{blue}0 \end{pmatrix} = (\color{red}{0.6} * \color{red}0) + (-\color{green}{0.8} * \color{green}1) + (\color{blue}0 * \color{blue}0) = -0.8
$$


### 叉乘

两个向量的叉乘，又叫向量积、外积、叉积，叉乘的运算结果是一个向量而不是一个标量。并且两个向量的叉积与这两个向量组成的坐标平面垂直。叉乘只在3D空间中有定义，它需要两个不平行向量作为输入，生成一个正交于两个输入向量的第三个向量。如果输入的两个向量也是正交的，那么叉乘之后将会产生3个互相正交的向量。这个等于是维度变换，2条不平行的向量一定可以确定出一个平面，然后就可以找出这个平面的垂线（法向量）。
$$
\begin{pmatrix} \color{red}{A_{x}} \\ \color{green}{A_{y}} \\ \color{blue}{A_{z}} \end{pmatrix} \times \begin{pmatrix} \color{red}{B_{x}} \\ \color{green}{B_{y}} \\ \color{blue}{B_{z}}  \end{pmatrix} = \begin{pmatrix} \color{green}{A_{y}} \cdot \color{blue}{B_{z}} - \color{blue}{A_{z}} \cdot \color{green}{B_{y}} \\ \color{blue}{A_{z}} \cdot \color{red}{B_{x}} - \color{red}{A_{x}} \cdot \color{blue}{B_{z}} \\ \color{red}{A_{x}} \cdot \color{green}{B_{y}} - \color{green}{A_{y}} \cdot \color{red}{B_{x}} \end{pmatrix}
$$

### 移动，缩放，旋转

移动的概念也比较简单，按照各个维度物体整体移动即可。

向量与单位位向量相乘结果不变，与有倍率的向量相乘就产生了缩放效果。同比例就是均匀缩放，也有按照不同维度来缩放的。

旋转要复杂一点，在3D空间中旋转需要定义一个角**和**一个旋转轴(Rotation Axis)。

通常情况下都是复合变换，例如先缩放2倍，然后位移了(1, 2, 3)个单位。
$$
\begin{bmatrix} \color{red}2 & \color{red}0 & \color{red}0 & \color{red}1 \\ \color{green}0 & \color{green}2 & \color{green}0 & \color{green}2 \\ \color{blue}0 & \color{blue}0 & \color{blue}2 & \color{blue}3 \\ \color{purple}0 & \color{purple}0 & \color{purple}0 & \color{purple}1 \end{bmatrix} . \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} \color{red}2x + \color{red}1 \\ \color{green}2y + \color{green}2  \\ \color{blue}2z + \color{blue}3 \\ 1 \end{bmatrix}
$$

# 坐标系统

## 变换

OpenGL希望在每次顶点着色器运行后，我们可见的所有顶点都为标准化设备坐标(Normalized Device Coordinate, NDC)。也就是说，每个顶点的**x**，**y**，**z**坐标都应该在**-1.0**到**1.0**之间，超出这个坐标范围的顶点都将不可见。通常在顶点着色器中将这些坐标变换为标准化设备坐标，然后将这些标准化设备坐标传入光栅器(Rasterizer)，将它们变换为屏幕上的二维坐标或像素。就是顶点坐标是先标准化后再变成屏幕坐标的，这样做的好处应该是解耦，标准化之后在不同的屏幕上显示不同的效果。

物体的顶点在最终转化为屏幕坐标之前还会被变换到多个坐标系统(Coordinate System)。将物体的坐标变换到几个**过渡**坐标系(Intermediate Coordinate System)的优点在于，在这些特定的坐标系统中，一些操作或运算更加方便和容易。比较重要的总共有5个不同的坐标系统：

- 局部空间(Local Space，或者称为物体空间(Object Space))，是对象相对于局部原点的坐标
- 世界空间(World Space)，物体相对于世界的全局原点，由模型矩阵(Model Matrix)来摆放一堆物体（就是虚拟的世界坐标，有了这个高一层的参照点物体之间才有相对位置的概念）
- 观察空间(View Space，或者称为视觉空间(Eye Space))，是从摄像机角度进行观察的坐标，通常是一系列的位移和旋转的组合后由观察矩阵(View Matrix)来存储
- 裁剪空间(Clip Space)，就是标准化到-1.0到1.0的范围内，判断哪些顶点将会出现在屏幕上。就是投影矩阵(Projection Matrix)来圈出可视范围（术语叫做**观察箱**(Viewing Box)，也被称为平截头体(Frustum)）。正交投影不论远近都以统一的方式投影在屏幕上。透视除法(Perspective Division)过程中我们将位置向量的x，y，z分量分别除以向量的齐次w分量（正交就是特例，w就是1），就会有透视投影中近大远小的效果了。因此NDC的顶点仅包含x、y和z三个信息。其中x、y表示规范化2D平面上的坐标，z则表示深度信息，也就是远近关系。根据x和y来显示顶点，并根据z信息来确定覆盖、遮挡关系。
- 屏幕空间(Screen Space)。视口变换(Viewport Transform)将位于-1.0到1.0范围的坐标变换到由glViewport函数所定义的屏幕坐标范围内。最后变换出来的坐标将会送到光栅器，将其转化为片段。

这就是一个顶点在最终被转化为片段之前需要经历的所有不同状态。

```c++
glm::mat4 scale         = glm::mat4(1.0f);
glm::mat4 model         = glm::mat4(1.0f);
glm::mat4 view          = glm::mat4(1.0f);
glm::mat4 projection    = glm::mat4(1.0f); 
model = glm::scale(scale, glm::vec3(scala_value, scala_value, scala_value));
model = glm::rotate(model, glm::radians(-55.0f), glm::vec3(1.0f, 0.0f, 0.0f));
view  = glm::translate(view, glm::vec3(0.0f, 0.0f, -3.0f));
projection = glm::perspective(glm::radians(projection_value), (float)SCR_WIDTH / (float)SCR_HEIGHT, 1.0f, 100.0f);

gl_Position = projection * view * model * scale * vec4(aPos, 1.0);
```

glm::rotate的第三个参数时旋转的轴（1.0f, 0.0f, 0.0f）就是x轴正方向，然后旋转的角度时第一个参数glm::radians(-55.0f)即右手手握x轴大拇指握住的方向反向55度，就是朝里面旋转了。

glm::perspective 视锥体的第一个参数fov的角度有放大和缩小的效果，只不过不是scala那样的线性。可以理解成为广角相机拍同一个景里面同一个人最后成像就变小了。因为背景更大了，相对来说人就变小了。

矩阵的乘法是从右往左的，所以顺序是先缩放，再移位，再换到观察最后透视得到NDC。其实模型矩阵包括位移、缩放与旋转，这些明显是一个体系里面的概念。变换完成后模型才与观察，透视是一个概念级别的。
$$
V_{clip} = M_{projection} \cdot M_{view} \cdot M_{model} \cdot V_{local}
$$

## 投影

移动，缩放等变换是非常符合直观思维的，观察系的变换就再加一个旋转即可。这些都不涉及到形变，很容易理解。投影中正交投影也不涉及形变是一种纯展示，而透视则有近大远小的效果。再举个简单的例子，新闻联播上一直挂着个CCTV1的标记，这个标记不管节目内容如何变化都是一成不变的，就像这个标记贴在屏幕上的感觉（游戏中的UI界面）。节目效果在各种场景一直在变（游戏中当前帧）。例如主持人近身播报，现场面对面采访都是大头像，各种规划效果之类的远景拍摄或者航拍都是小小的。这个东西的本质就是作为屏幕，这是一个有限的固定的输出设备，当有更多的东西要展示到这个固定的框内的时候，必须有一个缩放，而根据视觉成像的原理就是把场景往原处放，直到观察者刚好看到整个场景（尽收眼底）的时候。

从代码来看，这个也很清晰。观察者摄像头的镜头角度，投影屏幕的宽高比例以及z轴近点和远点就可以确认投影矩阵了。其实也比较容易理解，就是镜头角度一半的正切（tangent）

```c++
glm::mat4 projection = glm::perspective(glm::radians(camera.Zoom), (float)SCR_WIDTH / (float)SCR_HEIGHT, 0.1f, 100.0f);

template<typename T>
GLM_FUNC_QUALIFIER mat<4, 4, T, defaultp> perspectiveLH_NO(T fovy, T aspect, T zNear, T zFar)
{
    assert(abs(aspect - std::numeric_limits<T>::epsilon()) > static_cast<T>(0));

    T const tanHalfFovy = tan(fovy / static_cast<T>(2));

    mat<4, 4, T, defaultp> Result(static_cast<T>(0));
    Result[0][0] = static_cast<T>(1) / (aspect * tanHalfFovy);
    Result[1][1] = static_cast<T>(1) / (tanHalfFovy);
    Result[2][2] = (zFar + zNear) / (zFar - zNear);
    Result[2][3] = static_cast<T>(1);
    Result[3][2] = - (static_cast<T>(2) * zFar * zNear) / (zFar - zNear);
    return Result;
}
```

透视投影公式(n:near, f:far, r:视锥体高度半径 , t:视锥体宽度半径)：
$$
\begin{bmatrix} \color{red}n/r & \color{red}0 & \color{red}0 & \color{red}0 \\ \color{green}0 & \color{green}n/t & \color{green}0 & \color{green}0 \\ \color{blue}0 & \color{blue}0 & \color{blue}-(f+n)/f-n & \color{blue}-2f*n/(f-n) \\ \color{purple}0 & \color{purple}0 & \color{purple}-1 & \color{purple}0 \end{bmatrix}
$$
推导：

http://www.songho.ca/opengl/gl_projectionmatrix.html

https://blog.csdn.net/tanmx219/article/details/81407264



## 深度Z缓冲(Z-buffer)

OpenGL存储它的所有深度信息于一个Z缓冲(Z-buffer)中，也被称为深度缓冲(Depth Buffer)。GLFW会自动为你生成这样一个缓冲（就像它也有一个颜色缓冲来存储输出图像的颜色）。深度值存储在每个片段里面（作为片段的**z**值），当片段想要输出它的颜色时，OpenGL会将它的深度值和z缓冲进行比较，如果当前的片段在其它片段之后，它将会被丢弃，否则将会覆盖（这里涉及浮点数的大小比较，也会有精度问题。某个画面可能处于显示与隐藏的边缘疯狂切换，学名叫做深度冲突）。这个过程称为深度测试(Depth Testing)，它是由OpenGL自动完成的，而且默认是关闭的。

```c++
glEnable(GL_DEPTH_TEST);  
glDepthFunc(GL_LESS);  
```

| Function      | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| `GL_ALWAYS`   | The depth test always passes.                                |
| `GL_NEVER`    | The depth test never passes.                                 |
| `GL_LESS`     | Passes if the fragment's depth value is less than the stored depth value. |
| `GL_EQUAL`    | Passes if the fragment's depth value is equal to the stored depth value. |
| `GL_LEQUAL`   | Passes if the fragment's depth value is less than or equal to the stored depth value. |
| `GL_GREATER`  | Passes if the fragment's depth value is greater than the stored depth value. |
| `GL_NOTEQUAL` | Passes if the fragment's depth value is not equal to the stored depth value. |
| `GL_GEQUAL`   | Passes if the fragment's depth value is greater than or equal to the stored depth value. |

简单可想而知深度决定了被观察的可见性，那之前物体的颜色（片段着色器）是要先确定的。这就是一个大问题，模型的片段着色器计算是一个独理的过程，开销跟物体的多少以及精密成都相关，有些显然被遮挡的物体是可以不去计算的。现在大部分的GPU都提供一个叫做提前深度测试(Early Depth Testing)的硬件特性。提前深度测试允许深度测试在片段着色器之前运行。如果一个片段永远不会是可见的（它在其他物体之后），我们就能提前丢弃这个片段。（片段着色器里不要写入片段的深度值，只有这样没有关联的情况下才能够提前确认物体的遮挡。）

**@TODO可以脑补一下，如何去简单判断遮挡关系呢?**

遮挡剔除 (Occlusion Culling) 本质上是这样一个过程——消耗一小部分 CPU 来去掉不可见的物体，不改变最终渲染的画面的同时，降低 GPU 的负载。

https://www.zhihu.com/question/38060533

### 深度精度

深度缓冲包含了一个介于0.0和1.0之间的深度值，它将会与观察者视角所看见的场景中所有物体的z值进行比较。观察空间的z值可能是投影平截头体的**近平面**(Near)和**远平面**(Far)之间的任何值。我们需要一种方式来将这些观察空间的z值变换到[0, 1]范围之间，其中的一种方式就是将它们线性变换到[0, 1]范围之间（类似视口变化那样，用一个确定的范围来适应不同的输出设备）。
$$
\begin{equation} F_{depth} = \frac{z - near}{far - near} \end{equation}
$$

$$
\begin{equation} F_{depth} = \frac{1/z - 1/near}{1/far - 1/near} \end{equation}
$$

按理说这个变换应该是线性的，光学成像就是这个原理。但考虑人的关注点（注意力），倾向于集中注意力在比较近的物体上，所以弄成了一个近似倒数的曲线（非线性精度）。

### 深度冲突

一个很常见的视觉错误会在两个平面或者三角形非常紧密地平行排列在一起时会发生，深度缓冲没有足够的精度来决定两个形状哪个在前面。结果就是这两个形状不断地在切换前后顺序，这会导致很奇怪的花纹。这个现象叫做深度冲突(Z-fighting)，因为它看起来像是这两个形状在争夺(Fight)谁该处于顶端。

**不要把多个物体摆得太靠近，以至于它们的一些三角形会重叠**。手工活比较烦

**尽可能将近平面设置远一些**。将近平面远离观察者，我们将会对整个平截头体有着更大的精度。然而，将近平面设置太远将会导致近处的物体被裁剪掉。经验活需要积累

**使用更高精度的深度缓冲**。大部分深度缓冲的精度都是24位的，但现在大部分的显卡都支持32位的深度缓冲，这将会极大地提高精度。还是技术更新比较有生产力，这个精度提升足够了。虽然还是有浮点数的问题，但玩家要操作出这种场景就太难了。近似于消除问题了（概率小到一定程度在工程上认为解决了）



# 摄像机

OpenGL本身没有**摄像机**(Camera)的概念，但我们可以通过把场景中的所有物体往相反方向移动的方式来模拟出摄像机，产生一种摄像机移动的感觉，而不是场景在移动。定义一个摄像机，需要它在世界空间中的位置、观察的方向（指向z轴的负方向？）即可。有了观察方向之后就可以确定观察空间了，无非是再加上与观察方向垂直的平面来确定以摄像机的位置为原点的坐标系观察坐标系。OPGL一个指向它右测的向量以及一个指向它上方的向量。

## 方向向量

**方向**向量(Direction Vector)并不是最好的名字，因为它实际上指向从它到目标向量的相反方向。这玩意是一个逻辑概念，当从镜头观察物体时其实这个观察方向自然就出来了，只是因为坐标系的关系所以要弄一个反方向的方向向量出来，就是描述从物体的角度看摄像机这件事情。

```c++
glm::vec3 cameraPos = glm::vec3(0.0f, 0.0f, 3.0f);
glm::vec3 cameraTarget = glm::vec3(0.0f, 0.0f, 0.0f);
glm::vec3 cameraDirection = glm::normalize(cameraPos - cameraTarget);
glm::vec3 up = glm::vec3(0.0f, 1.0f, 0.0f); 
glm::vec3 cameraRight = glm::normalize(glm::cross(up, cameraDirection));
glm::vec3 cameraUp = glm::cross(cameraDirection, cameraRight);

glm::mat4 view;
view = glm::lookAt(glm::vec3(0.0f, 0.0f, 3.0f),
                   glm::vec3(0.0f, 0.0f, 0.0f),
                   glm::vec3(0.0f, 1.0f, 0.0f));

// Custom implementation of the LookAt function
glm::mat4 lookAt(glm::vec3 position, glm::vec3 target, glm::vec3 worldUp)
{
    // 1. Position = known
    // 2. Calculate cameraDirection
    glm::vec3 zaxis = glm::normalize(position - target);
    // 3. Get positive right axis vector
    glm::vec3 xaxis = glm::normalize(glm::cross(glm::normalize(worldUp), zaxis));
    // 4. Calculate camera up vector
    glm::vec3 yaxis = glm::cross(zaxis, xaxis);

    // Create translation and rotation matrix
    // In glm we access elements as mat[col][row] due to column-major layout
    glm::mat4 translation = glm::mat4(1.0f); // Identity matrix by default
    translation[3][0] = -position.x; // Third column, first row
    translation[3][1] = -position.y;
    translation[3][2] = -position.z;
    glm::mat4 rotation = glm::mat4(1.0f);
    rotation[0][0] = xaxis.x; // First column, first row
    rotation[1][0] = xaxis.y;
    rotation[2][0] = xaxis.z;
    rotation[0][1] = yaxis.x; // First column, second row
    rotation[1][1] = yaxis.y;
    rotation[2][1] = yaxis.z;
    rotation[0][2] = zaxis.x; // First column, third row
    rotation[1][2] = zaxis.y;
    rotation[2][2] = zaxis.z; 

    // Return lookAt matrix as combination of translation and rotation matrix
    return rotation * translation; // Remember to read from right to left (first translation then rotation)
}
```

$$
LookAt = \begin{bmatrix} \color{red}{R_x} & \color{red}{R_y} & \color{red}{R_z} & 0 \\ \color{green}{U_x} & \color{green}{U_y} & \color{green}{U_z} & 0 \\ \color{blue}{D_x} & \color{blue}{D_y} & \color{blue}{D_z} & 0 \\ 0 & 0 & 0  & 1 \end{bmatrix} * \begin{bmatrix} 1 & 0 & 0 & -\color{purple}{P_x} \\ 0 & 1 & 0 & -\color{purple}{P_y} \\ 0 & 0 & 1 & -\color{purple}{P_z} \\ 0 & 0 & 0  & 1 \end{bmatrix}
$$

封装一下就可以将世界空间变到观察空间。其实这个东西比较好理解，就是原点的移动重合后（平移向量）然后z轴夹角归零的旋转即可。

## 移动

摄像机移动（场景移动也可以转换成摄像机移动）是FPS游戏的常规操作。一般是位置移动和角度移动。

### 位置移动

位置移动有一个速度的概念，例如物体的行走，奔跑，跳跃等等各种会导致屏幕画面的整体平移。这个很好理解，一个人注视某个方向的视野会随着人的移动产生变化，变化的是视野中边缘的部分（游戏中人物在夜晚以及白天视野范围不一样，而且移动后与物体的距离达到一定的值就会丢失视野。）这个可以理解成在路上开车，随着车的前进视野是一直在变化的。如果打方向盘，那就是角度变化了。再来一个例子，直升机在起飞降落的时候，直上直下的情况画面也是整体平移。（普通人应该是适应不了这种操作的，对高度的敏感是后天培养加上仪表的辅助锻炼出来的，而鸟类是有这个竖直维度的能力的）

### 角度移动

角度的概念也很好理解，人站在某个地方不动的情况下转圈就可以观察到前后左右360度的全部视野。让后低头抬头又可以观察到上下360度的全部视野。飞行员牛逼的地方在于坐在位置上搞定上下前后左右的视野，特别是战斗机飞行员在各种高负载的机动中眼观六面还要想办法进入攻击位置咬住敌方瞄准锁定，这样很容易明白优秀的飞行员比飞机值钱的多。再举个简单的例子，在FPS游戏中鼠标通常用于角度控制，最明显的是视野前方的狙击，一瞬间靠感觉调整好预估的水平角度和竖直角度，开镜再次精确移动后狙杀。

还有一种不常见的角度变化，战斗机经常干的就是机腹朝天机头朝地倒着飞，这样绕着飞行线路旋转。**总结起来是俯仰角（pitch），偏航角（yaw）和滚转角**

```c++
    glm::vec3 front;
    front.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
    front.y = sin(glm::radians(pitch));
    front.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
    cameraFront = glm::normalize(front);
```



# 光照

## 颜色

现实世界中有无数种颜色，每一个物体都有它们自己的颜色。我们需要使用（有限的）数值来模拟真实世界中（无限）的颜色，所以并不是所有现实世界中的颜色都可以用数值来表示的。颜色可以数字化的由红色(Red)、绿色(Green)和蓝色(Blue)三个分量组成，这个是加色系的颜色表示方式，也就是叠加颜色来得到最终想要的颜色，是用来描述光线。白色的阳光实际上是所有可见颜色的集合（叠加到了极致就是全白了）。看到某一物体的颜色并不是这个物体真正拥有的颜色，而是它所反射的(Reflected)颜色。物体根据材质会吸收了其中的大部分颜色，仅反射了代表物体颜色的部分，被反射颜色的组合就是人眼所感知到的颜色。这个还是光线，只是变成减色系。也就是说外界光线先叠加到物体上是加色的过程，由于物体的材质对各种光进行反射是减色的过程。也就是说同一个物体再不同的光照下，被观察到的颜色是不一样的。

```c++
FragColor = vec4(lightColor * objectColor, 1.0);

// 白光照射能够反射蓝光的物体，呈现蓝色
lightingShader.setVec3("objectColor", 0.0f, 0.0f, 0.5f);
lightingShader.setVec3("lightColor",  1.0f, 1.0f, 1.0f);

// 红光照射能够反射蓝光的物体，呈现黑色
lightingShader.setVec3("objectColor", 0.0f, 0.0f, 0.5f);
lightingShader.setVec3("lightColor",  1.0f, 0.0f, 0.0f);
```



## 光照模型

现实世界的光照是极其复杂的，而且会受到诸多因素的影响，难以全量模拟。其实这也不是个啥问题，就是当初提出这些概念的时候机器的计算能力不够，按照目前的显卡能力来讲确实可以去模拟但并不经济（精确计算的话又很大的运算量，而人眼的区分度就只有那样，降低了事情的难度了）。光照在不规则的物体上会往各个方向散射，部分散射光线会照到物体形成干扰与叠加。这个计算如果不考虑光强度减弱那就是一个无线循环，就是一个底数很大的阶乘谁都算不了。把光当成粒子（这里不用考虑波粒二象性）的话按照运动学的方式来做并行计算，一次发射出去的各种颜色的粒子（速度无限大没有能量碰撞损失）看有多少个返回观察点（成像区域）即可。类似物体的运动那样力学就有重力，摩檫力还有物体质量以及各种阻力和系数来决定车在路面的运动行为或者船在水里的运动行为。简单的做法是需要一个理论来抽象出几种简单的光源效果来模拟实际行为，就是有差距但不是那么的大不会轻易倍眼睛观察到。

冯氏光照模型(Phong Lighting Model)主要结构由3个分量组成：环境(Ambient)、漫反射(Diffuse)和镜面(Specular)光照。

- 环境光照(Ambient Lighting)：即使在黑暗的情况下，世界上通常也仍然有一些光亮（月亮、远处的光），所以物体几乎永远不会是完全黑暗的。为了模拟这个，我们会使用一个环境光照常量，它永远会给物体一些颜色。这个感觉像是保底的概念，说白了就是物体材质决定的成像效果，所以其比重并不大。
- 漫反射光照(Diffuse Lighting)：模拟光源对物体的方向性影响(Directional Impact)。它是冯氏光照模型中视觉上最显著的分量。物体的某一部分越是正对着光源，它就会越亮。这个很好理解，就是正对光源的就直线反射回来容易落到观察区。这里应该是顶点决定了平面，然后与平面垂直的角度（这就又出现一个新的名字叫做法向量）决定了光照射过去后的分布集中的程度。法向量与光线的夹角就可以计算出一个分量来代表实际的照射量了（是指去的一样多的情况下，接收面积越小就越强，面积越大越分散。可以想象一下同等强度的电筒照水平射一个直角三角形的斜边和垂直边时二者成像的大小是角度的正弦值sinθ，垂直边的亮度高于斜边 ）。这个因素是源头（可以泛化一点理解成光粒子达到物体表面的数量），决定了物体用于反射的关粒子的数量。
- 镜面光照(Specular Lighting)：模拟有光泽物体上面出现的亮点。镜面光照的颜色相比于物体的颜色会更倾向于光的颜色，这个的本意是物体的材质光滑的时候能够尽量多反射光线。其实倍看到的这个亮点还取决于观察点的方向。

### 法向量

法向量只是一个方向向量，不能表达空间中的特定位置。同时，法向量没有齐次坐标（顶点位置中的w分量）。应用一个不等比缩放时（注意：等比缩放不会破坏法线，因为法线的方向没被改变，仅仅改变了法线的长度，而这很容易通过标准化来修复），法向量就不会再垂直于对应的表面了，这样光照就会被破坏。修复这个行为的诀窍是使用一个为法向量专门定制的模型矩阵。这个矩阵称之为法线矩阵(Normal Matrix)：模型矩阵左上角的逆矩阵的转置矩阵（逆转置矩阵）

```
Normal = mat3(transpose(inverse(model))) * aNormal;
```

https://www.jianshu.com/p/5b861ab6ad7a

https://zhuanlan.zhihu.com/p/110520337



## 材质

上面的镜面关照已经涉及到了材质的概念。有些物体反射光的时候不会有太多的散射(Scatter)，因而产生一个较小的高光点，而有些物体则会散射很多，产生一个有着更大半径的高光点。材质就是决定如题如何处理照射到的光粒子，针对冯氏模型那自然就有对环境光，漫反射光和镜面光的粒子的参数：

```
#version 330 core
struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
}; 

uniform Material material;
```

ambient材质向量定义了在环境光照下这个物体反射得是什么颜色，通常这是和物体颜色相同的颜色。diffuse材质向量定义了在漫反射光照下物体的颜色。（和环境光照一样）漫反射颜色也要设置为我们需要的物体颜色。specular材质向量设置的是镜面光照对物体的颜色影响

```c++
void main()
{    
    // 环境光
    vec3 ambient = lightColor * material.ambient;

    // 漫反射 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = lightColor * (diff * material.diffuse);

    // 镜面光
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = lightColor * (spec * material.specular);  

    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
}
```

可以看到镜面光计算的选取强度shininess与观察角度和反射角度的点乘比较大的值的平方。

## 光照贴图

现实世界中的物体通常并不只包含有一种材质，而是由多种材质所组成。想想一辆汽车：它的外壳非常有光泽，车窗会部分反射周围的环境，轮胎不会那么有光泽，所以它没有镜面高光，轮毂非常闪亮（如果你洗车了的话）。汽车同样会有漫反射和环境光颜色，它们在整个物体上也不会是一样的，汽车有着许多种不同的环境光/漫反射颜色。总之，这样的物体在不同的部件上都有不同的材质属性。前面已经提到漫反射和镜面是比较主要的因素（其实漫反射应该是最主要的），正对这两种属性也来一个细节方案即可。引入**漫反射**和**镜面光**贴图(Map)对物体的漫反射分量和镜面光分量有着更精确的控制。其实还是一种暴力的穷举，就是把各个点的属性又弄出一个维度，计算的时候精确求值。

```c++
vec3 ambient  = light.ambient  * vec3(texture(material.diffuse, TexCoords));
vec3 diffuse  = light.diffuse  * diff * vec3(texture(material.diffuse, TexCoords));  
vec3 specular = light.specular * spec * vec3(texture(material.specular, TexCoords));
FragColor = vec4(ambient + diffuse + specular, 1.0);
```

在真实场景中，通常是把复杂物体的多个网格的各种贴图数据进行组合，按照数据的类型分成漫反射，高光和法向量3张图（其实就跟2D的做法类似，atlas的概念把多种资源整合到一起，然后弄个索引可以降低小资源的加载消耗）。

## 光的类型

其实就是光源的属性，前面物体的属性讲完了现在回到光源自身的属性。通常有点光源（节能灯），平行光（激光笔，或者长条形的日光管），聚光灯（手电筒）

对于平行光，无所谓光源的位置，只有一个方向和强度的属性。理想情况下光照强度不会衰减，能量是集中的。

而点光源是一个球型模型，强度跟光源与物体的距离有关（就是球体的表面积，S=4πr²）。

https://blog.csdn.net/weixin_30399055/article/details/96374177

至于为啥弄了个常数和一次项的因子在经验公式中，因该是为了计算方便
$$
\begin{equation} F_{att} = \frac{1.0}{K_c + K_l * d + K_q * d^2} \end{equation}
$$

- 常数项通常保持为1.0，它的主要作用是保证分母永远不会比1小，否则的话在某些距离上它反而会增加强度，这肯定不是我们想要的效果。说白了如果点光源的功率（所有的光能量）只会分摊，所以即使距离光源接近与0，强度也是低于这个阈值的。
- 一次项会与距离值相乘，以线性的方式减少强度。这个应该是在比较仅的距离的时候方便计算，这时候二次方的影响比较小。
- 二次项会与距离的平方相乘，让光源以二次递减的方式减少强度。二次项在距离比较小的时候影响会比一次项小很多，但当距离值比较大的时候它就会比一次项更大了。

聚光灯是一个有夹角的光源，这个也比较容易理解成一个有散射的近似平行光源。例如手电筒随着照射距离其覆盖面逐步变大。所以这里的强度就与夹角和距离有关。至于边缘平滑的聚光，通过内圆锥(Inner Cone)和一个外圆锥(Outer Cone）来划出一个圆环来表示边缘部分的强度变化（从1到0）其实也是在考虑现实中空气的散射以及物体表面的反射之类的因素。

# 模型

模型通常都由3D艺术家在[Blender](http://www.blender.org/)、[3DS Max](http://www.autodesk.nl/products/3ds-max/overview)或者[Maya](http://www.autodesk.com/products/autodesk-maya/overview)这样的工具中精心制作。这些所谓的3D建模工具(3D Modeling Tool)可以让艺术家创建复杂的形状，并使用一种叫做UV映射(uv-mapping)的手段来应用贴图。这些工具将会在导出到模型文件的时候自动生成所有的顶点坐标、顶点法线以及纹理坐标。当使用建模工具对物体建模的时候，通常不会用单个形状创建出整个模型，每个模型都由几个子模型/形状组合而成。组合模型的每个单独的形状就叫做一个网格(Mesh)。比如说有一个人形的角色：头部、四肢、衣服、武器建模为分开的组件，并将这些网格组合而成的结果表现为最终的模型。

一个网格是我们在OpenGL中绘制物体所需的最小单位（顶点数据、索引和材质属性）。一个模型（通常）会包括多个网格。直接上代码看模型与网格的关系（类似顶层节点与实体，是工程上的组织方式以及标准，不涉及物理原理）：

```c++
class Mesh {
public:
    // mesh Data
    vector<Vertex>       vertices;
    vector<unsigned int> indices;
    vector<Texture>      textures;
    unsigned int VAO;

    // constructor
    Mesh(vector<Vertex> vertices, vector<unsigned int> indices, vector<Texture> textures)

    // render the mesh
    void Draw(Shader &shader) 
}

class Model 
{
public:
    // model data 
    vector<Texture> textures_loaded;	// stores all the textures loaded so far, optimization to make sure textures aren't loaded more than once.
    vector<Mesh>    meshes;
    string directory;
    bool gammaCorrection;

    // constructor, expects a filepath to a 3D model.
    Model(string const &path, bool gamma = false) : gammaCorrection(gamma)
    {
        loadModel(path);
    }

    // draws the model, and thus all its meshes
    void Draw(Shader &shader)
    {
        for(unsigned int i = 0; i < meshes.size(); i++)
            meshes[i].Draw(shader);
    }
}
```

# 高级特性

## 模板（轮廓）测试

当片段着色器处理完片段之后，**模板测试(Stencil Test)** 就开始执行了，和深度测试一样，它能丢弃一些片段。仍然保留下来的片段进入深度测试阶段，深度测试可能丢弃更多。模板测试基于另一个缓冲，这个缓冲叫做**模板缓冲(Stencil Buffer)** 模板缓冲中的**模板值(Stencil Value)**通常是8位的，因此每个片段/像素共有256种不同的模板值（译注：8位就是1字节大小，因此和char的容量一样是256个不同值）。这样我们就能将这些模板值设置为我们链接的，然后在模板测试时根据这个模板值，我们就可以决定丢弃或保留它了。

这一段是原话，理解起来是比较费劲的（实际用途：https://www.zhihu.com/question/319943763）。用法取决于其本质的概念，这个测试在整个教程中都是一个裁剪效果。可以用于判定什么显示什么不显示，只不过这个就特别像物体的轮廓的裁剪。这个看起来就很像是模具开模的过程了，用个稍大一点的把中间实际大小的给挖掉就变成一个有薄壁的模具了。举个不那么贴切的例子，狙击枪开镜就是一种模板操作，就是把狙击镜中的画面留下了，目镜以外的其他视野全部都丢了。

代码层面glStencilFunc跟深度缓冲glDepthFunc很类似，其参数是一致的就是换了个属性维度。GL_NEVER`、`GL_LEQUAL`、`GL_GREATER`、`GL_GEQUAL`、`GL_EQUAL`、`GL_NOTEQUAL`、`GL_ALWAYS

```c++
glEnable(GL_DEPTH_TEST);
glDepthFunc(GL_LESS);
glEnable(GL_STENCIL_TEST);
glStencilFunc(GL_NOTEQUAL, 1, 0xFF);
glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

glStencilMask(0xFF);
glStencilFunc(GL_ALWAYS, 0, 0xFF);
glEnable(GL_DEPTH_TEST);
```

但glStencilOp是描述如何更新模板缓冲，这个是深度缓冲没有的概念。深度比较单一，通过测试就显示，通不过就丢弃了。

`void glStencilOp(GLenum sfail, GLenum dpfail, GLenum dppass)`函数包含三个选项，我们可以指定每个选项的动作：

- **sfail**： 如果模板测试失败将采取的动作。
- **dpfail**： 如果模板测试通过，但是深度测试失败时采取的动作。
- **dppass**： 如果深度测试和模板测试都通过，将采取的动作。

每个选项都可以使用下列任何一个动作。

| 操作         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| GL_KEEP      | 保持现有的模板值                                             |
| GL_ZERO      | 将模板值置为0                                                |
| GL_REPLACE   | 将模板值设置为用`glStencilFunc`函数设置的**ref**值           |
| GL_INCR      | 如果模板值不是最大值就将模板值+1                             |
| GL_INCR_WRAP | 与`GL_INCR`一样将模板值+1，如果模板值已经是最大值则设为0     |
| GL_DECR      | 如果模板值不是最小值就将模板值-1                             |
| GL_DECR_WRAP | 与`GL_DECR`一样将模板值-1，如果模板值已经是最小值则设为最大值 |
| GL_INVERT    | Bitwise inverts the current stencil buffer value.            |

`glStencilOp`函数默认设置为 (GL_KEEP, GL_KEEP, GL_KEEP) ，所以任何测试的任何结果，模板缓冲都会保留它的值。

## 面剔除（Face culling）

从一个立方体的任意位置和方向上去看它，永远不能看到多于3个面。所以不需要去绘制那三个不会显示出来的面。其实就跟物体的正面能够被观察到，但是背面时被物体自身所遮挡的。这个严格来讲也是深度的概念，不透明的物体严格依照深度来判定遮挡关系。其实所谓的物体正面背面时取决于观察者的位置的，如果换个方向后原来的物体背面就变成正面了（在观察者换了方向之后，原反向上看的背面的顶点方向也逆向变成顺时针，自然就变成可见的正面了）。



## 帧缓冲（FrameBuffer）

用于写入颜色值的颜色缓冲，用于写入深度信息的深度缓冲，以及允许我们基于一些条件丢弃指定片段的模板缓冲。这些常规操作直接操作用于屏幕的帧，如果后续所有渲染操作将渲染到当前绑定的帧缓冲的附加缓冲中，渲染命令对窗口的视频输出不会产生任何影响。出于这个原因，它被称为离屏渲染（off-screen rendering）。其实所谓的离屏是一个视觉上的概念，所有的渲染过程都没有特殊性，只是东西没有更新到屏幕而已，等于没有获取焦点的后台程序，有数据但是不体现在交互上。



## 后处理（post processing）

在已经取得了渲染输出的每个颜色之后，在片段着色器里各种组合或者操作这些颜色是很容易的。这个就是看情况弄出各种视觉或者风格特效了。



## 立方体贴图（cube map）

这个概念的描述并不是很贴切，就不引用原文了。如果把它理解成环境贴图可能精确一些，其实也不是所有的环境都是立方体，但抽象一下就是眼观六面（上下左右前后）。这6张图的要求可是不低的，目视任何一个维度然后转身360°都能够看到一个连续的画面，举例说绕着y轴360转（偏航角）的前，右，后，左4张图是可以拼接成一个圆形的。然后绕着z轴360转（滚转角）的上，右，下，左是圆形。最后绕着x轴360°转（俯仰角）上，前，下，后也是圆形。

```c++
vector<std::string> faces
{
    FileSystem::getPath("resources/textures/skybox/right.jpg"),
    FileSystem::getPath("resources/textures/skybox/left.jpg"),
    FileSystem::getPath("resources/textures/skybox/top.jpg"),
    FileSystem::getPath("resources/textures/skybox/bottom.jpg"),
    FileSystem::getPath("resources/textures/skybox/front.jpg"),
    FileSystem::getPath("resources/textures/skybox/back.jpg")
};
```

| 纹理目标（Texture target）     | 方位 |
| ------------------------------ | ---- |
| GL_TEXTURE_CUBE_MAP_POSITIVE_X | 右   |
| GL_TEXTURE_CUBE_MAP_NEGATIVE_X | 左   |
| GL_TEXTURE_CUBE_MAP_POSITIVE_Y | 上   |
| GL_TEXTURE_CUBE_MAP_NEGATIVE_Y | 下   |
| GL_TEXTURE_CUBE_MAP_POSITIVE_Z | 后   |
| GL_TEXTURE_CUBE_MAP_NEGATIVE_Z | 前   |

这种用法下，只需要一个观察方向就可以决定整个环境的纹理，整个大背景完全不受移动的影响（营造出类似大背景的感觉，但方向不动的情况下，背景其实一点都没有变化），这个用法叫做天空盒子（sky box）。

在代码层面的处理也比较讨巧。深度测试默认是小于，然后天空盒使用的小于等于。xyww的设置让透视投影后z是1.0。这样但凡有个场景内的物体被渲染都会在天空盒的前面，既不会被盒子遮挡，而且盒子刚好通过测试也能够被显示出来。

```c++
glDepthFunc(GL_LEQUAL);

void main()
{
    vec4 pos = projection * view * vec4(position, 1.0);
    gl_Position = pos.xyww;
    TexCoords = position;
}
```

### 环境映射

#### 反射

反射环境也不太清楚是什么具体用法。前面帧缓冲中有涉及到反向观察物体。这里把环境当成物体的一种，也是算出了反方向的纹理。这种技术的用处一般应该是倒视镜之类的游戏中。

#### 折射

这个理论上讲是非常有意义的。即使是空气也会折射和散射光线（空气中的水汽，云层，雨水），这样才有更真实的效果。除了环境会折射，场景中的各种物体例如水，玻璃，钻石之类的能够让光线通过的都会有改变光线角度以及降低光线的强度等等。



## 几何着色器(Geometry Shader)

在顶点和片段着色器之间的一个可选的着色器。有意思的地方在于它可以把（一个或多个）顶点转变为完全不同的基本图形（primitive），从而生成比原来多得多的顶点。其实就是一个特定程序，用来自动生成顶点，其实还是顶点着色器的范畴。



### 实例化

这也是一个集中发送CPU到GPU数据的思想的体现。OpenGL在它可以绘制你的顶点数据之前必须做一些准备工作(比如告诉GPU从哪个缓冲读取数据，以及在哪里找到顶点属性，所有这些都会使CPU到GPU的总线变慢)。所以即使渲染顶点超快，而多次给你的GPU下达这样的渲染命令却未必。如果需要大量的绘制同一个物体在不同的位置就又意义了。等于一个绘制函数，一个物体数据，然后再自定义一个uniform位置变量（数组存了一堆偏移向量），顶点着色器就可以通过gl_InstanceID这个物体的索引来应用偏移量，画出多个物体。

```c++
for(unsigned int i = 0; i < 100; i++)
{
    shader.setVec2(("offsets[" + std::to_string(i) + "]")), translations[i]);
}

glDrawArraysInstanced(GL_TRIANGLES, 0, 6, 100);  
```

这个跟glDrawArrays是一个概念，多了一个参数100表示要画出的实例的个数。



## 抗锯齿技术(Anti-aliasing）

**锯齿边(Jagged Edge)**出现的原因是由顶点数据像素化之后成为片段的方式所引起的。从原理入手，光栅化顶点和片段着色器之间的所有算法和处理的集合。光栅化将属于一个基本图形的所有顶点转化为一系列片段。顶点坐标理论上可以含有任何坐标，但片段却不是这样，这是因为它们与你的窗口的解析度有关。光栅化必须以某种方式决定每个特定顶点最终结束于哪个片段/屏幕坐标上，这种多对少的映射关系决定了边缘部分相对近的顶点总会出现割裂。由于屏幕像素总量的限制，有些边上的像素能被渲染出来，而有些则不会体现出来的效果就是放大后的锯齿感。

**多采样抗锯齿(Multisample Anti-aliasing)**MSAA的真正工作方式是，每个像素只运行一次片段着色器，无论多少子样本被三角形所覆盖。片段着色器运行着插值到像素中心的顶点数据，最后颜色被储存近每个被覆盖的子样本中，每个像素的所有颜色接着将平均化，每个像素最终有了一个唯一颜色。这个技术比较自然，精度问题的处理方式自然是提高计算精度（在不明显增加计算量的前提下）。屏幕上一个点由0/1的状态（三角形计算这个点的中心是否在三角形内）变成了N个状态。只要采样点变多，那是否在三角形内以及在内的采样点的个数就变得有意义了。个数大于0可以决定像素点被使用，然后在内的采样点的个数与采样N的关系还可以决定像素的颜色。

付出的代价是为每个像素储存一个以上的颜色值的颜色缓冲(因为多采样需要我们为每个采样点储存一个颜色)。这就需要一个新的缓冲类型，它可以储存要求数量的多重采样样本，它叫做**多样本缓冲(Multisample Buffer)**。算是空间换时间的一种做法。



引申一下这个话题：FXAA、FSAA与MSAA有什么区别

https://www.zhihu.com/question/20236638

锯齿的来源是因为场景的定义在三维空间中是连续的，而最终显示的像素则是一个离散的二维数组。所以判断一个点到底没有被某个像素覆盖的时候单纯是一个“有”或者“没有"问题，丢失了连续性的信息，导致锯齿。

最直接的抗锯齿方法就是SSAA（Super Sampling AA）。拿4xSSAA举例子，假设最终屏幕输出的分辨率是800x600, 4xSSAA就会先渲染到一个分辨率1600x1200的buffer上，然后再直接把这个放大4倍的buffer下采样致800x600。这种做法在数学上是最完美的抗锯齿。但是劣势也很明显，光栅化和着色的计算负荷都比原来多了4倍，render target的大小也涨了4倍。

MSAA（Multi-Sampling AA）则很聪明的只是在光栅化阶段，判断一个三角形是否被像素覆盖的时候会计算多个覆盖样本（Coverage sample），但是在pixel shader着色阶段计算像素颜色的时候每个像素还是只计算一次。

Post Processing AA这一类技术。这一类东西包括FXAA，TXAA等，不依赖于任何硬件，完全用图像处理的方法来搞。有可能会依赖于一些其他的信息例如motion vector buffer或者前一贞的变换矩阵来找到上一贞像素对应的位置，就是主动探测出边缘，然后对边缘的锯齿进行平滑补偿（肯恩不太精确但省事，毕竟人的观察能力是很有限的）。

有句话说的挺好，抗锯齿只不过是分辨率不够高之前做的一个安慰剂。以后2k/4K屏幕和对应级别的显卡都会成为普通产品，自然就不会出现屏幕像素点太少了以至于边缘锯齿轻易被人眼观察到。比如说手机这种屏幕小分辨率还高的外设，压根就不用在乎锯齿。



## 法线贴图（normal mapping）

https://zhuanlan.zhihu.com/p/102131805

法线如果是基于面来说是一个很确定的东西，问题是两个面的边缘共顶点的时候怎么做？这里有两个新概念，**模型空间法线贴图**和**切线空间法线贴图**。正常（无双关）的成分范围为`[-1, 1]`。但是图像中颜色的成分范围为`[0, 1]`（或`[0, 255]`通常将其标准化为`[0, 1]`）。因此对法线进行缩放和偏移，使法线`(0, 0, 1)`变为颜色`(0.5, 0.5, 1)`。这是您在法线贴图中看到的浅蓝色，并且在使用切线空间法线时表示与插值顶点法线没有偏差。

法线贴图技术仅仅是让三角形渲染的时候，多了一个真实的法线值，用于做光照计算，而不能增加顶点值。因为一般时候，顶点值在计算光照的时候都用不到。

那么，是不是所有的复杂模型都可以用法线贴图来解决呢？当然是不可能的。说穿了，法线贴图仅仅是简单的视觉欺骗，一旦凹凸太明显的模型，使用了法线贴图，太靠近的时候，就穿帮了。所以，适用于法线贴图的场合，主要就是凹凸不太明显，细节很多，需要表现实时光照效果，不会太靠近观察的物体。





# 高级光照

## Blinn-Phong

冯氏光照模型已经不错了，这个算是一个改进型。原因是冯氏在镜面反射在某些条件下会失效，视线向量和反射向量的角度大于90度的话，点乘的结果就会是负数，镜面的贡献成分就会变成0。表现就是镜面区域边缘迅速减弱并截止，效果不太自然。用法线向量和半程向量(光源方向和视线向量的角平分线)来替换的精髓在于法向量。法向量与镜面是垂直关系，与其他向量的点乘不会变成负数。而且半程向量的计算更简单，相加后归一即可。反射向量则需要用到三角函数。

```c++
    if(blinn)
    {
        vec3 halfwayDir = normalize(lightDir + viewDir);  
        spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);
    }
    else
    {
        vec3 reflectDir = reflect(-lightDir, normal);
        spec = pow(max(dot(viewDir, reflectDir), 0.0), 8.0);
    }
```



# 其他概念





## 规范与实现

- 基于插件发布新功能。
- 使用状态机实现。更改的都是上下文，表现是异步执行的。屏幕刷新率可以算作状态机的驱动力
- 对象。不是实体的概念，是一种对属性集合的抽象（应该说是一堆属性的惯用的逻辑抽象）。这里的出发点应该是把基础抽象化成一些可复用的逻辑组件，以便上层应用轻松复用。





