# 🚀Wagtail-Doc-Advanced

## Install and run Wagtail
### first action
* check if you have an appropriate version of Python 3
* like python --version  or  python3 --version

### Create and activate a virtual environment
```
python -m venv mysite/env
```
```
source mysite/env/bin/activate
```
Note:
+ If you’re using version control such as `git`, then `mysite` is the directory for your project. You must exclude the `env` directory from any version control.

## Install Wagtail
```
pip install wagtail
```
### Generate your site
* Wagtail provides a start command similar to django-admin startproject.
* wagtail start mysite mysite  ...  generate new folder mysite inside mysite folder ... `wagtail start mysite inside mysite`
### Install project dependencies
- `cd mysite`
```
pip install -r requirements.txt
```
### Create the database
- To ensures that the tables in your database match the models in your project.
```
python manage.py migrate
```
### Create an admin user
```
python manage.py createsuperuser
```
### Start the server
```
python manage.py runserver
```
* access: `http://127.0.0.1:8000/`

### Models in wagtail (models.py)
* `body = RichTextField(blank=True)`
* `body` is a `RichTextField`, a special Wagtail field.
* it is possible to use Django core fields.
* Wagtail uses `normal Django templates` to render each page type. it looks for a template filename formed 
  from the app and model name, separating capital letters with underscores.
  For example, `HomePage` within the “home” app becomes home/`home_page.html `
  model name is `BlogIndexPage` template name is `blog_index_page.html`. blog/templates/blog/blog_index_page.html
  Conventionally, `you can place it within a templates folder within the app.`

### create a new app (in wagtail)
```
python manage.py startapp blog
```

* Use “Blog” as your page title, make sure it has the slug “blog” on the Promote tab, and publish it.
  we can now access the URL, `http://127.0.0.1:8000/blog` on site.
### Parents and children
* Much of the work in Wagtail revolves around the concept of hierarchical tree structures consisting of nodes and leaves.

### Overriding Context
* Posts are in chronological order. Generally blogs display content in reverse chronological order.
* Posts drafts are visible. You want to make sure that it displays only published content.
  To accomplish these, you need to do more than grab the index page’s children in the template. Instead, you want to modify the QuerySet in the model definition



## Customize your home page

### homepage should include the following features:
* Introduction: A concise introduction captures visitors’ attention.
* Biography: Include a brief biography that introduces yourself. This section should mention your name, role, expertise, and unique qualities.
* Hero Image: This may be a professional headshot or other image that showcases your work and adds visual appeal.
* Call to Action (CTA): Incorporate a CTA that guides visitors to take a specific action, such as “View Portfolio,” “Hire Me,” or “Learn More”.
* Resume: This is a document that provides a summary of your education, work experience, achievements, and qualifications.

`hero_cta_link` is a ForeignKey to `wagtailcore.Page`. The `wagtailcore.Page` is the base class for all other page types in Wagtail. 
This means all Wagtail pages inherit from wagtailcore.Page. For instance, your class HomePage(Page) inherits from wagtailcore.Page.










