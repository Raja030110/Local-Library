from django.shortcuts import render,get_object_or_404,redirect
from .models import Genre, Book,BookInstance,Author
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from .forms import book_renew_form
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

# @permission_required('catalog.can_mark_returned')
# @permission_required('catalog.can_edit')
@login_required
def index(request):
    num_books=Book.objects.all().count()
    num_instance=BookInstance.objects.all().count()
    num_instance_available=BookInstance.objects.filter(status__exact='a').count()
    num_Author=Author.objects.all().count()
    num_genre=Genre.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context={'num_books':num_books,'num_instance':num_instance,'num_instance_available':num_instance_available,'num_Author':num_Author ,'num_genre':num_genre,'num_visits':num_visits}
    return render(request,'design/index.html',context=context)




class BookListView(LoginRequiredMixin,generic.ListView):

    model=Book
    template_name='design/book_list.html'

    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # redirect_field_name = '/accounts/login/'




class BookDetailView(generic.DetailView):
    model=Book
    template_name='design/book_details.html'
    context_object_name='book'

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'design/bookinstance_list_borrowed_user.html'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_date')

class LoanedBooksByAdminListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'design/mybooks.html'
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_date')


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    form=book_renew_form()

    if request.method == 'POST':


        form = book_renew_form(request.POST)


        if form.is_valid():

            book_instance.due_date = form.cleaned_data['renew_date']
            book_instance.save()


            return HttpResponseRedirect(reverse('all-borrowed'))


    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form =  book_renew_form(initial={'renew_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'design/renew.html', context)
