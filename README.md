## Park Finder API Documentation.

### Problem Identification

The aim of this project is to create an API for a park review application. The problem it addresses is the lack of a centralised platform where users can find information about parks, including their addresses and reviews. Users can also add new parks and write their own reviews.

### Why is it a problem?

Finding information about parks can be a time-consuming process, particularly for individuals new to a certain area or those looking to explore different parks. Having a dedicated platform where users can find and share information about parks can greatly simplify this process. It also provides a community-driven approach to gathering and sharing information, as users can contribute by adding new parks and reviews.

### Chosen Database System

For this application I have decided to use PostgreSQL, a powerful, open-source object-relational database system. PostgreSQL offers advanced features such as full ACID compliance and support for complex operations and queries. It also offers strong performance and scalability, which can be essential for handling a large number of reviews and parks.

One of the main drawbacks of PostgreSQL compared to NoSQL databases like MongoDB is that it may not scale horizontally as well, which could be a concern for very large applications. Additionally, while PostgreSQL's strict schemas can be helpful for ensuring data consistency, they can also be less flexible than the schema-less models used by NoSQL databases.

### Key Functionalities and Benefits of an ORM

An Object-Relational Mapping (ORM) tool provides a bridge between an object-oriented programming language and a relational database. In this project, we've used SQLAlchemy, a SQL toolkit and ORM for Python. Some of the key functionalities and benefits of using an ORM like SQLAlchemy include:

- Abstraction of Database-Specific Syntax: ORMs allow developers to interact with databases using the programming language they are comfortable with, abstracting away SQL syntax.

- Data Consistency: By using classes and objects to represent tables and records, ORMs help to maintain consistency between the database and the application.

- Improved Productivity: Developers can focus on writing Python code instead of SQL queries, leading to increased productivity.

- Safe and Secure: ORMs automatically escape SQL queries, protecting the application from SQL injection attacks.

### API Endpoints

**User**

- POST /register: Register a user
- POST /login: Log in a user or admin

**Review**

- GET /review: Get all reviews, with optional filters.
- GET /review/user_id/park_id: Get user park review.
- GET /review/user_id: Get reviews by a user.
- POST /review/park_id: Create a new review.
- DELETE /review/user_id/park_id: Deletes a review (requires admin authorisation or user creator authorisation).
- PUT, PATCH /review/user_id/park_id: Update a review.

**Park**

- GET /park: Get all parks, with optional filters.
- GET /park/id: Get a specific park.
- GET /park/state/state_id: Gets parks in a state.
- GET /park/city/city_id: Gets parks in a city.
- GET /park/suburb/suburb_id: Gets parks in a suburb.
- GET /park/search: Search park by name.
- GET /park/park_id/review: Get reviews for a park.
- POST /park: Create a new park.
- DELETE /park/park_id: Delete a specific park (requires admin authorisation).
- PUT, PATCH /park/park_id: Update a specific park (requires admin authorisation).

**Address**

- GET /address: Gets all addresses.
- GET /address/address_id: Gets addresses by id.
- POST /address: Create a new address.
- DELETE /address/address_id: Delete an address. (requires admin authorisation).
- PUT, PATCH /address/address_id: Update an address. (requires admin authorisation).

**Suburb**

- GET /suburb: Get all suburbs.
- GET /suburb/id: Get a suburb.
- GET /suburb_id/addresses: Gets addresses within a suburb.
- POST /suburb: Create a suburb.
- DELETE /suburb/id: deletes a suburb (requires admin authorisation).
- PUT, PATCH /suburb/id: Update a specific suburb (requires admin authorisation)
  .
  **City**

- GET /city: Get all cities.
- GET /city/city_id: Get a city.
- GET /city/city_id/suburbs: Gets suburbs in a city.
- POST: /city: Create a city.
- DELETE /city/city_id: Deletes a city: (requires admin authorisation).
- PUT, PATCH /city/city_id: Update a specific city (requires admin .authorisation)

**state**

