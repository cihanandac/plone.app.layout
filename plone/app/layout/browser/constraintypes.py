from plone.autoform.form import AutoExtensibleForm
from plone.base.interfaces import ISelectableConstrainTypes
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.i18nmessageid import MessageFactory

from plone.app.content.browser.constraintypes import IConstrainForm, FormContentAdapter


# reuse the translations that we had in atcontenttypes
_ = MessageFactory("plone")


class ConstrainsFormView(AutoExtensibleForm, form.EditForm):
    schema = IConstrainForm
    label = _(
        "heading_set_content_type_restrictions",
        default="Restrict what types of content can be added",
    )
    template = ViewPageTemplateFile("constraintypes.pt")

    def getContent(self):
        return FormContentAdapter(self.context)

    def updateFields(self):
        super().updateFields()
        self.fields["allowed_types"].widgetFactory = CheckBoxFieldWidget
        self.fields["secondary_types"].widgetFactory = CheckBoxFieldWidget

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["allowed_types"].addClass("current_prefer_form")
        self.widgets["secondary_types"].addClass("current_allow_form")
        self.widgets["constrain_types_mode"].addClass("constrain_types_mode_form")

    def updateActions(self):
        super().updateActions()
        self.actions["save"].addClass("btn btn-primary")

    @button.buttonAndHandler(_("label_save", default="Save"), name="save")
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        allowed_types = data["allowed_types"]
        immediately_addable = [
            t for t in allowed_types if t not in data["secondary_types"]
        ]

        aspect = ISelectableConstrainTypes(self.context)
        aspect.setConstrainTypesMode(data["constrain_types_mode"])
        aspect.setLocallyAllowedTypes(allowed_types)
        aspect.setImmediatelyAddableTypes(immediately_addable)
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_("label_cancel", default="Cancel"), name="cancel")
    def handleCancel(self, action):
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
