var app;app=angular.module("madacra",["madacra.authentication"]);app.config(function($interpolateProvider,$routeProvider){$interpolateProvider.startSymbol("{+");return $interpolateProvider.endSymbol("+}");});app.controller("MainController",function($scope,authenticationService){});var module;module=angular.module("madacra.socketio",[]);module.provider("socketioService",function(){var provider;provider=this;this.namespace="madacra.io";this.$get=function(){var SocketioService;SocketioService=(function(){SocketioService.name='SocketioService';function SocketioService(){this.connect();}
SocketioService.prototype.connect=function(){var socket;socket=io.connect();return socket.on("connect",function(){console.log("connected");return socket.emit("test");});};return SocketioService;})();return new SocketioService();};});var module;module=angular.module("madacra.authentication",["madacra.socketio"]);module.factory("authenticationService",function(socketioService){var AuthenticationService;AuthenticationService=(function(){AuthenticationService.name='AuthenticationService';function AuthenticationService(){}
return AuthenticationService;})();return new AuthenticationService();});