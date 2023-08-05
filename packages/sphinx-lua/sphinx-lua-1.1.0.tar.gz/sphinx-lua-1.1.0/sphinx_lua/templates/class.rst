.. lua:class:: {{ name }}
{%- if model.inherits_from -%}
{{ ": " }}
{%- for base in model.inherits_from -%}
{{ base }}{{ ", " if not loop.last }}
{%- endfor -%}
{%- endif %}
{%- filter indent(width=4) %}


{% if model.desc -%}
    {{ model.desc | process_link }}
{%- endif %}
{% if model.usage %}
**Usage:**

.. code-block:: lua
    :linenos:

    {{ model.usage|indent(4) }}
{%- endif -%}

{# display class field #}
{%- for field in model.fields -%}
{%- with type=field.type -%}
.. lua:attribute:: {{ field.name }}: {% include "type.rst" %}

    {{ field.desc }}

{% endwith -%}
{%- endfor %}

{# display public methods first #}
{%- for method in model.methods -%}
{%- if method.visibility == "public" %}
{% include "method.rst" %}
{%- endif %}
{%- endfor %}

{# then display protected one #}
{%- for method in model.methods -%}
{%- if method.visibility == "protected" -%}
{%- include "method.rst"|indent(4) %}
{%- endif %}
{%- endfor %}
{%- endfilter %}
