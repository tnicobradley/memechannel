from flask import Flask, render_template, request, redirect, url_for, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import logging
from models import *
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
import string
import os
from cfg import *
import random
from werkzeug.utils import secure_filename
from hashlib import sha256
import datetime
from flask_mail import Mail, Message
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = serpassword
#app.config['SQLALCHEMY_DATABASE_URI']
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
patch_request_class(app, 5 * 1024 * 1024)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = imageDest
configure_uploads(app, photos)
mail = Mail(app)
app.config.from_pyfile('config.cfg')


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.mail.yahoo.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USE_TLS=False,
	MAIL_USERNAME = un,
	MAIL_PASSWORD = mailpw
	)

mail=Mail(app)



@app.route("/passwordresetcode/")
def passwordresetcode():
	if current_user.is_active and current_user.email != '':
		timenow = datetime.datetime.now()
		hashstring = current_user.password + str(timenow) + str(random.randint(0,1000))

		bytestring = bytes(hashstring, "utf-8")
		hashcode = hashpass(bytestring)
		randint = random.randint(0,4)
		sentcode = hashcode[randint:randint+5]
		bytestring = bytes(sentcode, "utf-8")
		newcode = resetcode(bytestring)
		print('\n')
		print('newcode: ', newcode)
		print('\n')
		#current_user.reset_update(newcode,datetime.datetime.now())
		tokenupdate = User.update(reset_token = newcode).where(User.id == current_user.id)
		tokenupdate.execute()
		tokentimeupdate = User.update(last_reset = datetime.datetime.now()).where(User.id == current_user.id)
		tokentimeupdate.execute()
		msg = Message(
			'imgin PASSWORD RESET',
		sender=un,
		recipients=
			[current_user.email])
		msg.body = "\n Password Reset for: " + current_user.username + "\n Your Password reset Code is: " + sentcode
		mail.send(msg)
		return(redirect(url_for('resetpassword')))
	else:
		return "You Do Not have an Email on your profile\n \n Email required to reset password!"

@app.route("/resetpassword/",methods=['GET', 'POST'])
def resetpassword():
	error = None
	if current_user.is_active == False:
		return redirect(url_for('home'))
	if request.method == 'POST':
		formtoken = request.form['formtoken']
		formpass = request.form['password']
		formpass2 = request.form['password2']
		if formpass != formpass2:
			error = 'Passwords Do Not Match'
		else:
			decode = bytes(formtoken,"utf-8")
			decoded = resetcode(decode)
			user = User.get(User.username == current_user.username)
			if decoded == user.reset_token:	#checks the code
				newpassword = bytes(formpass,"utf-8")
				hashedPW = hashpass(newpassword)
				passwordupdate = User.update(password = hashedPW).where(User.id == current_user.id)
				passwordupdate.execute()
				#return redirect(url_for('home'))
				return 'Password Updated'
			else:
				error = 'Incorrect or Expired Reset Code'
	return render_template('resetpassword.html', error=error)


@app.route("/resetsuccess/")
def resetsuccess():
	pass


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

login = LoginManager(app)
login.anonymous_user = Anonymous
def random_filename(size=10, chars=string.ascii_uppercase + string.digits):
	newname = ''.join(random.choice(chars) for _ in range(size))
	newname = newname+'.'
	return newname


def user_count():
	counter = ObjectCount.update(usercount = ObjectCount.usercount + 1).where(ObjectCount.selfidentifier == 'counter')
	counter.execute()
	counter = ObjectCount.get(ObjectCount.selfidentifier == 'counter')
	return str(counter.usercount)


def post_count():
	counter = ObjectCount.update(postcount = ObjectCount.postcount + 1).where(ObjectCount.selfidentifier == 'counter')
	counter.execute()
	counter = ObjectCount.get(ObjectCount.selfidentifier == 'counter')
	return counter.postcount


def follow_check(a_user,b_user):
	
	users_followed = (User
 					.select()
 					.join(UserLink, on=UserLink.following)
 					.where(UserLink.follower == b_user))
	for user in users_followed:
		if user.username == a_user.username:
			return True
	return False

app.jinja_env.globals.update(follow_check=follow_check)



#checks if b_user is blocking a_user
def block_check(a_user,b_user):
	
	users_blocked = (User
 					.select()
 					.join(UserBlock, on=UserBlock.blocking)
 					.where(UserBlock.blocker == b_user))
	for user in users_blocked:
		if user.username == a_user.username:
			return True
	return False

app.jinja_env.globals.update(block_check=block_check)


def nsfw_check(a_post,filtersetting):

	if a_post.nsfw == True and filtersetting == True:
		return True
	else: 
		return False

app.jinja_env.globals.update(nsfw_check=nsfw_check)

def nsfwFilter_check(filterbool):
	if filterbool == True:
		return True
	else:
		return False

