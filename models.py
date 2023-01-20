from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
import datetime

class Genre(models.Model):

    name=models.CharField(max_length=200,help_text='enter the Genre (e.g science fiction etc..)')

    def __str__(self):
        return self.name
class Book(models.Model):
    title=models.CharField(max_length=300)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    isbn=models.CharField('ISBN',max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre=models.ManyToManyField(Genre,help_text='select the genre for this book')
    language=models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-details',arg=[str(self.id)])
class BookInstance(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    book=models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint=models.CharField(max_length=200)
    due_date=models.DateField(null=True,blank=True)
    loan_status=(('m','Maintance'),('o','on_loan'),('a','Available'),('r','Reserved'),)
    status=models.CharField(max_length=1,choices=loan_status,blank=True,default='m',help_text='book Available')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_date and datetime.date.today() > self.due_date)

    class Meta:
        ordering=['due_date']
        permissions = (("can_mark_returned", "Set book as returned"),)
    def __str__(self):
        return f'{self.id}({self.book.title})'

class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_birth=models.DateField(blank=True,null=True)
    date_death=models.DateField(null=True,blank=True)

    class Meta:
        ordering=['last_name','first_name']
    def get_absolute_url(self):
        return reverse('author-details',arg=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'
class Language(models.Model):

    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):

        return self.name

class renewal_request(models.Model):
    date_today=datetime.date.today()+datetime.timedelta(weeks=3)
    applicate_name=models.CharField(max_length=200)
    apply_date=models.DateField(auto_now_add=True)
    id=models.UUIDField(primary_key=True,blank=True)
    renewdate=models.DateField(null=False,blank=False,default=date_today)

    def __str__(self):
        return self.applicate_name

    class Meta:
        ordering=['apply_date']
