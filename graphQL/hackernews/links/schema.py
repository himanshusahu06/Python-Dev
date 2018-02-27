import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from links.models import Link, Vote
from users.schema import get_user, UserType

######################## Query ########################

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

## define Types
class Query(graphene.ObjectType):
    links = graphene.List(LinkType, search=graphene.String())
    votes = graphene.List(VoteType)

    def resolve_links(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(url__icontains=search) | Q(description__icontains=search)
            )
            return Link.objects.filter(filter)
        else:
            return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

'''
query  {
  links {
    id
    url
  }
}

query  {
  links(search="search_string") {
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
    posted_by = graphene.Field(UserType)

    #2: Defines the data you can send to the server.
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3: The mutation method: it creates a link on the database using the data sent by the user,through the url and description parameters.
    # After, the server returns the CreateLink class with the data just created.
    def mutate(self, info, url, description):
        user = get_user(info) or None
        link = Link(
            url = url,
            description = description,
            posted_by=user
        )
        ## save the date
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = get_user(info) or None
        if not user:
            raise Exception("You must be logged in to vote!!!")

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception("Invalid Link!!")
        
        Vote.objects.create(
            user=user,
            link=link
        )

        return CreateVote(user=user, link=link)


'''
mutation {
  createLink(url: "www.facebook.com", description: "Facebook") {
    id,
    url,
    description
  }
}
'''

#4: Creates a mutation class with a field to be resolved, which points to our mutation defined before.
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
