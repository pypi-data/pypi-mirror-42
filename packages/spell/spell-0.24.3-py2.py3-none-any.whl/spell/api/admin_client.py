from spell.api import base_client


ADMIN_RESOURCE_URL = "admin"
ORG_RESOURCE_URL = "orgs"


class AdminClient(base_client.BaseClient):

    def create_org(self, name, billing_email):
        """Create a new org at the server

        Keyword arguments:
        name -- name of the new org (must be at least 4 characters)
        billing_email -- billing_email of the new org

        """
        payload = {
            "name": name,
            "billing_email": billing_email,
        }
        r = self.request("post", ORG_RESOURCE_URL, payload=payload)
        self.check_and_raise(r)

    def create_cluster(self, cluster_name, org_name, external_id, role_arn,
                       storage_uri, bastion_key, vpc_id, subnets, region):
        """Create a new cluster for an org

        Keyword arguments:
        cluster_name -- name of the new cluster
        org_name -- name of the org to add the cluster to
        external_id -- internally-generated id for external aws requests
        role_arn -- aws arn for role to assume
        storage_uri -- s3 uri for external spell resources
        bastion_key -- ssh private key for bastion access
        vpc_id -- aws id of vpc for worker machines
        subnets -- aws ids of subnets for worker machines
        region -- aws region for worker machines

        """
        payload = {
            "org_name": org_name,
            "cluster_name": cluster_name,
            "external_id": external_id,
            "role_arn": role_arn,
            "storage_uri": storage_uri,
            "ssh_bastion_private_key": bastion_key,
            "vpc_id": vpc_id,
            "subnets": subnets,
            "region": region,
        }
        r = self.request("post", "{}/{}".format(ADMIN_RESOURCE_URL, "clusters"), payload=payload)
        self.check_and_raise(r)
