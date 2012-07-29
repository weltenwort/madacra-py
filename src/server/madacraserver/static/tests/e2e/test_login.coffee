describe "the login dialog", ->
    beforeEach ->
        browser().navigateTo("/#/login")

    it "can log in successfully", ->
        input("loginUsername").enter("user1")
        input("loginPassword").enter("password1")
        element("button[name='loginSubmit']").click()

        expect(browser().location().url()).toBe("/")

    it "can display errors on unsuccessful login", ->
        input("loginUsername").enter("user1")
        input("loginPassword").enter("notpassword1")
        element("button[name='loginSubmit']").click()

        expect(browser().location().url()).toBe("/login")
        expect(element(".tooltip").text()).toBe("Invalid password for that username.")
