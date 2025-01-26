# from django.db import models

# # Create your models here.

from django import forms
from django.db import models
from wagtail.images.models import Image

from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Add these:
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel 

# import `index`` as this makes the model searchable
from wagtail.search import index


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    # add the get_context method:
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at') # only visible  published posts(live) and ordered by reverse-chron(order_by)
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    # `main_image` method in your BlogPage model, which returns the image from the first gallery item or `None` if no gallery items exist
    def main_image(self):
        gallery_item = self.gallery_images.first()
        image = Image.objects.get(title='sustainable-env')
        # file_name = image.file.name.split('/')[-1]
        # print("image Id:", image.id,"File Name:", file_name)
        findimage = Image.objects.get(id=image.id)
        file_name = findimage.file.name.split('/')[-1]
        # print(file_name)
        if gallery_item:
            # print("gallery_item.image:",gallery_item.image)
            return gallery_item.image
        else:
            return None

    # searchable fields
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        # to group the date and Authors fields `together for readability`.
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),

            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        # adding the InlinePanel to BlogPage.content_panels makes the gallery images available on the editing interface for BlogPage
        InlinePanel('gallery_images', label="Gallery images"),
    ]

# Orderable ... keep track of the ordering of images in the gallery.
class BlogPageGalleryImage(Orderable):
    # The `ParentalKey` to BlogPage is what attaches the `gallery images` to a `specific page`
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    # image is a `ForeignKey` to `Wagtail’s built-in Image model`, which `stores the actual images`.
    # on_delete=models.CASCADE on the foreign key means that deleting the image from the system also deletes the gallery entry.
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'