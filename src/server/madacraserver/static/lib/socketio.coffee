module = angular.module "madacra.socketio", []

module.factory "socket", ($rootScope) ->
    class SocketService
        constructor: ->
            @socket = io.connect()
            @events = []

        broadcastOnRootScope: (eventName) ->
            return (args...) ->
                $rootScope.$apply ->
                    $rootScope.$broadcast eventName, args...

        getNamespace: (namespace) ->
            return if namespace? and namespace != ""
                @socket.of(namespace)
            else
                @socket

        addEvent: (namespace, eventName) =>
            name = "#{namespace}:#{eventName}"
            if name not in @events
                @getNamespace(namespace).on(eventName, @broadcastOnRootScope(name))

        addEvents: (eventMap) =>
            for namespace, eventNames of eventMap
                for eventName in eventNames
                    @addEvent(namespace, eventName)

        emit: (namespace, eventName, data) =>
            @getNamespace(namespace).emit(eventName, data)

    return new SocketService()
