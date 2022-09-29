from django.shortcuts import render
from datetime import date
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import PostModel, CommentModel
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.views import View

    

def get_date(post):
    return post['date'] 

class StartingPageView(View):
    def get(self, request):
        print('5')
        try:
            latest_posts_list = list(PostModel.objects.all())
            print('6')
            latest_posts = latest_posts_list[-3:]
            return render(request,"blog/index.html",{
                'posts' : latest_posts
            })
        except:
            print('7')
            raise Http404()

class PostsView(View):
    def get(self, request):
        all_posts = PostModel.objects.all()
        return render(request, "blog/all-posts.html",{
            'all_posts' : all_posts
        })

class SuccessView(View):
    def get(self, request):
        return render(request, "blog/success.html")

class PostDetailView(View):
    def is_stored_post(self,request,post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request,slug):
        print('8')
        comment_form = CommentForm() #On a besoin de montrer le formulaire, sinon il n'apparaît pas
        identified_post = get_object_or_404(PostModel, slug=slug)
        comments =  CommentModel.objects.filter(post =  identified_post).order_by("-id")
        context = {
            'post' : identified_post,
            'comments' : comments,
            'comment_form': comment_form,
            'is_saved_for_later': self.is_stored_post(request,identified_post.id)}
        return render(request, "blog/post-detail.html",context)

    def post(self,request,slug):
        print('9')
        comment_form = CommentForm(request.POST)
        #print(comment_form)
        #print(slug)
        #try:
        #    print(PostModel.objects.get(slug=slug))
        #except:
        #    print("NOOOOPE")
        identified_post = PostModel.objects.get(slug=slug)
        if comment_form.is_valid():
            print('10')
            #On veut modifier le post attribué au comment:
            #On save avec commit = False, ce qui veut dire qu'on envoie pas la donnée vers
            #la base de données mais on peut sauver les données dans une variable de type modèle.
            comment = comment_form.save(commit = False)
            #On a alors plus qu'à modifier la variable puis à la sauver
            comment.post = identified_post
            comment.save()
            #On redirige vers la même page avec reverse()!
            return HttpResponseRedirect(reverse('post-detail-page', args = [slug]))
        print('11')
        comments = CommentModel.objects.filter(post =  identified_post).order_by("-id")
        context = {'post' : identified_post,
            'comments' : comments,
            'comment_form': comment_form,
            'is_saved_for_later': self.is_stored_post(request,identified_post.id)}
        print("12")

        return render(request, "blog/post-detail.html",context)


        #Une instance de Form possède une méthode is_valid() qui procède aux routines de validation 
        #pour tous ses champs. Lorsque la méthode est appelée et que tous les champs contiennent 
        #des données valables, celle-ci :
        #- renvoie True;
        #- insère les données du formulaire dans l’attribut cleaned_data.
        #C'est avant d'utiliser un modelForm
        #if form.is_valid():
        #    new_comment_data = CommentForm(author = form.cleaned_data['author'],
        #        content= form.cleaned_data['content'],
        #         author_mail = form.cleaned_data['author_mail'],
        #        post = PostModel.object.get(pk = form.cleaned_data['id']))
        #    new_comment_data.save()
        
#class ReadLaterView(View):
#    def get(self, request):
#        stored_posts = request.session.get("stored_posts")
#
#        context = {}
#
#        if stored_posts is None or len(stored_posts) == 0:
#            context["posts"] = []
#            context["has_posts"] = False
#        else:
#          posts = Post.objects.filter(id__in=stored_posts)
#          context["posts"] = posts
#          context["has_posts"] = True
#
#        return render(request, "blog/stored-posts.html", context)

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts)==0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = PostModel.objects.filter(id__in = stored_posts)
            context['posts'] = posts
            context["has_posts"] = True
        return render(request, "blog/stored-posts.html",context)


    def post(self, request):
        print('1')
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None : #Si pas de stored posts#
            stored_posts = [] #stored_posts est alors vide. => On peut afficher 
                              #une liste vide mais on ne peut pas afficher none
            print('2')
        post_id = int(request.POST['post_id'])
        print('3')
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
            print('4')
        elif post_id in stored_posts:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts
            print('4b')

        return HttpResponseRedirect('/')

