// Requires the inclusion of codenerix-utils.js

const BILLING_ADDRESS = '.c-billing-address';
const SHIPPING_ADDRESS = '.c-shipping-address';


function nameCompare(a, b) {
    if (a[lang+"__name"].toLowerCase() < b[lang+"__name"].toLowerCase())
        return -1;
    if (a[lang+"__name"].toLowerCase() > b[lang+"__name"].toLowerCase())
        return 1;
    return 0;
}

function LocalesClient(countriesApiURL, regionsApiURL, provincesApiURL, citiesApiURL) {
    var self = this;

    self.client = new ApiClient();

    self.listCountries = function(success, continent) {
        var data = {
            rowsperpage: 100000,
        }
        if (continent != undefined)
            data['continent'] = continent;
        self.client.get(countriesApiURL, data, function(data, status) {
            if (status == 'success') {
                success(data.table.body.sort(nameCompare));
            }
        });
    }

    self.listRegions = function(success, country) {
        var data = {
            rowsperpage: 100000,
            country: country,
        }
        self.client.get(regionsApiURL, data, function(data, status) {
            if (status == 'success') {
                success(data.table.body.sort(nameCompare));
            }
        });
    }

    self.listProvinces = function(success, region) {
        var data = {
            rowsperpage: 100000,
            region: region,
        }
        self.client.get(provincesApiURL, data, function(data, status) {
            if (status == 'success') {
                success(data.table.body.sort(nameCompare));
            }
        });
    }

    self.listCities = function(success, country, region, province) {
        data = {
            rowsperpage: 100000,
        }
        if (country != undefined && country != null)
            data['country'] = country;
        if (region != undefined && region != null)
            data['region'] = region;
        if (province != undefined && province != null)
            data['province'] = province;
        self.client.get(citiesApiURL, data, function(data, status) {
            if (status == 'success') {
                success(data.table.body.sort(nameCompare));
            }
        });
    }
}

function LocalesModel() {
    this.countries = ko.observableArray([]);

    this.billingRegions = ko.observableArray([]);
    this.billingProvinces = ko.observableArray([]);
    this.billingCities = ko.observableArray([]);

    this.shippingRegions = ko.observableArray([]);
    this.shippingProvinces = ko.observableArray([]);
    this.shippingCities = ko.observableArray([]);
}

