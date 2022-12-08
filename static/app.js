console.log('working on it...')
const $cupcakeContainer = $('#cupcakeContainer')

// submit cupcake form 
const $CupcakeForm = $("#CupcakeForm");
$CupcakeForm.submit(submit_New_Cupcake);
// update cupcake form
const $updateCupcakeForm = $("#updateCupcakeForm")
$updateCupcakeForm.submit(submit_Updated_Cupcake)

// form elements
const $flavor = $("#flavor");
const $size = $("#size");
const $rating = $("#rating");
const $image = $("#image");
const $token = $("#csrf_token")

function getFormData() {
    return {
        csrf_token: $token.val(),
        flavor: $flavor.val(),
        size: $size.val(),
        rating: $rating.val(),
        image: $image.val()
    }
}

async function submit_New_Cupcake(event) {
    event.preventDefault();
    formData = getFormData();
    res = await axios.post("http://127.0.0.1:5000/", data = formData);
    const $cupcakeElement = buildNew_CupcakeElement(res.data.cupcake);
    appendCupcake($cupcakeElement)

}

async function submit_Updated_Cupcake(event) {
    event.preventDefault();
    formData = getFormData();
    // dynamicly get cupcake id from the hidden input of cupcakeID
    const id = $('#cupcakeID').val()
    res = await axios.patch(`http://127.0.0.1:5000/cupcake/${id}`, data = formData);
    const $cupcakeElement = buildUpdated_CupcakeElement(res.data.cupcake);
    remove_and_appendCupcake($cupcakeElement)
}
function remove_and_appendCupcake(cupcake) {
    $('#cake_card').remove()
    $cupcakeContainer.append(cupcake)
}

function buildUpdated_CupcakeElement(cupcake) {
    return $(`<div id="cake_card" class="card mx-2" style="width: 30rem;">
    <img src="${cupcake.image}" class="img-thumbnail" alt="...">
    <div class="card-body">
        <h4 class="card-title">${cupcake.flavor}</h4>
        <ul class="ps-3">
            <li>Size: <span class="text-secondary fw-bold">${cupcake.size}</span></li>
            <li>Rating: <span class="text-secondary fw-bold">${cupcake.rating}</span></li>
        </ul>
        <a href="/" class="btn btn-primary">Home</a>
        <a href="/delete/${cupcake.id}" class="btn btn-danger">Delete</a>
    </div>
</div>`)
}

function buildNew_CupcakeElement(cupcake) {
    // const { flavor, size, image, rating, id } = cupcake;
    return $(`<div class="card mx-2" style="width: 18rem;">
            <img src="${cupcake.image}" class="img-thumbnail" alt="...">
            <div class="card-body">
            <h4 class="card-title">${cupcake.flavor}</h4>
            <ul class="ps-3">
                <li>Size: <span class="text-info fw-bold">${cupcake.size}</span></li>
                <li>Rating: <span class="text-info fw-bold">${cupcake.rating}</span></li>
                <li>test</li>
            </ul>
            <a href="/cupcake/${cupcake.id}" class="btn btn-secondary">Info</a>
            </div>
            </div>`)
}
function appendCupcake(cupcake) {
    $cupcakeContainer.append(cupcake)
}


