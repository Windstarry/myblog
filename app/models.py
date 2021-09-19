#!/usr/bin/env python3.8
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2021/09/16 11:23:50
@Author  :   windstarry 
@Version :   1.0
'''
# here put the import lib
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


#关注者关联表
followers = db.Table(
	'followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
	)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    '''
    User 是关系的右侧实体（左侧是父类），由于这是一种自引用关系，必须在两边使用相同的类。
    secondary 配置用于这个关系的关联表，就是在这个类上定义的关联表 followers。
    primaryjoin指定了左侧实体（关注者）与关联表链接的条件。关系左侧的连接条件是与关联表中follower_id字段匹配的用户ID。follwer.c.follower_id表达式引用了关联表中follower_id列。
    secondaryjoin指定了右侧实体（被关注者）与关联表链接的条件。这个条件与primaryjoin类似，唯一不同的是：现在使用的followed_id，它是关联表中的另一个外键。
    backref定义如何右侧实体访问这个关系。从左侧开始，关系被名称为 followed，因此右侧将使用名称followers 来表示链接到右侧目标用户的所有左侧用户。附加lazy 参数表示这个查询的执行模式，设置为dynamic模式的查询在特定请求之前不会运行，这也是我们设置帖子的一对多关系。
    lazy类似于同名参数backref，但这个适用于左侧查询而不是右侧。
    '''
    followed = db.relationship(
                                'User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id==id),
                                secondaryjoin=(followers.c.followed_id==id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic'
                                )

    def __repr__(self):
		#return '<User {}>'.format(self.username)
        return '<User {}, Email {}, Password_Hash {}, Posts {}'.format(self.username, self.email, self.password_hash, self.posts)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://cravatar.cn/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)


    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)


    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0


    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #user_id字段已作为一个外键初始化了，这表明它引用了users表中的id值
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


