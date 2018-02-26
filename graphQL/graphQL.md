# GraphQL

GraphQL is new, flexible API standard and alternative to REST. More precise, graphQL is query language for APIs.

enables **declarative data fetching**.

GraphQL server exposes single endpoint and respond to queries.

GraphQL minimized the amount of data that needs to be transfered over the network and improves application performance.

## GraphQL vs REST
* graphql is stateless server and structured access to resources whereas REST is strict specification.
* graphql is more flexible and efficiant in client-server communication because of it's stateless nature.

Sample GraphQL query...

```graphql
query {
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

## Overfetching and Underfetching

GraphQL solves problems with underfetching and overfetching.
* `Overfetching` - Downloading unnecessary data.
* `Underfetching` - doesn't download enough of the right information. Need to send multiple requests ([n+1 request problem](https://stackoverflow.com/questions/97197/what-is-n1-select-query-issue?answertab=votes#tab-top))


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
    allPersons: [
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
    allPersons: [
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

### Realtime updates with subscriptions

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



### Resolver Function

graph-ql server has one resolver function per field to retrieve the data for corresponding field.
