## 实验一：SQL定义功能、数据插入

**1．建立教学数据库的三个基本表：**
**S(Sno,Sname,Sgender,Sage,Sdept)   学生（学号，姓名，性别，年龄，系）** 
**SC(Sno,Cno,Grade)              选课（学号，课程号，成绩）**
**C(Cno,Cname,Cpno,Ccredit)      课程（课程号，课程名，先行课，学分）**

这三张表一开始老师给过我们了，可以直接查看其结构。

```sql
SQL> describe student
Name  Type         Nullable Default Comments 
----- ------------ -------- ------- -------- 
SNO   VARCHAR2(9)  Y                         
SNAME VARCHAR2(20) Y                         
SSEX  VARCHAR2(4)  Y                         
SAGE  NUMBER(2)    Y                         
SDEPT VARCHAR2(20) Y                         

SQL> describe sc;
Name  Type        Nullable Default Comments 
----- ----------- -------- ------- -------- 
SNO   VARCHAR2(9) Y                         
CNO   VARCHAR2(4) Y                         
GRADE NUMBER(3)   Y                         

SQL> describe course;
Name    Type         Nullable Default Comments 
------- ------------ -------- ------- -------- 
CNO     VARCHAR2(4)  Y                         
CNAME   VARCHAR2(20) Y                         
CPNO    VARCHAR2(4)  Y                         
CCREDIT NUMBER(2,1)  Y                         
```

然后再对着上面的结构创立新表。

```sql
SQL> create table S(
  2                          Sno char(9),
  3                          Sname char(20),
  4                          Sgender char(4),
  5                          Sage number(2),
  6                          Sdept char(20));

Table created


SQL> create table SC(
  2                          Sno char(9),
  3                          Cno char(4),
  4                          Grade number(3));

Table created


SQL> create table C(
  2                          Cno char(4),
  3                          Cname char(20),
  4                          Cpno char(4),
  5                          Ccredit number(2,1));

Table created
```

**2．DROP TABLE、ALTER TABLE、CREATE INDEX、DROP INDEX 及INSERT语句输入数据。**

drop table先将之前存在的三张表删了。

```sql
SQL> drop table SC;

Table dropped


SQL> drop table STUDENT;

Table dropped


SQL> drop table COURSE;

Table dropped
```

alter table给前面创的表增加主键。

```sql
SQL> alter table S add primary key(Sno);

Table altered
             

SQL> alter table SC add primary key(Sno,Cno);

Table altered


SQL> alter table C add primary key(Cno);

Table altered
```

create index时发现上一步加主键就已经给这几个主键建立了索引，所以不能直接对这几个属性建立索引。

```sql
SQL> create unique index Stusno on S(Sno);
create unique index Stusno on S(Sno)

ORA-01408: 此列列表已索引

SQL> select * from user_ind_columns where table_name = 'S';

INDEX_NAME                     TABLE_NAME                     COLUMN_NAME                                                                      COLUMN_POSITION COLUMN_LENGTH CHAR_LENGTH DESCEND
------------------------------ ------------------------------ -------------------------------------------------------------------------------- --------------- ------------- ----------- -------
SYS_C0012331                   S                              SNO                                                                                            1             9           9 ASC
                                                                                       1             4           4 ASC
```

我们可以把主键约束删除之后，再建立索引。

```sql
SQL> alter table S drop primary key;

Table altered


SQL> select * from user_ind_columns where table_name = 'S';

INDEX_NAME                     TABLE_NAME                     COLUMN_NAME                                                                      COLUMN_POSITION COLUMN_LENGTH CHAR_LENGTH DESCEND
------------------------------ ------------------------------ -------------------------------------------------------------------------------- --------------- ------------- ----------- -------                    


SQL> create unique index Stusno on S(Sno);

Index created


SQL> alter table SC drop primary key;

Table altered


SQL> alter table C drop primary key;

Table altered


SQL> create unique index Coucno on C(Cno);

Index created


SQL> create unique index SCno on SC(Sno ASC,Cno DESC);

Index created
```

drop index将刚才建立的三个索引删了。

```sql
SQL> drop index Stusno;

Index dropped


SQL> drop index CouCno;

Index dropped


SQL> drop index SCno;

Index dropped
```

insert语句将书上的数据插入表中。

