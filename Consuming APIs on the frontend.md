## Introduction

In today’s web applications, connecting your frontend with APIs is essential for delivering dynamic and interactive experiences. This reading introduces how to integrate API calls within a frontend framework using jQuery and connects it to a simple shopping list application backed by a Spring Boot REST API. In this reading, you will learn how to set up jQuery to make HTTP requests and display shopping list items from a backend API. You will recreate the shopping cart application created in the ungraded lab for a Shopping Cart CRUD with JavaScript. This time, instead of using JavaScript, you are going to use jQuery.

|**Important**|
|---|
|Please ensure that you have a functioning Spring Boot backend configured with a MySQL database and that relevant data is available in your products table. The examples provided utilize Spring Boot and jQuery for API requests, with the assumption that the backend is operating at _http://localhost:8080/api/v1/products_.|

## Introduction to AJAX

AJAX, which stands for asynchronous JavaScript and XML, is a technique used to create dynamic and asynchronous web applications. It allows the client (usually the browser) to request data from the server without reloading the entire webpage. This technique enhances user experience by providing smoother interactions and faster response times for web applications. While the name mentions XML, AJAX commonly uses JSON for data interchange in modern applications.

Here's the general and basic syntax for making an AJAX call in jQuery:

```
$.ajax({
    url: 'https://api.example.com/data',
    method: 'GET',
    data: { key1: 'value1', key2: 'value2' },
    contentType: 'application/json',
    dataType: 'json',
    success: function(response) {
        console.log('Success:', response);
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});

```


This jQuery _$.ajax()_ code snippet demonstrates how to make an asynchronous HTTP request to an API endpoint. Here’s a breakdown of each part:

|**Code**|**Explanation**|
|---|---|
|_$.ajax({ ... })_|The _$.ajax()_ function is _jQuery_'s core method for performing _AJAX_ requests. It allows you to configure all aspects of the request, including the _URL_, _HTTP_ method, data to send, content type, expected response type, and callback functions for success or error handling.|
|**Parameters inside** _**$.ajax()**_||
|_url: 'https://api.example.com/data'_|This specifies the API endpoint where the request is sent. In this example, it’s set to '_https://api.example.com/data._'|
|_method: 'GET'_|Specifies the HTTP method for the request. In this case, _GET_ is used to retrieve data. Common HTTP methods are _GET, POST, PUT_, and _DELETE_.<br><br>For _GET_ and _DELETE_ requests, data is usually sent as query parameters, while _POST_ and _PUT_ requests often include data in the request body.|
|_data: { key1: 'value1', key2: 'value2' }_|This contains the data to be sent with the request. Here, an object with two properties, key1 and key2, is provided.<br><br>For a _GET_ request, this data is automatically converted into query parameters, so the request URL might be the following:<br><br>_https://api.example.com/data?key1=value1&key2=value2_ <br><br>For a _POST_ or _PUT_ request, this data would typically be included in the request body.|
|_contentType: 'application/json'_|Sets the Content-Type header, specifying the format of the data being sent to the server. '_application/json_' tells the server that the data is in JSON format.<br><br>This is especially important for _POST_ or _PUT_ requests, where you’re sending data in JSON.|
|_dataType: 'json'_|Specifies the format of the expected response from the server. In this case, it’s set to 'json', meaning you expect the server to return JSON data.|
|_success: function(response) { ... }_|A callback function that runs if the request is successful.<br><br>_response_ contains the data returned by the server (in this case, parsed as a JavaScript object because dataType is set to 'json').|
|_error: function(xhr, status, error) { ... }_|A callback function that runs if the request fails. It provides three parameters:<br><br>1. **xhr**: the full XMLHttpRequest object, which contains details about the failed request.<br>    <br>2. **status**: a string describing the status of the request (e.g., "error").<br>    <br>3. **error**: a string that contains a textual error message, making debugging easier.|

|**Remember**|
|---|
|Since jQuery is a JavaScript library, you need to add it specifically to your HTML code using the following line in your HTML code:<br><br>    _<script src="https://code.jquery.com/jquery-3.7.1.js"></script>_<br><br>Make sure it is in the _head_ tag before the _body_ tag so that it is ready to be executed when the HTML elements are loaded on the page and interactive operations like _window.onLoad()_ can be performed. The rest of the HTML code remains the same as previously used in the Shopping Cart CRUD application with vanilla JavaScript code.|

## HTML setup

You will need to set up the HTML frontend first to create the Shopping Cart CRUD Application. Here are the files you will need.

1. **index.html:** This page serves as the initial entry point for the CRUD application.
    
2. **product.html:** This page displays a product’s details when selected from the _index.html_.
    
3. **edit.html:** This page displays a form for editing a product’s details on the backend database.
    
4. **add.html:** This page displays a form to add a new product to the backend database.
    

