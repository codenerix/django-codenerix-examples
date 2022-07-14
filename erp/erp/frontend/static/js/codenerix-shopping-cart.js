// Requires the inclusion of codenerix-utils.js
// Requires the inclusion of at least knockout-3.4.1.js

function ShoppingCartClient(shoppingCartApiURL, csrftoken) {
    var self = this;

    self.client = new ApiClient(csrftoken);

    self.add = function(pk, quantity, callback) {
        var data = {
            product_pk: pk,
            quantity: quantity,
        }
        self.client.post(shoppingCartApiURL, data, function(data, status) {
            if (status == 'success' && callback != null) {
                callback(data);
            }
        });
    }

    self.edit = function(pk, quantity, callback) {
        var data = {
            product_pk: pk,
            quantity: quantity,
        }
        self.client.put(shoppingCartApiURL, data, function(data, status) {
            if (status == 'success' && callback != null) {
                callback(data);
            }
        });
    }

    self.list = function(callback) {
        self.client.get(shoppingCartApiURL, null, function(data, status) {
            if (status == 'success' && callback != null) {
                callback(data);
            }
        });
    }

    self.remove = function(pk, callback) {
        var data = {
            product_pk: pk,
        }
        self.client.delete(shoppingCartApiURL, data, function(data, status) {
            if (status == 'success' && callback != null) {
                callback(data);
            }
        });
    }
}

function ProductModel(pk) {
    this.pk = pk;

    this.name = ko.observable('');
    this.description = ko.observable('');
    this.code = ko.observable('');
    this.url = ko.observable('');
    this.thumbnail = ko.observable('');
    this.features = ko.observableArray([]);
    this.attributes = ko.observableArray([]);
    this.tax = ko.observable(0.0);
    this.base_price = ko.observable(0.0);
    this.unit_price = ko.observable(0.0);
    this.total_price = ko.observable(0.0);
    this.quantity = ko.observable(0);
}

function ShoppingCartModel() {
    var self = this;

    self.count = ko.observable(0);
    self.total = ko.observable(0.0);
    self.subtotal = ko.observable(0.0);
    self.tax = ko.observable(0.0);
    self.products = ko.observableArray([]);

    self.setData = function(data) {
        if (data) {
            self.count(data.count);
            self.total(data.total);
            self.subtotal(data.subtotal);
            self.tax(data.tax);

            for (var i = 0; i < data.products.length; i ++) {
                product = data.products[i];

                productModel = new ProductModel(product.pk);

                productModel.name(product.name);
                productModel.description(product.description);
                productModel.code(product.code);
                productModel.url(product.url);
                productModel.thumbnail(product.thumbnail);
                productModel.features(product.features);
                productModel.attributes(product.attributes);
                productModel.tax(product.tax);
                productModel.base_price(product.base_price);
                productModel.unit_price(product.unit_price)
                productModel.total_price(product.total_price);
                productModel.quantity(product.quantity);

                self.products.push(productModel);
            }
        }
    }

    self.editProduct = function(pk, quantity, total_price, subtotal, total, tax) {
        for (var i = 0; i < self.products().length; i ++) {
            product = self.products()[i];
            if (product.pk == pk) {
                diffCount = quantity - product.quantity();

                product.quantity(quantity);
                product.total_price(total_price);

                self.total(total);
                self.subtotal(subtotal);
                self.tax(tax);

                break;
            }
        }
    }

    self.removeProduct = function(pk, count, subtotal, total, tax) {
        self.products.remove(function(product){
           return product.pk == pk;
        })[0];
        self.count(count);
        self.subtotal(subtotal);
        self.total(total);
        self.tax(tax);
    }
}

function ShoppingCartManager(shoppingCartApiURL, shoppingCartURL, csrftoken) {
    var self = this;

    self.cartClient = new ShoppingCartClient(shoppingCartApiURL, csrftoken);
    self.cartModel = new ShoppingCartModel();

    self.init = function() {    
        $('.shopping-cart').each(function(){
            ko.applyBindings(self.cartModel, $(this)[0]);
        });

        self.listProducts();
        return self;
    }

    self.listProducts = function() {
        self.cartClient.list(function(data) {
            self.cartModel.setData(data);
        });
    }

    self.removeProduct = function(pk) {
       self.cartClient.remove(pk, function(data) {
           self.cartModel.removeProduct(pk, data.count, data.subtotal, data.total, data.tax);
       });
    }

    self.addManyProducts = function(pk, quantity) {
        self.cartClient.add(pk, quantity, function(data) {
            window.location = shoppingCartURL;
        });
    }

    self.addOneProduct = function(pk) {
        self.addManyProducts(pk, 1);
    }

    self.editProduct = function(pk, quantity) {
        if (quantity > 0) {
            self.cartClient.edit(pk, quantity, function(data) {
                self.cartModel.editProduct(pk, quantity, data.total_price, data.subtotal, data.total, data.tax);
            });
        }
   }
}
