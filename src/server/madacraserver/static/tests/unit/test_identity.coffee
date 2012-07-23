describe "the identity service", ->
    beforeEach ->
        module("madacra.identity")

    it "can authenticate", inject (identity) ->
        expect(identity.authenticate).toBeDefined()
        identity.authenticate("user1", "password1")

        waitsFor ->
            identity.token?
        , "identity token is not set after server response", 1000