## Adding functionality via jQuery

Now, let’s add functionality to your shopping cart application via jQuery. You’ll implement the core actions needed for the CRUD operations—creating, reading, updating, and deleting products—by making AJAX requests to the backend API. 

Each action will connect the user interface to the Spring Boot API, allowing real-time interaction with the product database without needing a full page reload. Setting up these functions will make the application fully interactive, enabling seamless product management right from the frontend. 

Before you begin, you’ll need to explore the **index.js**.This code written in jQuery adds the functionality required for the actual operations that are shown in the HTML frontend listed below.

1. Create a new product by sending a _POST_ request to the backend.
    
2. Update an existing product by sending a _PUT_ request to the backend.
    
3. View all products or a single product by sending a _GET_ request to the backend.
    
4. Delete a product by sending a _DELETE_ request to the backend.
    

First, let's create a general function to handle AJAX requests. This function will make the code modular and allow you to reuse the function for any type of AJAX request.

```
// Main function to handle all AJAX requests

function ajaxRequest(url, method, data) {

    return $.ajax({

        url: url,

        method: method,

        contentType: 'application/json',

        data: data ? JSON.stringify(data) : undefined

    });

}
```

This function simplifies the CRUD operations, allowing you to handle all AJAX requests with one function. Let’s unpack function parameters used in the code.

- _url_: The API endpoint to which to send the request.
    
- _method_: The HTTP method (_GET, POST, PUT, DELETE_).
    
- _data_: The data to send (optional, only needed for _POST_ and _PUT_ requests).
    

## READ (_GET_): Fetching and displaying products

In this step, you'll focus on the Read operation of CRUD by fetching and displaying products from the backend. Using the _ajaxRequest()_ function, you’ll send a _GET_ request to retrieve the list of products from the API. Once retrieved, the data will be displayed dynamically on the webpage, allowing users to view all available products in real time. This setup ensures that the products are shown immediately without requiring a page reload.

### **Fetch all products**

Complete the following steps:

1. Use the _ajaxRequest()_ function to send a _GET_ request to retrieve products.
    
2. Dynamically display the products on the webpage.
    
