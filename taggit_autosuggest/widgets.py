import copy

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from taggit_autosuggest.utils import edit_string_for_tags


MAX_SUGGESTIONS = getattr(settings, 'TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS', 20)


class TagAutoSuggest(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            tags = [o.tag for o in value.select_related("tag")]
            value = edit_string_for_tags(tags)

        result_attrs = copy.copy(attrs)
        result_attrs['type'] = 'hidden'
        result_html = super(TagAutoSuggest, self).render(name, value,
            result_attrs)

        widget_attrs = copy.copy(attrs)
        widget_attrs['id'] += '__tagautosuggest'
        widget_html = super(TagAutoSuggest, self).render(name, value,
            widget_attrs)

        js = u"""
            <script type="text/javascript">
            (function ($) {

                $(document).ready(function (){

                    $("#%(widget_id)s").select2({
                        tags: [],
                        placeholder: '%(start_text)s',
                        minimumInputLength: 3,
                        ajax: {
                            url: '%(url)s',
                            dataType: 'json',
                            quietMillis: 400,
                            data: function (term, page) {
                                return {
                                    q: term,
                                    limit: %(retrieve_limit)s
                                };
                            },
                            results: function (data, page) {
                                return {results: data};
                            }
                        },
                        formatResult: function (object) {
                            if (object.name)
                                return object.name;
                            else
                                return object.text;
                        },
                        formatSelection: function (object) {
                            if (object.name)
                                return object.name;
                            else
                                return object.text;
                        },
                        createSearchChoice: function(term, data) {
                            if (data.length !== 0) {
                                if ($(data).filter(function() {
                                    var item;
                                    if (this.name)
                                        item = this.name
                                    else
                                        item = this.text
                                    return item.localeCompare(term) === 0;
                                }).length===0) {
                                    var retval = {id: term, text: term}
                                    return retval;
                                }
                            }
                            var retval = {id: term, text: term}
                            return retval;
                        }
                    });

                    /*
                    $('.as-selections').addClass('vTextField');
                    $('ul.as-selections li.as-original input').addClass('vTextField');

                    $('#%(result_id)s').parents().find('form').submit(function (){
                        tags_as_string = $("#as-values-%(widget_id)s").val();
                        $("#%(widget_id)s").remove();
                        $("#%(result_id)s").val(tags_as_string);
                    });
                    */
                });
            })(jQuery || django.jQuery);
            </script>""" % {
                'result_id': result_attrs['id'],
                'widget_id': widget_attrs['id'],
                'url': reverse('taggit_autosuggest-list'),
                'start_text': _("Enter Tag Here"),
                'empty_text': _("No Results"),
                'limit_text': _('No More Selections Are Allowed'),
                'retrieve_limit': MAX_SUGGESTIONS,
            }
        return result_html + widget_html + mark_safe(js)

    class Media:
        js_base_url = getattr(settings, 'TAGGIT_AUTOSUGGEST_STATIC_BASE_URL', '%s' % settings.STATIC_URL)
        css_url = getattr(settings,'TAGGIT_AUTOSUGGEST_CSS_URL','%sjquery-autosuggest/css/autoSuggest.css' % js_base_url)
        select2_css_url = getattr(settings,'TAGGIT_AUTOSUGGEST_JS_URL','%scss/select2.css' % js_base_url)
        js_url = getattr(settings,'TAGGIT_AUTOSUGGEST_JS_URL','%sjquery-autosuggest/js/jquery.autoSuggest.js' % js_base_url)
        select2_js_url = getattr(settings,'TAGGIT_AUTOSUGGEST_JS_URL','%sjs/libs/select2.min.js' % js_base_url)
        css = {
            'all': (css_url, select2_css_url)
        }
        js = (js_url, select2_js_url)
