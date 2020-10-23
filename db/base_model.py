from django.db import models

class BaseModel(models.Model):
    '''
    模型抽象基类，作为其他模型类的父类
    '''
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True  #模型中的嵌套类，该属性表示：主类是抽象类，不在数据库中生成表，只是作为被继承的父类
        # db_table = "order"  该属性表示为主类命名 表名
        #ordering = '[order_date]' 该属性表示按照某个条件进行数据库排序，比较复杂 不深究。