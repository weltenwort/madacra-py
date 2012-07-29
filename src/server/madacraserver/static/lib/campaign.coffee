module = angular.module "madacra.campaign", ["madacra.socketio"]

module.factory "campaign", ($rootScope, socket) ->
    class CampaignService
        constructor: ->
            @campaigns = {}

            socket.addEvents
                "/campaign": ["enumerate"]

            $rootScope.$on "/campaign:enumerate", (event, data) =>
                campaigns = data.campaigns
                for campaign in campaigns
                    @campaigns[campaign._id] = campaign

        enumerate: ->
            socket.emit("/campaign", "enumerate")

    return new CampaignService()

module.controller "CampaignListController", ($scope, campaign) ->
    campaign.enumerate()

    $scope.getCampaigns = ->
        return Object.values(campaign.campaigns)
