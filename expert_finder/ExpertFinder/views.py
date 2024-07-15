from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import expertise, CartItems, Profile
from .filters import expertiseFilter
import random, requests


def home(request):

    expertisecategory = expertise.objects.values('category').distinct()

    context={
        #fetch data from database in homecategorydata
        'homecategorydata': expertise.objects.all(),
        'expertisecategory': expertisecategory
    }
    return render(request, 'ExpertFinder/index.html', context)

# used to show product category wise (home page to category detail)
def filtercategory(request):
    cat = request.GET['cat']
    filteredcategories = expertise.objects.filter(category__icontains=cat)
    params = {'filteredcategories': filteredcategories, 'cat':cat}
    if len(cat)>0:
        return render(request, 'ExpertFinder/category_list.html', params)

def search(request):

    if request.user.is_authenticated:
        user_city = request.user.profile.city
    query = request.GET['query']
    city = request.GET['city']

    if len(query) > 77 or len(city)> 77:
        allExpertise = expertise.objects.none()

    if len(query)>0 and len(query)<78 and len(city)>0 and len(city)<78:
        allExpertiseLocation = expertise.objects.filter(location__icontains=city)
        allExpertiseTitle = allExpertiseLocation.filter(title__icontains=query)
        allExpertiseTags = allExpertiseLocation.filter(tags__icontains=query)
        allExpertise = allExpertiseTitle.union(allExpertiseTags)

    if len(query)<=0 and len(city)>0 and len(city)<78:
        allExpertise = expertise.objects.filter(location__icontains=city)

    if request.user.is_authenticated:
        if len(query)<=0 and len(city)<=0:
            allExpertise = expertise.objects.filter(location__icontains=user_city)

        if len(query)>0 and len(query)<78 and len(city)<=0:
            allExpertiseLocation = expertise.objects.filter(location__icontains=user_city)
            allExpertiseTitle = allExpertiseLocation.filter(title__icontains=query)
            allExpertiseTags =allExpertiseLocation.filter(tags__icontains=query)
            allExpertise = allExpertiseTitle.union(allExpertiseTags)

    params = {'allExpertise': allExpertise, 'query': query, 'city': city}
    return render(request, 'ExpertFinder/search-results.html', params)

#shows the list of all expertise in home page
class expertiseListView(ListView):
    model = expertise
    template_name = 'ExpertFinder/index.html'
    context_object_name = 'homecategorydata'


#shows all post by one user
class UserexpertiseListView(ListView):
    model = expertise
    template_name = 'ExpertFinder/expertise_list.html'
    context_object_name = 'homecategorydata'

    #display expertise by user
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return expertise.objects.filter(expert_identity=user).order_by('-date_posted')

# UnComment this and Comment another same
#Shows the detail view of the expertise
class expertiseDetailView(DetailView):
    model = expertise
    template_name = 'ExpertFinder/job-single.html'

# Use to create form to add new expertise
class expertiseCreateView(LoginRequiredMixin, CreateView):
    model = expertise
    fields = ['title','category','price','time_to_complete','location','tags','description']

    # Gets which user created the expertise
    def form_valid(self, form):
        form.instance.expert_identity = self.request.user
        form.instance.imgno = random.randint(1,9)
        messages.success(self.request,f'Your Expertise is LIVE NOW')
        return super().form_valid(form)


# Use to update the expertise
class expertiseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = expertise
    fields = ['title','category','price','time_to_complete','location','tags','description']

    # Gets which user created the expertise
    def form_valid(self, form):
        form.instance.expert_identity = self.request.user
        form.instance.imgno = random.randint(1,4)
        return super().form_valid(form)

    # Makes sure that only expertise creater can only edit expertise, no other expert can edit other's post
    def test_func(self):
        expertise = self.get_object()
        if self.request.user == expertise.expert_identity:
            return True
        return False

