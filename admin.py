from django.contrib import admin
from .models import *
def display_genre(self):

    return ', '.join(genre.name for genre in self.genre.all()[:3])

    # display_genre.short_description = 'Genre'
class bookadmininline(admin.TabularInline):
    model=BookInstance
class bookadmin(admin.ModelAdmin):
    list_display=('title','author',display_genre)
    inlines=[bookadmininline]


class bookinstanceadmin(admin.ModelAdmin):
    list_display=('book','id','status','due_date')
    list_filter=('status','due_date')
    fieldsets=((None,{'fields':('book','id','borrower')}),('AVAILABLITY',{'fields':('status','due_date')}),)
class bookinline(admin.TabularInline):
    model=Book
class Authoradmin(admin.ModelAdmin):
    list_display=('first_name','last_name','date_birth')
    inlines=[bookinline]






admin.site.register(Genre)
admin.site.register(Book,bookadmin)
admin.site.register(BookInstance,bookinstanceadmin)
admin.site.register(Author,Authoradmin)
admin.site.register(Language)
admin.site.register(renewal_request)



# Register your models here.
