// Manage libraries
codenerix_dellibs(['codenerixServices','codenerixControllers']);
codenerix_addlib('appControllers');

// Set the application
angular.module('codenerixApp', codenerix_libraries)
.run(codenerix_run)
.config(codenerix_config1)
.config(codenerix_config2)
.factory("ListMemory",function(){return {};});

// Angular Makagest Controllers
angular.module('appControllers', [])

// Base Controller
.controller('SettingsCtrl', ['$scope','$filter', function($scope,$filter) {
    $scope.settings_success=true;
    $scope.password_success=true;
}]);

