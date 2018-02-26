import graphene
from graphene_django import DjangoObjectType

from links.models import Link

######################## Query ########################

class LinkType(DjangoObjectType):
    class Meta:
        model = Link


## define Types
class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

'''
query  {
  links {
    id
    url
  }
}
'''

######################## Mutation ########################
# The process of sending data to server is called mutation
# Mutations are used for sending data and queries for getting data
# Mutation name wil be same as Class name
# Every Mutation Definition Must have mutate method

#1: Defines a mutation class.
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    #2: Defines the data you can send to the server.
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3: The mutation method: it creates a link on the database using the data sent by the user,through the url and description parameters.
    # After, the server returns the CreateLink class with the data just created.
    def mutate(self, info, url, description):
        link = Link(url = url, description = description)
        ## save the date
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description
        )

#4: Creates a mutation class with a field to be resolved, which points to our mutation defined before.
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()

'''
mutation {
  createLink(url: "www.facebook.com", description: "Facebook") {
    id,
    url,
    description
  }
}
'''

