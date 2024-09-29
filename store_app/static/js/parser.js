const products_names_elements = document.querySelectorAll(
  ".product-card__name"
);
const products_prices_elements = document.querySelectorAll(
  ".price__lower-price"
);
const products_img_elements = document.querySelectorAll(
  ".product-card__img-wrap > img"
);

const products_img_urls = [];
const insert_sql = [];
let current_img_id = 173;

for (let i = 0; i < products_names_elements.length; i++) {
  const product_img_url = products_img_elements[i].src;
  const product_object = {
    name: products_names_elements[i].textContent.slice(3),
    price: products_prices_elements[i].textContent.replace(/\D/g, ""),
    img: `products_images/${current_img_id}.webp`,
    description: await get_description(product_img_url),
  };

  products_img_urls.push(product_img_url);

  insert_sql.push(`
        (${current_img_id}, '${product_object.name}', '${product_object.description}', ${product_object.price}, '${product_object.img}')
    `);

  current_img_id += 1;
}

async function get_description(product_img_url) {
  const product_page_url = product_img_url.replace(/\/images.*/, "");
  const product_description_url = product_page_url + "/info/ru/card.json";

  const response = await fetch(product_description_url);
  const data = await response.json();
  return data.description;
}

console.log(products_img_urls);

console.log(`
    insert into store_app_product (id, name, description, price, image)
    values ${insert_sql.join(",")} 
`);
