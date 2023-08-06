from jinja2 import Template

tpl_provider= Template('''provider "{{ name }}" {
  {% for key, value in data %}
  {{ key }} = {{ value }}
  {% endfor %}
}''')

tpl_resource= Template('''provider "{{ name }}" {
  {% for key, value in data %}
  {{ key }} = {{ value }}
  {% endfor %}
}''')


tpl_module= Template('''module "{{ name }}" {
  {% for key, value in config %}
  {{ key }} = {{ value }}
  {% endfor %}
}''')

tpl_backend= Template('''terraform {
  backend "{{ name }}" {
    {% for key, value in data %}
    {{ key }} = {{ value }}
    {% endfor %}
  }
}''')

tpl_data= Template('''data "{{ data_type }}" "{{ name }}" {
  backend = {{ backend }}
  config {
    {% for key, value in config %}
    {{ key }} = {{ value }}
    {% endfor %}
  }
}''')