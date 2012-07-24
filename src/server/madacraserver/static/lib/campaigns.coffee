module = angular.module "madacra.campaigns", ["madacra.socketio"]

module.factory "campaigns", ($rootScope, socket) ->
    class CampaignsService
        constructor: ->
            @campaigns = {}

            socket.addEvents
                "/campaign": ["enumerate"]

            $rootScope.$on "/campaign:changed", (event, data) ->
                campaigns = data.campaigns
                for campaign in campaigns
                    @campaigns[campaign._id] = campaign

    return new CampaignsService()

module.controller "CampaignListController", ($scope, campaigns) ->
    $scope.getCampaigns = ->
        return Object.values(campaigns.campaigns)
