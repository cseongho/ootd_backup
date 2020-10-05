from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Category
from .forms import CommentForm, PostForm, CategoryForm
from settings.models import Setting

# Create your views here.

def home(request):
    return render(request, 'blog/home.html', {'home':home})

def feedback(request):
    return render(request, 'blog/feedback.html', {'feedback':feedback}) 

def market(request):
    return render(request, 'blog/market.html', {'market':market})

def ranking(request):
    return render(request, 'blog/ranking.html', {'ranking':ranking})

def get_category_count():
    category_query = Post.objects.values('categories__slug', 'categories__title').annotate(Count('categories__title'))
    return category_query

class PostCategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'categories'
    ordering = ['-date_created']
    paginate_by = 8

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(categories = self.category)

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super(PostCategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['settings'] = settings
        context['most_recent'] = most_recent
        context['category_count'] = category_count
        return context

class SearchListView(ListView):
    template_name = 'blog/search_result.html'
    context_object_name = 'search_queryset'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        context['head_title'] = 'Search'
        context['most_recent'] = most_recent
        context['settings'] = settings
        context['category_count'] = category_count
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            lookups = (Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(categories__title__icontains=query))
            return Post.objects.filter(lookups).distinct().order_by('-timestamp')

class PostListView(ListView):
    model = Post
    template_name = 'blog/feedback.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['settings'] = settings
        context['category_count'] = category_count
        return context

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'posts'
    form = CommentForm()

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['settings'] = settings
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post_detail', kwargs={'slug': post.slug}))

class PostCreateView(LoginRequiredMixin, CreateView): #edit
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    permission_required = 'blog.fields'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['settings'] = settings
        context['title'] = 'Create'
        context['submit'] = 'Create Post'
        context['head_title'] = 'Create Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('feedback')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['title'] = 'Update'
        context['settings'] = settings
        context['submit'] = 'Update Post'
        context['head_title'] = 'Update Post'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list_form.html'
    context_object_name = 'category'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['settings'] = settings
        context['title'] = 'Lists of Category'
        context['head_title'] = 'Lists of Category'
        return context

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/category_form.html'
    form_class = CategoryForm
    permission_required = 'blog.fields'
    success_url = reverse_lazy('post_create')

    def form_valid(self, form):
        category_form = super(CategoryCreateView, self).form_valid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['settings'] = settings
        context['title'] = 'Add New Category'
        context['submit'] = 'Create Category'
        context['head_title'] = 'Add new category'
        return context

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        settings = Setting.objects.last()
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['settings'] = settings
        context['title'] = 'Edit Category'
        context['submit'] = 'Update Category'
        context['head_title'] = 'Edit Category'
        return context

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False