module = angular.module "madacra.identity", ["madacra.socketio"]

loggedInPromise = ($q, identity) ->
    result = $q.defer()
    if identity.isAuthenticated()
        result.resolve(true)
    else
        result.reject("notLoggedIn")
    return result.promise

module.factory "identity", ($rootScope, $q, $timeout, socket) ->
    class IdentityService
        constructor: ->
            @token = null

            socket.addEvents
                "/identity": ["changed", "loginSuccessful", "loginFailed"]
                "": ["connect"]

            $rootScope.$on "/identity:changed", (event, data) =>
                @token = data.token

            $rootScope.$on "/identity:loginSuccessful", (event, data) =>
                @token = data.token

        authenticate: (username, password) ->
            socket.emit("/identity", "login", username: username, password: password)

        isAuthenticated: =>
            return @token?

    return new IdentityService()

module.controller "LoginController", ($scope, $rootScope, $route, $location, identity) ->
    $scope.loginUsername = ""
    $scope.loginPassword = ""

    $scope.login = ->
        destination = $location.search().destination
        identity.authenticate($scope.loginUsername, $scope.loginPassword)
        p = $rootScope.$waitOnce 10000,
            "/identity:loginSuccessful": true
            "/identity:loginFailed": false
        
        p.then ->
            if destination?
                $location.url(destination)
            else
                $route.reload()
        , ->
            console.log "fail"
