// Requires the inclusion of codenerix-utils.js
// Requires the inclusion of at least knockout-3.4.1.js

const STARS_GROUP = '.c-review-rating-input i';
const REVIEW_SUBMIT_BUTTON = '.c-product-review-input button';
const REVIEW_TEXTAREA = '.c-product-review-input textarea';

function RatingStars(callback) {
    var self = this;

    self.init = function() {
        $(STARS_GROUP).on('click', self.rate);
        return self;
    }

    self.rate = function() {
        var value = parseInt($(this)[0].attributes['data-value'].value);
        $(STARS_GROUP).each(function() {
            var item_value = parseInt($(this)[0].attributes['data-value'].value);
            if (item_value <= value)
                $(this)[0].className = 'fa fa-star';
            else $(this)[0].className = 'fa fa-star-o';
        });
        if (callback != undefined) {
            callback(value);
        }
    }

    self.getRating = function() {
        var result = 0;
        $(STARS_GROUP).each(function() {
            if ($(this)[0].className == 'fa fa-star')
                result = parseInt($(this)[0].attributes['data-value'].value);
        });
        return result;
    }
}

function ReviewForm(ReviewApiURL, csrftoken) {
    var self = this;

    self.apiClient = new ApiClient(csrftoken);

    self.init = function() {
        self.starsComponent = new RatingStars(function(newValue) {
            self.setRating(self.starsComponent.getRating());
        }).init()
        $(REVIEW_TEXTAREA).on('input', function() {
            self.setComments($(this)[0].value);
        });
        self.updateFormStatus();

        return self;
    }

    self.data = {
        'stars': 0,
        'reviews': '',
    };

    self.setRating = function(rating) {
        self.data['stars'] = rating * 2;
        self.updateFormStatus();
    }

    self.setComments = function(comments) {
        self.data['reviews'] = comments;
        self.updateFormStatus();
    }

    self.updateFormStatus = function() {
        if (self.data['stars'] > 0 && self.data['reviews'].trim() != '') {
            $(REVIEW_SUBMIT_BUTTON).prop('disabled', false);
        } else {
            $(REVIEW_SUBMIT_BUTTON).prop('disabled', true);
        }
    }

    self.submit = function(product_pk) {
        self.data['product'] = product_pk;
        self.apiClient.post(ReviewApiURL, self.data, function(data, status) {
            if (status == 'success') {
                location.reload();
            }
        }, true);
    }
}
