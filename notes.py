import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="./templates")
template_env = jinja2.Environment(loader=template_loader)

def overdue(clients_overdue):
    template_file = 'overdue_teams_note.j2'
    template = template_env.get_template(template_file)
    body = template.render(clients_overdue=clients_overdue)
    return body