from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.utils import timezone

# pip install django-braces
from braces.views import SelectRelatedMixin

from . import forms
from . import models


from django.contrib.auth import get_user_model
User = get_user_model() #When someone logeed in the session we could use it to call things about that user


class PostList(generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            # we used the variable name post_user to mark it and prefix it with self to call it again in the context method this makes it as an attribute
            #first we get all active users from the User modle  using prefetch_related with the backward key ( prefetch_related is better for the performance)
            #then we get the required user from the queryset by using get method
            self.userpost =User.objects.prefetch_related('user_posts').get(
                username__iexact=self.kwargs.get('username')
                )
            #We could also use the below method but it's not the best
            #self.post_user = models.Post.objects.filter(user__username__iexact=self.kwargs.get('username')) 
            print(self.kwargs)#returns the passed kwargs
            #User.objects.prefetch_related("posts")   returns all active users
            print(self.userpost)# check this. it returns the username of the post_user object
        except User.DoesNotExist:
            raise Http404
        else:
            #return all user posts using the backward key
            return self.userpost.user_posts.all() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.userpost
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        ) #returns the user's post


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)# means save the form in object that comes from the post model
        self.object.created_at = timezone.now()
        print(self.object.created_at)# print the time of the created post
        print(self.kwargs) # there is no kwargs here so we use request method
        self.object.user = self.request.user # injecting the user who create the post in the database
        print(self.object.user)#prints the username of the user in the terminal
        self.object.save()  #saving the obj and commit it in the database
        return super().form_valid(form) #returns the created form and redirecting automatically to it


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id) #gets all the posts created by the user it equivalent to Post.objects.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

from django.utils import timezone

print(timezone.now())