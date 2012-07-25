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
                "/identity": [
                    "changed"
                    "loginSuccessful"
                    "loginFailed"
                    "logoutSuccessful"
                    "signupSuccessful"
                    "signupFailed"
                ]
                #"": ["connect"]

            $rootScope.$on "/identity:loginSuccessful", (event, data) =>
                @token = data.token

            $rootScope.$on "/identity:logoutSuccessful", (event, data) =>
                @token = null

        logIn: (username, password) ->
            socket.emit("/identity", "login", username: username, password: password)

        logOut: ->
            socket.emit("/identity", "logout")

        isAuthenticated: =>
            return @token?

        signUp: (username, password) ->
            socket.emit("/identity", "signup", username: username, password: password)

    return new IdentityService()

module.controller "LoginController", ($scope, $rootScope, $route, $location, identity) ->
    $scope.loginUsername = ""
    $scope.loginPassword = ""
    $scope.loggingIn = false

    $scope.login = ->
        $scope.loggingIn = true
        destination = $location.search().destination
        identity.logIn($scope.loginUsername, $scope.loginPassword)
        p = $rootScope.$waitOnce 10000,
            "/identity:loginSuccessful": true
            "/identity:loginFailed": false
        
        p.then ->
            $scope.loggingIn = false
            if destination?
                $location.url(destination)
            else
                $route.reload()
        , ->
            $scope.loggingIn = false
            console.log "fail"

module.controller "SignupController", ($scope, $rootScope, $location, identity) ->
    $scope.signupUsername = ""
    $scope.signupPassword = ""
    $scope.signingUp = false

    $scope.signup = ->
        $scope.signingUp = true
        identity.signUp($scope.signupUsername, $scope.signupPassword)
        p = $rootScope.$waitOnce 10000,
            "/identity:loginSuccessful": true
            "/identity:signupFailed": false
        
        p.then ->
            $scope.signingUp = false
            $location.url("/")
        , ->
            $scope.signingUp = false
            console.log "fail"
