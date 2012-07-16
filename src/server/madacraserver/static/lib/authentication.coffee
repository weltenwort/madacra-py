module = angular.module "madacra.authentication", ["madacra.socketio"]

module.factory "authenticationService", (socketioService) ->
    class AuthenticationService
        constructor: ->

    return new AuthenticationService()
