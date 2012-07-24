describe "the $waitOnce method on the root scope", ->
    beforeEach ->
        module("madacra")

    it "exists", inject ($rootScope) ->
        expect($rootScope.$waitOnce).toBeDefined()

    it "resolves its promise correctly when given a list of events", inject ($rootScope) ->
        done = false
        p = $rootScope.$waitOnce(0, ["fooEvent"])
        p.then (result) ->
            done = result.event == "fooEvent"

        $rootScope.$broadcast "fooEvent",
            key: "value"
        $rootScope.$digest()

        waitsFor ->
            done
        , "the $waitOnce promise to be resolved", 1000

    it "resolves its promise correctly when given a mapping of events", inject ($rootScope) ->
        done = false
        p = $rootScope.$waitOnce 0,
            fooEvent: true

        p.then (result) ->
            done = result.event == "fooEvent"
        , (result) ->
            done = false

        $rootScope.$broadcast "fooEvent",
            key: "value"
        $rootScope.$digest()

        waitsFor ->
            done
        , "the $waitOnce promise to be resolved", 1000

    it "rejects its promise correctly when given a mapping of events", inject ($rootScope) ->
        done = false
        p = $rootScope.$waitOnce 0,
            fooEvent: false

        p.then (result) ->
            done = false
        , (result) ->
            done = result.event == "fooEvent"

        $rootScope.$broadcast "fooEvent",
            key: "value"
        $rootScope.$digest()

        waitsFor ->
            done
        , "the $waitOnce promise to be rejected", 1000

    it "times out correctly", inject ($rootScope, $timeout) ->
        done = false
        p = $rootScope.$waitOnce(1000, ["fooEvent"])
        p.then (result) ->
            done = false
        , (result) ->
            done = result.event == "timeout"

        $timeout.flush()

        waitsFor ->
            done
        , "the $waitOnce promise to time out correctly", 2000
