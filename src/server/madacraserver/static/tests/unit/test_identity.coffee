describe "the identity service", ->
    beforeEach ->
        module("madacra.identity")

    it "can log in and log out", inject (identity) ->
        expect(identity.logIn).toBeDefined()
        expect(identity.logOut).toBeDefined()
        identity.logIn("user1", "password1")

        waitsFor ->
            identity.token?
        , "identity token to be set after successful login", 1000

        runs ->
            identity.logOut()

        waitsFor ->
            identity.token == null
        , "identity token to be null after successful logout", 1000


    it "can fail to log in", inject ($rootScope, identity) ->
        done = false
        identity.logIn("user1", "password2")

        $rootScope.$on "/identity:loginFailed", ->
            done = true

        waitsFor ->
            done
        , "loginFailed event from server", 1000

    it "can sign up", inject (identity) ->
        expect(identity.signUp).toBeDefined()
        identity.signUp("testuser#{Date.now()}", "testpassword")

        waitsFor ->
            identity.token?
        , "identity token to be set after successful signup", 1000

    it "can fail to sign up", inject ($rootScope, identity) ->
        done = false
        identity.signUp("user1", "testpassword")

        $rootScope.$on "/identity:signupFailed", ->
            done = true

        waitsFor ->
            done
        , "signupFailed event from server", 1000
