from peewee import *
from base64 import b64encode
import datetime
import flask_security
import flask_admin as admin
from flask_admin.contrib.peewee import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user,AnonymousUserMixin
from playhouse.postgres_ext import PostgresqlExtDatabase
from cfg import *
import os
db = SqliteDatabase('posts.db',check_same_thread=False)





if 'HEROKU' in os.environ:
    DEBUG = False
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    pg_db = PostgresqlDatabase(url.path[1:], user=url.username, password=url.password,
                           host=url.hostname, port=url.port)  
    '''
    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': url.path[1:],
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
    	}
    '''
else:
    DEBUG = True
    pg_db = PostgresqlDatabase('imgin_dev', user=pguser, password=postgrespw,
                           host='localhost', port=5432)





def initialize_db():
	pg_db.connect()
	pg_db.create_tables([Post,Reply,User,UserInfo,ObjectCount,UserLink,UserBlock],safe=True)



class BaseModel(Model):
    class Meta:
        #database = db
        database = pg_db

class User(UserMixin,BaseModel):
	id = CharField(primary_key=True)
	tagname = CharField(max_length=80,null=False,default='')
	username = CharField(max_length=80,null=False,default='')
	email = CharField(max_length=120,null=False,default='',unique=True)
	is_admin = BooleanField(default=False)
	is_master = BooleanField(default=False)
	password = CharField(null = False,default='')
	nsfwfilter = BooleanField(default=False)
	reset_token = CharField(default='')
	last_reset = DateTimeField(default = datetime.datetime.now)

	def set_nsfw(self,bool):
		if bool == True:
			self.nsfwfilter = True
		else:
			self.nsfwfilter = False

	def reset_update(self,new_reset_token,new_reset):
		self.reset_token = new_reset_token
		self.last_reset = new_reset

	def __unicode__(self):
		return self.username


class Anonymous(AnonymousUserMixin):
	def __init__(self):
		self.username = 'Anonymous'
		self.nsfwfilter = True
	def set_nsfw(self,bool):
		if bool == True:
			self.nsfwfilter = True
		else:
			self.nsfwfilter = False


class UserInfo(BaseModel):
    key = CharField(max_length=64)
    value = CharField(max_length=64)

    user = ForeignKeyField(User)

    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)

class ObjectCount(BaseModel):
	selfidentifier = CharField()
	postcount = IntegerField(default=1)
	usercount = IntegerField(default=3)


class UserLink(BaseModel):
	following = ForeignKeyField(User, backref='related_to')
	follower = ForeignKeyField(User,backref='relationships')
	class Meta:
		indexes = (
			# Specify a unique multi-column index on from/to-user.
			(('follower', 'following'), True),
		)


class UserBlock(BaseModel):
	blocking = ForeignKeyField(User, backref='block_to')
	blocker = ForeignKeyField(User,backref='blockships')
	class Meta:
		indexes = (
			# Specify a unique multi-column index on from/to-user.
			(('blocker', 'blocking'), True),
		)



class Post(BaseModel):
	id = PrimaryKeyField()
	date = DateTimeField(default = datetime.datetime.now)
	title = CharField()
	text = TextField()
	image = TextField()
	user = ForeignKeyField(User)
	last_reply = DateTimeField(default = datetime.datetime.now)
	nsfw = BooleanField(default= False)
	eternal = BooleanField(default= False)
	replies = IntegerField(default=0)

class Reply(BaseModel):
	id = PrimaryKeyField()
	date = DateTimeField(default = datetime.datetime.now)
	text = TextField()
	post = ForeignKeyField(Post, backref='replies')
	image = TextField()
	user = ForeignKeyField(User)
	nsfw = BooleanField(default = False)



class UserAdmin(ModelView):
	#inline_models = (UserInfo)
	def is_accessible(self):
		column_sortable_list = [('id', User.id), ('tagname', User.tagname), ('email',User.email)]
		if current_user.is_master:
			return current_user.is_authenticated
		else:
			return False


class UserLinkAdmin(ModelView):
	#inline_models = (UserInfo)
	def is_accessible(self):
		if current_user.is_master:
			return current_user.is_authenticated
		else:
			return False

class BlockAdmin(ModelView):
	#inline_models = (UserInfo)
	def is_accessible(self):
		if current_user.is_master:
			return current_user.is_authenticated
		else:
			return False


class ObjectCountAdmin(ModelView):
	#inline_models = (UserInfo)
	def is_accessible(self):
		if current_user.is_master:
			return current_user.is_authenticated
		else:
			return False


class PostAdmin(ModelView):
	def is_accessible(self):
		if current_user.is_master:
			return current_user.is_authenticated
		else:
			return False
