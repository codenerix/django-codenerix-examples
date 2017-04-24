'use strict';

function currency_update(scope, side) {
    console.log("CURRENCY UPDATE: "+side);
}

function amount_update(scope){
    console.log("AMOUNT UPDATE: "+scope.rate);
    scope.buy_amount = scope.rate * scope.sell_amount;
};


// Angular Exchange Controllers
angular.module('codenerixExchangeControllers', [])
.controller('codenerixExchangeAddCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        
        console.log("Loading codenerixExchangeAddCtrl...");
        
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];
        multiadd($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, 0, "/"+ws_entry_point);
        
        $scope.amount_update = function () { amount_update($scope); }
        $scope.currency_update = function (side) { currency_update($scope, side); }
        
        console.log("Loaded codenerixExchangeAddCtrl...");
    }
])
.controller('codenerixExchangeEditCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        
        console.log("Loading codenerixExchangeEditCtrl...");
        
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];
        multiedit($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, 0, "/"+ws_entry_point);
        
        $scope.amount_update = function () { amount_update($scope); }
        $scope.currency_update = function (side) { currency_update($scope, side); }
        
        console.log("Loaded codenerixExchangeEditCtrl...");
    }
]);
