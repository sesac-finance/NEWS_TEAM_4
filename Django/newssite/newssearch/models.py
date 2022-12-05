from django.db import models


class TbComment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    newsid = models.ForeignKey('TbNews', models.DO_NOTHING, db_column='NewsID')  # Field name made lowercase.
    userid = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    writedat = models.DateTimeField(db_column='WritedAt', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_comment'


class TbDomain(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_domain'


class TbNews(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    domainid = models.ForeignKey(TbDomain, models.DO_NOTHING, db_column='DomainID')  # Field name made lowercase.
    maincategory = models.CharField(db_column='MainCategory', max_length=16, blank=True, null=True)  # Field name made lowercase.
    subcategory = models.CharField(db_column='SubCategory', max_length=16, blank=True, null=True)  # Field name made lowercase.
    writedat = models.DateTimeField(db_column='WritedAt', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    photourl = models.TextField(db_column='PhotoURL', blank=True, null=True)  # Field name made lowercase.
    writer = models.CharField(db_column='Writer', max_length=16, blank=True, null=True)  # Field name made lowercase.
    stickers = models.TextField(db_column='Stickers', blank=True, null=True)  # Field name made lowercase.
    press = models.CharField(db_column='Press', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_news'


class TbUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    domainid = models.ForeignKey(TbDomain, models.DO_NOTHING, db_column='DomainID', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_user'
