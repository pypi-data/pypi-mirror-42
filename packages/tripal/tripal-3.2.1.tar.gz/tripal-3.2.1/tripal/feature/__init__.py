from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from collections import OrderedDict

from tripal.client import Client

logging.getLogger("requests").setLevel(logging.CRITICAL)
log = logging.getLogger()


class FeatureClient(Client):
    """Manage Tripal features"""

    def get_features_tripal(self, feature_id=None):
        """
        Get features entities

        :type feature_id: int
        :param feature_id: A feature entity/node ID

        :rtype: list of dict
        :return: Feature entity/node information
        """

        if self.tripal.version == 3:

            if self.tripal.version == 3:
                raise NotImplementedError("Not possible in Tripal 3. You can use the 'entity get_bundles' command, and then the 'entity get_entities' command with the required type.")

        else:
            if feature_id:
                entities = [self._get('node/%s' % feature_id, {})]
            else:
                entities = self._get('node', {})

            entities = [n for n in entities if n['type'].startswith('chado_feature')]

        return entities

    def get_features(self, feature_id=None):
        """
        Get features entities

        :type feature_id: int
        :param feature_id: A feature entity/node ID

        :rtype: list of dict
        :return: Feature entity/node information
        """

        orgs = self._request('chado/list', {'table': 'feature'})
        if feature_id:
            orgs = [v for v in orgs if v['feature_id'] == str(feature_id)]
        return orgs

    def sync(self, organism=None, organism_id=None, max_sync='', types=[], ids=[],
             job_name=None, no_wait=None):
        """
        Synchronize some features (Tripal 2 only)

        :type organism: str
        :param organism: Common name of the organism to sync

        :type organism_id: str
        :param organism_id: ID of the organism to sync

        :type max_sync: str
        :param max_sync: Maximum number of features to sync (default: all)

        :type types: list of str
        :param types: List of types of records to be synced (e.g. gene mRNA, default: all)

        :type ids: list of str
        :param ids: List of names of records to be synced (e.g. gene0001, default: all)

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """

        if organism_id:
            found_org = self.tripal.organism.get_organisms(organism_id=organism_id)
            if not found_org:
                raise Exception("Invalid organism ID")
        elif organism:
            found_org = self.tripal.organism.get_organisms(common=organism)
            if not found_org:
                found_org = self.tripal.organism.get_organisms(abbr=organism)

            if not found_org:
                raise Exception("Invalid organism name")

            organism_id = found_org[0]['organism_id']

        if not organism_id:
            raise Exception("Either organism or organism_id is required")

        if not job_name:
            job_name = 'Sync Features'

        if self.tripal.version == 3:
            raise NotImplementedError("Not possible in Tripal 3. You probably want to use 'entity' -> 'publish' instead.")
        else:
            job_args = OrderedDict()
            job_args['base_table'] = 'feature'
            job_args['max_sync'] = max_sync
            job_args['organism_id'] = organism_id
            job_args['types'] = types
            job_args['ids'] = ids
            job_args['linking_table'] = 'chado_feature'
            job_args['node_type'] = 'chado_feature'

            r = self.tripal.job.add_job(job_name, 'chado_feature', 'chado_node_sync_records', job_args)
            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

        if no_wait:
            return r
        else:
            return self._run_job_and_wait(r['job_id'])

    def delete_orphans(self, job_name=None, no_wait=None):
        """
        Delete orphans Drupal feature nodes

        :type job_name: str
        :param job_name: Name of the job

        :type no_wait: bool
        :param no_wait: Return immediately without waiting for job completion

        :rtype: str
        :return: status
        """
        if not job_name:
            job_name = 'Delete orphan features'

        if self.tripal.version == 3:
            # FIXME Don't know if it's possible
            raise NotImplementedError("Not yet possible in Tripal 3")
        else:
            job_args = OrderedDict()
            job_args[0] = 'feature'
            job_args[1] = 250000
            job_args[2] = 'chado_feature'
            job_args[3] = 'chado_feature'

            r = self.tripal.job.add_job(job_name, 'chado_feature', 'chado_cleanup_orphaned_nodes', job_args)
            if 'job_id' not in r or not r['job_id']:
                raise Exception("Failed to create job, received %s" % r)

            if no_wait:
                return r
            else:
                return self._run_job_and_wait(r['job_id'])
