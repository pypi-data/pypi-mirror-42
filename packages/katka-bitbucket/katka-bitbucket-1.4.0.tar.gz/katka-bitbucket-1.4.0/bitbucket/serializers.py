from rest_framework import serializers

from . import constants
from .conf import settings


class BitbucketRequest(serializers.Serializer):
    credential_public_id = serializers.CharField(required=False)
    base_url = serializers.URLField(required=False,
                                    default=settings.DEFAULT_BITBUCKET_SERVICE_LOCATION)  # the bitbucket base url
    start = serializers.IntegerField(min_value=0, required=False)  # first element index of the response list
    limit = serializers.IntegerField(min_value=0, required=False)  # max number of elements to be retrieved


class BitbucketResponse(serializers.Serializer):
    start = serializers.IntegerField(required=False)  # first element index of the response list
    limit = serializers.IntegerField(required=False)  # max number of elements to be retrieved
    size = serializers.IntegerField(required=False)  # the number of retrieved elements
    isLastPage = serializers.BooleanField(required=False)
    nextPageStart = serializers.IntegerField(required=False)  # the index of the first element of the next page


# Bitbucket Projects

class BitbucketProjectsRequest(BitbucketRequest):
    name = serializers.CharField(required=False)  # filter for project name
    permission = serializers.ChoiceField(required=False, choices=constants.BITBUCKET_PROJECT_PERMISSIONS,
                                         default=constants.PROJECT_READ)


class BitbucketProjectDetails(serializers.Serializer):
    key = serializers.CharField(required=False)  # example AT (for a project named Atlassian)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)


class BitbucketProjectsResponse(BitbucketResponse):
    values = serializers.ListField(child=BitbucketProjectDetails(), required=False, default=list())


# Bitbucket Repos

class BitbucketReposRequest(BitbucketRequest):
    project_key = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class BitbucketRepoDetails(serializers.Serializer):
    slug = serializers.CharField(required=False)
    name = serializers.CharField(required=False)


class BitbucketReposResponse(BitbucketResponse):
    values = serializers.ListField(child=BitbucketRepoDetails(), required=False, default=list())