```sql
SQL> insert into S values('201215121','李勇','男',20,'CS');

1 row inserted


SQL> insert into S values('201215122','刘晨','女',19,'CS');

1 row inserted


SQL> insert into S values('201215123','王敏','女',18,'MA');

1 row inserted


SQL> insert into S values('201215125','张立','男',19,'IS');

1 row inserted


SQL> insert into SC values('201215121','1',92);

1 row inserted


SQL> insert into SC values('201215121','2',85);

1 row inserted


SQL> insert into SC values('201215121','3',88);

1 row inserted


SQL> insert into SC values('201215122','2',90);

1 row inserted


SQL> insert into SC values('201215122','3',80);

1 row inserted


SQL> insert into C values('1','数据库','5',4);

1 row inserted


SQL> insert into C values('2','数学',NULL,2);

1 row inserted


SQL> insert into C values('3','信息系统','1',4);

1 row inserted


SQL> insert into C values('4','操作系统','6',3);

1 row inserted


SQL> insert into C values('5','数据结构','7',4);

1 row inserted


SQL> insert into C values('6','数据处理',NULL,2);

1 row inserted


SQL> insert into C values('7','PASCAL语言','6',4);

1 row inserted
```

## 实验二：数据查询

**1．查询选修1号课程的学生学号与姓名。**

```sql
SQL> select Sno,Sname from S natural join SC where Cno='1';

SNO       SNAME
--------- --------------------
201215121 李勇
```

**2．查询选修课程名为数据库原理的学生学号与姓名。**

```sql
SQL> select Sno,Sname from (S natural join SC) natural join C where Cname='数据库';

SNO       SNAME
--------- --------------------
201215121 李勇
```

**3．查询不选1号课程的学生学号与姓名。**

```sql
SQL> select Sno,Sname from S where not exists (select * from SC where Sno=S.Sno and Cno='1');

SNO       SNAME
--------- --------------------
201215125 张立
201215122 刘晨
201215123 王敏
```



插入一组数据，方便后续查询。

```sql
SQL> insert into SC values('201215121','4',88);

1 row inserted


SQL> insert into SC values('201215121','5',88);

1 row inserted


SQL> insert into SC values('201215121','6',88);

1 row inserted


SQL> insert into SC values('201215121','7',88);

1 row inserted


SQL> insert into SC values('201215125','1',88);

1 row inserted
```

**4．查询学习全部课程学生姓名。**

换个方向理解：没有一门课程是这个学生不选的。

```sql
SQL> select Sname from S where not exists (select * from C where not exists(select * from SC where Sno=S.Sno and Cno=C.Cno));

SNAME
--------------------
李勇
```

**5．查询所有学生除了选修1号课程外所有成绩均及格的学生的学号和平均成绩，其结果按平均成绩的降序排列。**

```sql
SQL> select Sno,Avg(Grade) from SC where not exists (select * from SC where Cno='1' and Grade<60) group by Sno order by Avg(Grade) DESC;

SNO       AVG(GRADE)
--------- ----------
201215121 88.1428571
201215125         88
201215122         85
```

**6．查询选修数据库原理成绩第2名的学生姓名。**

```sql
SQL> select Sname from (S natural join SC) natural join C where Cname='数据库' and 
  2  Grade=(select max(Grade) from (S natural join SC) natural join C where Cname='数据库' and 
  3  Grade<(select max(Grade) from (S natural join SC) natural join C where Cname='数据库'));

SNAME
--------------------
张立
```

**7    查询所有4个学分课程中有3门以上（含3门）课程获80分以上（含80分）的学生的姓名。**

```sql
SQL> select Sname from (S natural join SC) natural join C where Ccredit=4 and Grade>=80 
  2  group by Sname having count(*)>=3;

SNAME
--------------------
李勇
```

**8    查询选课门数唯一的学生的学号。**

```sql
SQL> select Sno from Sc group by Sno having count(*)=1;

SNO
---------
201215125
```

**9．SELECT语句中各种查询条件的实验。**

查询条件设置为选了1号课程且成绩为92分的学生学号姓名。

```sql
SQL> select Sno,Sname from S natural join SC where Cno='1' and Grade=92;

SNO       SNAME
--------- --------------------
201215121 李勇
```

## 实验三：数据修改、删除

**1．把1号课程的非空成绩提高10％。**

```sql
SQL> update SC set Grade=1.1*Grade where Cno='1' and Grade is not NULL;

2 rows updated


SQL> select * from SC;

SNO       CNO  GRADE
--------- ---- -----
201215121 1      101
201215121 2       85
201215121 3       88
201215122 2       90
201215122 3       80
201215121 4       88
201215121 5       88
201215121 6       88
201215121 7       88
201215125 1       97

10 rows selected
```

**2．在SC表中删除课程名为数据库原理的成绩的元组。**

```sql
SQL> delete from SC where Cno=(select Cno from C where Cname='数据库'); 

2 rows deleted


SQL> select * from SC;

SNO       CNO  GRADE
--------- ---- -----
201215121 2       85
201215121 3       88
201215122 2       90
201215122 3       80
201215121 4       88
201215121 5       88
201215121 6       88
201215121 7       88

8 rows selected
```