- GET /state: Get all states.
- GET /state/id: Get a state.
- GET state/state_id/cities: Get cities in a state.
- POST /state: Create a state.
- DELETE /state: Delete a state (requires admin authorisation).
- PUT, PATCH /state: Update a state (requires admin authorisation).

### ERD

![ParkFinderERD](<./docs/PFAPI%20(4).jpg>)

### Third Party Services

Park Finder API uses the following third party services:

- **PostgreSQL:** This is used as the application's database.

- **Flask:** This is used to create the application's server and define its routes.

- **SQLAlchemy:** This is used as the application's ORM, providing an interface between the Python code and the database.

- **Marshmallow:** This is used for object serialization/deserialization, allowing for validation and transformation of data before it is sent to or received from the database.

- **Bcrypt:** This is used for hashing passwords, ensuring they are securely stored in the database.

- **JWT:** This is used for generating and decoding JWT tokens, which are used for user authentication.

### Models and Relationships

The database relations implemented in the application are designed to model the real-world relationships between various entities involved in the park review process. These are primarily one-to-many relationships, reflecting the hierarchical nature of geographical entities and the structure of user reviews.

**User-Park Relationship:** Each User can create multiple Parks, but each Park is associated with one User. This is a one-to-many relationship from User to Park. This relationship allows the application to track which user has created each park, enabling features like user profiles where you can see all parks created by a particular user.

**User-Review Relationship:** Each User can write multiple Reviews, but each Review is associated with one User. This is a one-to-many relationship from User to Review. This relationship allows the application to track which user has written each review, enabling features like user profiles where you can see all reviews by a particular user.

**Park-Review Relationship:** Each Park can have multiple Reviews, but each Review is associated with one Park. This is a one-to-many relationship from Park to Review. This relationship enables the application to aggregate all reviews for a particular park, which can be useful for features like a park detail page where users can see all reviews for that park.

**Park-Address Relationship:** Each Park has one Address, and each Address is associated with one Park. This is a one-to-one relationship between Park and Address. This relationship allows each park to have a specific location.

**Suburb-Address Relationship:** Each Suburb can contain multiple Addresses, but each Address is associated with one Suburb. This is a one-to-many relationship from Suburb to Address. This relationship enables the application to aggregate all addresses (and therefore parks) in a particular suburb.

**City-Suburb Relationship:** Each City contains multiple Suburbs, but each Suburb is within one City. This is a one-to-many relationship from City to Suburb. This relationship is important for enabling geographical browsing and search features, such as finding all suburbs within a city.

**State-City Relationship:** Each State contains multiple Cities, but each City is within one State. This is a one-to-many relationship from State to City. This relationship is necessary to model the hierarchical structure of geographical entities

### Database Relations to be Implemented in the Application

The database relations in this application are based on the relationships between the models. They are as follows:

- One-to-many relationships between User and Park, User and Review, State and City, City and Suburb, Suburb and Address, and Park and Review.

- One-to-one relationships between Park and Address.

These relations are implemented using SQLAlchemy's relationship function, which allows for easy navigation between related instances.

### Task Allocation and Tracking

Tasks in our project are allocated and tracked using a Trello board. The board is divided into several lists: To Do, In Progress, Testing and done. Each task is represented as a card and moved between these lists as it progresses through the development lifecycle.

**To Do:** This list contains tasks that need to be accomplished. Each card in this list represents a feature or a piece of functionality that needs to be implemented.

**In Progress:** This list contains tasks that are currently being worked on. These are tasks that have been started but not yet completed.

**Testing:** This list contains tasks related to testing that are being worked on or need to be done.

**Done:** This list contains tasks that have been completed. Once a task is fully implemented and tested, the card is moved to this list.

![Trello Board](./docs/Screenshot%202023-07-30%20062621.png)

[Link to Trello](https://trello.com/b/MjvbVjIg/parkfinderapi)
[Link to Github](https://github.com/BuzSaliji/Park_Finder_API)
