from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    description = models.TextField(_(u'description'))
    is_archived = models.BooleanField(_(u'archived?'))
    creator = models.ForeignKey(User, related_name="creator")
    creation_date = models.DateField(_(u'creation_date'))
    admins = models.ManyToManyField(User, related_name='admins')
    contribs = models.ManyToManyField(User, related_name='contribs')
    readers = models.ManyToManyField(User, related_name='readers')

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
	usecases = models.ManyToManyField(UseCase, related_name="usecases")

	def __unicode__(self):
		return u'Milestone %d : %s' % (self.id, self.version)

class Task(models.Model):
	title = models.CharField(_(u'title'), max_length=255)
	creation_date = models.DateField(_(u'creation_date'))
	description = models.TextField(_(u'description'))
	estimation_days = models.IntegerField(_(u'estimationInDays'))
	date_start = models.DateTimeField(_(u'Date start'))
	date_end = models.DateTimeField(_(u'Date end'))
	assigned_to = models.ForeignKey(User, related_name="assigned_to")
	use_case = models.ForeignKey(UseCase, related_name="use_case")
	created_by = models.ForeignKey(User, related_name="created_by")
	STAT_CHOICES = (('new','new'),('accepted','accepted'),('in progress','in progress'),('rejected','rejected'),('fixed','fixed'),('closed','closed'))
	status = models.CharField(_(u'status'), max_length=11, choices=STAT_CHOICES, default="new")
	TYPE_TASK_CHOICES = (('feature','feature'),('bug','bug'),('evolution','evolution'),('test','test'),('conception','conception'),('request','request'),('42','42'))
	typeTask = models.CharField(_(u'type'), max_length=10, choices=TYPE_TASK_CHOICES, default="feature")
	




