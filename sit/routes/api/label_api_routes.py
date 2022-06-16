from flask import request, render_template

from label import Label, LabelColor
from item import Item


def create_label():
    label_text = request.form['labelText']

    label_color = LabelColor.get_random()
    label = Label(text=label_text, color=label_color)
    label.create()

    all_labels = Label.get_all()

    return render_template('labels/list_labels.html', labels=all_labels)


def delete_label():
    label_id = int(request.args['id'])
    label_to_delete = Label.get_by_id(label_id)

    label_to_delete.delete()

    return '/labels'


def get_label_dropdown():
    item_id = int(request.args['item_id'])
    item_for_labels = Item.get_by_id(item_id)
    all_labels = Label.get_all()
    labels_on_item = [label.id for label in Label.get_for_item(item_for_labels)]
    return render_template('labels/labels_dropdown.html', labels=all_labels, item=item_for_labels,
                           selected=labels_on_item)


def edit_label():
    label_id = int(request.args['id'])

    text = request.form['labelText']

    label_to_update = Label.get_by_id(label_id)
    label_to_update.update_text(text)

    return render_template('labels/label_header.html', label=label_to_update)