```

function fetchProducts() {
    ajaxRequest('http://localhost:8080/api/v1/products', 'GET')
        .done(function(products) {
            var productContainer = $('#productContainer');
            productContainer.empty();
            var productCards = $.map(products, function(product) {
                return `
                    <div class="product-card">
                        <img src="${product.image}" alt="${product.title}">
                        <a href="product.html?id=${product.id}">${product.title</a>
                        <p>$${product.price.toFixed(2)} Rating: ${product.rating.rate}</p>
                    </div>
                `;
            }).join('');
            productContainer.html(productCards);
        })
        .fail(function(xhr) {
            handleError(xhr, 'fetch');
        });

}

fetchProducts(); // Call this function on page load

```
Great job! Here’s a brief explanation of the code:

- _ajaxRequest()_ sends a _GET_ request to fetch the product list.
    
- _$.map()_ iterates over each product, generating an HTML structure for each one.
    
- _productContainer.html(productCards)_ inserts the generated HTML into the _#productContainer_ div.
    

Now, let’s implement the Create operation. 

## CREATE (_POST_): Adding a new product

In this step, you’ll implement the Create operation, allowing users to add new products to the database. First, product information will be collected from a form on the webpage. Then, using the _ajaxRequest()_ function, you’ll send a _POST_ request with the new product data to the backend API. Upon successfully adding the product, the user is redirected to the main page, where they can find the updated list with the newly added item.

### **Add a product**

Complete the following steps:

1. Collect product information from a form.
    
2. Use _ajaxRequest()_ to send a _POST_ request with the new product data.
    
3. Redirect to the main page after the product is added.
    

```
function addProduct(productData) {
    ajaxRequest('http://localhost:8080/api/v1/products', 'POST', productData)
        .done(function() {
            alert('Product added successfully!');
            window.location.href = 'index.html';
        })
        .fail(function(xhr) {
            handleError(xhr, 'add');
        });
}

$('#productForm').on('submit', function(event) {
    event.preventDefault();
    var newProduct = {
        title: $('#title').val(),
        price: parseFloat($('#price').val()),
        description: $('#description').val(),
        category: $('#productCategory').val(),
        image: $('#imageURL').val(),
        rating: {
            rate: parseFloat($('#rating').val()) || 0,
            count: parseInt($('#ratingCount').val(), 10) || 0
        }
    };
    addProduct(newProduct);
});
```

Fantastic! Now, let’s investigate the code again before you implement the Update operation: 

- _addProduct():_ This function sends a _POST_ request to add a new product using the _ajaxRequest()_ function.
    
- Form submission: Prevents the default form behavior, gathers data from input fields, and calls _addProduct()_ with the new product information.
    

## UPDATE (_PUT_): Editing a product

In this step, you’ll implement the **Update operation**, enabling users to edit an existing product’s information. First, you’ll load the product’s current data into a form, allowing users to make changes. Then, using the _ajaxRequest()_ function, you’ll send a _PUT_ request with the updated product data to the backend API, which will update the product in the database. This approach lets users modify product details seamlessly, ensuring that the database reflects the latest information.

### **Update product information**

Complete the following steps:

1. Load the product’s current data for editing.
    
2. Use _ajaxRequest()_ to send a _PUT_ request with the updated data.
    

```
function updateProduct(productId, updatedData) {

    ajaxRequest('http://localhost:8080/api/v1/products/' + productId, 'PUT', updatedData)

        .done(function() {

            alert('Product updated successfully!');

            window.location.href = 'index.html';

        })

        .fail(function(xhr) {

            handleError(xhr, 'update');

        });

}

  

function loadProductForEditing(productId) {
    ajaxRequest('http://localhost:8080/api/v1/products/' + productId, 'GET')
        .done(function(product) {
            $('#title').val(product.title);
            $('#price').val(product.price);
            $('#description').val(product.description);
            $('#productCategory').val(product.category);
            $('#imageURL').val(product.image);
            $('#rating').val(product.rating.rate);
            $('#ratingCount').val(product.rating.count);
            $('#productForm').off('submit').on('submit', function(event) {
                event.preventDefault();
                var updatedProduct = {
                    title: $('#title').val(),
                    price: parseFloat($('#price').val()),
                    description: $('#description').val(),
                    category: $('#productCategory').val(),
                    image: $('#imageURL').val(),
                    rating: {
                        rate: parseFloat($('#rating').val()),
                        count: parseInt($('#ratingCount').val(), 10)
                    }
                };
                updateProduct(productId, updatedProduct);
            });
        })
        .fail(function(xhr) {
            handleError(xhr, 'fetch');
        });
}
```

Well done! You’re almost there. Let’s explore the code a bit more before you move on to implementing the Delete operation.

- _updateProduct()_: This sends a _PUT_ request to update the product by ID.
    
- _loadProductForEditing()_: This fetches the current product data for editing and pre-fills the form.
    
- Form submission: This triggers _updateProduct()_ with the updated product details.
    

## DELETE (_DELETE_): Removing a product

In this step, you’ll implement the Delete operation, allowing users to remove a product from the database by its ID. Before deletion, users will be prompted to confirm their choice to prevent accidental deletions. Once confirmed, the _ajaxRequest()_ function sends a _DELETE_ request to the backend API, permanently removing the specified product. After the deletion is successful, the user will be redirected to the main page to view the updated product list without the deleted item.

### **Delete a product by ID**

Complete the following steps:

1. Confirm the deletion.
    
2. Use _ajaxRequest()_ to send a _DELETE_ request to remove the product.
    
3. Redirect to the main page upon successful deletion.
    

```
function deleteProductById(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        ajaxRequest('http://localhost:8080/api/v1/products/' + productId, 'DELETE')
            .done(function() {
                alert('Product deleted successfully!');
                window.location.href = 'index.html';
            })
            .fail(function(xhr) {
                handleError(xhr, 'delete');
            });
    }
}
```

Great job! You’ve implemented the Delete operation. Here’s a brief explanation of the code:

- _deleteProductById()_: This sends a _DELETE_ request to remove the product by its ID.
    
- Confirmation Prompt: This asks the user to confirm before proceeding with deletion.
    

## Error handling

Let's create a function that displays messages based on error codes to handle errors. 

Complete the following steps:

1. Create a function _handleError()_ that takes two parameters _xhr_, and _action_.
    
2. Create an object called _errorMsg_ that stores different error codes and their messages. 
    
3. Create a message string that checks the status of the _xhr_ request, and if it is in the _errorMsg_ object, fetch the error message and append it to the string, or append the _Unexpected Error_ message.
    
4. Finally, an alert will be shown with the _action_ message.
    

```
function handleError(xhr, action) {
    var errorMsg = {
        404: 'Resource not found',
        403: 'Unauthorized request',
        500: 'Server error',
        0: 'Network error - request was blocked'
    };
    var status = xhr.status;
    var message = errorMsg[status] || 'Unexpected error: ' + status;
    alert('Failed to ' + action + ' product. ' + message);
}
```

## Conclusion

Well done! You now know how to build a simple shopping list application using Spring Boot as the backend API provider and jQuery for frontend interactions. You should have a functioning application capable of creating, displaying, updating, and deleting products. This foundational knowledge of API integration is essential for scaling and enhancing any web application. Once you are comfortable with jQuery and Spring Boot, consider experimenting with more complex frameworks to expand your skills further.