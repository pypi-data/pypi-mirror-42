import aether_chart_generator.args as args
import os
import sys
from mako.template import Template


arg_opts = args.arg_options()


def check_dir(dir_path):
    """Get directory path for template."""
    dir = dir_path
    if dir == '.':
        dir = os.getcwd()
    if not os.path.exists(dir):
        print("directory does not exist, exiting")
        os._exit(1)
    return dir


def get_templates_path():
    """Template loader."""
    for path in sys.path:
        template_path = os.path.join(path, 'aether_chart_generator', 'templates')
        if os.path.isdir(template_path):
            return template_path


def write_to_file(content, filepath, arg_opts):
    """Write out templates"""
    app = arg_opts['app']
    output = arg_opts['output']

    filename = os.path.basename(filepath).split('.')[0]
    ext = os.path.basename(filepath).split('.')[2]

    if filename == 'Chart':
        file_builder = "{}/{}.{}".format(app, filename, ext)
    else:
        file_builder = "{}/{}/{}.{}".format(app,
                                            'templates', filename, ext)

    outputpath = os.path.join(check_dir(output), file_builder)

    directory = os.path.dirname(outputpath)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(outputpath, 'w') as f:
        f.write(content)


def render_template(filepath, app):
    template = open(filepath, 'r').read()

    rendered_template = Template(template).render(app=app)
    write_to_file(rendered_template, filepath, arg_opts)


def main():
    template_path = get_templates_path()
    app = arg_opts['app']
    for dirpath, _, filenames in os.walk(template_path):
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            render_template(filepath, app)


if __name__ == '__main__':
    main()