function LocalesManager(countriesApiURL, regionsApiURL, provincesApiURL, citiesApiURL) {
    var self = this;

    self.client = new LocalesClient(countriesApiURL, regionsApiURL, provincesApiURL, citiesApiURL);
    self.model = new LocalesModel();

    self.regionsCache = {};
    self.provincesCache = {};
    self.countryCitiesCache = {};
    self.regionCitiesCache = {};
    self.provinceCitiesCache = {};

    self.updateBillingLocalesSelects = function() {
        var regions = $(BILLING_ADDRESS + ' #region');
        regions.removeAttr('disabled');
        if (self.model.billingRegions().length == 0) {
            regions.attr('disabled', 'disabled');
        }

        var provinces = $(BILLING_ADDRESS + ' #province');
        provinces.removeAttr('disabled');
        if (self.model.billingProvinces().length == 0) {
          provinces.attr('disabled', 'disabled');
        }

        var cities = $(BILLING_ADDRESS + ' #city');
        cities.removeAttr('disabled');
        if (self.model.billingCities().length == 0) {
            cities.attr('disabled', 'disabled');
        }
    }

    self.updateShippingLocalesSelects = function() {
        var regions = $(SHIPPING_ADDRESS + ' #region');
        regions.removeAttr('disabled');
        if (self.model.shippingRegions().length == 0) {
            regions.attr('disabled', 'disabled');
        }

        var provinces = $(SHIPPING_ADDRESS + ' #province');
        provinces.removeAttr('disabled');
        if (self.model.shippingProvinces().length == 0) {
          provinces.attr('disabled', 'disabled');
        }

        var cities = $(SHIPPING_ADDRESS + ' #city');
        cities.removeAttr('disabled');
        if (self.model.shippingCities().length == 0) {
            cities.attr('disabled', 'disabled');
        }
    }

    self.init = function(success) {
        $('.geodata').each(function(){
            ko.applyBindings(self.model, $(this)[0]);
        });

        self.client.listCountries(function(data) {
           self.model.countries(data);
           if (success != undefined)
                success();
        });

        $(BILLING_ADDRESS + ' #country').on('change', function() {
            geodata.setBillingCountry(parseInt($(this)[0].value));
        });
        $(BILLING_ADDRESS + ' #region').on('change', function() {
            geodata.setBillingRegion(parseInt($(this)[0].value));
        });
        $(BILLING_ADDRESS + ' #province').on('change', function() {
            geodata.setBillingProvince(parseInt($(this)[0].value));
        });

        $(SHIPPING_ADDRESS + ' #country').on('change', function() {
            geodata.setShippingCountry(parseInt($(this)[0].value));
        });
        $(SHIPPING_ADDRESS + ' #region').on('change', function() {
            geodata.setShippingRegion(parseInt($(this)[0].value));
        });
        $(SHIPPING_ADDRESS + ' #province').on('change', function() {
            geodata.setShippingProvince(parseInt($(this)[0].value));
        });

        self.updateBillingLocalesSelects();
        self.updateShippingLocalesSelects();

        return self;
    }

    self.getRegions = function(country, success) {
        if (country in self.regionsCache) {
            success(self.regionsCache[country]);
        } else {
            self.client.listRegions(function(data) {
                self.regionsCache[country] = data;
                success(data);
            }, country);
        }
    }

    self.getProvinces = function(region, success) {
        if (region in self.provincesCache) {
            success(self.provincesCache[region]);
        } else {
            self.client.listProvinces(function(data) {
                self.provincesCache[region] = data;
                success(data);
            }, region);
        }
    }

    self.getCities = function(country, region, province, success) {
        if (province != undefined && province != 0 && province in self.provinceCitiesCache) {
            success(self.provinceCitiesCache[province]);
        } else if (region != undefined && region != 0 && region in self.regionCitiesCache) {
            success(self.regionCitiesCache[region]);
        } else if (country != undefined && country != 0 && country in self.countryCitiesCache) {
            success(self.countryCitiesCache[country]);
        }
        self.client.listCities(function(data) {
            if (province != undefined && province != 0)
                self.provinceCitiesCache[province] = data;
            else if (region != undefined && region != 0)
                self.regionCitiesCache[region] = data;
            else if (country != undefined && country != 0)
                self.countryCitiesCache[country] = data;
            success(data);
        }, country, region, province);
    }

    self.setBillingCountry = function(country, success) {
        self.model.billingRegions([]);
        self.model.billingProvinces([]);
        self.model.billingCities([]);
        self.updateBillingLocalesSelects();

        if (country > 0) {
            self.getRegions(country, function(data) {
                if (data.length == 0) {
                    self.getCities(country, null, null, function(data) {
                        self.model.billingRegions([]);
                        self.model.billingProvinces([]);
                        self.model.billingCities(data);
                        self.updateBillingLocalesSelects();
                        if (success != undefined) {
                            success();
                        }
                    });
                } else {
                    self.model.billingRegions(data);
                    self.updateBillingLocalesSelects();
                    if (success != undefined) {
                        success();
                    }
                }
            });
        } else {
            if (success != undefined) {
                success();
            }
        }
    }

    self.setBillingRegion = function(region, success) {
        self.model.billingProvinces([]);
        self.model.billingCities([]);
        self.updateBillingLocalesSelects();

        if (region > 0) {
            self.getProvinces(region, function(data) {
                if (data.length == 0) {
                    self.getCities(null, region, null, function(data) {
                        self.model.billingCities(data);
                        self.model.billingProvinces([]);
                        self.updateBillingLocalesSelects();
                        if (success != undefined) {
                            success();
                        }
                    });
                } else {
                    self.model.billingProvinces(data);
                    self.updateBillingLocalesSelects();
                    if (success != undefined) {
                        success();
                    }
                }
            });
        } else {
            if (success != undefined) {
                success();
            }
        }
    }

    self.setBillingProvince = function(province, success) {
        self.model.billingCities([]);
        self.updateBillingLocalesSelects();

        if (province > 0) {
            self.getCities(null, null, province, function(data){
                self.model.billingCities(data);
                if (success != undefined) {
                    success();
                }
                self.updateBillingLocalesSelects();
            });
        } else {
            if (success != undefined) {
                success();
            }
        }
    }

    self.setShippingCountry = function(country) {
        self.model.shippingRegions([]);
        self.model.shippingProvinces([]);
        self.model.shippingCities([]);
        self.updateShippingLocalesSelects();

        if (country > 0) {
            self.getRegions(country, function(data) {
                if (data.length == 0) {
                    self.getCities(country, null, null, function(data) {
                        self.model.shippingRegions([]);
                        self.model.shippingProvinces([]);
                        self.model.shippingCities(data);
                        self.updateShippingLocalesSelects();
                    });
                } else {
                    self.model.shippingRegions(data);
                    self.updateShippingLocalesSelects();
                }
            });
        }
    }

    self.setShippingRegion = function(region) {
        self.model.shippingProvinces([]);
        self.model.shippingCities([]);
        self.updateShippingLocalesSelects();

        if (region > 0) {
            self.getProvinces(region, function(data) {
                if (data.length == 0) {
                    self.getCities(null, region, null, function(data) {
                        self.model.shippingCities(data);
                        self.model.shippingProvinces([]);
                        self.updateShippingLocalesSelects();
                    });
                } else {
                    self.model.shippingProvinces(data);
                    self.updateShippingLocalesSelects();
                }
            });
        }
    }

    self.setShippingProvince = function(province) {
        self.model.shippingCities([]);
        self.updateShippingLocalesSelects();

        if (province > 0) {
            self.getCities(null, null, province, function(data){
                self.model.shippingCities(data);
                self.updateShippingLocalesSelects();
            });
        }
    }

}
