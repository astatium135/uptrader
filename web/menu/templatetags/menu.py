from typing import Iterable
from django import template
from ..models import Menu
from django.utils import html

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, name, embracing_tag="ul", item_tag="li", caption_tag="h3", container_tag="div style='margin: 5px; border: 1px solid black; padding: 5px'"):
    """Отрисовывает меню. Принимает на вход подпись (поле label) корневой записи (с пустым полем parent)"""
    def make_closer_tag(tag: str):
        if not tag:
            return ""
        temp = str.split(tag, sep=" ")
        return temp[0]
    embracing_tag_closer = make_closer_tag(embracing_tag)
    item_tag_closer = make_closer_tag(item_tag)
    caption_tag_closer = make_closer_tag(caption_tag)
    container_tag_closer = make_closer_tag(container_tag)

    request = context['request']
    path = request.path
    tname = Menu.objects.model._meta.db_table
    
    menu = Menu.objects.raw(
    f'''
    WITH RECURSIVE ids(pid) AS (
        SELECT {tname}.id as pid FROM {tname} WHERE link=%(path)s
        UNION ALL
        SELECT {tname}.parent_id as pid FROM {tname}, ids WHERE {tname}.id = ids.pid
    )
    SELECT {tname}.* FROM {tname} WHERE label=%(name)s
    UNION
    SELECT {tname}.* FROM {tname}, {tname} AS fl WHERE {tname}.parent_id = fl.id AND fl.label=%(name)s
    UNION
    SELECT {tname}.* FROM {tname}, ids WHERE {tname}.parent_id=ids.pid AND EXISTS (SELECT {tname}.* FROM {tname},ids WHERE link=%(path)s AND id=ids.pid)
    ''', {'path': path, 'name': name}
    )
    
    menu = set(menu)
    
    root = next(item for item in menu if not item.parent)
    menu.remove(root)

    responce = ""
    if container_tag:
        responce += f"<{container_tag}>"
    if caption_tag:
        responce += f"<{caption_tag}>{root.label}</{caption_tag_closer}>"

    def make_tree(submenu, items: Iterable):
        submenu.items = []
        nonlocal responce
        responce += f"<{embracing_tag}>"
        for item in items:
            if item.parent == submenu:
                submenu.items.append(item)
        submenu.items.sort(key=lambda item: item.pk)
        for item in submenu.items:
            items.remove(item)
            responce += f"<{item_tag}><a href=\"{item.link}\">{item.label}</a>"
            make_tree(item, items)
            responce += f"</{item_tag_closer}>"
        responce += f"</{embracing_tag_closer}>"
    make_tree(root, menu)

    if container_tag_closer:
        responce += f"</{container_tag_closer}>"

    return html.format_html(responce)