app.jinja_env.globals.update(nsfwFilter_check=nsfwFilter_check)


def redirect_timer(count):
	while count > 0:
		time.sleep(1)
		count -= 1
	return count

app.jinja_env.globals.update(redirect_timer=redirect_timer)


@login.user_loader
def load_user(user_id):
	return User.get(User.id == user_id)   #USER MUST EXIST IN TABLE OR CRASH



def resetcode(rawstring):
	hashed = sha256(rawstring).hexdigest()
	code = hashed[4:9]
	return code

def hashpass(rawpass):
	hashed = sha256(rawpass).hexdigest()
	return hashed


try:
	User.create_table()
	UserInfo.create_table()
	Post.create_table()
except:
	pass
admin = Admin(app, name='imgin')
admin.add_view(PostAdmin(Post))
admin.add_view(UserAdmin(User))
admin.add_view(ObjectCountAdmin(ObjectCount))
admin.add_view(UserLinkAdmin(UserLink))
admin.add_view(BlockAdmin(UserBlock))





@app.before_request
def before_request():
	initialize_db()

@app.teardown_request
def teardown_request(exception):
	db.close()


def delete_image(filename):
	if filename != 'nothing.png':
		file_path = photos.path(filename)
		os.remove(file_path)
	return


@app.route('/', methods=['POST','GET'])
def home():
	prune_seconds = 3600
	posts = Post.select()
	replies = Reply.select()
	for post in posts:
		if post.eternal == False:
			time_on = datetime.datetime.now() - post.last_reply
			if post.replies == 0 and time_on.total_seconds() >= prune_seconds:
				delete_image(post.image)
				post.delete_instance()
			else:
				for reply in replies:
					if reply.post == post:
						if time_on.total_seconds() >= prune_seconds:
							delete_image(post.image)
							if reply.image != 'None':
								delete_image(reply.image)
							post.delete_instance()
							reply.delete_instance()
	check = request.form.get('sort')
	nsfw_filter = request.form.get('nsfwFilter')
	#if current_user.is_active:
	if nsfw_filter == 'True':
		current_user.set_nsfw(True)
	else:
		current_user.set_nsfw(False)

	if check == None:
		check = 'newest'
	if current_user.is_active:
		if check == 'newest':
			return render_template('home.html',posts=Post.select().order_by(Post.date.desc()),
				replies=Reply.select())
		elif check == 'bumped':
			return render_template('home.html',posts=Post.select().order_by(Post.last_reply.desc()),
				replies=Reply.select())
		elif check == 'following':
			return render_template('homefollowing.html',posts=Post.select().order_by(Post.date.desc()),
				replies=Reply.select())
	else:
		return render_template('homeout.html',posts=Post.select().order_by(Post.date.desc()),
			replies=Reply.select())


@app.route('/img/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],
                               filename)

@app.route('/initdb/')
def initdb():
	#user = User.create(id='1',username='Ricky',email='fuckoff.com',password='fuckoff',is_admin='yes')
	bytestring = bytes('fuckoff', "utf-8")
	user = User.create(id='1',tagname='MITHRANDIR',username='Mithrandir',email='greatestwizard@middleearth.com',password=hashpass(bytestring),is_admin=True,is_master=True) #create master/admin
	user2 = User.create(id='2',tagname='FEANOR',username='Fëanor',email='muhsilmarils@valinor.com',password=hashpass(bytestring),is_admin=True,is_master=True) #create master/admin
	user3 = User.create(id='3',tagname='DICK',username='Dick',email='blah@blah.com',password=hashpass(bytestring),is_admin=True,is_master=True) #create master/admin
	ObjectCount.create(selfidentifier = 'counter')  #creates the counter //rigged right now
	UserLink.create(following=user,follower=user2)
	UserLink.create(following=user2,follower=user)
	UserBlock.create(blocking=user,blocker=user3)
	UserBlock.create(blocking=user3,blocker=user)
	post1 = Post.create(title='One Post To Rule Them All',text='One post to find them \n one post to bring them all \n and in the darkness bind them\n in the land of imgin where the shadows lie.',image='onering.jpg',user=user,eternal=True)
	#user = User.get(User.id == '2')
	login_user(user)

	return 'Logged In'


# Route for handling the login page logic
@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	if current_user.is_active:
		return redirect(url_for('home'))
	if request.method == 'POST':
		formname = request.form['username']
		formname = formname.upper()
		query = User.select().where(User.tagname == formname)
		if query.exists():
			user = User.get(User.tagname == formname)
			bytestring = bytes(request.form['password'], "utf-8")
			if hashpass(bytestring) == user.password:
				login_user(user)
				return redirect(url_for('home'))
			else:
				error = 'Incorrect Password'
		else:
			error = 'Username Incorrect'  
	return render_template('login.html', error=error)




