describe "the campaign service", ->
    beforeEach ->
        module("madacra.campaign")
        module("madacra.identity")

    it "can enumerate campaigns after login", inject (campaign, identity) ->
        runs ->
            expect(campaign.enumerate).toBeDefined()
            identity.logIn("user1", "password1")

        waitsFor ->
            identity.token?
        , "identity token to be set after successful login", 1000
        
        runs ->
            campaign.enumerate()

        waitsFor ->
            Object.keys(campaign.campaigns).length > 0
        , "campaigns to be stored after they have been sent by the server", 1000
