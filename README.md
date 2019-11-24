# 语法分析器实验报告  

班内序号：05	姓名：李燕杰	学号：2017211919	班级：2017211503

## 实验结果  

完成了对课本要求文法的LR语法分析器实现，包括：  

1. 从**输入文法产生式**分析生成非终结符的**FIRST集**与**FOLLOW集**  
  <img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124114440734.png" alt="image-20191124114440734" style="zoom:40%;" />

2. 从**输入文法产生式**分析生成**项目集规范族**  
  <img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124114534855.png" alt="image-20191124114534855" style="zoom:50%;" />  

3. 从**项目集规范族**以及**FIRST & FOLLOW集**生成**SLR分析表**  
  <img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124115009631.png" alt="image-20191124115009631" style="zoom: 33%;" />
  
  其中-1为ERROR状态，action与编号的对应关系如下：  
  
  <img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124142000456.png" alt="image-20191124142000456" style="zoom:50%;" />

4. 从**分析表**与**输入记号流**产生分析过程  
  <img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124115037067.png" alt="image-20191124115037067" style="zoom: 33%;" /> 

上述各项中，运行python脚本Syntax.py所在控制台输出的仅有分析过程，其他项均在运行时同时生成的Syntax Result.txt文件中。

## 源码说明  

### 文本文件  

`Syntax Result.txt`为分析结果输出文件；

`Syntatic Analyzer Test File.txt`为测试记号流文件。 

### Automation.py  

Automation.py对应从文法产生式输入到分析表生成的处理过程，结构如下图所示，其中：  

- `cal_first(), cal_follow(), cal_first_follow()`对应FIRST集FOLLOW集的生成  
- `generate_collections(), partition(), calculate_closure()`对应项目集规范族的生成  
- `generate_table(), fill_table()`对应分析表的生成 

<center>
	<img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124142225463.png" alt="image-20191124142225463" style="zoom:33%;" />  
</center>

### Syntax.py  

 Syntax.py对应根据分析表对输入记号流进行分析的过程，结构如下图所示，其中：  

- `analyze()`对应调用Automation生成分析表与开始分析过程  
- `process(), make_action()`对应分析过程  

<center><img src="/Users/bigbrothersue/Library/Application Support/typora-user-images/image-20191124142932301.png" alt="image-20191124142932301" style="zoom:40%;" /></center>  