@app.route('/user/')
@app.route('/user/<username>')
def userpage(username):

	query = User.select().where(User.username == username)
	if query.exists():
		user_tocheck = User.get(User.username == username)
		if user_tocheck == current_user:
			if user_tocheck == current_user:
				return render_template('userpageself.html',user=user_tocheck,
								posts=Post.select().where(Post.user == user_tocheck).order_by(Post.date.desc())   )
		elif (block_check(user_tocheck,current_user) or block_check(current_user,user_tocheck))and current_user.is_active:
			return redirect(url_for('home'))
		elif follow_check(user_tocheck,current_user) and current_user.is_active:
			return render_template('userpagefollowing.html',user=user_tocheck,
								posts=Post.select().where(Post.user == user_tocheck).order_by(Post.date.desc())   )
		elif current_user.is_active:
			return render_template('userpage.html',user=user_tocheck,
								posts=Post.select().where(Post.user == user_tocheck).order_by(Post.date.desc())   )
		else:
			return render_template('userpageout.html',user=user_tocheck,
								posts=Post.select().where(Post.user == user_tocheck).order_by(Post.date.desc())   )
	else:
		return 'User Non-existant'


@app.route('/settings/')
def settings():
	pass





@app.route('/follow/')
@app.route('/follow/<username>')
def follow(username):
	url = '/user/' + username
	query = User.select().where(User.username == username)
	if query.exists() == False:
		return redirect(url_for('home'))
	to_follow = User.get(User.username == username)
	if block_check(to_follow,current_user) or block_check(current_user,to_follow):
		return redirect(url_for('home'))
	if follow_check(to_follow,current_user):
		return redirect(url)

	UserLink.create(follower=current_user,following=to_follow)
	return redirect(url)


@app.route('/block/')
@app.route('/block/<username>')
def block(username):
	url = '/user/' + username
	query = User.select().where(User.username == username)
	if query.exists() == False:
		return redirect(url_for('home'))
	to_block = User.get(User.username == username)
	if block_check(to_block,current_user):
		return redirect(url)
	if follow_check(to_block,current_user):
		users_links = (UserLink
 			.select()
 			.join(User, on=UserLink.following)
 			.where(UserLink.follower == current_user))
		for user in users_links:
			if user.following == to_block:
				user.delete_instance()

	if follow_check(current_user,to_block):
		user_links = (UserLink
 			.select()
 			.join(User, on=UserLink.following)
 			.where(UserLink.follower == to_block))
		for user in users_links:
			if user.following == current_user:
				user.delete_instance()
	UserBlock.create(blocker=current_user,blocking=to_block)
	return redirect(url)	


@app.route('/register/', methods=['GET','POST'])
def register():
	if current_user.is_active:
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':
		formname = request.form['username']
		emailAdr = request.form['email']
		tagname = formname.upper()
		if emailAdr == '':
			emailAdr = 'None'
		emailAdr = emailAdr.upper()
		query = User.select().where(User.tagname == tagname)
		query2 = User.select().where(User.email == emailAdr)
		print('HERE+++++++++++++++++++++++++++++++++++++++++++\n')
		print('emailAdr: ',emailAdr)
		print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
		if query.exists():
			error = 'Username Taken!'
		elif (('@' not in emailAdr) or ('.' not in emailAdr)) and (emailAdr != 'NONE'):
			error = 'Enter a Valid Email Address'
		elif query2.exists() and emailAdr != 'NONE':
			error = 'Email Already Registered!'	
		else: 
			if request.form['password'] != request.form['passwordcheck']:
				error = 'Password Fields Do Not Match!'
			elif len(request.form['password']) < 6:
				error = 'Required Password length: 6 characters'
			else:
				seed = str(datetime.datetime.now()) + str(random.randint(0,9999))
				emailbyte = bytes(seed, 'utf-8')
				emailAdr = hashpass(emailbyte)
				emailAdr = emailAdr[0:10]
				bytestring = bytes(request.form['password'], "utf-8")
				hashedpass = hashpass(bytestring)
				madetime = datetime.datetime.now()
				strtime = str(madetime)
				bytestring = bytestring + bytes(strtime,"utf-8")
				resetkey = resetcode(bytestring)
				user = User.create(tagname=tagname,username=formname,email=emailAdr,password=hashedpass,id=user_count(),reset_token=resetkey,last_reset=madetime)
				login_user(user)
				return redirect(url_for('home'))
	return render_template('register.html', error=error)


@app.route('/logout/')
def logout():
	logout_user()
	return redirect(url_for('home'))



@app.route('/deletethread/<postID>/')
@app.route('/deletethread/')
def deletethread(postID):
	query = Post.select().where(Post.id == postID)
	if query.exists():
		post = Post.get(Post.id == postID)
		if post.replies > 0:
			replies = Reply.select().where(Reply.post == postID)
			for reply in replies:
				if reply.image != 'None':
					delete_image(reply.image)
				reply.delete_instance()
		delete_image(post.image)
		post.delete_instance()
		return(redirect(url_for('home')))
	else:
		return(redirect(url_for('home')))


