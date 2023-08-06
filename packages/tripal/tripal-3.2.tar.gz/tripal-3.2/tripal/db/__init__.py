from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from collections import OrderedDict

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class DbClient(Client):
    """Access Tripal/Chado database"""

    def get_dbs(self, db_id=None, name=None):
        """
        Get all dbs

        :type db_id: str
        :param db_id: A db ID

        :type name: str
        :param name: filter on db name

        :rtype: list of dict
        :return: Dbs information
        """

        dbs = self._request('chado/list', {'table': 'db'})

        if db_id:
            dbs = [v for v in dbs if v['db_id'] == str(db_id)]
        if name:
            dbs = [v for v in dbs if v['name'] == name]

        return dbs

    def get_mviews(self, name=None):
        """
        Get all materialized views

        :type name: str
        :param name: filter on mview name

        :rtype: list of dict
        :return: materialized views information
        """

        data = {
            'table': 'tripal_mviews',
        }

        mvs = self._request('chado/list', data)

        if name:
            for m in mvs:
                if m['name'] == name:
                    return m

        return mvs

    def index(self, mode="website", table=None, index_name=None, queues=10, fields=[], links={}, tokenizer='standard', token_filters=[], exposed=False, index_url=None, job_name=None, no_wait=False):
        """
        Schedule database indexing using elasticsearch

        :type mode: str
        :param mode: Indexing mode: 'website' to index the website , 'nodes' for the website nodes, 'entities' for the website entities (Tripal 3), 'table' to index a single table, 'gene' to build a Gene search index (Tripal 3 only) (default: website) ('website' default to 'nodes' for Tripal 2, 'entities' for Tripal 3)

        :type table: str
        :param table: Table to index (only in 'table' mode)

        :type index_name: str
        :param index_name: Index name (only in 'table' mode)

        :type queues: int
        :param queues: Number of indexing task queues (Tripal 2 only)

        :type fields: list of str
        :param fields: Fields to index (only in 'table' mode), syntax: <field_name>|<field_type>, field_type should be one of 'string' (Tripal2), 'text' (Tripal3), 'keyword', 'date', 'long', 'double', 'boolean', 'ip', 'object', 'nested', 'geo_point', 'geo_shape', or 'completion'

        :type links: list of str
        :param links: List of links to show to users, syntax: <column-where-to-show-the-link>|</your/url/[any-column-name]> (Tripal 2 only)

        :type tokenizer: str
        :param tokenizer: Tokenizer to use (only in 'table' mode) (one of 'standard', 'letter', 'lowercase', 'whitespace', 'uax_url_email', 'classic', 'ngram', 'edge_ngram', 'keywordx', 'pattern', or 'path_hierarchy'; default='standard')

        :type token_filters: list of str
        :param token_filters:  Token filters (Tripal 3 only) (only in 'table' mode) (available filters are 'standard', 'asciifolding', 'length', 'lowercase', 'uppercase') (Default to ['standard', 'lowercase'])

        :type exposed: bool
        :param exposed: "Expose the index (read-only) to other websites

        :type index_url: str
        :param index_url: In order for other sites to link back to your results page, you must specify a path where the form for this index can be reached

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: str
        :return: Indexing information
        """

        modes = {
            'table': 'table',
            'website': 'website',
            'gene': 'gene',
            'nodes': 'nodes',
            'entities': 'entities'
        }

        if mode not in modes:
            raise Exception("Mode should be 'table', 'website', 'nodes', 'entities' or 'gene'")

        if mode == 'table' and not index_name:
            raise Exception("index_name is required in 'table' mode")

        tokenizers = {
            'standard': 'standard',
            'letter': 'letter',
            'lowercase': 'lowercase',
            'whitespace': 'whitespace',
            'uax_url_email': 'uax_url_email',
            'classic': 'classic',
            'ngram': 'ngram',
            'edge_ngram': 'edge_ngram',
            'keyword': 'keyword',
            'pattern': 'pattern',
            'path_hierarchy': 'path_hierarchy',
        }

        token_filters_list = {
            'standard': 'standard',
            'asciifolding': 'asciifolding',
            'length': 'length',
            'lowercase': 'lowercase',
            'uppercase': 'uppercase'
        }

        if tokenizer not in tokenizers:
            raise Exception("Unknown tokenizer")

        if (token_filters and not set(token_filters).issubset(token_filters_list)):
            raise Exception("Unknown token filters")

        if exposed and not index_url:
            raise Exception("An index url is required for the exposed flag")

        # 'website' redirect to node indexing in tripal code, but it's misleading.
        # We redirect users to entity indexing if Tripal 3, and node indexing in tripal 2
        # We leave the mode for node indexing at 'website' in Tripal 2 for back-compatibility

        if self.tripal.version == 3:
            if mode == 'website':
                mode = 'entities'
        else:
            if mode == 'nodes':
                mode = 'website'
            elif mode == 'entities' or mode == 'gene':
                raise NotImplementedError("These modes are not available for Tripal 2")

        fields_real = {}
        for f in fields:
            fs = f.split('|', 1)
            fields_real[fs[0]] = fs[1]

        links_real = {}
        for l in links:
            ls = l.split('|', 1)
            if ls[0] not in fields_real:
                raise Exception("Cannot add a link to column '%s' because it is not indexed" % ls[0])
            links_real[ls[0]] = ls[1]

        data = {
            'mode': mode,
            'table': table,
            'index_name': index_name,
            'queues': queues,
            'tokenizer': tokenizer,
            'token_filters': token_filters,
            'fields': fields_real,
            'links': links_real,
            'exposed': exposed,
            'index_url': index_url
        }

        res = self._request('elasticsearch/index', data)

        if res and 'status' in res and res['status'] == 'error':
            raise Exception("Failed to schedule indexing, error: %s" % res['errors'])

        if not job_name:
            job_name = 'Elasticsearch indexing'

        job_args = OrderedDict()
        job_args[0] = 10
        job_args[1] = 120

        r = self.tripal.job.add_job(job_name, 'tripal_rest_api', 'tripal_rest_api_run_indexing', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

        return res

    def populate_mviews(self, name=None, no_wait=None):
        """
        Populate materialized views

        :type name: str
        :param name: filter on mview name

        :type no_wait: bool
        :param no_wait: Do not wait for job to complete

        :rtype: str
        :return: Loading information
        """

        if name:
            mview_id = self.get_mviews(name)['mview_id']

            self._do_populate_mview(name, mview_id, no_wait)
        else:
            mviews = self.get_mviews()

            for m in mviews:
                self._do_populate_mview(m)

    def _do_populate_mview(self, mview, no_wait=False, job_name=None):
        if not job_name:
            job_name = 'Populate materialized views \'%s\'' % mview['name']

        print('Populating view \'%s\'' % mview['name'])

        job_args = OrderedDict()
        job_args[0] = mview['mview_id']

        r = self.tripal.job.add_job(job_name, 'tripal_core', 'tripal_populate_mview', job_args)
        if 'job_id' not in r or not r['job_id']:
            raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def tune(self):
        """
            Setup default entity index priority for whole website indexing

            :rtype: dict
            :return: "Status"

        """

        if self.tripal.version == 2:
            raise NotImplementedError("Tuning is not required in Tripal 2")

        data = {}

        res = self._request('elasticsearch/tune', data)

        if res and 'status' in res and res['status'] == 'error':
            raise Exception("Failed to schedule indexing, error: %s" % res['errors'])

        return res
