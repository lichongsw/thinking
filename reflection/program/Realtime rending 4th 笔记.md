渲染基本模型：







看到这个抽象的感觉是就是大力出奇迹，对最小几何基本单元（点）进行逐个计算。这个路子行得通是目前人眼的观察能力有限，只需要把一屏幕的数据暴力计算出来即可。



计算分解为自然部分和人为部分，再者还有一个物体自身的反射率。

自然部分是客观存在的次要组成部分，权重一般较小（特指主流的生活场景，充斥着各种非自然灯光），与观察的方向也有关。对于非常大的自然界场面例如蓝天白云，人为光照的影响几乎可以忽略，大场面中例如山川河流物体过于庞大，人眼只是观察轮廓，已经不需要计法线的影响了（小细节的物体的明暗已经不是焦点了，或者说不可察了）。Blinn-Phong模型中ambient 计算都是常量，就直接忽略了法线与观察角度的关系。

人为部分（近处的小场景）的权重就比较大了，毕竟是人眼的主要使用方式。各种非自然灯光被反射到人眼，针对每一种类光源（点光源，直射光灯不同的能量的散射特性）再展开计算即可。在局部来说舒适的光照能量不会过于衰减，台灯，壁灯，吊顶大灯这些日常使用的灯的光源强度基本上与需要照射的空间表面积是成比例的。

可以说只要对光线的运用到位，不管是大场面还是局部小空间，现代计算机渲染的画面肯定比实物更精美。简单操作就可以消除真实世界中各种噪音与瑕疵。