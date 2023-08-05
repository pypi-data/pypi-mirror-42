# -*- coding: utf-8 -*-
"""
    oy.contrib.form
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Provides a custom page contenttype.

    :copyright: (c) 2018 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

import time
import os.path
from jinja2 import Markup
from flask import (
    current_app,
    request,
    make_response,
    redirect,
    render_template,
    url_for,
    abort,
    flash,
)
from werkzeug import secure_filename
from flask_wtf import Form as HtmlForm
from oy.globals import current_page
from oy.boot.sqla import db
from oy.views import ContentView
from oy.dynamicform import DynamicForm
from oy.helpers import date_stamp
from oy.contrib.extbase import OyExtBase
from .admin import register_admin
from .models import FormEntry, FieldEntry, Form, Field


class FormView(ContentView):
    def store_form(self, form):
        entry = FormEntry(form_id=self.page.id)
        for f in form:
            field = (
                Field.query.filter_by(form_id=current_page.id)
                .filter_by(name=f.name)
                .one_or_none()
            )
            if field is None:
                continue
            field_entry = FieldEntry(key=f.name, field_id=field.id)
            data = f.data
            if field.type == "file_input":
                file_data = request.files[field.name]
                filename = "%s-%s-%s.%s" % (
                    field.name,
                    date_stamp(),
                    str(time.time()).replace(".", ""),
                    os.path.splitext(file_data.filename)[-1],
                )
                filename = secure_filename(filename)
                path = os.path.join(current_app.config["FORM_UPLOADS_PATH"], filename)
                file_data.save(path)
                data = filename
            field_entry.value = data
            db.session.add(field_entry)
            entry.fields.append(field_entry)
        db.session.add(entry)

    def serve(self):
        form = DynamicForm(self.page.fields).form
        if form.validate_on_submit():
            with db.session.no_autoflush:
                self.store_form(form)
            db.session.commit()
            flash(Markup(self.page.submit_message), "success")
            return redirect(request.path)
        return dict(form=form)


class Form(OyExtBase):
    """Extenssion entry point for oy forms."""

    module_args = dict(
        name="oy.contrib.form",
        import_name="oy.contrib.form",
        static_folder="static",
        template_folder="templates",
    )

    def init_app(self, app):
        app.add_contenttype_handler("form", FormView, methods=("GET", "POST"))
