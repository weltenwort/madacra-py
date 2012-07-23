describe "madacra", ->
    beforeEach ->
        browser().navigateTo("/")
    it "displays foo", ->
        expect(element("div").text()).toMatch(/foo/)
