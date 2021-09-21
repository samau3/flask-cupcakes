'use strict';

const BASE_URL = 'http://localhost:5000/api/cupcakes';

/*
* Post input values to API
*/
async function addCupcake(evt) {
    // evt.preventDefault();

    const flavor = $('#flavor').val();
    const size = $('#size').val();
    const image = $('#image').val();
    const rating = $('#rating').val();

    console.log('Function is running')
    const response = await axios.post(BASE_URL,
        {
            flavor,
            size,
            image,
            rating
        });
    console.log('added cupcake')
    console.log(response)

}

$('#cupcakeForm').on('submit', addCupcake)