module = angular.module "controls.tooltip", []

module.directive "tooltip", ->
    return {
        link: (scope, iElement, iAttrs) ->
            animation = iAttrs.tooltipAnimation ? true
            placement = iAttrs.tooltipPlacement ? "top"
            selector = iAttrs.tooltipSelector ? false
            title = iAttrs.tooltip
            trigger = if iAttrs.tooltipTrigger == "hover" then "hover" else "manual"

            iElement.tooltip
                animation: animation
                placement: placement
                selector: selector
                title: title
                trigger: trigger
            iElement.tooltip("hide")

            if trigger == "manual"
                scope.$watch iAttrs.tooltipTrigger, (value) ->
                    if value
                        iElement.tooltip("show")
                    else
                        iElement.tooltip("hide")
    }
