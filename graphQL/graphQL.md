# GraphQL

GraphQL is new, flexible API standard and alternative to REST. More precise, graphQL is query language for APIs. Get many resources in a single request.

enables **declarative data fetching**.

GraphQL server exposes single endpoint and respond to queries.

GraphQL minimized the amount of data that needs to be transfered over the network and improves application performance.

GraphQL solves problems with underfetching and overfetching.
* `Overfetching` - Downloading unnecessary data.
* `Underfetching` - doesn't download enough of the right information. Need to send multiple requests ([n+1 request problem](https://stackoverflow.com/questions/97197/what-is-n1-select-query-issue?answertab=votes#tab-top))

## GraphQL vs REST
* graphql is stateless server and structured access to resources whereas REST is strict specification.
* graphql is more flexible and efficiant in client-server communication because of it's stateless nature.


## GraphQL Query
Sample GraphQL query...

```graphql
query {
    # Queries can have comments!
    User (id: "er3fgr4th") {
        name
        posts {
            title
        }
        followers (last: 3) {
            name
        }
    }
}
```

Sample GraphQL server response..

```json
{
    "data" : {
        "User": {
            "name": "Himanshu Sahu",
            "posts": [
                { "title": "Learning GraphQL today" },
                { "title": "Learning GraphQL tomorrow" },
                { "title": "Will learn GraphQL forever" }
            ],
            "followers": [
                { "name": "John" },
                { "name": "Alice" },
                { "name": "Bob" }
            ]
        }
    }
}
```

Queries can have alias.

```graphql
query {
    User (id: "er3fgr4th") {
        fullName: name
        allPosts: posts {
            postTitle: title
        }
    }
}
```

Query Response.

```json
{
    "data" : {
        "User": {
            "fullName": "Himanshu Sahu",
            "allPosts": [
                { "postTitle": "Learning GraphQL today" },
                { "postTitle": "Learning GraphQL tomorrow" },
                { "postTitle": "Will learn GraphQL forever" }
            ]
        }
    }
}
```

## GraphQL Fragments

```graphql
query {
  firstPerson: Person(id: "cje5fqu1lc49z0137ij5hdpyc") {
    # Queries can have comments!
    personAge: age
    ID: id
    fullNamee: name
  }
  secondPerson: Person(id: "cje04b2kl1vda0194pltey9qn") {
    # Queries can have comments!
    personAge: age
    ID: id
    fullNamee: name
  }
}
```

since fields are repeated som we can create fragments (reusable units called fragments).

```graphql
query {
  firstPerson: Person(id: "cje5fqu1lc49z0137ij5hdpyc") {
      ...personFragments
  }
  secondPerson: Person(id: "cje04b2kl1vda0194pltey9qn") {
      ...personFragments
  }
}

fragment personFragments on Person {
    personAge: age
    ID: id
    fullNamee: name
}
```

## GraphQL Variables

```graphql
query GetPersonByNameQuery($id: ID){
  Person(id: $id) {
    name
    age
    id
  }
}
```
```json
{
    "id": "cje04b2kl1vda0194pltey9qn"
}
```

equivalant HTTP query.

```http
POST /simple/v1/cje04b0502ul801623k5028sc/ HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: a9b0cf56-7c90-7c38-8795-c92ec77cd201

{
	"query": "query GetPersonByNameQuery($id: ID){ Person(id: $id) { name age id } }",
	"variables": {
		"id": "cje04b2kl1vda0194pltey9qn"
	}
}
```

## GraphQL Directives
It helps to write dynamic queries.

```graphql
query Hero($episode: Episode, $withFriends: Boolean!, $skipAppearsIn: Boolean!) {
  hero(episode: $episode) {
    name
    friends @include(if: $withFriends) {
      name
    }
    appearsIn @skip(if: $skipAppearsIn)
  }
}
```
pass the variables.
```json
{
  "episode": "JEDI",
  "withFriends": true,
  "skipAppearsIn": true
}
```

response from graphQL server.
```json
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
```

since `withFriends` flag is true so graphql fetch that field and `skipAppearsIn` flag is true so graphql skip that field.

A directive can be attached to a field or fragment inclusion, and can affect execution of the query in any way the server desires

* `@include(if: Boolean)` Only include this field in the result if the argument is true.
* `@skip(if: Boolean)` Skip this field if the argument is true.


## GraphQL schema

* GraphQL uses strong type system to define capabilities of an API.
* Schema serves as contract between server and client.


### GraphQL Shcema Definition Language (SDL)

* Defining simple types (**!** - required field)

```graphql
type Person {
    name: String!
    age: Int!
}

type Post {
    title: String!
}
```

* Adding relation among types

```graphql
## this is one to many relationship between Person and Post.
## One person can be author of many posts but one post can have only one author.

type Person {
    name: String!
    age: Int!
    posts: [Post!]!
}

type Post {
    title: String!
    author: Person!
}
```

Sample GraphQL request (person with name)
```graphql
{
    allPersons {
        name
    }
}
```

Sample GraphQL response (person with name)
```json
{
    "allPersons": [
        { "name": "Himanshu" },
        { "name": "Alice" },
        { "name": "Bob" }
    ]
}
```

Sample GraphQL request (person with name and age both, will return only last 2 record)
```graphql
{
    allPersons(last: 2) {
        name
        age
    }
}
```

Sample GraphQL response (person with name and age both)
```json
{
    "allPersons": [
        { "name": "Himanshu", "age": 23 },
        { "name": "Alice", "age": 34 }
    ]
}
```

Sample GraphQL request (person with name, post that contain only title)
```graphql
{
    allPersons {
        name
        posts {
            title
        }
    }
}
```

## GraphQL mutations

* create
* update
* delete

```graphql
mutation {
    createPerson(name: "Himanshu", age: 23) {
        name
        age
    }
}
```

```graphql
{
    createPerson: {
        name: "Himanshu"
        age: 23
    }
}
```

## Realtime updates with subscriptions

When an client subscribe to an event, it will initiate and hold a steady connection to server.

```graphql
subscription {
    newPerson {
        name
        age
    }
}
```
In this example, client subscribed the server to get informed about new Person been created. It represent stream of data sent over to the client.


### Root types

```graphql
type Query {
    ...
}

type Mutation {
    ...
}

type Subscritption {
    ...
}
```

### Defining Query Schema
```graphql
{
    allPersons {
        name
    }
}
```
for this query we must define schema to process the query.

```graphql
type Query {
    allPersons (last: Int!): [Person!]!
}
```

### Defining Mutation Schema
```graphql
mutation {
    createPerson(name: "Bob", age: 36) {
        name
    }
}
```
for this query we must define schema to process the query.

```graphql
type Mutation {
    createPerson (name: String!, age: Int!): Person!
}
```

### Defining Subscription Schema
```graphql
subscription {
    newPerson {
        name
        age
    }
}
```
for this query we must define schema to process the query.

```graphql
type Subscription {
    newPerson: Person!
}
```

## Resolver Function

graph-ql server has one resolver function per field to retrieve the data for corresponding field.


http://graphql.org/learn
