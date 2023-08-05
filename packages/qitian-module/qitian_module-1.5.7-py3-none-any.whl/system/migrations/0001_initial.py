# Generated by Django 2.0.2 on 2018-10-22 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import system.utils.storage
import ueditor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='区域')),
            ],
            options={
                'verbose_name': '区域',
                'verbose_name_plural': '区域管理',
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='城市')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='站点名称')),
                ('domain', models.CharField(max_length=128, verbose_name='域名')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('status', models.BooleanField(choices=[(1, '启用'), (0, '禁用')], default=1, verbose_name='状态')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('site', models.ManyToManyField(blank=True, to='sites.Site', verbose_name='所属站点')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'db_table': 'sys_links',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='名称')),
                ('alias', models.CharField(blank=True, max_length=32, verbose_name='标签')),
                ('url', models.CharField(max_length=256, verbose_name='地址')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('status', models.IntegerField(choices=[(2, '隐藏'), (1, '显示')], default=1, verbose_name='状态')),
                ('sort', models.IntegerField(default=1, verbose_name='排序')),
                ('type', models.IntegerField(choices=[(3, '论坛'), (1, '店铺'), (2, '文章')], default=1, verbose_name='类别')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='system.Menu', verbose_name='上级菜单')),
                ('site', models.ManyToManyField(blank=True, to='sites.Site', verbose_name='所属站点')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单管理',
                'db_table': 'sys_menu',
            },
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='标题')),
                ('content', ueditor.models.UEditorField(blank=True, null=True, verbose_name='内容')),
                ('type', models.IntegerField(choices=[(1, '公告'), (2, '提醒'), (3, '消息')], verbose_name='类别')),
                ('target', models.IntegerField(blank=True, null=True, verbose_name='目标ID')),
                ('target_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='目标类型')),
                ('action', models.CharField(blank=True, max_length=32, null=True, verbose_name='动作类型')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '系统通知',
                'verbose_name_plural': '系统通知',
                'db_table': 'sys_notify',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='省份')),
                ('code', models.CharField(blank=True, max_length=32, verbose_name='代码')),
            ],
            options={
                'verbose_name': '省份',
                'verbose_name_plural': '省份管理',
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='SiteProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='站点标题')),
                ('sub_title', models.CharField(blank=True, max_length=128, verbose_name='副标题')),
                ('template', models.CharField(blank=True, max_length=64, verbose_name='模板名称')),
                ('slug', models.SlugField(help_text='图片、文件存储路径,为域名中间名称', max_length=64, verbose_name='简称别名')),
                ('meta_desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='关键词')),
                ('type', models.IntegerField(choices=[(1, '女性'), (2, '新闻'), (3, '企业')], default=1, verbose_name='站点类别')),
                ('logo', models.ImageField(blank=True, null=True, storage=system.utils.storage.ImageStorage(), upload_to='upload/sites', verbose_name='LOGO')),
                ('icon', models.ImageField(blank=True, null=True, storage=system.utils.storage.ImageStorage(), upload_to='upload/sites', verbose_name='ICON')),
                ('blocks', models.CharField(blank=True, help_text='使用英文,号分隔类别,:号后面为显示条数|分隔区块', max_length=255, null=True, verbose_name='模块设定')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='联系电话')),
                ('email', models.CharField(blank=True, max_length=64, verbose_name='Email')),
                ('qq', models.CharField(blank=True, max_length=64, verbose_name='QQ')),
                ('beian', models.CharField(blank=True, max_length=64, verbose_name='备案号')),
                ('baidu_verify', models.CharField(blank=True, max_length=64, verbose_name='百度验证')),
                ('tongji', models.TextField(blank=True, verbose_name='百度统计')),
                ('notice', models.TextField(blank=True, null=True, verbose_name='公告信息')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='system.City', verbose_name='所属城市')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.Site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '站点信息',
                'verbose_name_plural': '站点信息',
                'db_table': 'sys_site_property',
            },
        ),
        migrations.CreateModel(
            name='SmsCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=32, verbose_name='手机')),
                ('code', models.IntegerField(verbose_name='验证码')),
                ('used', models.BooleanField(default=False, verbose_name='是否验证')),
                ('ip', models.CharField(blank=True, max_length=32, verbose_name='IP')),
                ('user_agent', models.CharField(blank=True, max_length=255, verbose_name='User-Agent')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '验证码',
                'verbose_name_plural': '验证码管理',
                'db_table': 'sys_sms_code',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.IntegerField(verbose_name='目标ID')),
                ('target_type', models.CharField(max_length=32, verbose_name='目标类型')),
                ('action', models.CharField(blank=True, help_text='如: comment/like/post/update etc.', max_length=128, null=True, verbose_name='订阅动作')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '消息订阅',
                'verbose_name_plural': '消息订阅',
                'db_table': 'sys_subscription',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SubscriptionConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField(verbose_name='动作')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '订阅设置',
                'verbose_name_plural': '订阅设置',
                'db_table': 'sys_subscription_config',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserNotify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='已读')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('notify', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='system.Notify', verbose_name='通知')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户通知',
                'verbose_name_plural': '用户通知',
                'db_table': 'sys_user_notify',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VisitLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=128, verbose_name='访问页面')),
                ('ip', models.CharField(blank=True, max_length=32, verbose_name='IP')),
                ('user_agent', models.CharField(max_length=255, verbose_name='User-Agent')),
                ('plant_form', models.CharField(blank=True, max_length=255, verbose_name='用户终端')),
                ('referrer', models.CharField(blank=True, max_length=255, verbose_name='来源网站')),
                ('passport', models.CharField(blank=True, max_length=32, verbose_name='用户身份')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '访问记录',
                'verbose_name_plural': '访问记录',
                'db_table': 'sys_visit_log',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Province', verbose_name='所属省份'),
        ),
        migrations.AddField(
            model_name='area',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.City'),
        ),
    ]
