from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView
from plone.app.content.browser.tableview import TableBrowserView

from plone.app.content.browser.reviewlist import ReviewListTable


class FullReviewListView(BrowserView):
    def revlist(self):
        portal_membership = getToolByName(self.context, "portal_membership")
        portal_workflow = getToolByName(self.context, "portal_workflow")
        if portal_membership.isAnonymousUser():
            return []

        return portal_workflow.getWorklistsResults()

    def url(self):
        return self.context.absolute_url() + "/full_review_list"

    def review_table(self):
        table = ReviewListTable(self.context, self.request)
        return table.render()


class ReviewListBrowserView(TableBrowserView):
    table = ReviewListTable
