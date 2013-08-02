from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager
from taggit_autosuggest_select2.widgets import TagAutoSuggest


class TaggableManager(BaseTaggableManager):

    def formfield(self, form_class=TagField, **kwargs):
        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank,
            "widget": TagAutoSuggest(),
        }
        defaults.update(kwargs)

        return form_class(**defaults)
