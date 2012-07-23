module = angular.module "madacra.identity", ["madacra.socketio"]

module.factory "identity", ($rootScope, socket) ->
    class IdentityService
        constructor: ->
            @token = null

            socket.addEvents
                "/identity": ["changed"]
                "": ["connect"]

            $rootScope.$on "/identity:changed", (event, data) =>
                @token = data.token

        authenticate: (username, password) ->
            socket.emit("/identity", "login", username: username, password: password)

    return new IdentityService()
