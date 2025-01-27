from django import template

from base.models import FooterText

register = template.Library() # creates an instance of the Library class


@register.inclusion_tag("base/includes/footer_text.html", takes_context=True) # the template path that you’ll use to render the inclusion tag.
def get_footer_text(context):
    footer_text = context.get("footer_text", "") # tries to retrieve a value

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }