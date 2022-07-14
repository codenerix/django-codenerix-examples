'use strict';

angular.module('frontendControllers', [])
.controller('frontendWishlistCtrl', ['$scope', '$rootScope', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', '$location',
    function($scope, $rootScope, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, $location) {
        $scope.buy_wishlist_products = function(url) {
            var lines = [];
            $("input[name=checkline]:checked").each(function () {
                lines.push($(this).val());
            });
            if (lines.length != 0) {
                var data = {
                    'lines': lines
                };
                $http.post(url, data, {})
                .success(function(answer, status) {
                    if (status == 200) {
                        $window.location.href = answer.url;
                    } else {
                        console.log("Error " + status + ": " + answer);
                        console.log(answer);
                        alert("ERROR " + status + ": " + answer);
                    }
                }).error(function(data, status, headers, config) {
                    if (cnf_debug) {
                        alert(data);
                    } else {
                        alert(cnf_debug_txt);
                    }
                });
            }
        }
    }
])
.controller('frontendOrderlistCtrl',['$scope', '$rootScope', '$http', '$window', '$timeout', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register', '$location',
    function($scope, $rootScope, $http, $window, $timeout, $uibModal, $state, $stateParams, $templateCache, Register, $location) {
        $scope.request_invoice = function(order_pk) {
            var url = '/request_invoice/'+ order_pk;
            // Base window
            $scope.ws=url;
            
            // Base Window functions
            var functions = function(scope) {};
            var callback = function(scope, answer) {
                if (answer.error != null){
                    alert(answer.error_code + ": " + answer.error);
                }else{
                    alert(answer.message);
                }
            };
            
            $scope.cb_window = openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        }
    }
]);
