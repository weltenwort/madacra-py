app = angular.module "madacra", ["madacra.authentication"]

app.config ($interpolateProvider, $routeProvider) ->
    $interpolateProvider.startSymbol("{+")
    $interpolateProvider.endSymbol("+}")

app.controller "MainController", ($scope, authenticationService) ->

