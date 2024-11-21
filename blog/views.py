
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm

def index(request):
    posts = Post.objects.all()
    categorias = Category.objects.all()
    return render(request, 'blog/index.html', {'posts': posts, 'categorias': categorias})
def posts_por_categoria(request, category_id):
    categoria = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(categories=categoria)
    categorias = Category.objects.all()
    return render(request, 'blog/categorias.html', {'categoria': categoria, 'posts': posts, 'categorias': categorias})
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    categorias = Category.objects.all()
    comments = post.comments.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id)
        else:
            return redirect('login')  # Redirige al usuario al inicio de sesión si no está autenticado
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'categorias': categorias})