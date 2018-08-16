(function(angular) {
    'use strict';
    angular.module('chatApp').controller('appController', appController);
    function appController() {
        var self = this;
        self.greeting = 'Hello From Angular Controller';
        self.interpolate = 'Hello From Interpolate';
    }
}(angular));