# Use to delete the expertise
class expertiseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = expertise

    # Makes sure that only expertise creater can only edit expertise, no other expert can edit other's post
    def test_func(self):
        expertise = self.get_object()
        if self.request.user == expertise.expert_identity:
            return True
        return False
    success_url = '/'

#returns about page
def about(request):
    return render(request, 'ExpertFinder/about.html')

#returns contact page
def contact(request):
    return render(request, 'ExpertFinder/contact.html')

#returns login page
def login(request):
    return render(request, 'ExpertFinder/login.html')

def logout(request):
    return render(request, 'ExpertFinder/logout.html')

@login_required
def sitemap(request):
    return render(request, 'ExpertFinder/sitemap.html')

#signup page
def signup(request):
    if request.method == 'POST':
        #django automatic register form
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, You Can Now Login Here')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'ExpertFinder/signup.html', {'form': form})

#Shows the profile of the loged in user
@login_required
def profile(request):
    #Used to update the username, email, profile of loged in used
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'ExpertFinder/profile.html', context)

#AN
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(expertise, pk=pk)
    address = request.user.profile.address
    cart_item = CartItems.objects.create(
        address=address,
        item=item,
        user=request.user,
        ordered=False,
    )
    messages.info(request, "Added to Cart!!Continue Booking!!")
    return redirect("cart")

@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    totalcartvalue = cart_items.aggregate(Sum('item__price'))
    totalcartitems = len(cart_items)
    print(totalcartvalue)
    context = {
        'cart_items':cart_items,
        'totalcartvalue': totalcartvalue,
        'totalcartitems' : totalcartitems,
    }
    return render(request, 'ExpertFinder/cart.html', context)

class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        messages.info(requests, "Cart Item Deleted!")
        return False

@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    ordered_date=timezone.now()
    cart_items.update(ordered=True,ordered_date=ordered_date)
    messages.info(request, "HUURRAY! Expert Booked")
    return redirect("order_details")

@login_required
def order_details(request):
    items = CartItems.objects.filter(user=request.user, ordered=True,status="Active").order_by('-id')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True,status="Completed").order_by('-id')
    context = {
        'items':items,
        'cart_items':cart_items
    }
    return render(request, 'ExpertFinder/order_details.html', context)

@login_required
def admin_view(request):
    cart_items = CartItems.objects.filter(item__expert_identity=request.user, ordered=True,status="Completed").order_by('-delivery_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'ExpertFinder/admin_view.html', context)

@login_required
# @admin_required
def item_list(request):
    items = Items.objects.filter(expert_identity=request.user)
    context = {
        'items':items
    }
    return render(request, 'ExpertFinder/item_list.html', context)

@login_required
# @admin_required
def update_status(request,pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = CartItems.objects.filter(item__expert_identity=request.user, ordered=True,status="Active",pk=pk)
    delivery_date=timezone.now()
    if status == 'Completed':
        cart_items.update(status=status, delivery_date=delivery_date)
    return redirect('pending_orders')


@login_required
# @admin_required
def pending_orders(request):
    items = CartItems.objects.filter(item__expert_identity=request.user, ordered=True,status="Active").order_by('-id')
    context = {
        'items':items,
    }
    return render(request, 'ExpertFinder/pending_orders.html', context)

@login_required
def admin_dashboard(request):
    cart_items = CartItems.objects.filter(item__expert_identity=request.user, ordered=True)
    pending_total = CartItems.objects.filter(item__expert_identity=request.user, ordered=True,status="Active").count()
    completed_total = CartItems.objects.filter(item__expert_identity=request.user, ordered=True,status="Completed").count()
    total = CartItems.objects.filter(item__expert_identity=request.user, ordered=True).aggregate(Sum('item__price'))
    income = total.get("item__price__sum")
    context = {
        'pending_total' : pending_total,
        'completed_total' : completed_total,
        'income' : income,
    }
    return render(request, 'ExpertFinder/admin_dashboard.html', context)