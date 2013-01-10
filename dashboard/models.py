from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime

class Project(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    description = models.TextField(_(u'description'))
    is_archived = models.BooleanField(_(u'archived?'), default=False)
    creator = models.ForeignKey(User, related_name="project_creator")
    creation_date = models.DateField(_(u'creation_date'))
    admins = models.ManyToManyField(User, related_name='admins', blank=True, null=True,)
    contribs = models.ManyToManyField(User, related_name='contribs', blank=True, null=True,)
    readers = models.ManyToManyField(User, related_name='readers', blank=True, null=True,)

    def __unicode__(self):
        return u'Project %d : %s' % (self.id, self.name)


class UseCase(models.Model):
	title = models.CharField(_(u'title'), max_length=255)
	creation_date = models.DateField(_(u'creation_date'))
	description = models.TextField(_(u'description'))
	estimation_days = models.IntegerField(_(u'estimationInDays'))
	DIFF_CHOICES = (('1','1'),('2','2'),('3','3'),('5','5'),('8','8'),('13','13'))
	difficulty = models.CharField(_(u'difficulty'), max_length=2, choices=DIFF_CHOICES, default="1")
	TYPE_CHOICES = (('Functional','Functional'),('Technical','Technical'),('Other','Other'))
	typeCase = models.CharField(_(u'Type'), max_length=10, choices=TYPE_CHOICES, default='Technical')
	STATUS_CHOICES = (('new','new'),('accepted','accepted'),('rejected','rejected'),('realized','realized'),('delivered','delivered'))
	status = models.CharField(_(u'status'), max_length=8, choices=STATUS_CHOICES, default="new")
	created_by = models.ForeignKey(User, related_name="creator")

	def __unicode__(self):
		return u'UseCase %d : %s' % (self.id, self.title)

class Milestone(models.Model):
	version = models.CharField(_(u'version'), max_length=25)
	project = models.ForeignKey(Project, related_name="projectId")
	usecases = models.ManyToManyField(UseCase, related_name="usecases", blank=True, null=True,)

	def __unicode__(self):
		return u'Milestone %d : %s' % (self.id, self.version)

class Task(models.Model):
	title = models.CharField(_(u'title'), max_length=255)
	creation_date = models.DateField(_(u'creation_date'))
	description = models.TextField(_(u'description'))
	estimation_days = models.IntegerField(_(u'estimationInDays'), default=0)
	date_start = models.DateTimeField(_(u'Date start'), blank=True, null=True,)
	date_end = models.DateTimeField(_(u'Date end'), blank=True, null=True,)
	assigned_to = models.ForeignKey(User, related_name="assigned_to", blank=True, null=True,)
	use_case = models.ForeignKey(UseCase, related_name="use_case")
	created_by = models.ForeignKey(User, related_name="created_by")
	STAT_CHOICES = (('new','new'),('accepted','accepted'),('in progress','in progress'),('rejected','rejected'),('fixed','fixed'),('closed','closed'))
	status = models.CharField(_(u'status'), max_length=11, choices=STAT_CHOICES, default="new")
	TYPE_TASK_CHOICES = (('feature','feature'),('bug','bug'),('evolution','evolution'),('test','test'),('conception','conception'),('request','request'),('42','42'))
	typeTask = models.CharField(_(u'type'), max_length=10, choices=TYPE_TASK_CHOICES, default="feature")

class Room(models.Model):
	title = models.CharField(_(u'title'), max_length=255)
	creator = models.ForeignKey(User, related_name='room_creator', blank=True, null=True)
	created = models.DateTimeField(default=datetime.now())
	project = models.ForeignKey(Project, related_name="project_room")
	connected = []

	def add_message(self, atype, sender, message=None):
		m = Message(room=self, type=atype, author=sender, message=message)
		m.save()
		return m

	def say(self, sender, message):
		return self.add_message('m', sender, message)

	def join(self, user):
		self.connected.append(user)
		return self.add_message('j', user)

	def leave(self, user):
		self.connected.remove(user)
		return self.add_message('l', user)

	def messages(self, after_pk=None, after_date=None):
		m = Message.objects.filter(room=self)
		if after_pk:
			m = m.filter(pk__gt=after_pk)
		if after_date:
			m = m.filter(timestamp__gte=after_date)
		return m.order_by('pk')

	def nbmessages(self):
		m = Message.objects.filter(room=self)
		return len(m)

	def last_message_id(self):
		m = Message.objects.filter(room=self).order_by('pk')
		if m:
			return m[0].id
		else:
			return 0

	def list_connected(self):
		return self.connected

	def __unicode__(self):
		return 'Chat for %d %s' % (self.id, self.title)

MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)

class Message(models.Model):
    '''A message that belongs to a chat room'''
    room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    author = models.ForeignKey(User, related_name='message_author', blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        '''Each message type has a special representation, return that representation.
        This will also be translator AKA i18l friendly.'''
        if self.type == 's':
            return u'SYSTEM: %s' % self.message
        if self.type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.type == 'j':
            return 'JOIN: %s' % self.author
        elif self.type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message


class News(models.Model):
	author = models.ForeignKey(User, related_name='author')
	date = models.DateTimeField(_(u'date'), auto_now=True)
	title = models.CharField(_(u'title'), max_length=255)
	content = models.TextField(_(u'content'))
	project = models.ForeignKey(Project, related_name="project_news")

class Event(models.Model):
	title = models.CharField(_(u'title'), max_length=255)
	date_start = models.DateTimeField(_(u'Date start'), blank=True, null=True,)
	date_end = models.DateTimeField(_(u'Date end'), blank=True, null=True,)
	color = models.CharField(_(u'color'), max_length=17) #the name like 'yellow'
	all_day = models.BooleanField(_(u'all day'))
	project = models.ForeignKey(Project, related_name="project_event")

class Page(models.Model):
	name = models.CharField(_(u'name'), max_length=255)
	date = models.DateTimeField(_(u'date'), auto_now=True)
	content = models.TextField(_(u'content'))
	creator = models.ForeignKey(User, related_name='page_creator', blank=True, null=True)
	project = models.ForeignKey(Project, related_name="project_page")
