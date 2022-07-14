angular.module('codenerixPublicContactControllers', [])
.controller('codenerixPublicContactCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register','hotkeys',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, hotkeys) {
        $scope.msg = false;
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];
        $scope.submit_callback = function (listid, url, form, next, kind, answer, stat) {
            console.log($scope);
            console.log(form);
            $scope.currentRecord = {};
            form.$setUntouched();
            form.$setPristine();

            angular.forEach(form, function (element, name) {
                if (!name.startsWith('$')) {
                    element.$viewValue = '';
                    element.$render();
                }
            });

            $scope.msg = true;
            return "none";
        };

        multiadd($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, 0, "/"+ws_entry_point, hotkeys);
        
    }
]);
