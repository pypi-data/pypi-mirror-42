from datetime import datetime
import hashlib
import json

from manhattan.comparable import ComparableFrame
from manhattan.comparable.frames import _ComparableFrameMeta
from mongoframes import *
from mongoframes.queries import deep_merge, to_refs

from . import contexts

__all__ = ['PublisherFrame']


class _PublishableFrameMeta(_ComparableFrameMeta):
    """
    Meta class for `ComparableFrame`s to ensure that required fields are present
    in any defined set of fields (along with `_id`).
    """

    def __new__(meta, name, bases, dct):

        # If a set of fields is defined ensure it contains required fields
        if '_fields' in dct:

            # Flag indicating if there are changes that require publishing
            if not 'changes_pending' in dct['_fields']:
                dct['_fields'].update({'changes_pending'})

            # Checksum of the publishable data in the draft document
            if not 'last_checksum' in dct['_fields']:
                dct['_fields'].update({'last_checksum'})

            # Date/time indicating when the document was last published
            if not 'published' in dct['_fields']:
                dct['_fields'].update({'published'})

            # Checksum of the publishable data in the published document
            if not 'published_checksum' in dct['_fields']:
                dct['_fields'].update({'published_checksum'})

        return super(_PublishableFrameMeta, meta).__new__(
            meta,
            name,
            bases,
            dct
        )