**3．在S和SC表中删除学号为201215121的所有数据。**

好像没办法一步到位，那就分两次删吧。

```sql
SQL> delete from S where Sno='201215121';

1 row deleted


SQL> delete from SC where Sno='201215121';

6 rows deleted


SQL> select * from S;

SNO       SNAME                SGENDER SAGE SDEPT
--------- -------------------- ------- ---- --------------------
201215122 刘晨                 女        19 CS
201215123 王敏                 女        18 MA
201215125 张立                 男        19 IS

SQL> select * from SC;

SNO       CNO  GRADE
--------- ---- -----
201215122 2       90
201215122 3       80
```

## 实验四：视图的操作

**1．建立男学生的视图，属性包括学号、姓名、选修课程名和成绩。**

```sql
SQL> create view Stu_male(Sno,Sname,Cname,Grade) as select Sno,Sname,Cname,Grade from (S natural join SC) natural join C;

View created
```

**2．在男学生视图中查询平均成绩大于80分的学生学号与姓名。**

```sql
SQL> select Sno,Sname from Stu_male where Grade>80;

SNO       SNAME
--------- --------------------
201215122 刘晨
```

## 实验五：库函数，授权控制

**1．计算每个学生有成绩的课程门数、平均成绩。**

```sql
SQL> select S.Sno,count(SC.Sno),Avg(Grade) from S left join SC on S.Sno=SC.Sno group by S.Sno;

SNO       COUNT(SC.SNO) AVG(GRADE)
--------- ------------- ----------
201215125             0 
201215122             2         85
201215123             0 
```

**2．使用GRANT语句，把对基本表S、SC、C的使用权限授给其它用户。**

```sql
SQL> grant all on S to public;

Grant succeeded


SQL> grant all on SC to public;

Grant succeeded


SQL> grant all on C to public;

Grant succeeded
```

**3．实验完成后，撤消建立的基本表和视图。**

```sql
SQL> drop table S;

Table dropped


SQL> drop table SC;

Table dropped



SQL> drop table C;

Table dropped


SQL> drop view Stu_male;

View dropped
```

## 实验六：综合实验：实现一个小型管理信息系统 

熟练掌握Visual C++、Pro*C或Java访问数据库的方法，设计和实现学生通讯录或学生选课的一个小型管理信息系统。要求具有数据的增加、删除、修改和查询的基本功能，并尽可能提供较多的查询功能，用户界面要友好。课程结束前提交上机实验报告和程序。

之前做过一个南航图书馆管理系统，基于flask和postgreSQL数据库构建。Flask框架自由灵活，可扩展性强，透明可控，搭建简便。并且运用python可以很简单的建立postgreSQL 数据库连接。

这次想对于课堂教学使用的Oracle数据库进一步加深理解熟练掌握，故重新做了一个学生选课管理系统，发现Web框架对于Oracle 11g不兼容，故采用命令行的形式呈现。

### 一、实验平台

操作系统：windows10

开发工具：pycharm

数据库：oracle 11g

系统开发语言：python

### 二、系统介绍

本系统功能模块划分：

（1）对数据的浏览模块；

（2）对数据的查询模块；

（3）对数据的添加模块；

（4）对数据的修改模块；

（5）对数据的删除模块；

数据库一共使用了5张表M、A、S、C、SC，具体介绍如下：

**PS：对于字符类型的数据，赋成varchar属性（不然输出的时候对齐的很麻烦），需要去除字段前后空格**

M表结构如下：

| 属性名 |   MNO    |    PW    |
| :----: | :------: | :------: |
|  类型  | char(10) | char(16) |

M表存的是系统管理员manager的账号和密码。

A表结构如下：

| 属性名 |   SNO    |    PW    |
| :----: | :------: | :------: |
|  类型  | char(10) | char(16) |

A表存的是各个用户管理者admin的账号和密码。

S表结构如下：

| 属性名 |   SNO    |  SNAME   | SGENDER |   SAGE    |  SDEPT  |
| :----: | :------: | :------: | :-----: | :-------: | :-----: |
|  类型  | char(10) | char(16) | char(4) | number(2) | char(9) |

S表存的是书上P52的Student表。

C表结构如下：

| 属性名 |   CNO   |  CNAME   |  CPNO   |   CREDIT    |
| :----: | :-----: | :------: | :-----: | :---------: |
|  类型  | char(4) | char(20) | char(4) | number(2,1) |

C表存的是书上P52的Course表。

SC表结构如下：

