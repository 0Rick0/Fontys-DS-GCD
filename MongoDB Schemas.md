# Schemas in MongoDB

In MongoDB you store documents instead of rows like an traditional database.

Also MongoDB is more efficient at writing then reading. So it is better to have duplicate data and write more often.
Then to write once but have to complex lookups.

This means when you have a relation like this for student enrollment:

Student --- N:1 --- Class --- N:N --- Course

You need to store it like this:
```JSON
{
  "code": "ABC",
  "semester": "sem",
  "students": [
    {
      "nr": 1,
      "name": "name"
    }
  ],
  "courses": [
    {
      "name": "name",
      "credits": "credits"
    }
  ]
}
```

When a student enrolls, you wan't to add him to the class.
The class is the most important part of the relation so this is what you set as the root.

When the courses are centric you need to to way to many lookups and when the students are centric you can't add all classes.

For something like Facebook you would use a schema like this:

User --- 1:N --- Post --- N:N -- Comment --- N:1 -- User

```JSON
{
  "date": "ISO",
  "text": "text",
  "user": {
    "name": "name"
  },
  "comments": [
    {
      "date": "ISO",
      "text": "text",
      "commenter": {
        "name": "name"
      }
    }
  ]
}
```

A post is centric because the you want to create a feed. In this way you can simply filter on the username to personalise the feed and sort on date.
