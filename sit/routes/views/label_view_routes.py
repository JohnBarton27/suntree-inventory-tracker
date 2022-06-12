from flask import render_template

from label import Label


def get_labels():
    all_labels = Label.get_all()
    return render_template('labels/labels.html', labels=all_labels)


def label(label_id):
    label = Label(db_id=int(label_id))
    items = label.get_items()
    return render_template('labels/label.html', label=label, items=items)
