app = angular.module "madacra", ["madacra.identity"]

app.config ($interpolateProvider, $routeProvider) ->
    $interpolateProvider.startSymbol("{+")
    $interpolateProvider.endSymbol("+}")

app.controller "MainController", ($scope, identity) ->

