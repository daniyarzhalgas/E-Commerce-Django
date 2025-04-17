document.addEventListener("DOMContentLoaded", () => {
    console.log("products.js loaded!");
    const productContainer = document.getElementById("product-list");

    fetch("http://localhost/api/products/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch products");
            }
            return response.json();
        })
        .then(data => {
            data.forEach(product => {
                const productCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100 shadow-lg">
                            <img class="card-img-top p-3" src="${product.image}" alt="${product.name}"
                                 style="height: 200px; object-fit: contain;">
                            <div class="card-body text-center">
                                <h5 class="card-title">${product.name}</h5>
                                <p class="text-muted">Price: <strong>${product.price}тг</strong></p>
                            </div>
                        </div>
                    </div>
                `;
                productContainer.innerHTML += productCard;
            });
        })
        .catch(error => {
            console.error("Error loading products:", error);
            productContainer.innerHTML = "<p class='text-danger'>Failed to load products.</p>";
        });
});
