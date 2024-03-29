app = angular.module "madacra", ["madacra.identity", "madacra.campaign"]

app.config ($interpolateProvider, $routeProvider) ->
    $interpolateProvider.startSymbol("{+")
    $interpolateProvider.endSymbol("+}")

    $routeProvider.when "/",
        templateUrl: "/partials/campaign_list"
        controller: "CampaignListController"
        resolve:
            login: loggedInPromise
    $routeProvider.when "/login",
        templateUrl: "/partials/login"
        controller: "LoginController"
    $routeProvider.when "/signup",
        templateUrl: "/partials/signup"
        controller: "SignupController"
    $routeProvider.when "/foo",
        templateUrl: "/partials/login"
        controller: "FooController"
        resolve:
            login: loggedInPromise
    $routeProvider.otherwise
        redirectTo: "/"

    return

app.controller "MainController", ($scope, $route, $location, identity) ->
    $scope.$on "$routeChangeError", (event, d, u, reason) ->
        if reason == "notLoggedIn"
            destinationUrl = $location.url()
            $location.path("/login")
            $location.search
                destination: destinationUrl

app.run ($rootScope, $timeout, $q) ->
    $rootScope.$waitOnce = (timeout, events) ->
        if Object.isArray(events)
            eventsMap = {}
            for event in events
                eventsMap[event] = true
            events = eventsMap

        deferred = $q.defer()
        removalFunctions = []
        removeAll = ->
            for removalFunction in removalFunctions
                removalFunction()

        if timeout > 0
            $timeout ->
                removeAll()
                deferred.reject
                    event: "timeout"
                    arguments: []
            , timeout

        resolveCallback = (event, args...) ->
            removeAll()
            deferred.resolve
                event: event.name
                arguments: args
        rejectCallback = (event, args...) ->
            removeAll()
            deferred.reject
                event: event.name
                arguments: args

        for eventName, resolve of events
            if resolve
                removalFunctions.push($rootScope.$on(eventName, resolveCallback))
            else
                removalFunctions.push($rootScope.$on(eventName, rejectCallback))

        return deferred.promise