@app.route('/deletereply/<replyID>/')
@app.route('/deletereply/')
def deletereply(replyID):
	
	query2 = Reply.select().where(Reply.id == replyID)
	if query2.exists():
		query2.execute()
		reply = query2[0]
		postID = reply.post
		query = Post.select().where(Post.id == reply.post)
		if query.exists():
			post = Post.get(Post.id == postID)
			newcount = post.replies - 1
			reply_count_update = Post.update(replies = newcount).where(Post.id == postID)
			reply_count_update.execute()
			if reply.image != 'None':
				delete_image(reply.image)
			reply.delete_instance()
		return(redirect(url_for('thread',postID=postID)))
	else:
		return(redirect(url_for('home')))



@app.route('/thread/<postID>')
@app.route('/thread/')
def thread(postID):
	prune_seconds = 3600
	query = Post.select().where(Post.id == postID)
	if query.exists():
		thispost = Post.get(Post.id == postID)
		thisreplies = Reply.select().where(Reply.post == postID)
		if thispost.eternal == False:
			time_on = datetime.datetime.now() - thispost.last_reply
			if thispost.replies == 0 and time_on.total_seconds() >= prune_seconds:
					return(redirect(url_for('home')))
			else:
				for reply in thisreplies:
					if reply.post == thispost:
						if time_on.total_seconds() >= prune_seconds:
							return(redirect(url_for('home')))
	else:
		return(redirect(url_for('home')))
	replies = (Reply
          .select(Reply, Post)
          .join(Post)
          .order_by(Reply.date))

	

	if current_user.is_active:
		return render_template('thread.html',posts=Post.select().where(Post.id == postID),replies=Reply.select().where(Reply.post == postID))
	else:
		return render_template('threadout.html',posts=Post.select().where(Post.id == postID),replies=Reply.select().where(Reply.post == postID))



@app.route('/create/',methods=['POST'])
def create_post():
	if request.method == 'POST' and 'image' in request.files:
		randname = random_filename()
		filename = photos.save(request.files['image'],name=randname)
		if request.form.getlist('nsfw'):
			nsfwbool = True
		else:
			nsfwbool = False
		newpost = Post.create(
			title=request.form['title'],
			text=request.form['text'],
			image=filename,
			user=current_user,
			nsfw=nsfwbool

		)
	elif request.method == 'POST' and 'image' not in request.files:
           flash('Image Required...')
	return redirect(url_for('home'))


@app.route('/bumplimit/<postID>/')
@app.route('/bumplimit/')
def bumplimit(postID):
	return render_template('bumplimit.html',postID=postID)
	


@app.route('/thread/<postID>/reply/',methods=['POST'])
@app.route('/reply/',methods=['POST'])
def create_reply(postID):
	prune_seconds = 3600
	#this *************************************** block makes sure the post exists
	thispost = Post.get(Post.id == postID)
	thisreplies = Reply.select().where(Reply.post == postID)
	if thispost.eternal == False:
		time_on = datetime.datetime.now() - thispost.last_reply
		if thispost.replies == 0 and time_on.total_seconds() >= prune_seconds:
				return(redirect(url_for('home')))
		else:
			for reply in thisreplies:
				if reply.post == thispost:
					if time_on.total_seconds() >= prune_seconds:
						return(redirect(url_for('home')))
	#**************************************************** If not it redirects to home
	query = Post.select().where(Post.id == postID)
	if query.exists():
		thepost = query.execute()
		if thepost[0].replies > 149:
			time = datetime.datetime.now()
			return(redirect(url_for('bumplimit',postID=postID)))
	if request.method == 'POST' and 'image' in request.files:
		filename = photos.save(request.files['image'],name=random_filename())
		posttext = request.form['text']
		new_reply = Reply.create(
			text=request.form['text'],
			image=filename,
			post=postID,
			user=current_user,

		)
	elif request.method == 'POST' and 'image' not in request.files:
		new_reply = Reply.create(
			text=request.form['text'],
			image='None',
			post=postID,
			user=current_user

		)
	newcount = new_reply.post.replies + 1
	reply_count_update = Post.update(replies = newcount).where(Post.id == new_reply.post)
	reply_count_update.execute()
	reply_update = Post.update(last_reply = new_reply.date).where(Post.id == new_reply.post)
	reply_update.execute()
	return redirect(url_for('thread',postID=postID))



if __name__ == '__main__':
	#admin.add_view(UserAdmin(User))
	#admin.add_view(PostAdmin(Post))
	#admin.add_view(ModelView(Post, db.session))




	app.run(debug=True) #host='192.168.1.119' goes in app.run()