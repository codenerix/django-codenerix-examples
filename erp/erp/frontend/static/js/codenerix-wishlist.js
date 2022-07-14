// Requires the inclusion of codenerix-utils.js

function WishlistClient(wishlistApiURL, csrftoken) {
    var self = this;

    self.client = new ApiClient(csrftoken);

    self.add = function(pk, quantity, callback) {
        var data = {
            product_final: pk,
            quantity: quantity,
            priority: 'L'
        }
        self.client.post(wishlistApiURL, data, function(data, status) {
            if (status == 'success' && callback != null) {
                callback(data);
            }
        });
    }

}

function WishlistManager(wishlistURL, csrftoken) {
    var self = this;

    self.client = new WishlistClient(wishlistURL, csrftoken);

    self.addManyProducts = function(pk, quantity) {
        self.client.add(pk, quantity, function(data) {
            window.location = wishlistURL;
        });
    }

    self.addOneProduct = function(pk) {
        self.addManyProducts(pk, 1);
    }
}
