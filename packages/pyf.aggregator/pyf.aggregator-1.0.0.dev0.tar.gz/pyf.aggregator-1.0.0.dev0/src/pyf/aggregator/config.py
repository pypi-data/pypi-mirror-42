from elasticsearch_dsl import Boolean
from elasticsearch_dsl import Date
from elasticsearch_dsl import Integer
from elasticsearch_dsl import Keyword
from elasticsearch_dsl import Nested
from elasticsearch_dsl import Text


PACKAGE_FIELD_MAPPING = {
    "author": Text(),
    "author_email": Text(),
    "bugtrack_url": Text(),
    "classifiers": Keyword(),
    "description": Text(),
    "description_content_type": Text(),
    "docs_url": Text(),
    "download_url": Text(),
    "home_page": Text(),
    "keywords": Keyword(),
    "license": Keyword(),
    "maintainer": Text(),
    "maintainer_email": Text(),
    "name": Keyword(),
    "name_searchable": Text(),
    "package_url": Text(),
    "platform": Keyword(),
    "project_url": Text(),
    "project_urls": Nested(dynamic=True),
    "release_url": Text(),
    "requires_dist": Text(),
    "requires_python": Text(),
    "summary": Text(),
    "version": Keyword(),
    "urls": Nested(
        properties={
            "comment_text": Text(),
            "digests": Nested(properties={"md5": Text(), "sha256": Text()}),
            "filename": Text(),
            "has_sig": Boolean(),
            "packagetype": Keyword(),
            "python_version": Keyword(),
            "requires_python": Keyword(),
            "size": Integer(),
            "upload_time": Date(),
            "url": Text(),
        }
    ),
}