class PublishableFrame(ComparableFrame, metaclass=_PublishableFrameMeta):
    """
    The `PublishableFrame` class is a base class designed to provide support
    for a document to exist in both a draft and (potentially) a published
    state.

    The class works by creating a draft version of the frame's primary
    collection, for example let's say we have a collection of articles and we
    name our collection 'Article', our published articles would exist in the
    primary 'Article' collection but our draft articles would be added to a
    second collection named 'Article__draft__'.

    When a new publishable document is created it is added initially to the
    draft collection (e.g 'Article__draft__'). Any updates to the document are
    made to the document stored in the draft collection. At some point the
    document will be ready to publish, publishing the document involves
    copying it from the draft collection into the primary collection (e.g.
    'Article'), either as an insert initially or as an update on subsequent
    publishes.

    The `PublishableFrame` class (along with the publishing library) helps to
    handle the complexities of this process seemlessly so that for the most
    part few special considerations need to be made when implementing a
    publishing pipeline for a collection/frame.
    """

    _context_manager = contexts.ContextManager()

    _uncompared_fields = ComparableFrame._uncompared_fields | {
        'changes_pending',
        'last_checksum',
        'published',
        'published_checksum'
    }

    _unpublished_fields = {
        '_id',
        'created',
        'changes_pending',
        'last_checksum',
        'modified',
        'published',
        'published_checksum'
    }

    @property
    def can_publish(self):
        """
        Return True if a draft version of the document exists with changes to
        be published.
        """
        assert self.is_draft, 'Can only be called against the draft document'

        return self.changes_pending

    @property
    def can_revert(self):
        """
        Return True if the draft version of the document can be reverted to
        the currently published version.
        """
        assert self.is_draft, 'Can only be called against the draft document'

        # If the draft is the same as the published document we can't revert
        if not self.can_publish:
            return False

        # If there isn't a published version of the document then we can't
        # revert.
        with self._context_manager.published():
            if self.count(Q._id == self._id) == 0:
                return False

        return True

    @property
    def is_draft(self):
        """Return true if this is the draft version of the document"""
        return not (self.last_checksum is None)

    @property
    def publishable(self):
        """
        Return a dictionary of values from the draft document that are needed
        to publish the draft (e.g that need to be updated in the published
        document).
        """

        # Use a copy of the draft document as a basis the publishable
        # dictionary.
        publishable_doc = {}
        deep_merge(to_refs(self._document), publishable_doc)

        # Remove any keys from the document that have been flagged as
        # unpublishable.
        self._remove_keys(publishable_doc, self._unpublished_fields)

        return publishable_doc

    def delete(self):
        """Delete the draft and published version of the document"""

        # Delete draft
        with self._context_manager.draft():
            draft = self.one(Q._id == self._id, projection=None)
            if draft:
                super(PublishableFrame, draft).delete()

        # Delete published
        with self._context_manager.published():
            published = self.one(Q._id == self._id, projection=None)
            if published:
                super(PublishableFrame, published).delete()

    def get_checksum(self):
        """Return the checksum for the current document's publishable content"""
        #safe_publishable = self.__class__._json_safe(
        #    {k: to_refs(v) for k, v in self.publishable.items()}
        #)
        safe_publishable = self.__class__._json_safe(self.publishable)
        m = hashlib.sha256()
        m.update(json.dumps(safe_publishable, sort_keys=True).encode('utf-8'))
        return m.hexdigest()

    def publish(self, user):
        """
        Publish the document (push draft changes to the live collection).

        IMPORTANT: Changes to the draft document must have been committed to
        the database before publishing, uncommitted changes wont be published.
        """
        assert self.is_draft, 'Can only be called against the draft document'

        if not self.can_publish:
            return

        # Validate that the document can be published
        self.validate_publish()

        # Attempt to publish the document
        publishable_doc = self.publishable

        with self._context_manager.published():

            # Get the published document
            published = self.one(Q._id == self._id, projection=None)

            # If there isn't a published version of the document yet then
            # create one.
            if not published:
                published = self.__class__(_id=self._id)

            # Transfer the draft values to the published document
            for k, v in publishable_doc.items():
                setattr(published, k, v)

            # Publish the changes
            published.upsert()

            # Log the action
            entry = self.__class__._change_log_cls({
                 'type': 'UPDATED',
                 'documents': [published],
                 'user': user
            })
            entry.add_note('Published')
            entry.insert()

        # Flag the date when the document was published against both copies
        now = datetime.utcnow()

        # Calculate a checksum for the document
        clean_doc = self.__class__.by_id(self._id, projection=None)
        checksum = clean_doc.get_checksum()

        with self._context_manager.draft():
            self.get_collection().update(
                {'_id': self._id},
                {
                    '$set': {
                        'changes_pending': False,
                        'last_checksum': checksum,
                        'published_checksum': checksum,
                        'published': now
                    }
                }
            )

        with self._context_manager.published():
            self.get_collection().update(
                {'_id': self._id},
                {
                    '$set': {
                        'changes_pending': False,
                        'last_checksum': None,
                        'published_checksum': checksum,
                        'published': now
                    }
                }
            )

    def revert(self, user):
        """
        Revert the draft version of the document to the published version.
        """
        assert self.is_draft, 'Can only be called against the draft document'

        if not self.can_revert:
            return

        # Get published versions of the document
        with self._context_manager.published():
            published = self.one(Q._id == self._id, projection=None)

        # Revert draft field values to those of the published version
        for k in self._document.keys():
            if k not in self._unpublished_fields:
                setattr(self, k, getattr(published, k))

        # Save the reverted draft document
        self.update()

        # Log the action
        entry = self.__class__._change_log_cls({
             'type': 'UPDATED',
             'documents': [self],
             'user': user
        })
        entry.add_note('Reverted')
        entry.insert()

    def validate_publish(self):
        """
        Validate that it is possible to publish the current document.
        Validation is typically enforced to ensure that unique content in the
        draft collection is also unique in the published. A good example of
        this would be an article slug.

        This method should return either True or raise a `PublishingError`
        exception with details of the failure, e.g:

            raise PublishingError('Slug is not unique.')

        It's important to try and design systems that minimize the risk of
        validation errors as it can be difficult or confusing for users to
        understand the nature of unique content across the draft and published
        collections. Where possible take steps to ensure that you minimize
        the potential for unqiue content clashes and when not possible make
        sure you inform users of before they attempt to publish the content.

        Using the slug field as an example, if a administrator attempts to
        change the slug for an document it's recommended that the slug is
        validated against documents in the published collection not draft.
        """
        assert self.is_draft, 'Can only be called against the draft document'

        return True

    def insert(self):
        # Set the last check for draft documents
        if self.__class__._context_manager.is_draft:
            self.last_checksum = self.get_checksum()
            self.changes_pending = True
        super().insert()

    def update(self, *fields):
        # Update the checksums if we're updating the draft
        if self.is_draft:
            super().update(*fields)

            # Calculate a checksum for the document
            clean_doc = self.__class__.by_id(self._id, projection=None)
            self.last_checksum = clean_doc.get_checksum()
            self.changes_pending \
                    = self.last_checksum != self.published_checksum
            super().update('changes_pending', 'last_checksum')

        else:
            super().update(*fields)

    @classmethod
    def get_collection(cls):
        """Return a handle to the database collection for the class"""
        if cls._context_manager.is_draft:
            return getattr(
                cls.get_db(),
                '{collection}__draft__'.format(collection=cls._collection)
            )
        return getattr(cls.get_db(), cls._collection)

    def unpublish(self, user):
        """
        Unpublish the document (remove the associated published document).
        """

        assert self.published, \
            'Can only be called against the unpublished document'

        with self._context_manager.draft():
            self.get_collection().update(
                {'_id': self._id},
                {
                    '$set': {
                        'changes_pending': True,
                        'published_checksum': None,
                        'published': None
                    }
                }
            )

        with self._context_manager.published():
            self.get_collection().remove({'_id': self._id})

        # Log the action
        entry = self.__class__._change_log_cls({
             'type': 'UPDATED',
             'documents': [self],
             'user': user
        })
        entry.add_note('Unpublished')
        entry.insert()
