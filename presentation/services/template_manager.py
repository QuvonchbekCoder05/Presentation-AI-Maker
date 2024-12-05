from presentations.models.template import Template


def get_template_by_id(template_id):
    try:
        return Template.objects.get(id=template_id)
    except Template.DoesNotExist:
        return None