| 属性名 |   SNO    |   CNO   |   GRADE   |
| :----: | :------: | :-----: | :-------: |
|  类型  | char(10) | char(4) | number(3) |

SC表存的是书上P52的SC表。

### 三、代码设计

本程序一共设计三个文件，interface文件设计界面，utils文件中定义各种数据库的操作，也是最主要的一个文件，main文件试运行文件，在命令行中输入python main.py即可运行学生选课管理系统。

utils中定义三个类，如下：

1、Login_Judge(ID, PD)

该类是登录检验，通过查询M、A表中是否有对应的数据判断所输入的是否是正确的账号和密码。

2、StudentOption

该类定义了学生可选择的一些操作，具体设计模式如下：

①查看学生个人信息

②查看课程信息（可选择按课程号从小到大排序和按学分从小到大排序）

③查看学生个人课表

④选课（选课时候你输入的课程号要是不在C表里或者在SC表里，不能选课）

⑤退课（退课的时候不需要考虑是否选了这么课，直接输出退课成功就行了）

⑥修改账号密码（三次输错机会）

3、AdminOption

该类定义了管理员可选择的一些操作，具体设计模式如下：

①查看学生信息、课程信息、分数情况（查看全体学生信息时可以按学号升序排序也可以按专业分组排序；查询课程信息和学生操作时一样；查看全体学生分数情况时可按学生号排序和按课程号排序，两种排序成绩都是升序的）

②录入学生信息、课程信息（需要保证录入信息的正确性）

③修改学生信息、课程信息、成绩（需要保证修改的信息的正确性）

④删除学生信息、课程信息（删除的时候不需要考虑学号和课程号对不对，直接删除就行了）

⑤修改账号密码（三次输错机会）

### 四、实验步骤

1、编写程序；

2、通过pycharm编译；

3、运行试用结合使用体验修改代码；

### 五、实验结果

先展示一下之前做的图书馆管理系统的样式。

![](C:\Users\86173\Desktop\微信图片_20220625003940.png)

![微信图片_20220625003949](C:\Users\86173\Desktop\微信图片_20220625003949.png)

本次实验Django框架不能兼容11g，故采用在命令行中展示的形式。在命令行进入项目所在的目录下，运行python main.py，即可进入选课系统。

![](C:\Users\86173\Desktop\新建文件夹\1.png)

按任意键即可进入到登录页面，对于登录的设计，允许你输入错几次，但超过3次会被强制退出。

![](C:\Users\86173\Desktop\新建文件夹\2.png)

正确输入账号密码之后，进入到功能界面，这里以Administrator为例，可选择的功能如下所示：

![](C:\Users\86173\Desktop\新建文件夹\3.png)

比如说我们选择1，就可以选择对学生信息的增删查改或者退出。

![](C:\Users\86173\Desktop\新建文件夹\5.png)

这时我们选择1增加信息，可以发现若我们没有按照要求输入合理的信息，会自动退出。

![](C:\Users\86173\Desktop\新建文件夹\6.png)

正确结束时，我们会将学生信息录入S表，并且增加一个学生账号，密码默认为123456存入A表。

![7](C:\Users\86173\Desktop\新建文件夹\7.png)

在查询学生成绩的时候，也设计了多种查询方式，而且为了避免用户选择，我们直接选择两种查询结果都显示出来。

![](C:\Users\86173\Desktop\新建文件夹\8.png)

别的就不过多演示了，该系统考虑到了各种查询，分组查询、多表查询。

### 六、系统特色

1、使用多张表，在查询时可以进行各种多表查询、分组查询。

2、对表中的属性都设计了合理性检验，具体参考”三、代码设计“部分。

3、系统简介高效，可以满足用户的各种需求，是一个完整的学生选课管理系统。

4、对于系统中可能出现的问题，并没有修改表的结构，而是通过输入优化、存储优化来规避，比如说对课程号属性，表的定义为char类型，那么字符比较时1比10要大，我们可以把1统一成01，01比10小，即不用修改表属性。

5、对于学生用户的权限和管理员用户的权限都经过深思熟虑，保证学生的隐私、管理员的高效。

6、对于一些功能做了合并，比如删除学生成绩归并到修改学生成绩，输入-1，系统后置的sql语言会自己进行修改表中数据使数据为空。在另外的一些删除中，删除并不需要考虑数据是否存在，直接删除成功就行。

### 七、分工

本次实验是有祖元琨同学和唐娇同学组队完成的，由于是想要通过实验对于Oracle数据库更好地掌握，因此我们都对这个系统进行了完整的构建，共同设计用户、管理员该有的权限，对于每个表中的数据的增加和修改增加约束范围，因此分工比例为50%和50%。



