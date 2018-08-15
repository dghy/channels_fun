(function () {
  'use strict';
  angular
    .module('chatApp')
    .controller('chatController', ['$scope', function($scope) {
        $scope.testMessage = 'test from angular';
    }])
})();
