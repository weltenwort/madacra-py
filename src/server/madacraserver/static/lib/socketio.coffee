module = angular.module "madacra.socketio", []

module.provider "socketioService", () ->
    provider = @
    @namespace = "madacra.io"

    @$get = () ->
        class SocketioService
            constructor: ->
                @connect()

            connect: ->
                socket = io.connect()
                socket.on "connect", ->
                    console.log "connected"
                    socket.emit("test")

        return new SocketioService()

    return
