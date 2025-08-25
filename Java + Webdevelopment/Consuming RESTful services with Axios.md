​



![[consuming_restful_serv_with_axios.mp4]]

Accessing and managing data is a cornerstone of any modern web application.

Users expect apps to be dynamic, responsive, and capable of updating in real-time,

often based on remote data.

For a front-end app to deliver this experience,

it needs to fetch, update, and manage data from external sources,

typically RESTful services.

While JavaScript's Fetch API can handle these requests,

another tool often provides a smoother experience, Axios.

Axios is a JavaScript library designed to simplify HTTP requests,

offering a more readable syntax and automatic JSON handling

that many developers find essential when working with RESTful services.

This video covers using Axios to perform the full range of HTTP requests,

GET, POST, PUT, and DELETE.

With Axios, connecting to RESTful services becomes efficient and adaptable,

setting the foundation for dynamic and user-friendly web applications.

To get started with Axios, make sure your project includes it.

The simplest way is to link to a content delivery network, or CDN,

which loads Axios directly into your application,

making it ready for HTTP requests.

To add Axios to the project,

insert this line in the head section of your HTML file.

Start with a script tag, and for the src attribute,

use the CDN link for the Axios library.

Add the async attribute, then close the script tag.

This link is a content delivery network, or CDN URL,

that provides a fast and reliable way to include Axios in your project.

If you ever need to locate this link,

visit the official Axios documentation, or search for Axios CDN online.

Reputable CDN providers like JS Deliver or Unpackage

will have the latest version of Axios ready to use.

With Axios now set up in the project,

it's ready to handle various HTTP requests.

So how do you actually retrieve data from an external API with Axios?

For this example, let's retrieve a list of Pokémon

from the Poké API using a GET request.

Here's how easy it is to fetch data with Axios.

Notice how clean and readable this code is compared to fetch.

Axios automatically converts the response into JSON format,

so there's no need to call response.json.

The .then method handles successful responses,

while .catch captures any errors, whether HTTP-related or network issues.

Now that Axios can handle GET requests,

it's time to explore how it can send data back to the server.

Let's say you want to add a new Pokémon to your app.

Here you'll send a JSON object with the Pokémon details.

In this example, Axios sends a POST request

with Pokémon data as the request body,

automatically setting the content type header to application forward slash JSON.

On a successful response, the added Pokémon's data is logged to the console.

Axios simplifies POST requests

by handling JSON stringification and headers for you.

You can observe the axios.post function

that sends the POST request using the URL and POST data.

Note that the actual Poké API is read-only

and does not support POST requests,

but you could create your own database backend

with a POST endpoint if needed.

Let's keep building on this

by examining how to modify data with a PUT request.

Updating data is essential when something in your app changes.

Let's say you want to update a Pokémon's details.

With a PUT request, Axios can modify a specific data

for an existing Pokémon.

In this PUT request, you send the updated Pokémon details

along with the Pokémon ID in the URL.

Axios again simplifies handling the request body and headers,

making the code more concise.

So what about removing data?

Let's dive into the DELETE request.

Sometimes data needs to be deleted,

especially in admin tasks

where certain items or records like Pokémon

need to be removed from a catalog.

With the DELETE request,

Axios makes this process straightforward.

In this example, you'll remove a Pokémon by its ID,

sending the Pokémon ID in the URL.

If successful, a confirmation message appears in the console

Like the other methods,

.catch captures any errors,

such as if the Pokémon ID doesn't exist.

With Axios, handling tasks like updating or deleting data

becomes clean and efficient.

By now, you've examined how Axios manages GET, POST, PUT,

and DELETE requests,

each with simplified syntax

and built-in features that streamline your code.

So what makes Axios a strong choice

over the Fetch API in these scenarios?

Let's explore some key advantages

that make it a go-to option for developers.

Axios automatically parses JSON responses

and converts request bodies into JSON format,

reducing repetitive code.

Axios requires less code for setup and error handling,

making requests more readable and maintainable,

especially in complex applications.

Axios allows you to distinguish

between server response errors and network issues

directly in the .catch block.

Axios supports older browsers that may lack full Fetch support,

making it versatile for applications with a wide user base.

These features make Axios a valuable tool

for developers who want efficient, readable code

for managing RESTful services.

In this video, you learned how to use Axios

to handle HTTP requests,

covering GET, POST, PUT, and DELETE methods

to interact with the RESTful API.

Axios simplifies these interactions,

making your code more readable and manageable.

With these techniques,

you're well-equipped to create dynamic, maintainable applications,

a vital skill as you advance in your development journey.