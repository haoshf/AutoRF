from django.db import models


class Project(models.Model):
    """
    项目表
    """
    id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(verbose_name='项目名称', max_length=32, unique=True)
    Documentation = models.CharField(verbose_name='项目描述', max_length=255)
    Suite_Setup = models.CharField(verbose_name='项目数据初始化', max_length=128)
    Suite_Teardown = models.CharField(verbose_name='项目数据清理', max_length=128)
    Test_Setup = models.CharField(verbose_name='用例数据初始化', max_length=128)
    Test_Teardown = models.CharField(verbose_name='用例数据清理', max_length=128)
    Force_Tags = models.CharField(verbose_name='项目标记', max_length=32)
    Library = models.CharField(verbose_name='引用库', max_length=128)
    Resource = models.CharField(verbose_name='引用资源', max_length=128)
    Variables = models.CharField(verbose_name='引用变量', max_length=128)
    Scalar_Variables = models.CharField(verbose_name='普通变量', max_length=128)
    List_Variables = models.CharField(verbose_name='列表变量', max_length=128)
    Dict_Variables = models.CharField(verbose_name='字典变量', max_length=128)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project'

class Resource(models.Model):
    """
    资源表
    """
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(to='Project',on_delete=models.SET(1))
    resource_name = models.CharField(verbose_name='资源名称', max_length=32,null=False)
    Documentation = models.CharField(verbose_name='资源描述', max_length=255)
    Library = models.CharField(verbose_name='引用库', max_length=128)
    Resource = models.CharField(verbose_name='引用资源', max_length=128)
    Variables = models.CharField(verbose_name='引用变量', max_length=128)
    Scalar_Variables = models.CharField(verbose_name='普通变量', max_length=128)
    List_Variables = models.CharField(verbose_name='列表变量', max_length=128)
    Dict_Variables = models.CharField(verbose_name='字典变量', max_length=128)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)

    def __str__(self):
        return self.resource_name

    class Meta:
        db_table = 'resource'
        unique_together = (("project", "resource_name"),)

class Suite(models.Model):
    """
    用例集表
    """
    id = models.BigAutoField(primary_key=True)
    suite_name = models.CharField(verbose_name='套件名称', max_length=32,null=False)
    project = models.ForeignKey(to="Project",null=False,on_delete=models.CASCADE)
    Documentation = models.CharField(verbose_name='套件描述', max_length=255)
    Suite_Setup = models.CharField(verbose_name='套件数据初始化', max_length=128)
    Suite_Teardown = models.CharField(verbose_name='套件数据清理', max_length=128)
    Test_Setup = models.CharField(verbose_name='用例数据初始化', max_length=128)
    Test_Teardown = models.CharField(verbose_name='用例数据清理', max_length=128)
    Test_Template = models.CharField(verbose_name='用例模版', max_length=128)
    Test_Timeout = models.CharField(verbose_name='超时时间', max_length=32)
    Force_Tags = models.CharField(verbose_name='项目标记', max_length=32)
    Default_Tags = models.CharField(verbose_name='套件标记', max_length=32)
    Library = models.CharField(verbose_name='引用库', max_length=128)
    Resource = models.CharField(verbose_name='引用资源', max_length=128)
    Variables = models.CharField(verbose_name='引用变量', max_length=128)
    Scalar_Variables = models.CharField(verbose_name='普通变量', max_length=128)
    List_Variables = models.CharField(verbose_name='列表变量', max_length=128)
    Dict_Variables = models.CharField(verbose_name='字典变量', max_length=128)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)
    sort = models.IntegerField(verbose_name='排序',null=True)
    def __str__(self):
        return self.suite_name

    class Meta:
        db_table = 'suite'
        unique_together = (("project", "suite_name"),)

