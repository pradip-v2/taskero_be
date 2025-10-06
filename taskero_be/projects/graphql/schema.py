import graphene
from graphene_django import DjangoObjectType

from taskero_be.projects.models import Project


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = "__all__"


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)

    def resolve_all_projects(root, info):
        # We can easily optimize query count in the resolve method
        return Project.objects.all()


schema = graphene.Schema(query=Query)
