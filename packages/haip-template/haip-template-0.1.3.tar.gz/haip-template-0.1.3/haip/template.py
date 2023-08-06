import os
import json
import jinja2
import haip.config as config

async def render(template_filename, *, template_dir=None, **args):
    tpl_dir = _get_template_dir(template_dir)
    tpl_type = _get_template_type(template_filename)
    if tpl_type == 'sql':
        for key in args.keys():
            args[key] = _sql_escape(args[key])
    j2 = jinja2.Environment(loader=jinja2.FileSystemLoader(tpl_dir), enable_async=True)
    tpl = j2.get_template(template_filename)
    resp = await tpl.render_async(**args)
    return _decode(resp, template_filename)

def _get_template_dir(template_dir):
    cfg = config.get(template_dir=config.MANDATORY)
    if template_dir is None:
        return cfg.template_dir
    if template_dir.startswith('/'):
        return template_dir
    return cfg.template_dir + os.sep + template_dir

def _get_template_type(filename):
    _, suffix = os.path.splitext(filename)
    if len(suffix):
        return suffix[1:]
    return ''

def _decode(data_string, filename):
    _, suffix = os.path.splitext(filename)
    if suffix == '.json':
        return json.loads(data_string)
    return data_string

def _sql_escape(value):
    # similiar to mysql-connector conversion.py
    if value is None:
        return value
    value = str(value)
    value = value.replace('\\', '\\\\')
    value = value.replace('\n', '\\n')
    value = value.replace('\r', '\\r')
    value = value.replace('\047', '\134\047')  # single quotes
    value = value.replace('\042', '\134\042')  # double quotes
    value = value.replace('\032', '\134\032')  # for Win32
    return value
    