class Keyword(models.Model):
    """
    资源表
    """
    id = models.BigAutoField(primary_key=True)
    resource = models.ForeignKey(to='Resource',null=False,on_delete=models.CASCADE)
    keyword_name = models.CharField(verbose_name='关键字名称', max_length=128,null=False)
    Documentation = models.TextField(verbose_name='关键字描述')
    Arguments = models.CharField(verbose_name='参数', max_length=512)
    Teardown = models.CharField(verbose_name='还原操作', max_length=128)
    Return_Value = models.CharField(verbose_name='返回结果', max_length=128)
    Timeout = models.CharField(verbose_name='超时时间', max_length=32)
    Tags = models.CharField(verbose_name='标识', max_length=128)
    Table_value = models.TextField(verbose_name='关键字内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)


    class Meta:
        db_table = 'keyword'
        unique_together = (("resource", "keyword_name"),)

class Testcase(models.Model):
    """
    资源表
    """
    id = models.BigAutoField(primary_key=True)
    suite = models.ForeignKey(to='Suite',null=False,on_delete=models.CASCADE)
    testcase_name = models.CharField(verbose_name='用例名称', max_length=32,null=False)
    Documentation = models.CharField(verbose_name='用例描述', max_length=255)
    Setup = models.CharField(verbose_name='初始化', max_length=128)
    Teardown = models.CharField(verbose_name='还原操作', max_length=128)
    Timeout = models.CharField(verbose_name='超时时间', max_length=32)
    Template = models.CharField(verbose_name='超时时间', max_length=32)
    Tags = models.CharField(verbose_name='标识', max_length=128)
    Table_value = models.TextField(verbose_name='用例内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)
    sort = models.IntegerField(verbose_name='排序',null=True)

    class Meta:
        db_table = 'testcase'
        unique_together = (("suite", "testcase_name"),)

class Library(models.Model):
    """
    库文件表
    """
    id = models.BigAutoField(primary_key=True)
    library_name = models.CharField(verbose_name='库名称', max_length=32,null=False)
    documentation = models.TextField(verbose_name='方法描述',null=True)
    class_name = models.CharField(verbose_name='类名称', max_length=128)
    filepath = models.CharField(verbose_name='文件相对路径', max_length=32)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)

    class Meta:
        db_table = 'library'

class Method(models.Model):
    """
    库方法表
    """
    id = models.BigAutoField(primary_key=True)
    library = models.ForeignKey(to='Library',null=False,on_delete=models.CASCADE)
    method_name = models.CharField(verbose_name='方法名称', max_length=128)
    documentation = models.TextField(verbose_name='方法描述',null=True)
    Arguments = models.CharField(verbose_name='参数', max_length=128)
    Return_Value = models.CharField(verbose_name='返回结果', max_length=128)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=False,null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)

    class Meta:
        db_table = 'method'

class Task(models.Model):
    """
    任务表
    """
    id = models.BigAutoField(primary_key=True)
    task_name = models.ForeignKey(to="Project",null=False,on_delete=models.DO_NOTHING)
    documentation = models.TextField(verbose_name='任务内容',null=False)
    status = models.CharField(verbose_name='任务状态', max_length=128)
    user = models.ForeignKey(to="UserInfo",null=False,on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(verbose_name='开始时间', auto_now_add=False,null=True)
    end_time = models.DateTimeField(verbose_name='结束时间', auto_now_add=False,null=True)
    take_time = models.CharField(verbose_name='耗时',max_length=128,null=True)
    report_path = models.CharField(verbose_name='详细报告',max_length=128,null=True)
    log_path = models.CharField(verbose_name='实时日志',max_length=128,null=True)#项目所在路径

    class Meta:
        db_table = 'task'

class Trigger(models.Model):
    """
    调度任务表
    """
    id = models.BigAutoField(primary_key=True)
    trigger_name = models.ForeignKey(to="Project",null=False,on_delete=models.DO_NOTHING)
    enable = models.BooleanField(verbose_name='调度状态', max_length=128)
    user = models.ForeignKey(to="UserInfo",null=False,on_delete=models.DO_NOTHING)
    Cron = models.CharField(verbose_name='时间调度',max_length=128,null=True)
    status = models.CharField(verbose_name='运行状态', max_length=128)

    class Meta:
        db_table = 'trigger'


class UserInfo(models.Model):
    """
    用户表
    """
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


    def __str__(self):
        return self.username
    class Meta:
        db_table = 'userinfo'

class Smtp(models.Model):
    """
    邮件配置表
    """
    id = models.BigAutoField(primary_key=True)
    project_name = models.ForeignKey(to="Project",null=False,on_delete=models.DO_NOTHING)
    mail_host = models.CharField(verbose_name='邮箱地址', max_length=64,null=False)
    mail_user = models.EmailField(verbose_name='发件人邮箱', max_length=32,null=False)
    mail_pass = models.CharField(verbose_name='邮箱授权码', max_length=64,null=False)
    receivers = models.TextField(verbose_name='收件人',null=False)
    cc = models.TextField(verbose_name='抄送人',null=True)
    enable = models.BooleanField(verbose_name='开关状态', max_length=32)
    title = models.TextField(verbose_name='邮件主题',null=False)
    documentation = models.TextField(verbose_name='邮件内容',null=False)
    user = models.ForeignKey(to="UserInfo",null=False,on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=False,null=True)

    class Meta:
        db_table = 'smtp'